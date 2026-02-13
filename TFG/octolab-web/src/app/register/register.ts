import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: '../login/login.css'
})
export class RegisterComponent {
  registerData = {
    nombre: '',
    apellido1: '',
    apellido2: '',
    apodo: '',
    email: '',
    password: ''
  };
  errorMessage = '';

  constructor(private http: HttpClient, public router: Router) {}

  onRegister() {
    const url = 'http://localhost:5276/api/Auth/register'; 

    this.http.post(url, this.registerData).subscribe({
      next: () => {
        alert('¡Usuario registrado con éxito!');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.errorMessage = 'Error al registrar. El email podría estar duplicado.';
        console.error(err);
      }
    });
  }
}