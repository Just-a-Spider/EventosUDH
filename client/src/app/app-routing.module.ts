import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthView } from './views/auth/auth.component';
import { HomeView } from './views/home/home.component';
import { LandingView } from './views/landing/landing.component';
import { ProfileView } from './views/profile/profile.component';

const routes: Routes = [
  { path: 'landing', component: LandingView },
  { path: 'auth', component: AuthView },
  {
    path: '',
    component: HomeView,
    children: [],
  },
  { path: 'me', component: ProfileView },
  { path: '**', redirectTo: 'landing' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
