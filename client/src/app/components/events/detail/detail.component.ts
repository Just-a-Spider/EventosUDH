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
  event: FullEvent = new FullEvent();
  eventDate = new Date();
  participants: User[] = [];

  constructor(private router: Router, private eventsService: EventsService) {
    this.getEventDetails();
  }

  getEventDetails() {
    // example url http://localhost:4200/detail/1b6d42bb-f038-4913-92a0-26b6662047fb
    // we need to extract the id from the url
    const url = window.location.href;
    const id = url.split('/').pop();

    this.eventsService.getEvent(id!).subscribe({
      next: (event) => {
        this.event = event;
        this.eventDate = new Date(event.start_date!);
        this.getParticipants();
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

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
      .toggleEventParticipation(
        this.event.id!,
        !this.event.is_participant!
      )
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

  goBack() {
    this.router.navigate(['']);
  }
}
