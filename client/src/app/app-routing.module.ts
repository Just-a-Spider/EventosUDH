import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthView } from './views/auth/auth.component';
import { HomeView } from './views/home/home.component';
import { LandingView } from './views/landing/landing.component';
import { ProfileView } from './views/profile/profile.component';
import { EventListComponent } from './components/events/list/list.component';
import { RestorePassView } from './views/restore-pass/restore-pass.component';

const routes: Routes = [
  { path: 'landing', component: LandingView },
  { path: 'auth', component: AuthView },
  {path: 'reset-password',component:RestorePassView},

  {
    path: '',
    component: HomeView,
    children: [{ path: '', component: EventListComponent }],
  },
  { path: 'me', component: ProfileView },
  { path: '**', redirectTo: 'landing' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
