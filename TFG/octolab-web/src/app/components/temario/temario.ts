import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-temario',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './temario.html',
  styleUrl: './temario.css'
})
export class TemarioComponent {
  modulos = [
    { titulo: 'Introducción a Octolab', lecciones: 5 },
    { titulo: 'Fundamentos de la ciberseguridad', lecciones: 8 },
    { titulo: 'Prácticas de Seguridad', lecciones: 10 }
  ];

  usuarioActivo() {
    if (typeof window !== 'undefined') {
      const datos = localStorage.getItem('usuario_activo');
      return datos ? JSON.parse(datos) : null;
    }
    return null;
  }
}