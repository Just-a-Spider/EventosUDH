import { Component } from '@angular/core';
import { EventsService } from '../../../services/events.service';
import { SimpleEvent } from '../../../classes/event.class';

@Component({
  selector: 'event-list',
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss',
})
export class EventListComponent {
  events: SimpleEvent[] = [];

  constructor(private eventsService: EventsService) {
    this.eventsService.getEvents().subscribe((events) => {
      this.events = events.results;
    });
  }

  seeEvent(eventId: string) {
    this.eventsService.getEvent(eventId).subscribe((event) => {
      this.eventsService.setCurrentEvent(event);
    });
  }
}
