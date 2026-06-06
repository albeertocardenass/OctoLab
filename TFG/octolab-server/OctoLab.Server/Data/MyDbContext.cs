using Microsoft.EntityFrameworkCore;
using OctoLab.Server.Models.Entities;
using ProyectoRS.Server.Models.Database.Entities;

namespace OctoLab.Server.Data
{
    public class MyDbContext : DbContext
    {
        public MyDbContext(DbContextOptions<MyDbContext> options) : base(options)
        {
        }

        public DbSet<Usuario> Usuarios { get; set; }
        public DbSet<Publicacion> Publicaciones { get; set; }
        public DbSet<UsuarioLike> UsuarioLikes { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Usuario>().HasIndex(u => u.Email).IsUnique();
            modelBuilder.Entity<Usuario>().HasIndex(u => u.Apodo).IsUnique();

            modelBuilder.Entity<Publicacion>()
                .HasOne(p => p.Usuario)
                .WithMany()
                .HasForeignKey(p => p.UsuarioId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<UsuarioLike>()
                .HasKey(ul => new { ul.UsuarioId, ul.PublicacionId });

            modelBuilder.Entity<UsuarioLike>()
                .HasOne(ul => ul.Usuario)
                .WithMany(u => u.Likes)
                .HasForeignKey(ul => ul.UsuarioId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<UsuarioLike>()
                .HasOne(ul => ul.Publicacion)
                .WithMany(p => p.Likes)
                .HasForeignKey(ul => ul.PublicacionId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}