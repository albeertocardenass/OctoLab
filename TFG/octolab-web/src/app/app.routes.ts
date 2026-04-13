import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { RegisterComponent } from './components/register/register';
import { HomeComponent } from './components/home/home';
import { AdminPanelComponent } from './components/admin/admin';
import { adminGuard, authGuard, usuarioGuard } from './guards/auth.guards';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { 
    path: 'admin', 
    component: AdminPanelComponent,
    canActivate: [adminGuard] 
  },
  {
    path: 'home',
    component: HomeComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
      
      // 2. Ruta de inicio (donde estará el contenido principal de la home)
      { 
        path: 'inicio', 
        loadComponent: () => import('./components/inicio/inicio').then(m => m.InicioComponent) 
      },
      
      { path: 'temario', loadComponent: () => import('./components/temario/temario').then(m => m.TemarioComponent) },
      { path: 'comunidad', loadComponent: () => import('./components/comunidad/comunidad').then(m => m.ComunidadComponent) },
      { path: 'donaciones', loadComponent: () => import('./components/donation/donation').then(m => m.DonationComponent) },
      { 
        path: 'configuracion', 
        loadComponent: () => import('./components/configuracion/configuracion').then(m => m.ConfiguracionComponent),
        canActivate: [usuarioGuard]
      },
    ]
  }
];