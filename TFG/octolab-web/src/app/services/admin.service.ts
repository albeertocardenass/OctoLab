import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private apiUrl = '/api/Usuarios';

  constructor(private http: HttpClient) {}

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