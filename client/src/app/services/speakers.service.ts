import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../classes/user.class';

@Injectable({
  providedIn: 'root',
})
export class SpeakersService {
  private apiUrl = environment.apiUrl + 'speakers/';

  constructor(private http: HttpClient) {}

  getSpeakers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl, {
      withCredentials: true,
    });
  }

  deleteSpeaker(speakerId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${speakerId}/`, {
      withCredentials: true,
    });
  }

  editSpeaker(speakerId: number, speaker: User): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}${speakerId}/`, speaker, {
      withCredentials: true,
    });
  }
}
