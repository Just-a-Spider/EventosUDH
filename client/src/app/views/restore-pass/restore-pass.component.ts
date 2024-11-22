import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Message } from 'primeng/api';
import { Router } from '@angular/router';

@Component({
  selector: 'app-restore-pass',
  templateUrl: './restore-pass.component.html',
  styleUrls: ['./restore-pass.component.scss'], // Cambiado de `styleUrl` a `styleUrls`
})
export class RestorePassView {

  constructor(private router: Router, private authService: AuthService) {
    // Inicializa el formulario con validaciones
  }



  // Método para redirigir al login
  goBackToLogin() {
    this.router.navigate(['/auth']); // Redirige al componente de login
  }
}
