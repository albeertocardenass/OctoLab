namespace OctoLab.Server.DTOs;

public class PublicacionCrearDto
{
    public string Contenido { get; set; } = string.Empty;
    public string? ImagenBase64 { get; set; }
    public long? PublicacionPadreId { get; set; }
}