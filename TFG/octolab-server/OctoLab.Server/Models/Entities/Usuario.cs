using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace OctoLab.Server.Models.Entities
{
    public class Usuario
    {
        [Key]
        public long Id { get; set; }
        public required string Nombre { get; set; }
        public required string Apellido1 { get; set; }
        public string? Apellido2 { get; set; }
        public required string Apodo { get; set; }
        public required string Email { get; set; }
        public required string Password { get; set; }
        // LONGTEXT para almacenar la imagen en base64 directamente en la BD
        [Column(TypeName = "LONGTEXT")]
        public string? Avatar { get; set; }
        public string? Descripcion { get; set; }
        public string Rol { get; set; } = "Usuario";
        public int Puntos { get; set; } = 0;
        public DateTime FechaRegistro { get; set; } = DateTime.Now;
        public DateTime UltimaConexion { get; set; } = DateTime.Now;
        public string ModulosDesbloqueados { get; set; } = "";
        public string TemasCompletados { get; set; } = "";
    }
}