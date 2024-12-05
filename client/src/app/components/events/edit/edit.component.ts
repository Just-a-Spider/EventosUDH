import { Component, Input, OnChanges } from '@angular/core';
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
export class EditEventForm implements OnChanges {
  @Input() event: FullEvent = new FullEvent();

  speakers: AddEventSpeaker[] = [];
  uploadedImage: File | null = null;
  imagePreview: string | ArrayBuffer | null = null;
  virtualEvent = false;
  studentOrganizer = false;
  eventCategories: Item[] = [];

  placeholderDates = {
    start: '',
    end: '',
  };

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

  ngOnChanges() {
    if (this.event && this.event.speakers!) {
      this.speakers = this.event.speakers!.map((speaker) => ({
        first_name: speaker.speaker.first_name || '',
        last_name: speaker.speaker.last_name || '',
        email: speaker.speaker.email || '',
        subject: speaker.subject || '',
      }));
      this.studentOrganizer = this.event.student_organizer !== null;
      this.virtualEvent =
        this.event.location === '' || this.event.location === null;
      this.placeholderDates.start = this.event.start_date
        ? new Date(this.event.start_date).toISOString()
        : '';
      this.placeholderDates.end = this.event.end_date
        ? new Date(this.event.end_date).toISOString()
        : '';
    }
  }

  uploadImage(event: any, item: FileUpload) {
    this.uploadedImage = event.files[0];
    item.clear();
    const reader = new FileReader();
    if (this.uploadedImage) {
      reader.readAsDataURL(this.uploadedImage);
    }
    reader.onload = () => {
      this.event.promotional_image = reader.result as string;
    };
  }

  updateEvent() {
    const event = this.event;
    const formData = new FormData();
    formData.append('title', event.title!);
    formData.append('description', event.description!);
    formData.append('start_date', new Date(event.start_date!).toISOString());
    formData.append('end_date', new Date(event.end_date!).toISOString());
    // Print the dates to the console
    console.log(new Date(event.start_date!).toISOString());
    console.log(new Date(event.end_date!).toISOString());
    if (this.virtualEvent) {
      formData.append('location', '');
    }

    if (this.studentOrganizer) {
      formData.append('organizer', '');
    }

    // Get the event_type id from the name
    const eventType = this.eventCategories.find(
      (category) => category.name === event.event_type
    );
    if (eventType) {
      formData.append('event_type', eventType.id);
    }

    if (this.uploadedImage) {
      formData.append('promotional_image', this.uploadedImage);
    }

    // Add speakers
    formData.append('speakers', JSON.stringify(this.speakers));

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
    // Remove the speaker from the event speakers
    this.event.speakers!.splice(index, 1);
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
