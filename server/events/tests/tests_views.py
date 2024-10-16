from django.urls import reverse
from rest_framework import status
from events.models import Event, EventType
from faculties.models import Faculty
from server.utils.test_base_test import BaseTest

class EventTypeViewSetTestCase(BaseTest):
    def setUp(self):
        self.register_student()
        self.login_user()
        self.event_type = EventType.objects.create(name='Conference')

    def test_get_event_types(self):
        response = self.client.get(reverse('event-types-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.event_type.name)

    def test_create_event_type(self):
        reponse = self.client.post(reverse('event-types-list'), {'name': 'Workshop'})
        self.assertEqual(reponse.status_code, status.HTTP_201_CREATED)

class EventListCreateTestCase(BaseTest):
    def setUp(self):
        self.coordinator = self.get_coordinator()
        self.login_user()
        self.event_type = EventType.objects.create(name='Conference')
        self.faculty = Faculty.objects.create(name='Faculty 1', coordinator=self.coordinator)

    def test_get_events(self):
        response = self.client.get(reverse('events-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_event(self):
        data = {
            'title': 'Event 1',
            'description': 'Description of event 1',
            'start_date': '2022-01-01T00:00:00Z',
            'end_date': '2022-01-01T00:00:00Z',
            'location': 'Location of event 1',
            'event_type': self.event_type.id,
        }
        response = self.client.post(reverse('event-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

class EventViewSetTestCase(BaseTest):
    def setUp(self):
        self.coordinator = self.get_coordinator()
        self.login_user()
        self.event_type = EventType.objects.create(name='Conference')
        self.faculty = Faculty.objects.create(name='Faculty 1', coordinator=self.coordinator)
        self.event = Event.objects.create(
            title='Event 1',
            description='Description of event 1',
            start_date='2022-01-01T00:00:00Z',
            end_date='2022-01-01T00:00:00Z',
            location='Location of event 1',
            event_type=self.event_type,
            organizer=self.coordinator,
            faculty=self.faculty
        )

    def test_get_event(self):
        response = self.client.get(reverse('event-detail', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.event.title)

    def test_update_event(self):
        data = {
            'title': 'Event 2',
            'description': 'Description of event 2',
            'start_date': '2022-01-01T00:00:00Z',
            'end_date': '2022-01-01T00:00:00Z',
            'location': 'Location of event 2',
            'event_type': self.event_type.id,
        }
        response = self.client.patch(reverse('event-detail', args=[self.event.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Event 2')

    def test_delete_event(self):
        response = self.client.delete(reverse('event-detail', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_add_participant(self):
        response = self.client.post(reverse('event-add-participant', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.event.participants.count(), 1)
