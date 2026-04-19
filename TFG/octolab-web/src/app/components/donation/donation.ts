import { Component, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
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

  cantidad: number = 5;
  cantidadPersonalizada: number | null = null;
  pagando: boolean = false;
  mensajeExito: string = '';
  mensajeError: string = '';

  ngOnInit() {
    const exito = this.route.snapshot.queryParams['exito'];
    const cancelado = this.route.snapshot.queryParams['cancelado'];

    if (exito) {
      this.mensajeExito = '¡Gracias por tu donación! Tu apoyo significa mucho para OctoLab.';
      this.cdr.detectChanges();
    }
    if (cancelado) {
      this.mensajeError = 'Pago cancelado. Puedes intentarlo de nuevo cuando quieras.';
      this.cdr.detectChanges();
    }
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