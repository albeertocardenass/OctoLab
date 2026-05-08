using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using OctoLab.Server.Data;
using OctoLab.Server.Models.Entities;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Linq;
using OctoLab.Server.DTOs;
using Microsoft.AspNetCore.Authorization;

namespace OctoLab.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UsuariosController : ControllerBase
    {
        private readonly MyDbContext _context;
        private readonly IConfiguration _config;

        public UsuariosController(MyDbContext context, IConfiguration config)
        {
            _context = context;
            _config = config;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Usuario>>> GetUsuarios()
        {
            return await _context.Usuarios.AsNoTracking().ToListAsync();
        }

        [HttpPost("ping")]
        [Authorize]
        public async Task<IActionResult> Ping()
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized();

            var usuario = await _context.Usuarios.FindAsync(long.Parse(userIdClaim));
            if (usuario == null) return NotFound();

            usuario.UltimaConexion = DateTime.Now;
            await _context.SaveChangesAsync();

            return Ok();
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] UsuarioLogin dto)
        {
            var usuario = await _context.Usuarios
                .FirstOrDefaultAsync(u => u.Email == dto.Email);

            if (usuario == null || usuario.Password != EncriptarNativo(dto.Password))
            {
                return Unauthorized(new { mensaje = "Email o contraseña incorrectos" });
            }

            usuario.UltimaConexion = DateTime.Now;
            await _context.SaveChangesAsync();

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:Key"]!));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var claims = new[]
            {
                new Claim(ClaimTypes.Name, usuario.Nombre ?? ""),
                new Claim(ClaimTypes.Role, usuario.Rol ?? "Usuario"),
                new Claim("Id", usuario.Id.ToString())
            };

            var tokenDescriptor = new JwtSecurityToken(
                claims: claims,
                expires: DateTime.Now.AddDays(7),
                signingCredentials: creds
            );

            var tokenFinal = new JwtSecurityTokenHandler().WriteToken(tokenDescriptor);

            return Ok(new
            {
                token = tokenFinal,
                usuario = new
                {
                    id = usuario.Id,
                    nombre = usuario.Nombre,
                    email = usuario.Email,
                    rol = usuario.Rol,
                    apodo = usuario.Apodo,
                    avatar = usuario.Avatar,
                    puntos = usuario.Puntos,
                    modulosDesbloqueados = string.IsNullOrEmpty(usuario.ModulosDesbloqueados)
                        ? new List<int>()
                        : usuario.ModulosDesbloqueados.Split(',').Select(int.Parse).ToList()
                }
            });
        }

        [HttpPut("cambiar-rol")]
        public async Task<IActionResult> CambiarRol([FromBody] RolUpdateDto dto)
        {
            var usuario = await _context.Usuarios.FindAsync(dto.Id);
            if (usuario == null) return NotFound();

            usuario.Rol = (string)dto.NuevoRol;
            _context.Entry(usuario).State = EntityState.Modified;
            await _context.SaveChangesAsync();
            return Ok();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteUsuario(long id)
        {
            var usuario = await _context.Usuarios.FindAsync(id);
            if (usuario == null) return NotFound();
            _context.Usuarios.Remove(usuario);
            await _context.SaveChangesAsync();
            return Ok();
        }

        [HttpPut("actualizar-puntos")]
        [Authorize]
        public async Task<IActionResult> ActualizarPuntos([FromBody] PuntosUpdateDto dto)
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized(new { mensaje = "No se encontró el ID en el token" });

            var userId = long.Parse(userIdClaim);
            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            usuario.Puntos = dto.Puntos;
            await _context.SaveChangesAsync();

            return Ok(new { message = "Puntos actualizados correctamente" });
        }

        [HttpPut("actualizar-progreso")]
        [Authorize]
        public async Task<IActionResult> ActualizarProgreso([FromBody] ProgresoUpdateDto dto)
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized();

            var userId = long.Parse(userIdClaim);
            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            usuario.Puntos = dto.Puntos;
            usuario.ModulosDesbloqueados = dto.ModulosDesbloqueados != null && dto.ModulosDesbloqueados.Any()
                ? string.Join(",", dto.ModulosDesbloqueados)
                : "";

            await _context.SaveChangesAsync();
            return Ok(new { mensaje = "Progreso actualizado correctamente" });
        }

        private static string EncriptarNativo(string password)
        {
            using (var sha256 = System.Security.Cryptography.SHA256.Create())
            {
                var bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
                return Convert.ToBase64String(bytes);
            }
        }
    }
}