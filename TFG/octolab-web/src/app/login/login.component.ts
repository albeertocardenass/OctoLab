import { Component } from '@angular/core';
import { Router } from '@angular/router'; // 1. Importar el Router

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  // 2. Inyectar en el constructor
  constructor(private router: Router) {}

  onLogin() {
    // Aquí iría tu validación (ej: con auth.service.ts)
    const success = true; 

    if (success) {
      console.log('Login exitoso, redirigiendo...');
      // 3. Navegar a la ruta 'home'
      this.router.navigate(['/home']);
    }
  }
}