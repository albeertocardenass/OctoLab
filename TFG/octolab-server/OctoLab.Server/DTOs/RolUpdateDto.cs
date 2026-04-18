namespace OctoLab.Server.DTOs  // ⚠️ Estaba en Controllers, muévelo a DTOs
{
    public class RolUpdateDto
    {
        public long Id { get; set; }        // era object?[]?
        public string NuevoRol { get; set; } = string.Empty;  // era object
    }
}