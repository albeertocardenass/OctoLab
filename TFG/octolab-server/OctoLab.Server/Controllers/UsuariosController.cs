using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Data;
using OctoLab.Server.Models.Entities;

namespace OctoLab.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UsuariosController : ControllerBase
    {
        private readonly AppDbContext _context;
        public UsuariosController(AppDbContext context) { _context = context; }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Usuario>>> GetUsuarios()
        {
            return await _context.Usuarios.AsNoTracking().ToListAsync();
        }

        [HttpPut("cambiar-rol")]
        public async Task<IActionResult> CambiarRol([FromBody] RolUpdateDto dto)
        {
            var usuario = await _context.Usuarios.FindAsync(dto.Id);
            if (usuario == null) return NotFound();

            usuario.Rol = dto.NuevoRol;
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
    }

    public class RolUpdateDto
    {
        public long Id { get; set; }
        public string NuevoRol { get; set; } = string.Empty;
    }
}