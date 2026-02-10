import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="fade-in">
      <h2>⚙️ Configuración de Perfil</h2>
      
      <div class="form-group">
        <label>Nombre de Usuario</label>
        <input type="text" [(ngModel)]="usuarioActivo.nombre">
      </div>

      <div class="form-group">
        <label>Email de Notificaciones</label>
        <input type="email" [(ngModel)]="usuarioActivo.email">
      </div>

      <div class="form-group">
        <label>Nueva Contraseña</label>
        <input type="password" [(ngModel)]="usuarioActivo.password" placeholder="Escribe para cambiarla">
      </div>

      <button class="btn-save" (click)="guardarCambios()">Guardar Cambios</button>
      
      <p *ngIf="mensaje" [style.color]="error ? 'red' : 'green'" style="margin-top: 15px; font-weight: bold;">
        {{ mensaje }}
      </p>
    </div>
  `,
  styles: [`
    .form-group { margin-bottom: 1.5rem; display: flex; flex-direction: column; max-width: 400px; }
    label { margin-bottom: 0.5rem; font-weight: 600; color: #475569; }
    input { padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; }
    .btn-save { background: #1e293b; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; transition: 0.3s; }
    .btn-save:hover { background: #334155; }
    .fade-in { animation: fadeIn 0.5s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  `]
})
export class ConfiguracionComponent implements OnInit {
  usuarioActivo: any = { id: 0, nombre: '', email: '', password: '' };
  mensaje: string = '';
  error: boolean = false;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const datos = localStorage.getItem('usuario');
      if (datos) {
        this.usuarioActivo = JSON.parse(datos);
        this.usuarioActivo.password = ''; 
      }
    }
  }

  guardarCambios() {

    const url = `http://localhost:5276/api/Usuarios/${this.usuarioActivo.id}`;

    this.http.put(url, this.usuarioActivo).subscribe({
      next: (res: any) => {
        if (isPlatformBrowser(this.platformId)) {

          localStorage.setItem('usuario', JSON.stringify(this.usuarioActivo));
          this.mensaje = '¡Datos actualizados! Recargando...';
          this.error = false;

          setTimeout(() => window.location.reload(), 1500);
        }
      },
      error: (err) => {
        this.error = true;
        this.mensaje = 'Error al conectar con la base de datos.';
        console.error(err);
      }
    });
  }
}