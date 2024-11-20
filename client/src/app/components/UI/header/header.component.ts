import { Component } from '@angular/core';
import { ButtonInterface, BUTTONS } from '../../../interfaces/ui.interface';
import { ThemeService } from '../../../services/misc/theme.service';
import { AuthService } from '../../../services/auth.service';
import { User } from '../../../classes/user.class';

@Component({
  selector: 'ui-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  mode: string;
  selButtonStyle: ButtonInterface;
  isDarkMode = true;

  constructor(
    private authService: AuthService,
    private themeService: ThemeService
  ) {
    this.authService.getUser().subscribe({
      next: (user) => {
        this.authService.setUser(user);
      },
      error: () => {
        window.location.href = '/auth';
      },
    });
    this.isDarkMode = localStorage.getItem('theme') === 'true';
    if (!this.isDarkMode) {
      this.themeService.changeTheme();
    }
    this.mode = localStorage.getItem('profileMode') || 'student';
    this.selButtonStyle = themeService.buttonStyle;
  }

  toggleLightDark() {
    this.isDarkMode = !this.isDarkMode;
    this.themeService.changeTheme();
  }

  logout() {
    this.authService.logout();
  }
}
