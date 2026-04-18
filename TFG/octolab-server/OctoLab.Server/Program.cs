using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using OctoLab.Server.Data;
using System.Text;
using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers().AddJsonOptions(options =>
{
    options.JsonSerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles;
    options.JsonSerializerOptions.WriteIndented = true;
    options.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
});

builder.Services.AddHttpClient();

builder.Services.AddDbContext<MyDbContext>(options =>
{
    var dbPath = Path.Combine(Directory.GetCurrentDirectory(), "octolab.db"); // ← cambiado
    options.UseSqlite($"Data Source={dbPath}");
});

builder.Services.AddScoped<Seeder>();

var keyStr = builder.Configuration["Jwt:Key"]!;
var key = Encoding.UTF8.GetBytes(keyStr);

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
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

var app = builder.Build();

if (app.Environment.IsDevelopment())
    app.UseDeveloperExceptionPage();

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

    if (!dbContext.Usuarios.Any())
    {
        var seeder = scope.ServiceProvider.GetRequiredService<Seeder>();
        await seeder.SeedAsync();
    }
}