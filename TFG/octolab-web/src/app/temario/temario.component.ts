import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-temario',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="fade-in">
      <h2>📚 Temario del Curso</h2>
      <p>Explora los módulos de aprendizaje disponibles en Octolab.</p>
      <div class="list-container">
        <div class="module-card" *ngFor="let mod of modulos">
          <div class="icon">📖</div>
          <div class="info">
            <h3>{{ mod.titulo }}</h3>
            <p>{{ mod.lecciones }} lecciones</p>
          </div>
          <button class="btn-open">Abrir</button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .module-card { display: flex; align-items: center; background: #f8fafc; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #e2e8f0; transition: transform 0.2s; }
    .module-card:hover { transform: translateX(10px); border-color: #4f46e5; }
    .icon { font-size: 2rem; margin-right: 1.5rem; }
    .info { flex: 1; }
    .info h3 { margin: 0; color: #1e293b; }
    .info p { margin: 5px 0 0; color: #64748b; font-size: 0.9rem; }
    .btn-open { background: #4f46e5; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
    .fade-in { animation: fadeIn 0.5s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  `]
})
export class TemarioComponent {
  modulos = [
    { titulo: 'Introducción a Angular', lecciones: 5 },
    { titulo: 'Arquitectura Standalone', lecciones: 8 },
    { titulo: 'Navegación y Rutas Hijas', lecciones: 4 }
  ];
}