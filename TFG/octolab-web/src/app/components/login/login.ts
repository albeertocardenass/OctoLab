import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class LoginComponent {
  loginData = { email: '', password: '' };
  errorMessage = '';

  constructor(private http: HttpClient, public router: Router) {}

  onLogin() {
    const url = '/api/Auth/login';

    this.http.post(url, this.loginData).subscribe({
      next: (response: any) => {
        console.log('Login exitoso:', response);
        localStorage.setItem('usuario_activo', JSON.stringify(response.usuario));

        if (response.usuario.rol === 'Admin') {
          this.router.navigate(['/admin']);
        } else {
          this.router.navigate(['/home/inicio']);
        }
      },
      error: (error) => {
        this.errorMessage = 'Email o contraseña incorrectos';
        console.error('Error en el login', error);
      }
    });
  }

  entrarComoInvitado() {
    const url = '/api/Auth/invitado';

    this.http.post(url, {}).subscribe({
      next: (response: any) => {
        console.log('Acceso como invitado:', response);
        localStorage.setItem('usuario_activo', JSON.stringify(response.usuario));
        this.router.navigate(['/home/inicio']);
      },
      error: (error) => {
        this.errorMessage = 'No se pudo acceder como invitado';
        console.error('Error al entrar como invitado', error);
      }
    });
  }

  mostrarPassword: boolean = false;

  toggleMostrarPassword() {
    this.mostrarPassword = !this.mostrarPassword;
  }
}