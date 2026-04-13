using System.ComponentModel.DataAnnotations;

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

        public string Avatar { get; set; } = "default-avatar.png";

        public string? Descripcion { get; set; }

        public string Rol { get; set; } = "Usuario";

        public DateTime FechaRegistro { get; set; } = DateTime.Now;

        public DateTime? UltimaConexion { get; set; } = null;
    }
}
