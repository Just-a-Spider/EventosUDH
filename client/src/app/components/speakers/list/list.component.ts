import { Component } from '@angular/core';
import { SpeakersService } from '../../../services/speakers.service';
import { User } from '../../../classes/user.class';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'speakers-list',
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss',
  providers: [MessageService],
})
export class SpeakersListComponent {
  speakers: User[] = [];
  displayNewDialog = false;

  constructor(
    private speakersService: SpeakersService,
    private messageService: MessageService
  ) {
    this.speakersService.getSpeakers().subscribe({
      next: (speakers) => {
        this.speakers = speakers;
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  deleteSpeaker(speakerId: number) {
    this.speakersService.deleteSpeaker(speakerId).subscribe({
      next: () => {
        this.speakers = this.speakers.filter(
          (speaker) => speaker.id !== speakerId
        );
        this.messageService.add({
          severity: 'success',
          summary: 'Ponente eliminado',
          detail: 'Ponente eliminado correctamente',
        });
      },
      error: (error) => {
        console.error(error);
      },
    });
  }
}
