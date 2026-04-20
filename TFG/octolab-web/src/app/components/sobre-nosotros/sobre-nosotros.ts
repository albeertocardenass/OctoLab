import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sobre-nosotros',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sobre-nosotros.html',
  styleUrl: './sobre-nosotros.css',
})
export class SobreNosotrosComponent {
  equipo = [
    {
      nombre: 'Juan Alberto Campaña Espejo',
      alias: 'Juan Alberto',
      descripcion: 'Apasionado de la tecnología y el desarrollo. Cree que la ciberseguridad debería ser accesible para todo el mundo, no solo para expertos.',
      emoji: '🦈'
    },
    {
      nombre: 'Alberto Cárdenas Palomo',
      alias: 'Alberto',
      descripcion: 'Curioso por naturaleza y amante de los retos técnicos. Convencido de que la mejor forma de aprender es construyendo cosas reales.',
      emoji: '🐙'
    }
  ];

}

