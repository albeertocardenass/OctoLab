namespace OctoLab.Server.DTOs
{
    public class VerificarCodigoDto
    {
        public long UsuarioId { get; set; }
        public int TemaId { get; set; }
        public string Codigo { get; set; } = "";
    }
}
