import { Component } from '@angular/core';

@Component({
  selector: 'app-comunidad',
  standalone: true,
  template: `
    <div class="fade-in">
      <h2>👥 Comunidad Octolab/SharkLab</h2>
      <p>Pregunta y conecta con otros Sharks y comparte tu progreso</p>
      <div class="forum-preview">
        <div class="post">
          <p><strong>Alberto Cárdenas:</strong> "¿Es suficiente con usar un ORM (como Prisma, Sequelize o Entity Framework) para estar 100% protegido contra SQL Injection, o existen escenarios donde todavía podríamos ser vulnerables?"</p>
          <p><strong>Juan Alberto:</strong>"¿Cuál es la diferencia real entre un 'Exploit' y un 'Payload' en Metasploit? Siempre los confundo."
          <span class="tag">Ayuda</span></p>
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