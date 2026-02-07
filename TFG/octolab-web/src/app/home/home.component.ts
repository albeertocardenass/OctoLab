import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router'; // Importante para las rutas

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule], // Asegúrate de importar RouterModule
  templateUrl: './home.component.html', 
  styleUrls: ['./home.component.css'] 
})
export class HomeComponent {
  // Lista de pestañas para iterar en el HTML
  tabs: string[] = ['Inicio', 'Temario', 'Comunidad', 'Donaciones', 'Configuración'];
  
  // Pestaña activa por defecto
  activeTab: string = 'Inicio';

  selectTab(tabName: string) {
    this.activeTab = tabName;
  }
  constructor(public router: Router) {} // Inyectamos el router
}