using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Data;
using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

// Configuración de Controladores y JSON
builder.Services.AddControllers().AddJsonOptions(options =>
{
    options.JsonSerializerOptions.ReferenceHandler = ReferenceHandler.IgnoreCycles;
    options.JsonSerializerOptions.WriteIndented = true;
    options.JsonSerializerOptions.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
});

// Base de Datos SQLite
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=octolab.db"));

// Configuración de CORS (Abierto para desarrollo con Angular)
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Middlewares - EL ORDEN ES IMPORTANTE
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}

// app.UseHttpsRedirection(); // Coméntalo si tienes problemas con el puerto HTTPS en local
app.UseStaticFiles(); // Necesario para servir las fotos de los avatares
app.UseRouting();

app.UseCors();

// Estos dos deben ir en este orden específico
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();