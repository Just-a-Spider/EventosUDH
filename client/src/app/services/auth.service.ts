import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { User } from '../classes/user.class';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private googleApiUrl = environment.apiUrl + 'oauth/login/google-oauth2/';
  private apiUrl = environment.apiUrl + 'auth/';
  private userSubject: BehaviorSubject<User>;
  user$: Observable<User>;

  setUser(user: User) {
    this.userSubject.next(user);
  }

  constructor(private http: HttpClient) {
    this.userSubject = new BehaviorSubject<User>(new User());
    this.user$ = this.userSubject.asObservable();
  }

  register(data: any) {
    return this.http.post(`${this.apiUrl}register/`, data, {
      withCredentials: true,
    });
  }

  login(data: any) {
    return this.http.post(`${this.apiUrl}login/`, data, {
      withCredentials: true,
    });
  }

  googleLogin() {
    window.location.href = this.googleApiUrl;
  }

  logout() {
    this.http
      .get(`${this.apiUrl}logout/`, {
        withCredentials: true,
      })
      .subscribe({
        next: (response) => {
          window.location.href = '/auth';
        },
        error: (error) => {
          console.error(error);
        },
      });
  }

  getUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}me/`, {
      withCredentials: true,
    });
  }
}
