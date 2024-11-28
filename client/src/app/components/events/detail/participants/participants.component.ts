import { Component, Input } from '@angular/core';
import { User } from '../../../../classes/user.class';

@Component({
  selector: 'event-participants',
  templateUrl: './participants.component.html',
  styleUrl: './participants.component.scss',
})
export class EventParticipantsComponent {
  @Input() participants: User[] = [];
}
