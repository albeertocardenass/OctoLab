import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedIn = false;

  login(user: string, pass: string): boolean {
    if (user === 'admin' && pass === '1234') {
      this.loggedIn = true;
      return true;
    }
    return false;
  }

  isLoggedIn() { return this.loggedIn; }
}