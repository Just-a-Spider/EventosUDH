import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import {
  provideHttpClient,
  withFetch,
  withInterceptors,
} from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Pipes
import { CapitalizePipe } from './pipes/capitalize.pipe';

// PrimeNG stuff
import { PrimeNGModule } from './prime-ng.module';

// Local Components
import { EventDetailComponent } from './components/events/detail/detail.component';
import { LiveClockComponent } from './components/events/detail/live-clock/live-clock.component';
import { EventParticipantsComponent } from './components/events/detail/participants/participants.component';
import { EventSpeakersComponent } from './components/events/detail/speakers/speakers.component';
import { EventListComponent } from './components/events/list/list.component';
import { NewEventForm } from './components/events/new/new.component';
import { HeaderComponent } from './components/UI/header/header.component';
import { NotificationsComponent } from './components/UI/header/notifications/notifications.component';
import { SideBarComponent } from './components/UI/side-bar/side-bar.component';
import { apiKeyInterceptor } from './interceptors/api-key.interceptor';
import { TranslateRolePipe } from './pipes/translate-role.pipe';
import { AuthView } from './views/auth/auth.component';
import { HomeView } from './views/home/home.component';
import { LandingView } from './views/landing/landing.component';
import { ProfileView } from './views/profile/profile.component';
import { ResetPasswordView } from './views/reset-password/reset-password.component';
import { EditEventForm } from './components/events/edit/edit.component';
import { SpeakersListComponent } from './components/speakers/list/list.component';
import { SpeakerDetailComponent } from './components/speakers/detail/detail.component';
import { NewComponent } from './components/speakers/new/new.component';

@NgModule({
  declarations: [
    AppComponent,
    // Pipes
    CapitalizePipe,
    TranslateRolePipe,

    // Views
    AuthView,
    HomeView,
    ProfileView,
    LandingView,

    // Components
    SideBarComponent,
    HeaderComponent,
    NotificationsComponent,
    EventListComponent,
    EventDetailComponent,
    NewEventForm,
    LiveClockComponent,
    EventParticipantsComponent,
    EventSpeakersComponent,
    ResetPasswordView,
    EditEventForm,
    SpeakersListComponent,
    SpeakerDetailComponent,
    NewComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    PrimeNGModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  providers: [
    provideHttpClient(withFetch(), withInterceptors([apiKeyInterceptor])),
    provideAnimationsAsync(),
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
