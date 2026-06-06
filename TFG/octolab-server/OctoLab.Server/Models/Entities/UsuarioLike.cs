using ProyectoRS.Server.Models.Database.Entities;

namespace OctoLab.Server.Models.Entities
{
    public class UsuarioLike
    {
        public long UsuarioId { get; set; }
        public Usuario? Usuario { get; set; }

        public long PublicacionId { get; set; }
        public Publicacion? Publicacion { get; set; }
    }
}