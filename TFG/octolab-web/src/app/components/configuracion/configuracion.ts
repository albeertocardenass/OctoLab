import { Component, OnInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './configuracion.html',
  styleUrl: './configuracion.css'
})
export class ConfiguracionComponent implements OnInit {
  
  // 1. Inyectamos dependencias (Adiós error TS1206)
  private readonly platformId = inject(PLATFORM_ID);
  private readonly http = inject(HttpClient);

  usuarioActivo: any = { id: 0, nombre: '', email: '', password: '' };
  mensaje: string = '';
  error: boolean = false;

  constructor() {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      // 2. Usamos 'usuario_activo' para mantener la sesión unificada
      const datos = localStorage.getItem('usuario_activo');
      if (datos) {
        try {
          this.usuarioActivo = JSON.parse(datos);
          // Ocultamos el password por seguridad en el formulario
          this.usuarioActivo.password = ''; 
        } catch (e) {
          console.error('Error al cargar datos de configuración', e);
        }
      }
    }
  }

  guardarCambios() {
    // Usamos el ID dinámico (soportando id o Id según tu server .NET)
    const idUsuario = this.usuarioActivo.id || this.usuarioActivo.Id;
    const url = `http://localhost:5276/api/Usuarios/${idUsuario}`;

    this.http.put(url, this.usuarioActivo).subscribe({
      next: () => {
        if (isPlatformBrowser(this.platformId)) {
          // Actualizamos el storage para que el nombre cambie en el Header de inmediato
          localStorage.setItem('usuario_activo', JSON.stringify(this.usuarioActivo));
          
          this.mensaje = 'Datos actualizados con éxito';
          this.error = false;
          
          // Recarga suave para refrescar toda la UI
          setTimeout(() => window.location.reload(), 1500);
        }
      },
      error: (err: any) => {
        this.error = true;
        this.mensaje = 'Error al conectar con el servidor';
        console.error('Error en PUT usuarios:', err);
      }
    });
  }
}