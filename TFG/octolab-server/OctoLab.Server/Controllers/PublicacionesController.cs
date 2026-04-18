using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Data;
using OctoLab.Server.DTOs;
using ProyectoRS.Server.Models.Database.Entities;

namespace OctoLab.Server.Controllers;

[Route("api/[controller]")]
[ApiController]
public class PublicacionesController : ControllerBase
{
    private readonly MyDbContext _context;

    public PublicacionesController(MyDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    [AllowAnonymous]
    public async Task<ActionResult<IEnumerable<object>>> GetPublicaciones()
    {
        return await _context.Publicaciones
            .Include(p => p.Usuario)
            .OrderByDescending(p => p.Fecha)
            .Select(p => new
            {
                p.Id,
                p.Contenido,
                p.Imagen,
                p.Fecha,
                Autor = p.Usuario!.Nombre,
                AutorApodo = p.Usuario!.Apodo,
                AutorAvatar = p.Usuario!.Avatar,
                p.UsuarioId,
                p.PublicacionPadreId
            })
            .ToListAsync();
    }

    [HttpPost]
    [Authorize]
    public async Task<IActionResult> PostPublicacion(PublicacionCrearDto dto)
    {
        var userIdClaim = User.FindFirst("Id")?.Value;
        if (userIdClaim == null) return Unauthorized();

        var userId = long.Parse(userIdClaim);

        var rutaImagen = await GuardarImagenPublicacion(dto.ImagenBase64);

        var nuevaPublicacion = new Publicacion
        {
            Contenido = dto.Contenido,
            Imagen = rutaImagen,
            UsuarioId = userId,
            Fecha = DateTime.Now,
            PublicacionPadreId = dto.PublicacionPadreId
        };

        _context.Publicaciones.Add(nuevaPublicacion);

        int puntosGanados = 0;
        bool esPrimeraPublicacion = !await _context.Publicaciones
            .AnyAsync(p => p.UsuarioId == userId && p.PublicacionPadreId == null);

        if (esPrimeraPublicacion)
        {
            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario != null)
            {
                usuario.Puntos += 50;
                puntosGanados = 50;
            }
        }

        await _context.SaveChangesAsync();

        return Ok(new { mensaje = "Publicado con éxito", puntosGanados });
    }

    private async Task<string?> GuardarImagenPublicacion(string? base64)
    {
        if (string.IsNullOrEmpty(base64) || !base64.Contains("base64,")) return null;

        var base64Data = base64.Substring(base64.IndexOf(",") + 1);
        var imageBytes = Convert.FromBase64String(base64Data);

        var folderPath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "publicaciones");
        if (!Directory.Exists(folderPath)) Directory.CreateDirectory(folderPath);

        var fileName = Guid.NewGuid().ToString() + ".jpg";
        var filePath = Path.Combine(folderPath, fileName);

        await System.IO.File.WriteAllBytesAsync(filePath, imageBytes);

        var request = HttpContext.Request;
        return $"{request.Scheme}://{request.Host}/publicaciones/{fileName}";
    }

    [HttpDelete("{id}")]
    [Authorize]
    public async Task<IActionResult> DeletePublicacion(long id)
    {
        var publicacion = await _context.Publicaciones.FindAsync(id);
        if (publicacion == null) return NotFound();

        var userId = User.FindFirst("Id")?.Value;
        if (publicacion.UsuarioId.ToString() != userId && !User.IsInRole("Admin"))
            return Forbid();

        _context.Publicaciones.Remove(publicacion);
        await _context.SaveChangesAsync();
        return Ok();
    }
}