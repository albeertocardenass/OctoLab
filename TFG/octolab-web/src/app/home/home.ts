import { Component, OnInit, Inject, PLATFORM_ID, HostListener } from '@angular/core';
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
  usuarioActivo: any = null;
  isMenuOpen: boolean = false;
  isDarkMode: boolean = false;

  constructor(
    public router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const datos = localStorage.getItem('usuario');
      if (datos) {
        this.usuarioActivo = JSON.parse(datos);
      }
      // Mantiene el tema si se recarga la página
      this.isDarkMode = document.body.classList.contains('dark-theme');
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
      localStorage.removeItem('usuario');
      localStorage.removeItem('token');
      document.body.classList.remove('dark-theme');
    }
    this.router.navigate(['/login']);
  }

  descargarAppPython() {
    const link = document.createElement('a');
    link.href = 'assets/OctoLab_v1.exe';
    link.download = 'OctoLab_v1.exe';
    link.click();
  }
}