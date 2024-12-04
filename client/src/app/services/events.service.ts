import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { FullEvent } from '../classes/event.class';
import { User } from '../classes/user.class';

@Injectable({
  providedIn: 'root',
})
export class EventsService {
  private apiUrl = environment.apiUrl + 'events/';

  constructor(private http: HttpClient) {}

  // General Actions
  getEvents(limit: number, offset: number, myEvents: boolean): Observable<any> {
    let endpoint = myEvents ? 'my-events/' : '';
    let params = new HttpParams()
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    return this.http.get<any>(`${this.apiUrl}${endpoint}`, {
      params,
      withCredentials: true,
    });
  }

  getEvent(id: string): Observable<FullEvent> {
    return this.http.get<FullEvent>(`${this.apiUrl}${id}/`, {
      withCredentials: true,
    });
  }

  createEvent(event: any): Observable<FullEvent> {
    return this.http.post<FullEvent>(this.apiUrl, event, {
      withCredentials: true,
    });
  }

  editEvent(eventId: string, event: any): Observable<FullEvent> {
    return this.http.put<FullEvent>(`${this.apiUrl}${eventId}/`, event, {
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

  // Special Actions
  getSpeakers(): Observable<User[]> {
    return this.http.get<User[]>(`${environment.apiUrl}speakers/`, {
      withCredentials: true,
    });
  }

  getEventTypes(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}event-types/`, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
}
