import { Component } from '@angular/core';
import { ButtonInterface } from '../../../interfaces/ui.interface';
import { AuthService } from '../../../services/auth.service';
import { ThemeService } from '../../../services/misc/theme.service';
import { Router } from '@angular/router';

@Component({
  selector: 'ui-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  selButtonStyle: ButtonInterface;
  isDarkMode = true;
  displayNotis = false;
  displayCreateEvent = false;
  isOnAuth = true;
  role: string = localStorage.getItem('role') as string;

  constructor(
    private router: Router,
    private authService: AuthService,
    private themeService: ThemeService
  ) {
    this.isOnAuth = window.location.pathname === '/auth';
    if (!this.isOnAuth) {
      this.authService.user$.subscribe({
        next: (user) => {
          this.isOnAuth = false;
          localStorage.setItem('role', user.role!);
          this.role = user.role!;
        },
        error: () => {
          this.isOnAuth = true;
        },
      });
    }
    this.isDarkMode = localStorage.getItem('theme') === 'true';
    if (!this.isDarkMode) {
      this.themeService.changeTheme();
    }
    this.selButtonStyle = themeService.buttonStyle;
  }

  toggleLightDark() {
    this.isDarkMode = !this.isDarkMode;
    this.themeService.changeTheme();
  }

  logout() {
    this.authService.logout();
  }

  goToSpeakers() {
    this.router.navigate(['/speakers']);
  }

  goToEvents() {
    this.router.navigate(['/events']);
  }

  goToProfile() {
    this.router.navigate(['/profile']);
  }

  goToMyEvents() {
    this.router.navigate(['/my-events']);
  }
}
