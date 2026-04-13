import { Component, OnInit, inject, PLATFORM_ID, HostListener, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule], // Ya no necesita HttpClientModule aquí porque no pide noticias
  templateUrl: './home.html', 
  styleUrls: ['./home.css'] 
})
export class HomeComponent implements OnInit {
  private readonly platformId = inject(PLATFORM_ID);
  private readonly cdr = inject(ChangeDetectorRef);
  public readonly router = inject(Router);

  usuarioActivo: any = null;
  isMenuOpen: boolean = false;
  isDarkMode: boolean = false;

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const datos = localStorage.getItem('usuario_activo'); 
      
      if (datos) {
        try {
          this.usuarioActivo = JSON.parse(datos);
        } catch (e) {
          this.router.navigate(['/login']);
        }
      } else {
        this.router.navigate(['/login']);
      }

      const temaGuardado = localStorage.getItem('tema');
      this.isDarkMode = temaGuardado === 'dark';
      if (this.isDarkMode) {
        document.body.classList.add('dark-theme');
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
        localStorage.setItem('tema', 'dark');
      } else {
        document.body.classList.remove('dark-theme');
        localStorage.setItem('tema', 'light');
      }
    }
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('usuario_activo');
      localStorage.removeItem('token');
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