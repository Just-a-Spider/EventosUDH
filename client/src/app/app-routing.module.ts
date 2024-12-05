import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EventListComponent } from './components/events/list/list.component';
import { authGuard } from './guards/auth.guard';
import { AuthView } from './views/auth/auth.component';
import { HomeView } from './views/home/home.component';
import { LandingView } from './views/landing/landing.component';
import { ProfileView } from './views/profile/profile.component';
import { ResetPasswordView } from './views/reset-password/reset-password.component';
import { SpeakersListComponent } from './components/speakers/list/list.component';

const routes: Routes = [
  { path: 'landing', component: LandingView },
  { path: 'auth', component: AuthView },
  { path: 'reset-password', component: ResetPasswordView },
  {
    path: '',
    component: HomeView,
    canActivate: [authGuard],
    children: [
      { path: 'events', component: EventListComponent },
      { path: 'my-events', component: EventListComponent },
      { path: 'speakers', component: SpeakersListComponent },
    ],
  },
  { path: 'profile', component: ProfileView, canActivate: [authGuard] },
  { path: '**', redirectTo: 'events' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
