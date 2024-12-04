import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FileUpload } from 'primeng/fileupload';
import { AddEventSpeaker, FullEvent } from '../../../classes/event.class';
import { User } from '../../../classes/user.class';
import { EventsService } from '../../../services/events.service';

interface Item {
  id: string;
  name: string;
}

@Component({
  selector: 'event-create-form',
  templateUrl: './new.component.html',
  styleUrl: './new.component.scss',
})
export class NewEventForm {
  speakers: AddEventSpeaker[] = [];
  eventForm: FormGroup;
  uploadedImage: File | null = null;
  imagePreview: string | ArrayBuffer | null = null;
  virtualEvent = false;
  studentOrganizer = false;
  eventCategories: Item[] = [];

  registeredSpeakers: User[] = [];

  constructor(private eventsService: EventsService, private fb: FormBuilder) {
    this.eventsService.getSpeakers().subscribe({
      next: (speakers: User[]) => {
        this.registeredSpeakers = speakers;
        console.log(this.registeredSpeakers);
      },
    });
    this.eventsService.getEventTypes().subscribe({
      next: (eventTypes: Item[]) => {
        this.eventCategories = eventTypes;
        console.log(this.eventCategories);
      },
    });
    this.eventForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      start_date: [new Date(), Validators.required],
      end_date: [new Date(), Validators.required],
      location: [''],
      student_organizer: [''],
      event_type: ['', Validators.required],
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

  createEvent() {
    console.log(this.speakers);
    if (this.eventForm.valid) {
      const formValue = this.eventForm.value;
      const speakers = this.speakers.map((speaker) => {
        return {
          first_name: speaker.first_name,
          last_name: speaker.last_name,
          email: speaker.email,
          subject: speaker.subject,
        };
      });
      const dates = {
        start_date: formValue.start_date,
        end_date: formValue.end_date,
      };

      const newEventFormData: FormData = new FormData();

      newEventFormData.append('title', formValue.title);
      newEventFormData.append('description', formValue.description);
      newEventFormData.append('location', formValue.location);
      newEventFormData.append('event_type', formValue.event_type);
      // Add dates as ISO strings
      newEventFormData.append('start_date', dates.start_date.toISOString());
      newEventFormData.append('end_date', dates.end_date.toISOString());
      // Add speakers
      newEventFormData.append('speakers', JSON.stringify(speakers));
      // Add image
      if (this.uploadedImage) {
        newEventFormData.append('promotional_image', this.uploadedImage);
      }
      // Add student organizer
      newEventFormData.append('student_organizer', formValue.student_organizer);

      this.eventsService
        .createEvent(newEventFormData)
        .subscribe((event: FullEvent) => {
          console.log(event);
        });
    }
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
