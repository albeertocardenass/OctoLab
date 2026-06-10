import { Component, inject } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { API_BASE } from '../../services/api.config';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class RegisterComponent {
  private http = inject(HttpClient);
  public router = inject(Router);

  registerData = {
    nombre: '',
    apellido1: '',
    apellido2: '',
    apodo: '',
    email: '',
    password: '',
  };

  errorMessage = '';
  mostrarPassword = false;
  mostrarConfirmar = false;
  confirmarPassword = '';

  get pwReqs() {
    const pw = this.registerData.password;
    return {
      len:   pw.length >= 6,
      upper: /[A-Z]/.test(pw),
      digit: /[0-9]/.test(pw),
    };
  }

  get pwValid() {
    return this.pwReqs.len && this.pwReqs.upper && this.pwReqs.digit;
  }

  onRegister() {
    if (this.registerData.password !== this.confirmarPassword) {
      this.errorMessage = 'Las contraseñas no coinciden.';
      return;
    }

    this.http.post(`${API_BASE}/api/Auth/register`, this.registerData).subscribe({
      next: (_res) => {
        alert('¡Usuario registrado con éxito!');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Error completo:', err);
        if (err.error?.field === 'email') {
          this.errorMessage = 'El correo ya está registrado.';
        } else if (err.error?.field === 'apodo') {
          this.errorMessage = 'El apodo ya está en uso.';
        } else if (typeof err.error === 'string') {
          this.errorMessage = err.error;
        } else {
          this.errorMessage = 'Error al registrar. Revisa consola y backend.';
        }
      },
    });
  }
}