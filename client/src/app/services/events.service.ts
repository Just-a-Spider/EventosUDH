import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { CreateEvent, FullEvent, SimpleEvent } from '../classes/event.class';
import { BehaviorSubject, Observable } from 'rxjs';
import { User } from '../classes/user.class';

@Injectable({
  providedIn: 'root',
})
export class EventsService {
  private apiUrl = environment.apiUrl + 'events/';

  constructor(private http: HttpClient) {}

  getEvents(): Observable<any> {
    return this.http.get<any>(this.apiUrl, { withCredentials: true });
  }

  getEvent(id: string): Observable<FullEvent> {
    return this.http.get<FullEvent>(`${this.apiUrl}${id}/`, {
      withCredentials: true,
    });
  }

  createEvent(event: CreateEvent): Observable<FullEvent> {
    return this.http.post<FullEvent>(this.apiUrl, event, {
      withCredentials: true,
    });
  }

  // Actions related to the current event
  getParticipants(eventId: string): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}${eventId}/participants/`, {
      withCredentials: true,
    });
  }

  toggleEventParticipation(eventId: string, join: boolean) {
    const action = join ? 'join-event' : 'leave-event';
    return this.http.get(`${this.apiUrl}${eventId}/${action}/`, {
      withCredentials: true,
    });
  }
}
