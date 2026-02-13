import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
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
  tabs: string[] = ['Inicio', 'Temario', 'Comunidad', 'Donaciones', 'Configuración'];

  constructor(
    public router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {

    if (isPlatformBrowser(this.platformId)) {
      const datos = localStorage.getItem('usuario');
      if (datos) {
        this.usuarioActivo = JSON.parse(datos);
        this.usuarioActivo.rol = 'Admin';
      }
    }
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('usuario');
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
