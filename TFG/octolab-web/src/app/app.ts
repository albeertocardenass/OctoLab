import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true, // Asegúrate de que tenga esto
  imports: [RouterOutlet], // Eliminamos LoginComponent de aquí
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('octolab-web');
}