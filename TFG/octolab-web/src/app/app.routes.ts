import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: 'home',
    component: HomeComponent,
    children: [
      { path: 'inicio', loadComponent: () => import('./inicio/inicio.component').then(m => m.InicioComponent) },
      { path: 'temario', loadComponent: () => import('./temario/temario.component').then(m => m.TemarioComponent) },
      { path: 'comunidad', loadComponent: () => import('./comunidad/comunidad.component').then(m => m.ComunidadComponent) },
      { path: 'donaciones', loadComponent: () => import('./donation/donation.component').then(m => m.DonationComponent) },
      { path: 'configuracion', loadComponent: () => import('./configuracion/configuracion.component').then(m => m.ConfiguracionComponent) },
    ]
  }
];