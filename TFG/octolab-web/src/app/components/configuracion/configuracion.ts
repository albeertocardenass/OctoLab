import { Component, OnInit, OnDestroy, inject, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../../services/auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-configuracion',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './configuracion.html',
  styleUrl: './configuracion.css'
})
export class ConfiguracionComponent implements OnInit, OnDestroy {
  private readonly platformId = inject(PLATFORM_ID);
  private readonly http = inject(HttpClient);
  private readonly cdr = inject(ChangeDetectorRef);
  private readonly authService = inject(AuthService);
  private sub: Subscription | null = null;

  usuarioActivo: any = { id: 0, nombre: '', email: '', password: '', avatar: '' };
  mensaje: string = '';
  error: boolean = false;
  imagenPreview: string | null = null;
  subiendoAvatar: boolean = false;
  avatarError: boolean = false;

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.sub = this.authService.usuario$.subscribe(usuario => {
        if (usuario) {
          this.usuarioActivo = { ...usuario, password: '' };
          this.avatarError = false;
          this.cdr.detectChanges();
        }
      });
    }
  }

  ngOnDestroy() {
    this.sub?.unsubscribe();
  }

  get avatarSrc(): string | null {
    if (this.imagenPreview) return this.imagenPreview;
    const av = this.usuarioActivo?.avatar;
    if (av && av.startsWith('http')) return av;
    return null;
  }

  onAvatarImgError() {
    this.avatarError = true;
    this.cdr.detectChanges();
  }

  seleccionarImagen(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      this.imagenPreview = reader.result as string;
      this.avatarError = false;
      this.cdr.detectChanges();
      this.subirAvatar(this.imagenPreview);
    };
    reader.readAsDataURL(file);
  }

  private subirAvatar(base64: string) {
    const idUsuario = this.usuarioActivo.id || this.usuarioActivo.Id;
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });

    this.subiendoAvatar = true;
    this.cdr.detectChanges();

    this.http.post<any>(`/api/Usuarios/${idUsuario}/avatar`, { imagenBase64: base64 }, { headers }).subscribe({
      next: (res) => {
        this.subiendoAvatar = false;
        this.imagenPreview = null;
        this.usuarioActivo.avatar = res.avatarUrl;
        this.authService.actualizarUsuarioLocal(this.usuarioActivo);
        this.mensaje = 'Foto de perfil actualizada';
        this.error = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.subiendoAvatar = false;
        this.error = true;
        this.mensaje = `Error al subir la imagen (${err.status})`;
        this.cdr.detectChanges();
      }
    });
  }

  guardarCambios() {
    const idUsuario = this.usuarioActivo.id || this.usuarioActivo.Id;
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });

    this.http.put(`/api/Usuarios/${idUsuario}`, this.usuarioActivo, { headers }).subscribe({
      next: () => {
        if (isPlatformBrowser(this.platformId)) {
          this.authService.actualizarUsuarioLocal(this.usuarioActivo);
          this.mensaje = 'Datos actualizados con éxito';
          this.error = false;
          this.cdr.detectChanges();
        }
      },
      error: (err: any) => {
        this.error = true;
        this.mensaje = `Error al conectar con el servidor (${err.status})`;
        this.cdr.detectChanges();
      }
    });
  }
}
