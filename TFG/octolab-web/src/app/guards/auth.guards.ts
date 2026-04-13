import { inject, PLATFORM_ID } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (isPlatformBrowser(platformId)) {
    const datos = localStorage.getItem('usuario_activo');
    if (datos) return true;
    router.navigate(['/login']);
    return false;
  }
  return true;
};

export const adminGuard: CanActivateFn = () => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (isPlatformBrowser(platformId)) {
    const datos = localStorage.getItem('usuario_activo');
    if (datos) {
      const user = JSON.parse(datos);
      const rol = user.rol || user.Rol;
      if (rol === 'Admin') return true;
    }
    router.navigate(['/home']);
    return false;
  }
  return true;
};

export const usuarioGuard: CanActivateFn = () => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (isPlatformBrowser(platformId)) {
    const datos = localStorage.getItem('usuario_activo');
    if (datos) {
      const user = JSON.parse(datos);
      const rol = user.rol || user.Rol;
      if (rol === 'Admin' || rol === 'Usuario') return true;
    }
    router.navigate(['/home/inicio']);
    return false;
  }
  return true;
};