import { Component, Input } from '@angular/core';
import { EventsService } from '../../../services/events.service';
import { FullEvent } from '../../../classes/event.class';
import { User } from '../../../classes/user.class';
import { Router } from '@angular/router';

@Component({
  selector: 'event-detail',
  templateUrl: './detail.component.html',
  styleUrl: './detail.component.scss',
})
export class EventDetailComponent {
  @Input() event: FullEvent = new FullEvent();
  eventDate = new Date();
  participants: User[] = [];

  constructor(private router: Router, private eventsService: EventsService) {}

  getParticipants() {
    this.eventsService.getParticipants(this.event.id!).subscribe({
      next: (participants) => {
        this.participants = participants;
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  joinLeaveEvent() {
    this.eventsService
      .toggleEventParticipation(this.event.id!, !this.event.is_participant!)
      .subscribe({
        next: () => {
          this.getParticipants();
          this.event.is_participant = !this.event.is_participant;
        },
        error: (error) => {
          console.error(error);
        },
      });
  }
}
