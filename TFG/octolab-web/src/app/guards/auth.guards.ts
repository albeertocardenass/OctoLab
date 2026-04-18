import { inject, PLATFORM_ID } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (!isPlatformBrowser(platformId)) return true;

  const userStr = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
  if (userStr && userStr !== 'undefined' && userStr !== 'null') return true;

  router.navigate(['/login']);
  return false;
};

export const adminGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (!isPlatformBrowser(platformId)) return true;

  const userStr = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
  if (userStr && userStr !== 'undefined' && userStr !== 'null') {
    const user = JSON.parse(userStr);
    const rol = user.rol || user.Rol;
    if (rol === 'Admin') return true;
  }
  
  router.navigate(['/home/inicio']);
  return false;
};

export const usuarioGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (!isPlatformBrowser(platformId)) return true;

  const userStr = localStorage.getItem('usuario') || sessionStorage.getItem('usuario');
  if (userStr && userStr !== 'undefined' && userStr !== 'null') return true;

  router.navigate(['/login']);
  return false;
};