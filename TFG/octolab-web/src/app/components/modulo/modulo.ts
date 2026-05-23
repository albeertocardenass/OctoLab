import {
  Component, OnInit, OnDestroy, AfterViewInit,
  ViewChild, ElementRef, HostListener, PLATFORM_ID,
  inject, NgZone, ChangeDetectorRef, ChangeDetectionStrategy
} from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import type { PDFDocumentProxy } from 'pdfjs-dist';

const MODULOS: Record<number, string> = {
  1:  'Fundamentos de Ciberseguridad',
  2:  'Seguridad en Sistemas Operativos',
  3:  'Redes y Seguridad de Redes',
  4:  'Ethical Hacking / Pentesting',
  5:  'Análisis de Vulnerabilidades',
  6:  'Ingeniería Social',
  7:  'Seguridad Web',
  8:  'Seguridad en Dispositivos Móviles',
  9:  'Criptografía Básica',
  10: 'Seguridad en la Nube',
  11: 'Respuesta ante Incidentes',
  12: 'Legalidad y Ética',
};

@Component({
  selector: 'app-modulo',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './modulo.html',
  styleUrl: './modulo.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ModuloComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('canvas')        canvasRef!:        ElementRef<HTMLCanvasElement>;
  @ViewChild('pdfArea')       pdfAreaRef!:       ElementRef<HTMLDivElement>;
  @ViewChild('canvasWrapper') canvasWrapperRef!: ElementRef<HTMLDivElement>;

  private platformId  = inject(PLATFORM_ID);
  private route       = inject(ActivatedRoute);
  private router      = inject(Router);
  private authService = inject(AuthService);
  private zone        = inject(NgZone);
  private cdr         = inject(ChangeDetectorRef);

  moduloId    = 0;
  moduloIdStr = '';
  titulo      = '';

  cargando   = true;
  errorMsg   = '';

  paginaActual = 1;
  totalPaginas = 0;
  renderizando = false;

  codigoInput   = '';
  verificando   = false;
  mensajeCodigo = '';
  tipoMensaje: 'ok' | 'error' | '' = '';

  private pdf: PDFDocumentProxy | null = null;
  private viewReady     = false;
  private pendingRender = false;
  private resizeObserver: ResizeObserver | null = null;

  ngOnInit(): void {
    this.moduloId    = Number(this.route.snapshot.paramMap.get('id'));
    this.moduloIdStr = String(this.moduloId).padStart(2, '0');
    this.titulo      = MODULOS[this.moduloId] ?? `Módulo ${this.moduloIdStr}`;

    if (!isPlatformBrowser(this.platformId)) return;

    const usuario = this.authService.getUsuarioActual();
    const desbloqueados: number[] = (usuario?.modulosDesbloqueados ?? []).map(Number);

    if (!desbloqueados.includes(this.moduloId) && usuario?.rol !== 'Admin') {
      this.router.navigate(['/home/temario']);
      return;
    }

    this.authService.getPdfModulo(this.moduloId).subscribe({
      next: (blob) => this.cargarPdf(blob),
      error: (err) => {
        this.cargando = false;
        this.errorMsg = err.status === 404
          ? 'El PDF de este módulo aún no está disponible.'
          : 'Error al cargar el PDF. Inténtalo más tarde.';
        this.cdr.detectChanges();
      }
    });
  }

  ngAfterViewInit(): void {
    this.viewReady = true;
    if (this.pendingRender) {
      this.pendingRender = false;
      this.iniciarConResizeObserver();
    }
  }

  ngOnDestroy(): void {
    this.pdf?.destroy();
    this.resizeObserver?.disconnect();
  }

  private async cargarPdf(blob: Blob): Promise<void> {
    const { GlobalWorkerOptions, getDocument } = await import('pdfjs-dist');
    GlobalWorkerOptions.workerSrc = 'assets/pdf.worker.min.mjs';

    const buffer  = await blob.arrayBuffer();
    this.pdf      = await getDocument({ data: buffer }).promise;
    this.totalPaginas = this.pdf.numPages;
    this.cargando = false;
    this.cdr.detectChanges();

    if (this.viewReady) {
      // Wait one frame so Angular renders the canvas/wrapper elements
      requestAnimationFrame(() => this.iniciarConResizeObserver());
    } else {
      this.pendingRender = true;
    }
  }

  private iniciarConResizeObserver(): void {
    if (!this.pdfAreaRef) return;

    this.resizeObserver?.disconnect();
    this.resizeObserver = new ResizeObserver(() => {
      if (this.pdf && !this.renderizando) {
        this.renderizarPagina(this.paginaActual);
      }
    });
    // Observing pdfArea triggers immediately with current size → first render
    this.resizeObserver.observe(this.pdfAreaRef.nativeElement);
  }

  async renderizarPagina(num: number): Promise<void> {
    if (!this.pdf || !this.canvasRef || !this.canvasWrapperRef) return;
    this.renderizando = true;
    this.cdr.detectChanges();

    const page    = await this.pdf.getPage(num);
    const wrapper = this.canvasWrapperRef.nativeElement;
    const cs      = window.getComputedStyle(wrapper);
    const W       = Math.max(wrapper.clientWidth  - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight),  200);
    const H       = Math.max(wrapper.clientHeight - parseFloat(cs.paddingTop)  - parseFloat(cs.paddingBottom), 200);
    const vp1     = page.getViewport({ scale: 1 });
    const scale   = Math.min(W / vp1.width, H / vp1.height);
    const vp      = page.getViewport({ scale });

    const canvas = this.canvasRef.nativeElement;
    canvas.width  = vp.width;
    canvas.height = vp.height;
    const ctx = canvas.getContext('2d')!;

    await page.render({ canvasContext: ctx, viewport: vp, canvas }).promise;

    this.renderizando = false;
    this.cdr.detectChanges();
  }

  anterior(): void {
    if (this.paginaActual > 1 && !this.renderizando) {
      this.paginaActual--;
      this.renderizarPagina(this.paginaActual);
    }
  }

  siguiente(): void {
    if (this.paginaActual < this.totalPaginas && !this.renderizando) {
      this.paginaActual++;
      this.renderizarPagina(this.paginaActual);
    }
  }

  @HostListener('document:keydown', ['$event'])
  onKey(e: KeyboardEvent): void {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') this.siguiente();
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   this.anterior();
  }

  volver(): void {
    this.router.navigate(['/home/temario']);
  }

  submitCodigo(): void {
    if (!this.codigoInput.trim() || this.verificando) return;
    this.verificando   = true;
    this.mensajeCodigo = '';
    this.tipoMensaje   = '';
    this.cdr.detectChanges();

    this.authService.verificarCodigo(this.moduloId, this.codigoInput.trim()).subscribe({
      next: (res) => this.zone.run(() => {
        this.verificando   = false;
        this.tipoMensaje   = 'ok';
        this.mensajeCodigo = `¡Correcto! +${res.puntosGanados} pts. Total: ${res.puntos} pts.`;
        this.codigoInput   = '';
        const u = this.authService.getUsuarioActual();
        if (u) this.authService.actualizarUsuarioLocal({ ...u, puntos: res.puntos });
        this.cdr.detectChanges();
      }),
      error: (err) => this.zone.run(() => {
        this.verificando   = false;
        this.tipoMensaje   = 'error';
        this.mensajeCodigo = err.error?.mensaje ?? 'Código incorrecto o ya utilizado.';
        this.cdr.detectChanges();
      })
    });
  }
}
