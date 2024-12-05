import { Component, Input } from '@angular/core';
import { User } from '../../../classes/user.class';

@Component({
  selector: 'speaker-detail',
  templateUrl: './detail.component.html',
  styleUrl: './detail.component.scss',
})
export class SpeakerDetailComponent {
  @Input() speaker: User = new User();

  constructor() {}

  getFullName(): string {
    return `${this.speaker.first_name} ${this.speaker.last_name}`;
  }
}
