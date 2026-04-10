import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
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
    // Asegúrate de que este puerto coincide con el de tu servidor
    const url = `http://localhost:5276/api/Usuarios/${this.usuarioActivo.id}`;

    this.http.put(url, this.usuarioActivo).subscribe({
      next: () => {
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem('usuario', JSON.stringify(this.usuarioActivo));
          this.mensaje = 'Datos actualizados con exito';
          this.error = false;
          setTimeout(() => window.location.reload(), 1500);
        }
      },
      error: (err) => {
        this.error = true;
        this.mensaje = 'Error al conectar con el servidor';
        console.error(err);
      }
    });
  }
}