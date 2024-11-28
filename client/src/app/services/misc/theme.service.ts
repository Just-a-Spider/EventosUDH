import { DOCUMENT } from '@angular/common';
import { inject, Injectable } from '@angular/core';
import { ButtonInterface, BUTTONS } from '../../interfaces/ui.interface';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  #document = inject(DOCUMENT);
  buttonStyle: ButtonInterface;

  constructor() {
    const savedMode = localStorage.getItem('role');
    if (savedMode === 'coordinator' || savedMode === 'speaker') {
      const currentMode = savedMode;
      this.buttonStyle =
        BUTTONS.find((button) => button.mode === currentMode) || BUTTONS[0];
    } else {
      localStorage.setItem('role', 'student');
      this.buttonStyle = BUTTONS[0];
    }
  }

  changeTheme() {
    const linkElement = this.#document.getElementById(
      'app-theme'
    ) as HTMLLinkElement;
    if (linkElement.href.includes('light')) {
      linkElement.href = 'theme-dark.css';
      localStorage.setItem('theme', 'true');
    } else {
      linkElement.href = 'theme-light.css';
      localStorage.setItem('theme', 'false');
    }
  }
}
