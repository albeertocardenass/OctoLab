import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly platformId = inject(PLATFORM_ID);
  private readonly darkMode$ = new BehaviorSubject<boolean>(false);

  readonly isDarkMode$ = this.darkMode$.asObservable();

  get isDarkMode(): boolean {
    return this.darkMode$.value;
  }

  init(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    const saved = localStorage.getItem('tema') === 'dark';
    this.darkMode$.next(saved);
    this.applyClass(saved);
  }

  toggle(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    const next = !this.darkMode$.value;
    this.darkMode$.next(next);
    this.applyClass(next);
    localStorage.setItem('tema', next ? 'dark' : 'light');
  }

  private applyClass(dark: boolean): void {
    document.body.classList.toggle('dark-theme', dark);
  }
}
