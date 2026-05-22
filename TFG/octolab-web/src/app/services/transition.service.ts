import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TransitionService {
  private readonly active$ = new BehaviorSubject<boolean>(false);
  readonly isActive$ = this.active$.asObservable();

  show(): void { this.active$.next(true); }
  hide(): void { this.active$.next(false); }
}
