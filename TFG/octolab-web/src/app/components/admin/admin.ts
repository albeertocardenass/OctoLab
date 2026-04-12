import { Component, OnInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { AdminService } from '../../services/admin.service'; 

@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, RouterModule],
  templateUrl: './admin.html',
  styleUrls: ['./admin.css']
})
export class AdminPanelComponent implements OnInit {
  
  // Inyección de dependencias moderna
  private readonly platformId = inject(PLATFORM_ID);
  private readonly adminService = inject(AdminService);
  private readonly router = inject(Router);
  public readonly authService = inject(AuthService);

  // Array de usuarios que vendrá de octolab.db
  usuarios: any[] = [];

  constructor() {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      const storedUser = localStorage.getItem('usuario_activo');
      if (!storedUser) {
        this.router.navigate(['/login']);
        return;
      }

      const user = JSON.parse(storedUser);
      // Soportamos 'rol' y 'Rol' por si el servidor varía
      const userRol = user.rol || user.Rol;
      
      if (userRol !== 'Admin') {
        this.router.navigate(['/home']);
        return;
      }
    }

    // 2. Cargar la lista inicial de la DB
    this.cargarUsuarios();
  }

  // En admin.component.ts
    cargarUsuarios() {
      this.adminService.getUsuarios().subscribe({
        next: (res) => {
          // Forzamos la asignación en un nuevo ciclo de ejecución
          setTimeout(() => {
            this.usuarios = [...res]; 
            console.log('Usuarios cargados:', this.usuarios.length);
          }, 0);
        },
        error: (err) => console.error('Error al conectar con la API:', err)
      });
    }

  getUsuariosActivos(): number {
    if (this.usuarios.length === 0) return 0;

    const ahora = new Date();
    // Definimos el límite: por ejemplo, conectados en las últimas 24 horas
    const limiteActivo = 24 * 60 * 60 * 1000; 

    return this.usuarios.filter(u => {
      const fechaConexion = new Date(u.ultimaConexion || u.UltimaConexion);
      const diferencia = ahora.getTime() - fechaConexion.getTime();
      return diferencia < limiteActivo;
    }).length;
  }

  toggleAdminRole(user: any) {
    const id = user.id || user.Id;
    const currentRol = user.rol || user.Rol;
    const nuevoRol = currentRol === 'Admin' ? 'Usuario' : 'Admin';

    this.adminService.cambiarRol(id, nuevoRol).subscribe({
      next: () => {
        console.log('Rol cambiado con éxito');
        this.cargarUsuarios(); // RECARGA LA TABLA
      },
      error: (err) => console.error('Error al cambiar rol', err)
    });
  }

  eliminarUsuario(id: number) {
    if (confirm('¿Estás seguro de que deseas eliminar este usuario de la base de datos?')) {
      this.adminService.eliminarUsuario(id).subscribe({
        next: () => {
          // Filtramos el array local para que desaparezca de la tabla sin recargar
          this.usuarios = this.usuarios.filter(u => (u.id || u.Id) !== id);
        },
        error: (err: any) => {
          alert('No se pudo eliminar el usuario. Revisa la consola.');
          console.error(err);
        }
      });
    }
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  esActivo(fecha: any): boolean {
    if (!fecha) return false;
    const ahora = new Date().getTime();
    const conexion = new Date(fecha).getTime();
    const limite = 24 * 60 * 60 * 1000; // 24 horas
    return (ahora - conexion) < limite;
  }

}