import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedIn = false;
  private currentUser: any = null;

  constructor() {
    // Al cargar el servicio, verificamos si hay una sesión guardada
    if (typeof window !== 'undefined') {
      const savedUser = localStorage.getItem('usuario_activo');
      if (savedUser) {
        this.currentUser = JSON.parse(savedUser);
        this.loggedIn = true;
      }
    }
  }

  // Este método lo llamarás desde el onLogin() de tu LoginComponent
  setUser(user: any) {
    this.currentUser = user;
    this.loggedIn = true;
    localStorage.setItem('usuario_activo', JSON.stringify(user));
  }

  getNombreUsuario(): string {
    return this.currentUser?.nombre || 'Usuario';
  }

  getRol(): string {
    return this.currentUser?.rol || 'Invitado';
  }

  isLoggedIn(): boolean {
    return this.loggedIn;
  }

  isAdmin(): boolean {
    return this.getRol() === 'Admin';
  }

  logout() {
    this.loggedIn = false;
    this.currentUser = null;
    localStorage.removeItem('usuario_activo');
    localStorage.removeItem('usuario'); // Limpieza extra por si acaso
  }
}
