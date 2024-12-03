import { User } from './user.class';

export class EventSpeaker {
  speaker?: User;
  subject?: string;
}

export class SimpleEvent {
  id?: string;
  title?: string;
  location?: string;
  event_type?: string;
  promotional_image?: string;
  organizer?: string;
  student_organizer?: string;
}

export class FullEvent {
  id?: string;
  title?: string;
  location?: string;
  is_participant?: boolean;
  event_type?: string;
  promotional_image?: string;
  organizer?: string;
  student_organizer?: string;
  speakers?: EventSpeaker[];
  description?: string;
  start_date?: string;
  end_date?: string;
  created_at?: string;
}

export interface CreateEvent {
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  location: string;
  promotional_image: File | null;
  organizer: string;
  student_organizer: string;
  event_type: string;
  speakers: EventSpeaker[];
}
