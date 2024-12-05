import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { catchError, map, take } from 'rxjs/operators';
import { User } from '../classes/user.class';
import { AuthService } from '../services/auth.service';
import { of } from 'rxjs';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.getUser().pipe(
    take(1),
    map((user: User) => {
      if (user.username !== '' || user.username !== undefined) {
        authService.setUser(user);
        return true;
      } else {
        router.navigate(['/auth']);
        return false;
      }
    }),
    catchError(() => {
      router.navigate(['/auth']);
      return of(false);
    })
  );
};
