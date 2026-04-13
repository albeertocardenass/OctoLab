using Microsoft.AspNetCore.Mvc;
using System.Xml.Linq;

namespace OctoLab.Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class NoticiasController : ControllerBase
    {
        private readonly HttpClient _httpClient;

        public NoticiasController(IHttpClientFactory httpClientFactory)
        {
            _httpClient = httpClientFactory.CreateClient();
        }

        [HttpGet]
        public async Task<ActionResult> GetNoticias()
        {
            try
            {
                var rssUrl = "https://feeds.feedburner.com/TheHackersNews";
                var response = await _httpClient.GetStringAsync(rssUrl);

                var xml = XDocument.Parse(response);
                var noticias = xml.Descendants("item")
                    .Take(10)
                    .Select(item =>
                    {
                        var enclosure = item.Element("enclosure");
                        var imagen = enclosure?.Attribute("url")?.Value ?? "";

                        return new
                        {
                            titulo = item.Element("title")?.Value ?? "",
                            enlace = item.Element("link")?.Value ?? "",
                            fecha = item.Element("pubDate")?.Value ?? "",
                            imagen
                        };
                    });

                return Ok(noticias);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error al obtener noticias: {ex.Message}");
            }
        }

        [HttpGet("imagen")]
        public async Task<ActionResult> GetImagen([FromQuery] string url)
        {
            try
            {
                var bytes = await _httpClient.GetByteArrayAsync(url);
                var contentType = "image/jpeg";
                if (url.EndsWith(".png")) contentType = "image/png";
                if (url.EndsWith(".gif")) contentType = "image/gif";
                if (url.EndsWith(".webp")) contentType = "image/webp";
                return File(bytes, contentType);
            }
            catch
            {
                return NotFound();
            }
        }
    }
}