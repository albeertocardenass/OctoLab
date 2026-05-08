namespace OctoLab.Server.DTOs
{
    public class ProgresoUpdateDto
    {
        public int Puntos { get; set; }
        public List<int> ModulosDesbloqueados { get; set; } = new();
    }
}