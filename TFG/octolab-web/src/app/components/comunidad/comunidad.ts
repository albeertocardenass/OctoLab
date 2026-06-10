import { Component, OnInit, ViewChild, ElementRef, PLATFORM_ID, inject, signal } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { PublicacionService } from '../../services/publicaciones.service';
import { AuthService } from '../../services/auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { API_BASE } from '../../services/api.config';

@Component({
  selector: 'app-comunidad',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './comunidad.html',
  styleUrls: ['./comunidad.css'],
})
export class ComunidadComponent implements OnInit {
  private pubService = inject(PublicacionService);
  private authService = inject(AuthService);
  private platformId = inject(PLATFORM_ID);
  private router = inject(Router);
  private http = inject(HttpClient);

  usuarioActivo: any = null;
  nuevaPublicacion: string = '';
  publicaciones = signal<any[]>([]);
  pageSize: number = 10;
  paginaActual: number = 1;

  respondiendo: number | null = null;
  textoRespuesta: string = '';

  @ViewChild('postsList') postsListRef!: ElementRef;

  ngOnInit() {
    this.cargarDatosSeguros();
    if (isPlatformBrowser(this.platformId)) {
      this.cargarComunidad();
    }
  }

  cargarDatosSeguros() {
    if (isPlatformBrowser(this.platformId)) {
      const datosUser = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
      if (datosUser && datosUser !== 'null' && datosUser !== 'undefined') {
        this.usuarioActivo = JSON.parse(datosUser);
      }
    }
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  cargarComunidad() {
    this.pubService.obtenerPublicaciones().subscribe({
      next: (data: any[]) => {
        const lista = data
          .filter(p => !p.publicacionPadreId)
          .sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime())
          .map(p => ({
            ...p,
            liked: false,
            totalLikes: 0,
            respuestas: data
              .filter(r => r.publicacionPadreId === p.id)
              .sort((a, b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime())
          }));
        this.publicaciones.set(lista);
        lista.forEach(p => this.cargarLikes(p));
      },
      error: (err) => console.error('Error al cargar publicaciones', err)
    });
  }

  cargarLikes(post: any) {
    this.http.get<any>(`${API_BASE}/api/Likes/${post.id}`, { headers: this.getHeaders() }).subscribe({
      next: (res) => {
        post.totalLikes = res.totalLikes;
        post.liked = res.liked;
        // Forzar reactividad actualizando el signal con el mismo array
        this.publicaciones.update(v => [...v]);
      }
    });
  }

  toggleLike(postId: number) {
    if (!this.usuarioActivo) {
      this.router.navigate(['/login']);
      return;
    }
    this.http.post<any>(`${API_BASE}/api/Likes/${postId}`, {}, { headers: this.getHeaders() }).subscribe({
      next: (res) => {
        const lista = this.publicaciones();
        const post = lista.find(p => p.id === postId);
        if (post) {
          post.liked = res.liked;
          post.totalLikes += res.liked ? 1 : -1;
          this.publicaciones.update(v => [...v]);
        }
      }
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
          const usuarioActualizado = {
            ...this.authService.getUsuarioActual(),
            puntos: (this.authService.getUsuarioActual()?.puntos || 0) + res.puntosGanados
          };
          this.authService.actualizarUsuarioLocal(usuarioActualizado);
          this.usuarioActivo = usuarioActualizado;
          alert(`¡Primera publicación! +${res.puntosGanados} Puntos Octo`);
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
    return !!url && (url.startsWith('http') || url.startsWith('data:'));
  }

  cambiarPageSize(size: number) {
    this.pageSize = size;
    this.paginaActual = 1;
  }

  get totalPaginas(): number {
    return Math.ceil(this.publicaciones().length / this.pageSize);
  }

  paginaAnterior() {
    if (this.paginaActual > 1) {
      this.paginaActual--;
      this.scrollAlInicio();
    }
  }

  paginaSiguiente() {
    if (this.paginaActual < this.totalPaginas) {
      this.paginaActual++;
      this.scrollAlInicio();
    }
  }

  private scrollAlInicio() {
    if (!isPlatformBrowser(this.platformId)) return;
    this.postsListRef?.nativeElement?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  get publicacionesVisibles() {
    const inicio = (this.paginaActual - 1) * this.pageSize;
    return this.publicaciones().slice(inicio, inicio + this.pageSize);
  }
}
