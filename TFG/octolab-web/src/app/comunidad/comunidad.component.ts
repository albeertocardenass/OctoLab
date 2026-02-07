import { Component } from '@angular/core';

@Component({
  selector: 'app-comunidad',
  standalone: true,
  template: `
    <div class="fade-in">
      <h2>👥 Comunidad Octolab</h2>
      <p>Conecta con otros desarrolladores y comparte tus progresos.</p>
      <div class="forum-preview">
        <div class="post">
          <strong>Alberto Cárdenas:</strong> "¿Alguien sabe cómo inyectar el Router en un componente standalone?"
          <span class="tag">Ayuda</span>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .forum-preview { margin-top: 2rem; }
    .post { padding: 1rem; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .tag { background: #fee2e2; color: #ef4444; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 10px; }
  `]
})
export class ComunidadComponent {}