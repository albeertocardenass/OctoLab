import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { API_BASE } from './api.config';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedIn = false;
  private currentUser: any = null;
  private pingInterval: any = null;
  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID);

  constructor() {
    if (typeof window !== 'undefined') {
      const savedUser = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
      if (savedUser) {
        this.currentUser = JSON.parse(savedUser);
        this.loggedIn = true;
        this.iniciarPing();
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

    this.iniciarPing();
  }

  private iniciarPing() {
    if (!isPlatformBrowser(this.platformId)) return;
    
    this.detenerPing();
    
    // Ping inmediato al login
    this.enviarPing();
    
    // Ping cada 2 minutos
    this.pingInterval = setInterval(() => {
      this.enviarPing();
    }, 2 * 60 * 1000);
  }

  private enviarPing() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (!token) return;

    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    this.http.post(`${API_BASE}/api/Usuarios/ping`, {}, { headers }).subscribe();
  }

  private detenerPing() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
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
    this.detenerPing();
    this.loggedIn = false;
    this.currentUser = null;
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    sessionStorage.removeItem('usuario');
    sessionStorage.removeItem('token');
  }
}