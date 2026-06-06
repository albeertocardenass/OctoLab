using OctoLab.Server.Models.Entities;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProyectoRS.Server.Models.Database.Entities
{
    public class Publicacion
    {
        public long Id { get; set; }
        public string Contenido { get; set; } = string.Empty;
        [Column(TypeName = "LONGTEXT")]
        public string? Imagen { get; set; }
        public DateTime Fecha { get; set; } = DateTime.Now;
        public long UsuarioId { get; set; }
        public long? PublicacionPadreId { get; set; }
        public Usuario? Usuario { get; set; }
        public ICollection<UsuarioLike> Likes { get; set; } = new List<UsuarioLike>();
    }
}