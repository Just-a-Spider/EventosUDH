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
  getUserValue() {
    return this.userSubject.value;
  }

  getRole() {
    return this.userSubject.value.role as string;
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
        next: () => {
          this.userSubject.next(new User());
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

  sendResetPasswordEmail(email: string, role: string) {
    return this.http.post(`${this.apiUrl}send-password-reset-token/`, {
      email,
      role,
    });
  }

  resetPassword(token: string, password: string) {
    return this.http.post(`${this.apiUrl}password-reset/`, {
      token,
      password,
    });
  }

  saveProfile(file: File | null = null, user: User) {
    const formData = new FormData();
    formData.append('username', user.username!);
    formData.append('email', user.email!);
    formData.append('linkedin', user.linkedin!);
    if (file) {
      formData.append('profile_picture', file);
    }
    return this.http.post(`${this.apiUrl}profile/`, formData, {
      withCredentials: true,
    });
  }
}
