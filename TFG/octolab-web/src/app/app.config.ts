import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { routes } from './app.routes';
import { provideNgxStripe } from 'ngx-stripe';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withFetch()),
    provideNgxStripe('pk_test_51TNsyoR897G8mIVmKBZ8Nl3r5j79f1qZaPszuAvVozMGoSKoixmjEhuuQvkzhxC4SzZsQiwp6Z4P8arKxfrDTdxt00mGVj8e08')
  ]
};