import { Component, inject, ChangeDetectorRef, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxStripeModule } from 'ngx-stripe';
import { API_BASE } from '../../services/api.config';

@Component({
  selector: 'app-donation',
  standalone: true,
  imports: [CommonModule, FormsModule, NgxStripeModule],
  templateUrl: './donation.html',
  styleUrl: './donation.css'
})
export class DonationComponent implements OnInit {
  private http = inject(HttpClient);
  private cdr = inject(ChangeDetectorRef);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private platformId = inject(PLATFORM_ID);

  cantidad: number = 0;
  cantidadPersonalizada: number | null = null;
  pagando: boolean = false;
  mensajeExito: string = '';
  mensajeError: string = '';
  nombreUsuario: string = '';

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.nombreUsuario = this.resolverNombreUsuario();

      const exito = this.route.snapshot.queryParams['exito'];
      const cancelado = this.route.snapshot.queryParams['cancelado'];

      if (exito) {
        this.mensajeExito = 'exito';
        this.darPuntosDonacion();
        this.cdr.detectChanges();
      }

      if (cancelado) {
        this.mensajeError = 'Pago cancelado. Puedes intentarlo de nuevo cuando quieras.';
        this.cdr.detectChanges();
      }
    }
  }

  private resolverNombreUsuario(): string {
    const raw = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
    if (!raw) return '';
    try {
      const u = JSON.parse(raw);
      return u?.nombre || u?.Nombre || '';
    } catch {
      return '';
    }
  }

  volverAlInicio() {
    this.router.navigate(['/home/inicio']);
  }

  private darPuntosDonacion() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (!token) return;
    this.http.post(`${API_BASE}/api/Pagos/donar-puntos`, {}, {
      headers: new HttpHeaders({ Authorization: `Bearer ${token}` })
    }).subscribe();
  }

  seleccionarCantidad(valor: number) {
    this.cantidad = valor;
    this.cantidadPersonalizada = null;
  }

  get cantidadFinal(): number {
    return this.cantidadPersonalizada && this.cantidadPersonalizada > 0
      ? this.cantidadPersonalizada
      : this.cantidad;
  }

  iniciarPago() {
    if (this.cantidadFinal < 1) {
      this.mensajeError = 'La cantidad mínima es 1€';
      return;
    }

    this.mensajeError = '';
    this.pagando = true;
    this.cdr.detectChanges();

    this.http.post<any>(`${API_BASE}/api/Pagos/crear-sesion`, {
      cantidad: this.cantidadFinal
    }).subscribe({
      next: (res) => {
        window.location.href = res.url;
      },
      error: () => {
        this.mensajeError = 'Error al conectar con el servidor de pagos.';
        this.pagando = false;
        this.cdr.detectChanges();
      }
    });
  }
}
