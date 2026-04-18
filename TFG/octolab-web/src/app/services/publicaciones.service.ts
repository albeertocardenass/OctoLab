import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';
import { API_BASE } from './api.config';

@Injectable({
  providedIn: 'root'
})
export class PublicacionService {
  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID);
  private apiUrl = `${API_BASE}/api/Publicaciones`;

  private getHeaders() {
    let token = '';
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem('token') || sessionStorage.getItem('token') || '';
    }
    return new HttpHeaders({
      'Authorization': token ? `Bearer ${token}` : ''
    });
  }

  obtenerPublicaciones(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  crearPublicacion(publicacion: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, publicacion, { headers: this.getHeaders() });
  }

  borrarPublicacion(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }
}