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

        private static readonly Dictionary<int, int> PuntosPorTema = new()
        {
            {  1, 240 },  // Fundamentos          (coste 180)
            {  2, 280 },  // Sistemas Operativos  (coste 250)
            {  3, 280 },  // Redes                (coste 250)
            {  4, 420 },  // Ethical Hacking       (coste 380)
            {  5, 350 },  // Vulnerabilidades      (coste 320)
            {  6, 310 },  // Ingeniería Social     (coste 290)
            {  7, 380 },  // Seguridad Web         (coste 340)
            {  8, 310 },  // Dispositivos Móviles  (coste 290)
            {  9, 420 },  // Criptografía          (coste 380)
            { 10, 350 },  // Nube                  (coste 320)
            { 11, 350 },  // Respuesta Incidentes  (coste 320)
            { 12, 250 },  // Legalidad             (coste 260)
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


            var completados = string.IsNullOrEmpty(usuario.TemasCompletados)
                ? new HashSet<int>()
                : new HashSet<int>(usuario.TemasCompletados.Split(',').Select(int.Parse));

            if (completados.Contains(dto.TemaId))
                return BadRequest(new { mensaje = "Este tema ya fue completado anteriormente." });


            var codigoEsperado = GenerarCodigoHex(userId, dto.TemaId);
            if (!string.Equals(dto.Codigo.Trim(), codigoEsperado, StringComparison.OrdinalIgnoreCase))
                return BadRequest(new { mensaje = "Código incorrecto." });


            var puntosGanados = PuntosPorTema.GetValueOrDefault(dto.TemaId, 100);
            usuario.Puntos += puntosGanados;


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
