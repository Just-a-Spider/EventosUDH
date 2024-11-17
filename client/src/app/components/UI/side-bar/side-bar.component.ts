import { Component, OnInit } from '@angular/core';
import { filter, take } from 'rxjs/operators';
import { User } from '../../../classes/user.class';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'ui-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss'],
})
export class SideBarComponent implements OnInit {
  user: User = new User();

  selectedCourseId: string = '';

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.getUser();
  }

  getUser() {
    this.authService.getUser();
    this.authService.user$
      .pipe(
        filter((user) => user !== null), // Filter out null values
        take(1) // Ensure the subscription happens only once
      )
      .subscribe({
        next: (user) => {
          this.user = user;
        },
        error: (error) => {
          console.error(error);
        },
      });
  }

  logout() {
    this.authService.logout();
  }
}
