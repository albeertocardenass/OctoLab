import { Component, OnInit, HostListener, PLATFORM_ID, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PublicacionService } from '../../services/publicaciones.service';

@Component({
  selector: 'app-comunidad',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './comunidad.html',
  styleUrls: ['./comunidad.css'],
})
export class ComunidadComponent implements OnInit {
  private pubService = inject(PublicacionService);
  private platformId = inject(PLATFORM_ID);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef);

  usuarioActivo: any = null;
  nuevaPublicacion: string = '';
  publicaciones: any[] = [];
  cantidadVisible: number = 10;

  respondiendo: number | null = null;
  textoRespuesta: string = '';

  ngOnInit() {
    this.cargarDatosSeguros();
    this.cargarComunidad();
  }

  cargarDatosSeguros() {
    if (isPlatformBrowser(this.platformId)) {
      const datosUser = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
      if (datosUser && datosUser !== 'null' && datosUser !== 'undefined') {
        this.usuarioActivo = JSON.parse(datosUser);
      }
    }
  }

  cargarComunidad() {
    this.pubService.obtenerPublicaciones().subscribe({
      next: (data) => {
        this.publicaciones = data
          .filter(p => !p.publicacionPadreId)
          .sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime())
          .map(p => ({
            ...p,
            respuestas: data
              .filter(r => r.publicacionPadreId === p.id)
              .sort((a, b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime())
          }));
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error al cargar publicaciones', err)
    });
  }

  publicar() {
    if (!this.usuarioActivo || !this.usuarioActivo.id) {
      this.router.navigate(['/login']);
      return;
    }
    if (!this.nuevaPublicacion?.trim()) return;

    const body = { contenido: this.nuevaPublicacion };

    this.pubService.crearPublicacion(body).subscribe({
      next: (res: any) => {
        this.nuevaPublicacion = '';

        if (res.puntosGanados > 0) {
          const enLocal = !!localStorage.getItem('usuario');
          const storage = enLocal ? localStorage : sessionStorage;
          const userData = JSON.parse(storage.getItem('usuario')!);
          userData.puntos = (userData.puntos || 0) + res.puntosGanados;
          storage.setItem('usuario', JSON.stringify(userData));
          this.usuarioActivo = userData;
          alert(`🎉 ¡Primera publicación! +${res.puntosGanados} Puntos Octo`);
        }

        this.cargarComunidad();
      },
      error: (err) => console.error('Error al publicar:', err)
    });
  }

  responder(postId: number) {
    if (!this.usuarioActivo || !this.usuarioActivo.id) {
      this.router.navigate(['/login']);
      return;
    }
    if (!this.textoRespuesta?.trim()) return;

    const body = {
      contenido: this.textoRespuesta,
      publicacionPadreId: postId
    };

    this.pubService.crearPublicacion(body).subscribe({
      next: () => {
        this.textoRespuesta = '';
        this.respondiendo = null;
        this.cargarComunidad();
      },
      error: (err) => console.error('Error al responder:', err)
    });
  }

  toggleResponder(postId: number) {
    if (this.respondiendo === postId) {
      this.respondiendo = null;
      this.textoRespuesta = '';
    } else {
      this.respondiendo = postId;
      this.textoRespuesta = '';
    }
  }

  borrar(id: number) {
    if (confirm('¿Seguro que quieres borrar este mensaje?')) {
      this.pubService.borrarPublicacion(id).subscribe({
        next: () => this.cargarComunidad(),
        error: () => alert('No se pudo borrar.')
      });
    }
  }

  onKeydownPublicar(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.publicar();
    }
  }

  onKeydownResponder(event: KeyboardEvent, postId: number) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.responder(postId);
    }
  }

  esImagenReal(url: string): boolean {
    return !!url && url.startsWith('http');
  }

  get publicacionesVisibles() {
    return this.publicaciones.slice(0, this.cantidadVisible);
  }

  @HostListener('window:scroll')
  onScroll(): void {
    if (isPlatformBrowser(this.platformId)) {
      const pos = (document.documentElement.scrollTop || document.body.scrollTop) + document.documentElement.offsetHeight;
      const max = document.documentElement.scrollHeight;
      if (pos >= max - 100 && this.cantidadVisible < this.publicaciones.length) {
        this.cantidadVisible += 10;
        this.cdr.detectChanges();
      }
    }
  }
}