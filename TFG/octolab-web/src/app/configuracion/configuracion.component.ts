import { Component } from '@angular/core';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  template: `
    <div class="fade-in">
      <h2>⚙️ Configuración</h2>
      <div class="form-group">
        <label>Nombre de Usuario</label>
        <input type="text" value="Admin">
      </div>
      <div class="form-group">
        <label>Email de Notificaciones</label>
        <input type="email" value="admin@octolab.com">
      </div>
      <button class="btn-save">Guardar Cambios</button>
    </div>
  `,
  styles: [`
    .form-group { margin-bottom: 1.5rem; display: flex; flex-direction: column; max-width: 400px; }
    label { margin-bottom: 0.5rem; font-weight: 600; color: #475569; }
    input { padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; }
    .btn-save { background: #1e293b; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; }
  `]
})
export class ConfiguracionComponent {}