using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi;
using OctoLab.Server.Data;
using Stripe;
using Swashbuckle.AspNetCore.Filters;
using System.Text;
using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers().AddJsonOptions(options =>
{
    options.JsonSerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles;
    options.JsonSerializerOptions.WriteIndented = true;
    options.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
});

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition(JwtBearerDefaults.AuthenticationScheme, new OpenApiSecurityScheme
    {
        BearerFormat = "JWT",
        Name = "Authorization",
        Description = "Escribe **_SOLO_** tu token JWT",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.Http,
        Scheme = JwtBearerDefaults.AuthenticationScheme
    });
    options.OperationFilter<SecurityRequirementsOperationFilter>(true, JwtBearerDefaults.AuthenticationScheme);
});

builder.Services.AddHttpClient();

builder.Services.AddDbContext<MyDbContext>(options =>
{
    var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
});

builder.Services.AddScoped<Seeder>();

var keyStr = builder.Configuration["Jwt:Key"]!;
var key = Encoding.UTF8.GetBytes(keyStr);

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(key),
            ValidateIssuer = false,
            ValidateAudience = false
        };
    });

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader();
    });
});

StripeConfiguration.ApiKey = builder.Configuration["Stripe:SecretKey"];

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseStaticFiles();
app.UseRouting();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

await InitDatabaseAsync(app.Services);

app.Run();

static async Task InitDatabaseAsync(IServiceProvider serviceProvider)
{
    using IServiceScope scope = serviceProvider.CreateScope();
    using MyDbContext dbContext = scope.ServiceProvider.GetRequiredService<MyDbContext>();

    await dbContext.Database.EnsureCreatedAsync();
    await AplicarColumnasAusentesAsync(dbContext);

    if (!dbContext.Usuarios.Any())
    {
        var seeder = scope.ServiceProvider.GetRequiredService<Seeder>();
        await seeder.SeedAsync();
    }
}

static async Task AplicarColumnasAusentesAsync(MyDbContext dbContext)
{
    var columnas = new[]
    {
        ("TemasCompletados",     "ALTER TABLE Usuarios ADD COLUMN TemasCompletados VARCHAR(1000) NOT NULL DEFAULT ''"),
        ("ModulosDesbloqueados", "ALTER TABLE Usuarios ADD COLUMN ModulosDesbloqueados VARCHAR(1000) NOT NULL DEFAULT ''"),
        ("Puntos",               "ALTER TABLE Usuarios ADD COLUMN Puntos INT NOT NULL DEFAULT 0"),
        ("UltimaConexion",       "ALTER TABLE Usuarios ADD COLUMN UltimaConexion DATETIME(6) NOT NULL DEFAULT '0001-01-01 00:00:00'"),
    };

    var conn = dbContext.Database.GetDbConnection();
    await conn.OpenAsync();
    try
    {
        // Añadir columnas ausentes
        foreach (var (col, alterSql) in columnas)
        {
            using var check = conn.CreateCommand();
            check.CommandText = $"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='Usuarios' AND COLUMN_NAME='{col}'";
            var count = Convert.ToInt32(await check.ExecuteScalarAsync());
            if (count == 0)
            {
                using var alter = conn.CreateCommand();
                alter.CommandText = alterSql;
                await alter.ExecuteNonQueryAsync();
            }
        }

        // Migrar columnas a LONGTEXT si aún son VARCHAR (para almacenar base64 en BD)
        var columnasLongText = new[]
        {
            ("Usuarios",     "Avatar",  "ALTER TABLE Usuarios MODIFY COLUMN Avatar LONGTEXT NULL"),
            ("Publicaciones","Imagen",  "ALTER TABLE Publicaciones MODIFY COLUMN Imagen LONGTEXT NULL"),
        };

        foreach (var (tabla, columna, alterSql) in columnasLongText)
        {
            using var checkType = conn.CreateCommand();
            checkType.CommandText = $"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='{tabla}' AND COLUMN_NAME='{columna}'";
            var colType = (await checkType.ExecuteScalarAsync())?.ToString();
            if (colType != null && colType.ToLower() != "longtext")
            {
                using var alterCol = conn.CreateCommand();
                alterCol.CommandText = alterSql;
                await alterCol.ExecuteNonQueryAsync();
            }
        }
    }
    finally
    {
        await conn.CloseAsync();
    }
}