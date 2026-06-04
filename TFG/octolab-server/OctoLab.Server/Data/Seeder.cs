using Bogus;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Models.Entities;
using ProyectoRS.Server.Models.Database.Entities;
using System.Security.Cryptography;
using System.Text;

namespace OctoLab.Server.Data;

public class Seeder
{
    private const int FAKE_USERS_COUNT = 5;
    private const int POSTS_COUNT = 10;
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
            var admins = new List<Usuario>
            {
                new Usuario
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
                },
                new Usuario
                {
                    Nombre = "Juan Alberto",
                    Apellido1 = "Campaña",
                    Apellido2 = "Espejo",
                    Email = "jace123@octolab.com",
                    Apodo = "Jace",
                    Password = EncriptarNativo("123456"),
                    Rol = "Admin",
                    Avatar = "default-avatar.jpg",
                    Descripcion = "Co-fundador de OctoLab",
                    Puntos = 999
                },
                new Usuario
                {
                    Nombre = "Alberto",
                    Apellido1 = "Cárdenas",
                    Apellido2 = "Palomo",
                    Email = "cardenasboy123@octolab.com",
                    Apodo = "CardenasBoy",
                    Password = EncriptarNativo("123456"),
                    Rol = "Admin",
                    Avatar = "default-avatar.jpg",
                    Descripcion = "Co-fundador de OctoLab",
                    Puntos = 999
                }
            };

            await _context.Usuarios.AddRangeAsync(admins);
        }
    }

    private async Task SeedFakeUsersAsync()
    {
        if (await _context.Usuarios.CountAsync() <= 3)
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

        
        var contenidos = new List<string>
        {
            "Llevo 1 semana sin poder completar el último laboratorio. ¿Alguien que me pueda ayudar?",
            "¿Alguien puede explicarme la diferencia entre cifrado simétrico y asimétrico?",
            "!Si donas a OctoLab te dan recompensas!",
            "El módulo de redes me está costando bastante. ¿Algún consejo para entender mejor las subnets?",
            "Alguien ha conseguido todos los labs?",
            "¿Qué herramienta usáis para análisis de vulnerabilidades? Yo uso Nmap.",
            "Acabo de registrarme en OctoLab. Espero aprender mucho aquí.",
            "El laboratorio de Metasploit es brutal. Muy bien explicado todo.",
            "!Sacad más laboratorios!",
            "Llevo una semana en la plataforma y ya he aprendido más que en meses por mi cuenta."
        };
        

        var faker = new Faker("es");
        var publicaciones = new List<Publicacion>();

        for (int i = 0; i < POSTS_COUNT; i++)
        {
            publicaciones.Add(new Publicacion
            {
                Contenido = contenidos[i % contenidos.Count],
                Fecha = faker.Date.Recent(30),
                UsuarioId = faker.PickRandom(todosLosUsuarios).Id
            });
        }

        await _context.Publicaciones.AddRangeAsync(publicaciones);
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