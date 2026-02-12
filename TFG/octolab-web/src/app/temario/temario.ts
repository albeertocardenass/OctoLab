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
    { titulo: 'Introducción a Angular', lecciones: 5 },
    { titulo: 'Arquitectura Standalone', lecciones: 8 },
    { titulo: 'Navegación y Rutas Hijas', lecciones: 4 }
  ];
}