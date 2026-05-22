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
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TemarioComponent implements OnInit {
  private authService = inject(AuthService);
  private zone = inject(NgZone);
  private cdr = inject(ChangeDetectorRef);

  usuario: any = null;
  modulosDesbloqueadosSet = new Set<number>();
  desbloqueando = new Set<number>();

  modulos: Modulo[] = [
    { id: 1,  costo: 180, icono: '01', titulo: 'Fundamentos de Ciberseguridad',      descripcion: 'Protección de sistemas, Tríada CIA e importancia en la era digital.' },
    { id: 2,  costo: 250, icono: '02', titulo: 'Seguridad en Sistemas Operativos',   descripcion: 'Actualizaciones, parches, antivirus y gestión del menor privilegio.' },
    { id: 3,  costo: 250, icono: '03', titulo: 'Redes y Seguridad de Redes',          descripcion: 'Protocolos TCP/IP, Firewalls, VPN, segmentación y Wi-Fi seguro.' },
    { id: 4,  costo: 380, icono: '04', titulo: 'Ethical Hacking / Pentesting',        descripcion: 'Evaluación de resiliencia, simulacros y uso de Kali Linux o Metasploit.' },
    { id: 5,  costo: 320, icono: '05', titulo: 'Análisis de Vulnerabilidades',        descripcion: 'Amenazas, vulnerabilidades, cálculo de riesgos y medidas de mitigación.' },
    { id: 6,  costo: 290, icono: '06', titulo: 'Ingeniería Social',                   descripcion: 'Phishing, Vishing, Baiting y tácticas de manipulación psicológica.' },
    { id: 7,  costo: 340, icono: '07', titulo: 'Seguridad Web',                       descripcion: 'Prevención de SQL Injection, XSS, CSRF y validación de entradas.' },
    { id: 8,  costo: 290, icono: '08', titulo: 'Seguridad en Dispositivos Móviles',   descripcion: 'Protección contra robo, malware, biometría y políticas BYOD/MDM.' },
    { id: 9,  costo: 380, icono: '09', titulo: 'Criptografía Básica',                 descripcion: 'Cifrado en reposo y tránsito, E2EE y certificados digitales (CA).' },
    { id: 10, costo: 320, icono: '10', titulo: 'Seguridad en la Nube',               descripcion: 'Modelos SaaS, PaaS, IaaS, riesgos asociados y gobernanza IAM/SLA.' },
    { id: 11, costo: 320, icono: '11', titulo: 'Respuesta ante Incidentes',           descripcion: 'Fases de respuesta, contención, recuperación y Regla de Backup 3-2-1.' },
    { id: 12, costo: 260, icono: '12', titulo: 'Legalidad y Ética',                  descripcion: 'Cumplimiento del GDPR, principios éticos y diferencias de seguridad.' }
  ];

  ngOnInit(): void {
    this.usuario = this.authService.getUsuarioActual();

    if (this.usuario) {
      if (!this.usuario.modulosDesbloqueados) {
        this.usuario.modulosDesbloqueados = [];
      }
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
    if (this.estaDesbloqueado(mod.id)) {
      alert(`Abriendo: ${mod.titulo}`);
      return;
    }

    if (this.estaDesbloqueando(mod.id)) return;

    if (!this.usuario || this.usuario.puntos < mod.costo) {
      alert('No tienes puntos suficientes para desbloquear este tema.');
      return;
    }

    const nuevosPuntos = this.usuario.puntos - mod.costo;

    this.desbloqueando.add(mod.id);
    this.modulosDesbloqueadosSet.add(mod.id);
    this.usuario = {
      ...this.usuario,
      puntos: nuevosPuntos,
      modulosDesbloqueados: [...this.usuario.modulosDesbloqueados, mod.id]
    };
    this.authService.actualizarUsuarioLocal(this.usuario);
    this.cdr.detectChanges();

    const modulosArray = Array.from(this.modulosDesbloqueadosSet);
    this.authService.actualizarProgreso(nuevosPuntos, modulosArray).subscribe({
      next: () => {
        this.zone.run(() => {
          this.desbloqueando.delete(mod.id);
          this.cdr.detectChanges();
          console.log(`Módulo ${mod.id} desbloqueado correctamente.`);
        });
      },
      error: (err) => {
        console.error(err);
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
          this.cdr.detectChanges();
          alert('Error de conexión. No se pudo desbloquear el módulo.');
        });
      }
    });
  }
}