import { Component, OnInit } from '@angular/core';
import { FullEvent, SimpleEvent } from '../../../classes/event.class';
import { AuthService } from '../../../services/auth.service';
import { EventsService } from '../../../services/events.service';
import { NavigationEnd, Router } from '@angular/router';
import { User } from '../../../classes/user.class';

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
  limit = 12;
  offset = 0;
  totalItems = 0;
  currentPage = 1;
  title: string;
  participants: User[] = [];

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

  seeEditEvent(eventId: string, edit = false) {
    this.eventsService.getEvent(eventId).subscribe({
      next: (event) => {
        this.currentEvent = event;
        if (edit) {
          this.displayEdit = true;
        } else {
          this.getParticipants();
          this.displayEvent = true;
        }
      },
      error: (error) => {
        console.error(error);
      },
    });
  }
}
