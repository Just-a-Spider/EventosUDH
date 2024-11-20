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

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.getUser();
  }

  getUser() {
    this.authService.user$
      .pipe(
        filter((user) => user.username !== undefined)
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
