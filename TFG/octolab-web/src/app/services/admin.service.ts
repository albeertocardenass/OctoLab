import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE } from './api.config';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private apiUrl = `${API_BASE}/api/Usuarios`;

  constructor(private http: HttpClient) { }

  getUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  cambiarRol(id: number, nuevoRol: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/cambiar-rol`, { id, nuevoRol });
  }

  eliminarUsuario(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}