import { Component, OnInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.html',
  styleUrl: './inicio.css',
})
export class InicioComponent implements OnInit {
  
  // 1. Inyectamos la dependencia de plataforma de forma moderna
  private readonly platformId = inject(PLATFORM_ID);
  
  usuarioActivo: any = null;

  // 2. Constructor limpio
  constructor() {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      // 3. Usamos 'usuario_activo' para ser consistentes con Login y Home
      const datos = localStorage.getItem('usuario_activo');
      
      if (datos) {
        try {
          this.usuarioActivo = JSON.parse(datos);
          console.log('Usuario cargado en Inicio:', this.usuarioActivo);
        } catch (error) {
          console.error('Error al leer los datos de inicio:', error);
        }
      }
    }
  }
}