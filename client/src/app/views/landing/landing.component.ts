import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.scss'],
})
export class LandingView {
  fondo: string = '/udhlog.png';
  buttonText: string = 'Empezar';
  rotatingText: string[] = [
    '¿Quiénes somos?',
    'Propósito',
    'Integrantes',
    'hola',
  ];
  currentIndex: number = 0;
  currentDescription: string = '';

  constructor(private router: Router) {
    this.startRotatingText();
  }

  startRotatingText() {
    setInterval(() => {
      this.currentIndex = (this.currentIndex + 1) % this.rotatingText.length;
      this.updateDescription();
    }, 4000);
  }

  updateDescription() {
    switch (this.currentIndex) {
      case 0:
        this.currentDescription =
          'Somos una plataforma dedicada a brindar la facilidad para poder tomar y realizar tutorías personalizadas para todos.';
        break;
      case 1:
        this.currentDescription =
          'Nuestro propósito es facilitar el acceso al conocimiento de una manera accesible y eficaz; incentivando el ayudar a quien lo necesite.';
        break;
      case 2:
        this.currentDescription =
          'Contamos el grupo 2 conformado por: Andre, Lady y Marcel';
        break;
    }
  }

  onHoverStart() {
    this.buttonText = 'Good luck';
  }

  onHoverEnd() {
    this.buttonText = 'Empezar';
  }

  goBackToLogin() {
    this.router.navigate(['/auth']); // Redirige al componente de login
  }
}
