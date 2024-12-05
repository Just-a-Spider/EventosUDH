import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { FullEvent, SimpleEvent } from '../classes/event.class';
import { BehaviorSubject, Observable } from 'rxjs';
import { User } from '../classes/user.class';

@Injectable({
  providedIn: 'root',
})
export class EventsService {
  private apiUrl = environment.apiUrl + 'events/';
  private currentEventSubject: BehaviorSubject<FullEvent>;
  currentEvent$: Observable<FullEvent>;

  setCurrentEvent(event: FullEvent) {
    this.currentEventSubject.next(event);
    localStorage.setItem('currentEvent', JSON.stringify(event));
  }

  constructor(private http: HttpClient) {
    const savedEvent = localStorage.getItem('currentEvent');
    this.currentEventSubject = new BehaviorSubject<FullEvent>(
      savedEvent ? JSON.parse(savedEvent) : new FullEvent()
    );
    this.currentEvent$ = this.currentEventSubject.asObservable();
  }

  getEvents(): Observable<any> {
    return this.http.get<any>(this.apiUrl, { withCredentials: true });
  }

  getEvent(id: string): Observable<FullEvent> {
    return this.http.get<FullEvent>(`${this.apiUrl}${id}/`, {
      withCredentials: true,
    });
  }

  // Actions related to the current event
  getParticipants(eventId: string): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}${eventId}/participants/`, {
      withCredentials: true,
    });
  }

  joinEvent(eventId: string) {
    this.http
      .get(`${this.apiUrl}${eventId}/join-event/`, {
        withCredentials: true,
      })
      .subscribe({
        next: (response) => {
          console.log(response);
        },
        error: (error) => {
          console.error(error);
        },
      });
  }

  leaveEvent(eventId: string) {
    this.http
      .get(`${this.apiUrl}${eventId}/leave-event/`, {
        withCredentials: true,
      })
      .subscribe({
        next: (response) => {
          console.log(response);
        },
        error: (error) => {
          console.error(error);
        },
      });
  }
}
