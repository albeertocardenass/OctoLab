import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedIn = false;
  private currentUser: any = null;

  constructor() {
    if (typeof window !== 'undefined') {
      const savedUser = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
      if (savedUser) {
        this.currentUser = JSON.parse(savedUser);
        this.loggedIn = true;
      }
    }
  }

  setUser(user: any, token: string, rememberMe: boolean) {
    this.currentUser = user;
    this.loggedIn = true;
    
    const userData = JSON.stringify(user);
    if (rememberMe) {
      localStorage.setItem('token', token);
      localStorage.setItem('usuario', userData);
    } else {
      sessionStorage.setItem('token', token);
      sessionStorage.setItem('usuario', userData);
    }
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
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    sessionStorage.removeItem('usuario');
    sessionStorage.removeItem('token');
  }
}
