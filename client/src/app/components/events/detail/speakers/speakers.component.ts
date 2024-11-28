import { Component, Input } from '@angular/core';

@Component({
  selector: 'event-speakers',
  templateUrl: './speakers.component.html',
  styleUrl: './speakers.component.scss',
})
export class EventSpeakersComponent {
  @Input() speakers: any[] = [];

  constructor() {}
}
