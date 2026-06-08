import { Component, OnInit, OnDestroy, inject, PLATFORM_ID, HostListener, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  private readonly platformId = inject(PLATFORM_ID);
  private readonly cdr = inject(ChangeDetectorRef);
  private readonly authService = inject(AuthService);
  readonly themeService = inject(ThemeService);
  public readonly router = inject(Router);

  usuarioActivo: any = null;
  isMenuOpen: boolean = false;
  private sub: Subscription | null = null;

  get isDarkMode(): boolean {
    return this.themeService.isDarkMode;
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.sub = this.authService.usuario$.subscribe(usuario => {
        if (usuario) {
          this.usuarioActivo = { ...usuario };
          this.cdr.detectChanges();
        }
      });

      if (!this.usuarioActivo) {
        const datos = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
        if (datos) {
          try {
            this.usuarioActivo = JSON.parse(datos);
          } catch {
            this.router.navigate(['/login']);
          }
        } else {
          this.router.navigate(['/login']);
        }
      }

      this.themeService.init();
    }
  }

  ngOnDestroy() {
    this.sub?.unsubscribe();
  }

  esAvatarValido(av: any): boolean {
    return !!av && (av.startsWith('http') || av.startsWith('data:'));
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
    this.themeService.toggle();
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      this.authService.logout();
      localStorage.clear();
      sessionStorage.clear();
    }
    this.isMenuOpen = false;
    this.usuarioActivo = null;
    this.router.navigate(['/login']);
  }

  descargarApp() {
    if (isPlatformBrowser(this.platformId)) {
      const link = document.createElement('a');
      link.href = 'assets/OctolabDesktop.exe';
      link.download = 'OctolabDesktop.exe';
      link.click();
    }
  }
}
