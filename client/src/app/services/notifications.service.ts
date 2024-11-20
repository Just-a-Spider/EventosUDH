import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  FullNotification,
  PopUpNotification,
} from '../classes/notifications.class';
import { User } from '../classes/user.class';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root',
})
export class NotificationsService {
  private socket: WebSocket | undefined;
  private notificationSubject: Subject<PopUpNotification> =
    new Subject<PopUpNotification>();
  private socketUrl = `${environment.socketUrl}notifications/`;

  private licenseIdSubject = new BehaviorSubject<string>('');
  licenseId$ = this.licenseIdSubject.asObservable();

  constructor(private authService: AuthService, private http: HttpClient) {
    this.connect();
  }

  private async connect() {
    this.authService.getUser().subscribe({
      next: (user: User) => {
        const username = user.username;
        const wsUrl = `${this.socketUrl}${username}/`;

        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = (event) => {};

        this.socket.onmessage = (event) => {
          let message = JSON.parse(event.data);
          this.notificationSubject.next(message);
          this.getNotifications().subscribe(); // Re-fetch notifications
        };

        this.socket.onerror = (event) => {
          console.error('WebSocket error:', event);
        };
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  close() {
    if (this.socket) {
      this.socket.close();
    }
  }

  getNotifications(seen: boolean = false): Observable<FullNotification[]> {
    if (seen) {
      return this.http.get<FullNotification[]>(
        `${environment.apiUrl}notifications/seen/`,
        {
          withCredentials: true,
        }
      );
    }
    return this.http.get<FullNotification[]>(
      `${environment.apiUrl}notifications/unseen/`,
      {
        withCredentials: true,
      }
    );
  }

  getNotificationUpdates(): Observable<PopUpNotification> {
    return this.notificationSubject.asObservable();
  }

  markSeen(notificationId: string): Observable<any> {
    return this.http.get(
      `${environment.apiUrl}notifications/${notificationId}/`,
      {
        withCredentials: true,
      }
    );
  }

  goToLicense(licenseId: string) {
    this.licenseIdSubject.next(licenseId);
  }

  clearSeen() {
    return this.http.delete(`${environment.apiUrl}notifications/clear/`, {
      withCredentials: true,
    });
  }
}
