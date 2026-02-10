using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Data;
using OctoLab.Server.Models.Entities;

namespace OctoLab.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly AppDbContext _context;

        public AuthController(AppDbContext context)
        {
            _context = context;
        }

        [HttpPost("register")]
        public async Task<ActionResult<Usuario>> Register(Usuario usuario)
        {

            if (await _context.Usuarios.AnyAsync(u => u.Email == usuario.Email))
            {
                return BadRequest("El correo electrónico ya está registrado.");
            }

            _context.Usuarios.Add(usuario);
            await _context.SaveChangesAsync();

            return Ok(new { mensaje = "Usuario registrado con éxito", usuarioId = usuario.Id });
        }

        [HttpPost("login")]
        public async Task<ActionResult> Login([FromBody] LoginDto loginDto)
        {
            var usuario = await _context.Usuarios
                .FirstOrDefaultAsync(u => u.Email == loginDto.Email && u.Password == loginDto.Password);

            if (usuario == null)
            {
                return Unauthorized("Email o contraseña incorrectos.");
            }

            return Ok(new
            {
                mensaje = "Login correcto",
                usuario = new { usuario.Nombre, usuario.Apodo, usuario.Rol }
            });
        }
    }

    public class LoginDto
    {
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }
}