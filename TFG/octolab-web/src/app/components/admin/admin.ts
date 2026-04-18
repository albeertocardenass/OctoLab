import { Component, OnInit, inject, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
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

  private readonly platformId = inject(PLATFORM_ID);
  private readonly adminService = inject(AdminService);
  private readonly router = inject(Router);
  private readonly cdr = inject(ChangeDetectorRef);
  public readonly authService = inject(AuthService);

  usuarios: any[] = [];

  constructor() { }

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      const storedUser = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
      if (!storedUser) {
        this.router.navigate(['/login']);
        return;
      }

      const user = JSON.parse(storedUser);
      const userRol = user.rol || user.Rol;

      if (userRol !== 'Admin') {
        this.router.navigate(['/home']);
        return;
      }

      this.cargarUsuarios();
    }
  }

  cargarUsuarios() {
    this.adminService.getUsuarios().subscribe({
      next: (res) => {
        this.usuarios = res;
        console.log('Usuarios cargados:', this.usuarios.length, this.usuarios);
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error al conectar con la API:', err)
    });
  }

  getUsuariosActivos(): number {
    if (this.usuarios.length === 0) return 0;
    const ahora = new Date();
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
        this.cargarUsuarios();
      },
      error: (err) => console.error('Error al cambiar rol', err)
    });
  }

  eliminarUsuario(id: number) {
    if (confirm('¿Estás seguro de que deseas eliminar este usuario de la base de datos?')) {
      this.adminService.eliminarUsuario(id).subscribe({
        next: () => {
          this.usuarios = this.usuarios.filter(u => (u.id || u.Id) !== id);
          this.cdr.detectChanges();
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
    const limite = 24 * 60 * 60 * 1000;
    return (ahora - conexion) < limite;
  }
}