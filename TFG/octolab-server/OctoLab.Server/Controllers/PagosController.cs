using Microsoft.AspNetCore.Mvc;
using Stripe.Checkout;

namespace OctoLab.Server.Controllers;

[Route("api/[controller]")]
[ApiController]
public class PagosController : ControllerBase
{
    private readonly IConfiguration _config;

    public PagosController(IConfiguration config)
    {
        _config = config;
    }

    [HttpPost("crear-sesion")]
    public ActionResult CrearSesion([FromBody] PagoDto dto)
    {
        var frontendUrl = _config["FrontendUrl"]?.TrimEnd('/') ?? "https://octolab.site";
        var options = new SessionCreateOptions
        {
            PaymentMethodTypes = new List<string> { "card" },
            LineItems = new List<SessionLineItemOptions>
        {
            new SessionLineItemOptions
            {
                PriceData = new SessionLineItemPriceDataOptions
                {
                    Currency = "eur",
                    UnitAmount = (long)(dto.Cantidad * 100),
                    ProductData = new SessionLineItemPriceDataProductDataOptions
                    {
                        Name = "Donación a OctoLab",
                        Description = $"Donación de {dto.Cantidad}€"
                    }
                },
                Quantity = 1
            }
        },
            Mode = "payment",
            SuccessUrl = $"{frontendUrl}/home/donaciones?exito=true",
            CancelUrl = $"{frontendUrl}/home/donaciones?cancelado=true"
        };

        var service = new SessionService();
        var session = service.Create(options);

        return Ok(new { url = session.Url });
    }

    [HttpGet("estado-sesion")]
    public ActionResult EstadoSesion([FromQuery] string session_id)
    {
        var service = new SessionService();
        var session = service.Get(session_id);

        return Ok(new
        {
            status = session.Status,
            customerEmail = session.CustomerDetails?.Email
        });
    }
}

public class PagoDto
{
    public decimal Cantidad { get; set; }
}