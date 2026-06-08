import { Component, inject, ChangeDetectorRef, OnInit, OnDestroy, PLATFORM_ID, ElementRef, ViewChild, NgZone } from '@angular/core';
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
export class DonationComponent implements OnInit, OnDestroy {
  private http = inject(HttpClient);
  private cdr = inject(ChangeDetectorRef);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private platformId = inject(PLATFORM_ID);
  private zone = inject(NgZone);

  @ViewChild('confettiCanvas') confettiCanvasRef!: ElementRef<HTMLCanvasElement>;

  cantidad: number = 0;
  cantidadPersonalizada: number | null = null;
  pagando: boolean = false;
  mensajeExito: string = '';
  mensajeError: string = '';
  nombreUsuario: string = '';
  countdown: number = 5;

  private redirectTimer: any = null;
  private countdownTimer: any = null;
  private confettiAnim: any = null;

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.nombreUsuario = this.resolverNombreUsuario();
    }

    const exito = this.route.snapshot.queryParams['exito'];
    const cancelado = this.route.snapshot.queryParams['cancelado'];

    if (exito) {
      this.mensajeExito = '¡Gracias por tu donación!';
      this.darPuntosDonacion();
      this.iniciarCuentaAtras();
      this.cdr.detectChanges();
      setTimeout(() => this.lanzarConfetti(), 100);
    }

    if (cancelado) {
      this.mensajeError = 'Pago cancelado. Puedes intentarlo de nuevo cuando quieras.';
      this.cdr.detectChanges();
    }
  }

  ngOnDestroy() {
    this.limpiarTimers();
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

  private iniciarCuentaAtras() {
    if (!isPlatformBrowser(this.platformId)) return;
    this.countdown = 5;

    this.countdownTimer = setInterval(() => {
      this.zone.run(() => {
        this.countdown--;
        this.cdr.detectChanges();
        if (this.countdown <= 0) {
          this.limpiarTimers();
          this.router.navigate(['/home/inicio']);
        }
      });
    }, 1000);
  }

  private limpiarTimers() {
    if (this.redirectTimer) { clearTimeout(this.redirectTimer); this.redirectTimer = null; }
    if (this.countdownTimer) { clearInterval(this.countdownTimer); this.countdownTimer = null; }
    if (this.confettiAnim) { cancelAnimationFrame(this.confettiAnim); this.confettiAnim = null; }
  }

  volverAlInicio() {
    this.limpiarTimers();
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

  private lanzarConfetti() {
    if (!isPlatformBrowser(this.platformId)) return;
    const canvas = this.confettiCanvasRef?.nativeElement;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const colores = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];
    const particulas: any[] = [];

    for (let i = 0; i < 120; i++) {
      particulas.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height - canvas.height,
        w: Math.random() * 10 + 5,
        h: Math.random() * 6 + 3,
        color: colores[Math.floor(Math.random() * colores.length)],
        rot: Math.random() * Math.PI * 2,
        vy: Math.random() * 3 + 2,
        vx: (Math.random() - 0.5) * 2,
        vrot: (Math.random() - 0.5) * 0.15,
        alpha: 1
      });
    }

    const animar = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let activas = 0;

      for (const p of particulas) {
        p.y += p.vy;
        p.x += p.vx;
        p.rot += p.vrot;
        if (p.y > canvas.height * 0.7) {
          p.alpha -= 0.02;
        }
        if (p.alpha <= 0) continue;
        activas++;

        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.translate(p.x + p.w / 2, p.y + p.h / 2);
        ctx.rotate(p.rot);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      }

      if (activas > 0) {
        this.confettiAnim = requestAnimationFrame(animar);
      }
    };

    this.confettiAnim = requestAnimationFrame(animar);
  }
}
