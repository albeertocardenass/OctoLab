import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule, HttpClientModule],
  templateUrl: './register.html',
  styleUrl: '../login/login.css',
})
export class RegisterComponent {
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

  constructor(
    private http: HttpClient,
    public router: Router,
  ) {}

  onRegister() {
    console.log('Submit ejecutado');

    if (this.registerData.password !== this.confirmarPassword) {
      this.errorMessage = 'Las contraseñas no coinciden.';
      return;
    }

    const url = 'http://localhost:5276/api/Auth/register';

    console.log('Enviando a:', url);
    console.log('Datos:', this.registerData);

    this.http.post(url, this.registerData).subscribe({
      next: (res) => {
        console.log('Respuesta OK:', res);
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
