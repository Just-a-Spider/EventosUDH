import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, filter, Observable, Subject } from 'rxjs';
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
    this.authService.user$
      .pipe(filter((user) => user.username !== undefined))
      .subscribe({
        next: (user: User) => {
          const username = user.username;
          const wsUrl = `${this.socketUrl}${username}/`;

          // Check if there's an existing connection in session storage
          const existingConnection = sessionStorage.getItem('wsConnection');
          if (
            existingConnection &&
            this.socket &&
            this.socket.readyState === WebSocket.OPEN
          ) {
            return;
          }

          this.socket = new WebSocket(wsUrl);

          this.socket.onopen = (event) => {
            // Save the connection state in session storage
            sessionStorage.setItem('wsConnection', 'open');
          };

          this.socket.onmessage = (event) => {
            let message = JSON.parse(event.data);
            this.notificationSubject.next(message);
            this.getNotifications().subscribe(); // Re-fetch notifications
          };

          this.socket.onclose = (event) => {
            // Remove the connection state from session storage
            sessionStorage.removeItem('wsConnection');
            // Attempt to reconnect
            setTimeout(() => {
              this.connect();
            }, 1000); // Reconnect after 1 second
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
