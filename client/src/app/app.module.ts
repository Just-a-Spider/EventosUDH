import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Pipes
import { CapitalizePipe } from './pipes/capitalize.pipe';

// PrimeNG stuff
import { PrimeNGModule } from './prime-ng.module';

// Local Components
import { HeaderComponent } from './components/UI/header/header.component';
import { NotificationsComponent } from './components/UI/header/notifications/notifications.component';
import { SideBarComponent } from './components/UI/side-bar/side-bar.component';
import { AuthView } from './views/auth/auth.component';
import { HomeView } from './views/home/home.component';
import { LandingView } from './views/landing/landing.component';
import { ProfileView } from './views/profile/profile.component';
import { EventListComponent } from './components/events/list/list.component';
import { EventDetailComponent } from './components/events/detail/detail.component';
import { RestorePassView } from './views/restore-pass/restore-pass.component';


@NgModule({
  declarations: [
    AppComponent,

    // Pipes
    CapitalizePipe,

    // Views
    AuthView,
    HomeView,
    ProfileView,
    LandingView,
    RestorePassView,

    // Components
    SideBarComponent,
    HeaderComponent,
    NotificationsComponent,
    EventListComponent,
    EventDetailComponent,
    RestorePassView,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    PrimeNGModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  providers: [provideHttpClient(withFetch()), provideAnimationsAsync()],
  bootstrap: [AppComponent],
})
export class AppModule {}
