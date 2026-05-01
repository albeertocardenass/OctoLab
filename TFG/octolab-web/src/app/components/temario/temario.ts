import { Component, OnInit, inject, NgZone, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { AuthService } from '../../services/auth.service';

interface Modulo {
  id: number;
  costo: number;
  icono: string;
  titulo: string;
  descripcion: string;
}

@Component({
  selector: 'app-temario',
  standalone: true,
  imports: [CommonModule, DecimalPipe],
  templateUrl: './temario.html',
  styleUrl: './temario.css',
  changeDetection: ChangeDetectionStrategy.OnPush   // ← detección explícita
})
export class TemarioComponent implements OnInit {
  private authService = inject(AuthService);
  private zone = inject(NgZone);
  private cdr = inject(ChangeDetectorRef);           // ← forzamos actualización manual

  usuario: any = null;

  // Set para lookup O(1) en lugar de .some() con iteración
  modulosDesbloqueadosSet = new Set<number>();

  // Tracks módulos en proceso de desbloqueo para evitar doble clic
  desbloqueando = new Set<number>();

  modulos: Modulo[] = [
    { id: 1,  costo: 20, icono: '🔐', titulo: 'Fundamentos de Ciberseguridad',      descripcion: 'Protección de sistemas, Tríada CIA e importancia en la era digital.' },
    { id: 2,  costo: 30, icono: '🖥️', titulo: 'Seguridad en Sistemas Operativos',   descripcion: 'Actualizaciones, parches, antivirus y gestión del menor privilegio.' },
    { id: 3,  costo: 30, icono: '🌐', titulo: 'Redes y Seguridad de Redes',          descripcion: 'Protocolos TCP/IP, Firewalls, VPN, segmentación y Wi-Fi seguro.' },
    { id: 4,  costo: 50, icono: '🕵️‍♂️', titulo: 'Ethical Hacking / Pentesting',   descripcion: 'Evaluación de resiliencia, simulacros y uso de Kali Linux o Metasploit.' },
    { id: 5,  costo: 40, icono: '🔍', titulo: 'Análisis de Vulnerabilidades',        descripcion: 'Amenazas, vulnerabilidades, cálculo de riesgos y medidas de mitigación.' },
    { id: 6,  costo: 30, icono: '🧠', titulo: 'Ingeniería Social',                   descripcion: 'Phishing, Vishing, Baiting y tácticas de manipulación psicológica.' },
    { id: 7,  costo: 40, icono: '🛡️', titulo: 'Seguridad Web',                      descripcion: 'Prevención de SQL Injection, XSS, CSRF y validación de entradas.' },
    { id: 8,  costo: 30, icono: '📱', titulo: 'Seguridad en Dispositivos Móviles',   descripcion: 'Protección contra robo, malware, biometría y políticas BYOD/MDM.' },
    { id: 9,  costo: 50, icono: '🔑', titulo: 'Criptografía Básica',                 descripcion: 'Cifrado en reposo y tránsito, E2EE y certificados digitales (CA).' },
    { id: 10, costo: 40, icono: '☁️', titulo: 'Seguridad en la Nube',               descripcion: 'Modelos SaaS, PaaS, IaaS, riesgos asociados y gobernanza IAM/SLA.' },
    { id: 11, costo: 40, icono: '🚨', titulo: 'Respuesta ante Incidentes',           descripcion: 'Fases de respuesta, contención, recuperación y Regla de Backup 3-2-1.' },
    { id: 12, costo: 20, icono: '⚖️', titulo: 'Legalidad y Ética',                  descripcion: 'Cumplimiento del GDPR, principios éticos y diferencias de seguridad.' }
  ];

  ngOnInit(): void {
    this.usuario = this.authService.getUsuarioActual();

    if (this.usuario) {
      if (!this.usuario.modulosDesbloqueados) {
        this.usuario.modulosDesbloqueados = [];
      }
      // Construimos el Set inicial para lookups rápidos
      this.sincronizarSet();
    }
  }

  private sincronizarSet(): void {
    this.modulosDesbloqueadosSet = new Set(
      (this.usuario?.modulosDesbloqueados ?? []).map(Number)
    );
  }

  estaDesbloqueado(id: number): boolean {
    return this.modulosDesbloqueadosSet.has(id);
  }

  estaDesbloqueando(id: number): boolean {
    return this.desbloqueando.has(id);
  }

  obtenerTemasVistos(): number {
    return this.modulosDesbloqueadosSet.size;
  }

  get progresoPorcentaje(): number {
    return (this.obtenerTemasVistos() / this.modulos.length) * 100;
  }

  desbloquearOAbrir(mod: Modulo): void {
    // Si ya está desbloqueado → abrir directamente
    if (this.estaDesbloqueado(mod.id)) {
      alert(`Abriendo: ${mod.titulo}`);
      return;
    }

    // Evitar solicitudes duplicadas mientras se procesa
    if (this.estaDesbloqueando(mod.id)) return;

    if (!this.usuario || this.usuario.puntos < mod.costo) {
      alert('No tienes puntos suficientes para desbloquear este tema.');
      return;
    }

    const nuevosPuntos = this.usuario.puntos - mod.costo;

    // ── Actualización optimista ANTES de la petición ──────────────────────
    this.desbloqueando.add(mod.id);
    this.modulosDesbloqueadosSet.add(mod.id);
    this.usuario = {
      ...this.usuario,
      puntos: nuevosPuntos,
      modulosDesbloqueados: [...this.usuario.modulosDesbloqueados, mod.id]
    };
    this.authService.actualizarUsuarioLocal(this.usuario);
    this.cdr.detectChanges();                        // ← fuerza render inmediato
    // ──────────────────────────────────────────────────────────────────────

    this.authService.actualizarPuntos(nuevosPuntos).subscribe({
      next: () => {
        this.zone.run(() => {
          this.desbloqueando.delete(mod.id);
          this.cdr.detectChanges();                  // ← actualiza spinner/botón al terminar
          console.log(`Módulo ${mod.id} desbloqueado correctamente.`);
        });
      },
      error: (err) => {
        console.error(err);

        // Rollback si falla el servidor
        this.zone.run(() => {
          this.desbloqueando.delete(mod.id);
          this.modulosDesbloqueadosSet.delete(mod.id);
          this.usuario = {
            ...this.usuario,
            puntos: this.usuario.puntos + mod.costo,
            modulosDesbloqueados: this.usuario.modulosDesbloqueados.filter(
              (id: number) => Number(id) !== mod.id
            )
          };
          this.authService.actualizarUsuarioLocal(this.usuario);
          this.cdr.detectChanges();                  // ← actualiza la UI en rollback
          alert('Error de conexión. No se pudo desbloquear el módulo.');
        });
      }
    });
  }
}