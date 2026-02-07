import { Component } from '@angular/core';

@Component({
  selector: 'app-donation',
  standalone: true,
  template: `
    <div class="donation-container fade-in">
      <div class="heart">❤️</div>
      <h2>Apoya el Proyecto</h2>
      <p>OctolabWeb es gratuito gracias a personas como tú.</p>
      <div class="options">
        <button class="btn-tier">☕ Invitar a un café (5€)</button>
        <button class="btn-tier">🍕 Cena de Devs (15€)</button>
      </div>
    </div>
  `,
  styles: [`
    .donation-container { text-align: center; padding: 3rem; }
    .heart { font-size: 4rem; margin-bottom: 1rem; }
    .options { display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; }
    .btn-tier { border: 2px solid #4f46e5; background: white; color: #4f46e5; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
    .btn-tier:hover { background: #4f46e5; color: white; }
  `]
})
export class DonationComponent {}