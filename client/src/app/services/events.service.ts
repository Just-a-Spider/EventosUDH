import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { FullEvent, SimpleEvent } from '../classes/event.class';
import { BehaviorSubject, Observable } from 'rxjs';

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
    const savedCourse = localStorage.getItem('currentCourse');
    this.currentEventSubject = new BehaviorSubject<FullEvent>(
      savedCourse ? JSON.parse(savedCourse) : new FullEvent()
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
}
