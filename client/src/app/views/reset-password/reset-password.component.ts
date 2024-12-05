import { Component, OnInit } from '@angular/core';
import { Message } from 'primeng/api';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrl: './reset-password.component.scss',
})
export class ResetPasswordView implements OnInit {
  email!: string;
  role: string = 'student';
  token: string | null = null;
  password!: string;
  confirmPassword!: string;
  messages: Message[] = [];
  categories: any[] = [
    { name: 'Estudiante', key: 'student' },
    { name: 'Coordinador', key: 'coordinator' },
    { name: 'Ponente', key: 'speaker' },
  ];

  constructor(private router: Router, private authService: AuthService) {}

  ngOnInit() {
    this.getToken();
  }

  getToken() {
    // Fetch the token from the URL
    const url = new URL(window.location.href);
    const token = url.searchParams.get('token');
    if (token !== null) {
      this.token = token;
    }
  }

  sendResetPasswordEmail() {
    this.authService.sendResetPasswordEmail(this.email, this.role).subscribe(() => {
      this.messages = [
        {
          severity: 'success',
          summary: 'Correo enviado',
          detail: 'Revisa tu bandeja de entrada',
        },
      ];
    });
  }

  resetPassword() {
    if (this.password !== this.confirmPassword) {
      this.messages = [
        {
          severity: 'error',
          summary: 'Error',
          detail: 'Las contraseñas no coinciden',
        },
      ];
      return;
    }

    this.authService.resetPassword(this.token!, this.password).subscribe(() => {
      this.messages = [
        {
          severity: 'success',
          summary: 'Contraseña cambiada',
          detail: 'Inicia sesión con tu nueva contraseña',
        },
      ];
      // wait 3 seconds before redirecting
      setTimeout(() => {
        this.router.navigate(['/auth']);
      }, 3000);
    });
  }

  goBackToLogin() {
    this.router.navigate(['/auth']);
  }
}
