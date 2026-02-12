import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { RegisterComponent } from './register/register';
import { HomeComponent } from './home/home';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: 'home',
    component: HomeComponent,
    children: [
      { path: 'inicio', loadComponent: () => import('./inicio/inicio').then(m => m.InicioComponent) },
      { path: 'temario', loadComponent: () => import('./temario/temario').then(m => m.TemarioComponent) },
      { path: 'comunidad', loadComponent: () => import('./comunidad/comunidad').then(m => m.ComunidadComponent) },
      { path: 'donaciones', loadComponent: () => import('./donation/donation').then(m => m.DonationComponent) },
      { path: 'configuracion', loadComponent: () => import('./configuracion/configuracion').then(m => m.ConfiguracionComponent) },
    ]
  }
];