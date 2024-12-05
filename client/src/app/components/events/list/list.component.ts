import { Component } from '@angular/core';
import { EventsService } from '../../../services/events.service';
import { SimpleEvent } from '../../../classes/event.class';
import { AuthService } from '../../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'event-list',
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss',
})
export class EventListComponent {
  role: string;
  events: SimpleEvent[] = [];

  constructor(
    private router: Router,
    private eventsService: EventsService,
    private authService: AuthService
  ) {
    this.role = this.authService.getRole();
    this.eventsService.getEvents().subscribe((events) => {
      this.events = events.results;
    });
  }

  seeEvent(eventId: string) {
    this.eventsService.getEvent(eventId).subscribe((event) => {
      this.eventsService.setCurrentEvent(event);
      this.router.navigate(['/detail']);
    });
  }
}
