using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Data;
using OctoLab.Server.Models.Entities;
using OctoLab.Server.DTOs;
using Microsoft.AspNetCore.Authorization;

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

        [HttpGet]
        [Authorize(Roles = "Admin")]
        public async Task<ActionResult<IEnumerable<Usuario>>> GetUsuarios()
        {
            return await _context.Usuarios.ToListAsync();
        }

        [HttpPost("register")]
        public async Task<ActionResult> Register(UsuarioRegister dto)
        {

            if (await _context.Usuarios.AnyAsync(u => u.Email == dto.Email))
            {
                return BadRequest("El correo electrónico ya está registrado.");
            }

            var nuevoUsuario = new Usuario
            {
                Nombre = dto.Nombre,
                Apellido1 = dto.Apellido1,
                Apellido2 = dto.Apellido2,
                Email = dto.Email,
                Password = dto.Password,
                Apodo = dto.Apodo,
                Rol = "Usuario"
            };

            _context.Usuarios.Add(nuevoUsuario);
            await _context.SaveChangesAsync();

            return Ok(new { mensaje = "Usuario registrado con éxito", usuarioId = nuevoUsuario.Id });
        }

        [HttpPost("login")]
        public async Task<ActionResult> Login([FromBody] UsuarioLogin loginDto)
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
                usuario = new { usuario.Nombre, usuario.Apodo, usuario.Id, usuario.Rol }
            });
        }
    }
}


