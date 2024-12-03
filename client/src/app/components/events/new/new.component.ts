import { Component } from '@angular/core';
import { EventsService } from '../../../services/events.service';
import { CreateEvent, FullEvent } from '../../../classes/event.class';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'event-form',
  templateUrl: './new.component.html',
  styleUrl: './new.component.scss',
})
export class NewEventComponent {
  eventForm: FormGroup;
  new_event: CreateEvent = {
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    location: '',
    promotional_image: null,
    organizer: '',
    student_organizer: '',
    event_type: '',
    speakers: [],
  };

  constructor(private eventsService: EventsService, private fb: FormBuilder) {
    this.eventForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      start_date: ['', Validators.required],
      end_date: ['', Validators.required],
      location: ['', Validators.required],
      promotional_image: [null],
      organizer: ['', Validators.required],
      student_organizer: ['', Validators.required],
      event_type: ['', Validators.required],
      speakers: ['', Validators.required],
    });
  }

  createEvent() {
    this.eventsService
      .createEvent(this.new_event)
      .subscribe((event: FullEvent) => {
        console.log(event);
      });
  }

  onSubmit() {
    if (this.eventForm.valid) {
      this.new_event = this.eventForm.value;
      this.createEvent();
    }
  }
}
