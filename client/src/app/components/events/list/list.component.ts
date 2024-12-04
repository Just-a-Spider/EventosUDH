import { Component, OnInit } from '@angular/core';
import { FullEvent, SimpleEvent } from '../../../classes/event.class';
import { AuthService } from '../../../services/auth.service';
import { EventsService } from '../../../services/events.service';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'event-list',
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss',
})
export class EventListComponent implements OnInit {
  role: string;
  events: SimpleEvent[] = [];
  displayEvent = false;
  displayEdit = false;
  currentEvent: FullEvent = new FullEvent();
  pageOptions: number[] = [];
  pageDropdownOptions: { label: string; value: number }[] = [];
  limit = 10;
  offset = 0;
  totalItems = 0;
  currentPage = 1;
  title: string;

  constructor(
    private router: Router,
    private eventsService: EventsService,
    private authService: AuthService
  ) {
    const myEvents = this.router.url === '/my-events';
    if (myEvents) {
      this.title = 'Mis Eventos';
    } else {
      this.title = 'Próximos Eventos';
    }
    this.role = this.authService.getRole();
  }

  ngOnInit() {
    this.loadEvents();
  }

  loadEvents() {
    const myEvents = this.router.url === '/my-events';
    this.eventsService.getEvents(this.limit, this.offset, myEvents).subscribe({
      next: (response) => {
        this.events = response.results;
        this.totalItems = response.count;
        this.pageOptions = Array.from(
          { length: Math.ceil(this.totalItems / this.limit) },
          (_, i) => i + 1
        );
        this.pageDropdownOptions = this.pageOptions.map((page) => ({
          label: page.toString(),
          value: page,
        }));
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  prevPage() {
    if (this.offset > 0) {
      this.offset -= this.limit;
      this.currentPage--;
      this.loadEvents();
    }
  }

  nextPage() {
    if (this.offset + this.limit < this.totalItems) {
      this.offset += this.limit;
      this.currentPage++;
      this.loadEvents();
    }
  }

  onPageChange(event: any) {
    this.currentPage = event.value;
    this.offset = (this.currentPage - 1) * this.limit;
    this.loadEvents();
  }

  seeEditEvent(eventId: string, edit = false) {
    this.eventsService.getEvent(eventId).subscribe({
      next: (event) => {
        this.currentEvent = event;
        if (edit) {
          this.displayEdit = true;
          console.log('Edit event');
          console.log(this.currentEvent);
        } else {
          this.displayEvent = true;
        }
      },
      error: (error) => {
        console.error(error);
      },
    });
  }
}
