import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { TransitionService } from '../../services/transition.service';
import { API_BASE } from '../../services/api.config';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class LoginComponent implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private platformId = inject(PLATFORM_ID);
  private authService = inject(AuthService);
  private transitionService = inject(TransitionService);

  loginData = { email: '', password: '' };
  recuerdame = false;
  errorMessage = '';
  returnUrl: string = '/home/inicio';
  mostrarPassword = false;

  ngOnInit() {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/home/inicio';
  }

  onLogin() {
    this.http.post(`${API_BASE}/api/Usuarios/login`, this.loginData).subscribe({
      next: (res: any) => {
        if (isPlatformBrowser(this.platformId)) {
          const token = res.token || res.Token;
          const usuario = res.usuario || res.Usuario;

          if (!token || !usuario) {
            this.errorMessage = 'Error en la respuesta del servidor';
            return;
          }

          this.authService.setUser(usuario, token, this.recuerdame);

          const rol = usuario.rol || usuario.Rol;
          const destino = rol === 'Admin' ? '/admin' : this.returnUrl;

          this.transitionService.show();
          setTimeout(() => {
            this.router.navigateByUrl(destino);
            setTimeout(() => this.transitionService.hide(), 700);
          }, 1800);
        }
      },
      error: (err) => {
        this.errorMessage = 'Email o contraseña incorrectos.';
        console.error('Error en el login:', err);
      }
    });
  }

  entrarComoInvitado() {
    if (isPlatformBrowser(this.platformId)) {
      const usuarioInvitado = { rol: 'Invitado', nombre: 'Invitado', apodo: 'Invitado' };
      this.authService.setUser(usuarioInvitado, 'token-invitado', false);
      this.transitionService.show();
      setTimeout(() => {
        this.router.navigateByUrl('/home/inicio');
        setTimeout(() => this.transitionService.hide(), 700);
      }, 1200);
    }
  }

  toggleMostrarPassword() {
    this.mostrarPassword = !this.mostrarPassword;
  }
}
