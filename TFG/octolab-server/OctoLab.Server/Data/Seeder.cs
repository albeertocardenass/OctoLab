using Bogus;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Models.Entities;
using ProyectoRS.Server.Models.Database.Entities;
using System.Security.Cryptography;
using System.Text;

namespace OctoLab.Server.Data;

public class Seeder
{
    private const int FAKE_USERS_COUNT = 5;  // ← era 30
    private const int POSTS_COUNT = 10;      // ← era 50
    private readonly MyDbContext _context;

    public Seeder(MyDbContext context)
    {
        _context = context;
    }

    public async Task SeedAsync()
    {
        await SeedAdminsAsync();
        await SeedFakeUsersAsync();
        await _context.SaveChangesAsync();
        await SeedPublicacionesAsync();
        await _context.SaveChangesAsync();
    }

    private async Task SeedAdminsAsync()
    {
        if (!await _context.Usuarios.AnyAsync(u => u.Rol == "Admin"))
        {
            var admin = new Usuario
            {
                Nombre = "Paco",
                Apellido1 = "Jefe",
                Apellido2 = "Supremo",
                Email = "paco@prueba.com",
                Apodo = "AdminPaco",
                Password = EncriptarNativo("1234"),
                Rol = "Admin",
                Avatar = "default-avatar.jpg",
                Descripcion = "Administrador principal de Octolab",
                Puntos = 999
            };

            _context.Usuarios.Add(admin);
        }
    }

    private async Task SeedFakeUsersAsync()
    {
        if (await _context.Usuarios.CountAsync() <= 1)
        {
            var passwordHasheada = EncriptarNativo("1234");

            Faker<Usuario> faker = new Faker<Usuario>("es")
                .RuleFor(u => u.Nombre, f => f.Name.FirstName())
                .RuleFor(u => u.Apellido1, f => f.Name.LastName())
                .RuleFor(u => u.Apellido2, f => f.Name.LastName())
                .RuleFor(u => u.Apodo, f => f.Internet.UserName())
                .RuleFor(u => u.Email, (f, u) => f.Internet.Email(u.Nombre, u.Apellido1))
                .RuleFor(u => u.Password, f => passwordHasheada)
                .RuleFor(u => u.Rol, f => "Usuario")
                .RuleFor(u => u.Avatar, f => "default-avatar.jpg")
                .RuleFor(u => u.Descripcion, f => f.Lorem.Sentence())
                .RuleFor(u => u.Puntos, f => f.Random.Int(0, 500));

            var usuarios = faker.Generate(FAKE_USERS_COUNT);
            await _context.Usuarios.AddRangeAsync(usuarios);
        }
    }

    private async Task SeedPublicacionesAsync()
    {
        if (await _context.Publicaciones.AnyAsync()) return;

        var todosLosUsuarios = await _context.Usuarios.ToListAsync();

        var fakerPublicaciones = new Faker<Publicacion>("es")
            .RuleFor(p => p.Contenido, f => f.Lorem.Paragraph())
            .RuleFor(p => p.Fecha, f => f.Date.Recent(30))
            .RuleFor(p => p.UsuarioId, f => f.PickRandom(todosLosUsuarios).Id);

        var posts = fakerPublicaciones.Generate(POSTS_COUNT);
        await _context.Publicaciones.AddRangeAsync(posts);
    }

    private static string EncriptarNativo(string password)
    {
        using (var sha256 = SHA256.Create())
        {
            var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
            return Convert.ToBase64String(bytes);
        }
    }
}