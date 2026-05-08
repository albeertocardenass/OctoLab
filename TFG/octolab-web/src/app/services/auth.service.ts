import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { API_BASE } from './api.config';
import { Observable } from 'rxjs';

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

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    return new HttpHeaders({ 'Authorization': `Bearer ${token}` });
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
    this.enviarPing();
    this.pingInterval = setInterval(() => {
      this.enviarPing();
    }, 2 * 60 * 1000);
  }

  private enviarPing() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (!token) return;
    this.http.post(`${API_BASE}/api/Usuarios/ping`, {}, { headers: this.getAuthHeaders() }).subscribe();
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

  getUsuarioActual() {
    return this.currentUser;
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

  actualizarPuntos(nuevosPuntos: number): Observable<any> {
    const url = `${API_BASE}/api/Usuarios/actualizar-puntos`;
    const body = { puntos: nuevosPuntos };
    return this.http.put<any>(url, body, { headers: this.getAuthHeaders() });
  }

  actualizarProgreso(nuevosPuntos: number, modulosDesbloqueados: number[]): Observable<any> {
    const url = `${API_BASE}/api/Usuarios/actualizar-progreso`;
    const body = { puntos: nuevosPuntos, modulosDesbloqueados };
    return this.http.put<any>(url, body, { headers: this.getAuthHeaders() });
  }

  actualizarUsuarioLocal(usuarioActualizado: any) {
    this.currentUser = usuarioActualizado;
    const userData = JSON.stringify(usuarioActualizado);
    if (localStorage.getItem('usuario')) {
      localStorage.setItem('usuario', userData);
    } else {
      sessionStorage.setItem('usuario', userData);
    }
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