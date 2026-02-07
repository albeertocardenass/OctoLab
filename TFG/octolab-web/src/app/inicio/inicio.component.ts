import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="inicio-container">
      <div class="welcome-section">
        <h1>¡Hola de nuevo, Admin! 👋</h1>
        <p>Bienvenido al panel central de OctolabWeb. Aquí tienes un resumen de lo que está pasando.</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <span class="icon">📊</span>
          <div class="data">
            <span class="label">Progreso Total</span>
            <span class="value">65%</span>
          </div>
        </div>
        <div class="stat-card">
          <span class="icon">📚</span>
          <div class="data">
            <span class="label">Temas Vistos</span>
            <span class="value">12 / 20</span>
          </div>
        </div>
        <div class="stat-card">
          <span class="icon">🌟</span>
          <div class="data">
            <span class="label">Puntos Octo</span>
            <span class="value">1,250</span>
          </div>
        </div>
      </div>

      <div class="info-box">
        <h3>📢 Última actualización</h3>
        <p>Hemos añadido nuevos módulos en la sección de <strong>Temario</strong>. ¡No olvides echarles un vistazo!</p>
      </div>
    </div>
  `,
  styles: [`
    .inicio-container {
      animation: fadeIn 0.5s ease-in-out;
    }
    .welcome-section h1 {
      color: #1e293b;
      font-size: 1.8rem;
      margin-bottom: 0.5rem;
    }
    .welcome-section p {
      color: #64748b;
      margin-bottom: 2rem;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2rem;
    }
    .stat-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 1.5rem;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .stat-card .icon {
      font-size: 2rem;
    }
    .stat-card .label {
      display: block;
      font-size: 0.85rem;
      color: #64748b;
    }
    .stat-card .value {
      font-size: 1.25rem;
      font-weight: bold;
      color: #4f46e5;
    }
    .info-box {
      background: #eef2ff;
      border-left: 4px solid #4f46e5;
      padding: 1.5rem;
      border-radius: 8px;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `]
})
export class InicioComponent {}