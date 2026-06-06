using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Data;
using OctoLab.Server.Models.Entities;

namespace OctoLab.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class LikesController : ControllerBase
    {
        private readonly MyDbContext _context;

        public LikesController(MyDbContext context)
        {
            _context = context;
        }

        [HttpPost("{publicacionId}")]
        [Authorize]
        public async Task<IActionResult> ToggleLike(long publicacionId)
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized();
            var userId = long.Parse(userIdClaim);

            var like = await _context.UsuarioLikes
                .FirstOrDefaultAsync(ul => ul.UsuarioId == userId && ul.PublicacionId == publicacionId);

            if (like != null)
            {
                _context.UsuarioLikes.Remove(like);
                await _context.SaveChangesAsync();
                return Ok(new { liked = false });
            }
            else
            {
                _context.UsuarioLikes.Add(new UsuarioLike
                {
                    UsuarioId = userId,
                    PublicacionId = publicacionId
                });
                await _context.SaveChangesAsync();
                return Ok(new { liked = true });
            }
        }

        [HttpGet("{publicacionId}")]
        [Authorize]
        public async Task<IActionResult> GetLikes(long publicacionId)
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized();
            var userId = long.Parse(userIdClaim);

            var totalLikes = await _context.UsuarioLikes
                .CountAsync(ul => ul.PublicacionId == publicacionId);

            var liked = await _context.UsuarioLikes
                .AnyAsync(ul => ul.UsuarioId == userId && ul.PublicacionId == publicacionId);

            return Ok(new { totalLikes, liked });
        }
    }
}