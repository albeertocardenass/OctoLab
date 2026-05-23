using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using OctoLab.Server.Data;
using OctoLab.Server.DTOs;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;

namespace OctoLab.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TemarioController : ControllerBase
    {
        private readonly MyDbContext _context;

        // Puntos que se otorgan al completar cada tema del laboratorio
        private static readonly Dictionary<int, int> PuntosPorTema = new()
        {
            { 1, 100 },   // Reconocimiento con Nmap
            { 2, 150 },   // Explotación con Metasploit
        };

        public TemarioController(MyDbContext context)
        {
            _context = context;
        }

        [HttpPost("verificar-codigo")]
        [Authorize]
        public async Task<IActionResult> VerificarCodigo([FromBody] VerificarCodigoDto dto)
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized();
            var userId = long.Parse(userIdClaim);

            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            // Comprobar que el tema no fue completado ya
            var completados = string.IsNullOrEmpty(usuario.TemasCompletados)
                ? new HashSet<int>()
                : new HashSet<int>(usuario.TemasCompletados.Split(',').Select(int.Parse));

            if (completados.Contains(dto.TemaId))
                return BadRequest(new { mensaje = "Este tema ya fue completado anteriormente." });

            // Validar el código (mismo algoritmo que el cliente Python)
            var codigoEsperado = GenerarCodigoHex(userId, dto.TemaId);
            if (!string.Equals(dto.Codigo.Trim(), codigoEsperado, StringComparison.OrdinalIgnoreCase))
                return BadRequest(new { mensaje = "Código incorrecto." });

            // Sumar puntos
            var puntosGanados = PuntosPorTema.GetValueOrDefault(dto.TemaId, 100);
            usuario.Puntos += puntosGanados;

            // Registrar tema como completado
            completados.Add(dto.TemaId);
            usuario.TemasCompletados = string.Join(",", completados);

            await _context.SaveChangesAsync();

            return Ok(new
            {
                puntos = usuario.Puntos,
                puntosGanados
            });
        }

        [HttpGet("progreso/{usuarioId}")]
        [Authorize]
        public async Task<IActionResult> GetProgreso(long usuarioId)
        {
            var usuario = await _context.Usuarios.FindAsync(usuarioId);
            if (usuario == null) return NotFound();

            var completados = string.IsNullOrEmpty(usuario.TemasCompletados)
                ? new List<int>()
                : usuario.TemasCompletados.Split(',').Select(int.Parse).ToList();

            return Ok(new { temasCompletados = completados, puntos = usuario.Puntos });
        }

        [HttpGet("{moduloId}/pdf")]
        [Authorize]
        public async Task<IActionResult> GetPdf(int moduloId)
        {
            var userIdClaim = User.FindFirst("Id")?.Value;
            if (userIdClaim == null) return Unauthorized();
            var userId = long.Parse(userIdClaim);

            var usuario = await _context.Usuarios.FindAsync(userId);
            if (usuario == null) return NotFound();

            var desbloqueados = string.IsNullOrEmpty(usuario.ModulosDesbloqueados)
                ? new HashSet<int>()
                : new HashSet<int>(usuario.ModulosDesbloqueados.Split(',').Select(int.Parse));

            if (!desbloqueados.Contains(moduloId) && usuario.Rol != "Admin")
                return Forbid();

            var pdfsDir = Path.Combine(Directory.GetCurrentDirectory(), "Resources", "Pdfs");
            var pdfPath = Directory.EnumerateFiles(pdfsDir, $"Tema {moduloId:D2}*").FirstOrDefault();

            if (pdfPath == null)
                return NotFound(new { mensaje = "PDF no disponible para este módulo todavía." });

            return PhysicalFile(pdfPath, "application/pdf");
        }

        // Mismo algoritmo que utils/crypto.py en el cliente Python:
        // raw = f"{usuario_id}-{tema_id}-{int(time.time() // 86400)}-octolab"
        // hashlib.sha256(raw).hexdigest()[:16].upper()
        private static string GenerarCodigoHex(long usuarioId, int temaId)
        {
            var dia = DateTimeOffset.UtcNow.ToUnixTimeSeconds() / 86400;
            var raw = $"{usuarioId}-{temaId}-{dia}-octolab";
            using var sha256 = SHA256.Create();
            var hash = sha256.ComputeHash(Encoding.UTF8.GetBytes(raw));
            return Convert.ToHexString(hash)[..16].ToUpper();
        }
    }
}
