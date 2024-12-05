import { Component, Input } from '@angular/core';
import { FileUpload } from 'primeng/fileupload';
import { AddEventSpeaker, FullEvent } from '../../../classes/event.class';
import { User } from '../../../classes/user.class';
import { EventsService } from '../../../services/events.service';

interface Item {
  id: string;
  name: string;
}

@Component({
  selector: 'event-edit-form',
  templateUrl: './edit.component.html',
  styleUrl: './edit.component.scss',
})
export class EditEventForm {
  @Input() event: FullEvent = new FullEvent();

  speakers: AddEventSpeaker[] = [];
  uploadedImage: File | null = null;
  imagePreview: string | ArrayBuffer | null = null;
  virtualEvent = false;
  studentOrganizer = false;
  eventCategories: Item[] = [];

  registeredSpeakers: User[] = [];

  constructor(private eventsService: EventsService) {
    this.eventsService.getEventTypes().subscribe({
      next: (eventTypes) => {
        this.eventCategories = eventTypes.map((category) => {
          return {
            id: category.id,
            name: category.name,
          };
        });
      },
      error: (error) => {
        console.error(error);
      },
    });

    this.eventsService.getSpeakers().subscribe({
      next: (speakers) => {
        this.registeredSpeakers = speakers;
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  uploadImage(event: any, item: FileUpload) {
    this.uploadedImage = event.files[0];
    item.clear();
    const reader = new FileReader();
    if (this.uploadedImage) {
      reader.readAsDataURL(this.uploadedImage);
    }
    reader.onload = () => {
      this.imagePreview = reader.result;
    };
  }

  updateEvent() {
    const event = this.event;
    const formData = new FormData();
    formData.append('title', event.title!);
    formData.append('description', event.description!);
    formData.append('start_date', event.start_date!.toISOString());
    formData.append('end_date', event.end_date!.toISOString());
    formData.append('location', event.location!);
    formData.append('virtual', this.virtualEvent ? 'true' : 'false');
    formData.append(
      'student_organizer',
      this.studentOrganizer ? 'true' : 'false'
    );
    formData.append('event_type', event.event_type!);

    if (this.uploadedImage) {
      formData.append('image', this.uploadedImage);
    }

    this.speakers.forEach((speaker) => {
      formData.append('speakers', JSON.stringify(speaker));
    });

    this.eventsService.editEvent(event.id!, formData).subscribe({
      next: (updatedEvent) => {
        console.log(updatedEvent);
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  // Speakers
  removeSpeaker(index: number) {
    this.speakers.splice(index, 1);
  }

  addSpeaker() {
    this.speakers.push({
      first_name: '',
      last_name: '',
      email: '',
      subject: '',
    });
  }

  addRegisteredSpeaker(speaker: User) {
    this.speakers.push({
      first_name: speaker.first_name!,
      last_name: speaker.last_name!,
      email: speaker.email!,
      subject: '',
    });
  }
}
