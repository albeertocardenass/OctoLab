using OctoLab.Server.Models.Entities;

namespace ProyectoRS.Server.Models.Database.Entities;

public class Publicacion
{
    public long Id { get; set; }
    public string Contenido { get; set; } = string.Empty;
    public string? Imagen { get; set; }
    public DateTime Fecha { get; set; } = DateTime.Now;
    public long UsuarioId { get; set; }
    public long? PublicacionPadreId { get; set; } // ← nuevo
    public Usuario? Usuario { get; set; }
}