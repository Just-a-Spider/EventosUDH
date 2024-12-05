import { Component } from '@angular/core';
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
  currentEvent: FullEvent = new FullEvent();
  eventDate = new Date();
  participants: User[] = [];

  constructor(private router: Router, private eventsService: EventsService) {
    this.eventsService.currentEvent$.subscribe((event) => {
      this.currentEvent = event;
      this.eventDate = new Date(this.currentEvent.start_date!);
    });
    this.getParticipants();
  }

  getParticipants() {
    this.eventsService.getParticipants(this.currentEvent.id!).subscribe({
      next: (participants) => {
        this.participants = participants;
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  joinLeaveEvent() {
    if (this.currentEvent.is_participant!) {
      this.eventsService.leaveEvent(this.currentEvent.id!);
      this.currentEvent.is_participant = false;
    } else {
      this.eventsService.joinEvent(this.currentEvent.id!);
      this.currentEvent.is_participant = true;
    }
    this.getParticipants();
  }

  goBack() {
    this.router.navigate(['']);
  }
}
