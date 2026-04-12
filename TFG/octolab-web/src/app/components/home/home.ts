import { Component, OnInit, inject, PLATFORM_ID, HostListener } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html', 
  styleUrls: ['./home.css'] 
})
export class HomeComponent implements OnInit {
  // 1. Inyectamos dependencias con inject() (Elimina el error TS1206)
  private readonly platformId = inject(PLATFORM_ID);
  public readonly router = inject(Router);

  usuarioActivo: any = null;
  isMenuOpen: boolean = false;
  isDarkMode: boolean = false;

  // El constructor queda limpio
  constructor() {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      // 2. Buscamos la sesión guardada
      const datos = localStorage.getItem('usuario_activo'); 
      
      if (datos) {
        try {
          this.usuarioActivo = JSON.parse(datos);
          console.log('Sesión recuperada en Home:', this.usuarioActivo);
        } catch (e) {
          console.error('Error al parsear datos del usuario', e);
          this.router.navigate(['/login']);
        }
      } else {
        console.warn('No se encontró sesión, redirigiendo...');
        this.router.navigate(['/login']);
      }
    }
  }

  toggleMenu(event: Event) {
    event.stopPropagation();
    this.isMenuOpen = !this.isMenuOpen;
  }

  @HostListener('document:click')
  closeMenu() {
    this.isMenuOpen = false;
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    if (isPlatformBrowser(this.platformId)) {
      if (this.isDarkMode) {
        document.body.classList.add('dark-theme');
      } else {
        document.body.classList.remove('dark-theme');
      }
    }
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      // Limpiamos TODAS las posibles claves de sesión
      localStorage.removeItem('usuario_activo');
      localStorage.removeItem('usuario');
      localStorage.removeItem('token');
      document.body.classList.remove('dark-theme');
    }
    this.router.navigate(['/login']);
  }

  descargarAppPython() {
    if (isPlatformBrowser(this.platformId)) {
      const link = document.createElement('a');
      link.href = 'assets/OctoLab_v1.exe';
      link.download = 'OctoLab_v1.exe';
      link.click();
    }
  }
}