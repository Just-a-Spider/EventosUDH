import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EventDetailComponent } from './components/events/detail/detail.component';
import { EventListComponent } from './components/events/list/list.component';
import { NewEventComponent } from './components/events/new/new.component';
import { authGuard } from './guards/auth.guard';
import { AuthView } from './views/auth/auth.component';
import { HomeView } from './views/home/home.component';
import { LandingView } from './views/landing/landing.component';
import { ProfileView } from './views/profile/profile.component';
import { ResetPasswordView } from './views/reset-password/reset-password.component';

const routes: Routes = [
  { path: 'landing', component: LandingView },
  { path: 'auth', component: AuthView },
  { path: 'reset-password', component: ResetPasswordView },
  {
    path: '',
    component: HomeView,
    canActivate: [authGuard],
    children: [
      { path: '', component: EventListComponent },
      { path: 'detail/:id', component: EventDetailComponent },
      { path: 'new', component: NewEventComponent },
    ],
  },
  { path: 'me', component: ProfileView, canActivate: [authGuard] },
  { path: '**', redirectTo: 'landing' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
