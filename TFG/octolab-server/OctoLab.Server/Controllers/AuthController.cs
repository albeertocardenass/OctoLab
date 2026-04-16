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
                return BadRequest(new { field = "email", message = "El correo electrónico ya está registrado." });
            }

            if (await _context.Usuarios.AnyAsync(u => u.Apodo == dto.Apodo))
            {
                return BadRequest(new { field = "apodo", message = "El apodo ya está en uso." });
            }

            var nuevoUsuario = new Usuario
            {
                Nombre = dto.Nombre,
                Apellido1 = dto.Apellido1,
                Apellido2 = dto.Apellido2,
                Email = dto.Email,
                Password = dto.Password,
                Apodo = dto.Apodo,
                Rol = "Usuario",
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

            usuario.UltimaConexion = DateTime.Now;

            _context.Usuarios.Update(usuario);
            await _context.SaveChangesAsync();

            return Ok(new
            {
                mensaje = "Login correcto",
                usuario = new
                {
                    usuario.Nombre,
                    usuario.Apodo,
                    usuario.Id,
                    usuario.Rol,
                    usuario.UltimaConexion
                }
            });
        }

        [HttpPost("invitado")]
        public ActionResult LoginInvitado()
        {
            return Ok(new
            {
                mensaje = "Acceso como invitado",
                usuario = new
                {
                    Nombre = "Invitado",
                    Apodo = "Invitado",
                    Id = 0,
                    Rol = "Invitado",
                    UltimaConexion = DateTime.Now
                }
            });
        }
    }
}