import { Component, OnInit, inject, ChangeDetectorRef, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.css']
})
export class InicioComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly cdr = inject(ChangeDetectorRef);
  private readonly platformId = inject(PLATFORM_ID);

  noticias: any[] = [];
  cargandoNoticias = true;
  usuarioActivo: any = null;

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      const datos = localStorage.getItem('usuario_activo');
      if (datos) this.usuarioActivo = JSON.parse(datos);
      
      this.cargarNoticias();
    }
  }

  cargarNoticias() {
    this.http.get<any[]>('/api/Noticias').subscribe({
      next: (res) => {
        this.noticias = res;
        this.cargandoNoticias = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.cargandoNoticias = false;
        this.cdr.detectChanges();
      }
    });
  }

  getImagenUrl(url: string): string {
    return `/api/Noticias/imagen?url=${encodeURIComponent(url)}`;
  }
}