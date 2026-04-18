using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using OctoLab.Server.Data;
using OctoLab.Server.Models.Entities;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using OctoLab.Server.DTOs;

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
        
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] UsuarioLogin dto)
        {
            var usuario = await _context.Usuarios
                .FirstOrDefaultAsync(u => u.Email == dto.Email);

            if (usuario == null || usuario.Password != EncriptarNativo(dto.Password))
            {
                return Unauthorized(new { mensaje = "Email o contraseña incorrectos" });
            }

            var keyStr = "Esta_Es_Una_Clave_Super_Secreta_De_Octolab_2024_🦈";
            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:Key"]!));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var claims = new[]
             {
            new Claim(ClaimTypes.Name, usuario.Nombre ?? ""),
            new Claim(ClaimTypes.Role, usuario.Rol ?? "Usuario"),
            new Claim("Id", usuario.Id.ToString())  // ← mayúscula, igual que PublicacionesController
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
                    puntos = usuario.Puntos
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