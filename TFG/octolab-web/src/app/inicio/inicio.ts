import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.html',
  styleUrl: './inicio.css',
})

export class InicioComponent implements OnInit {
  usuarioActivo: any = null;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const datos = localStorage.getItem('usuario');
      if (datos) {
        this.usuarioActivo = JSON.parse(datos);
      }
    }
  }
}
