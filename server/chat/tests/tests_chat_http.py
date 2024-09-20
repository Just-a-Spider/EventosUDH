from django.urls import reverse
from chat.models import Chat
from server.utils.test_base_test import BaseTest

REGISTER_USER_DATA_2 = {
    'first_name': 'Jane',
    'last_name': 'Doe',
    'gender': True,
    'username': 'janedoe',
    'email': 'jane.doe@udh.edu.pe',
    'password': 'password123'
}

class HttpChatsListTest(BaseTest):
    def setUp(self):
        user = self.get_user()
        user_2 = self.get_user(register_data=REGISTER_USER_DATA_2)
        self.chat = Chat.objects.create()
        self.chat.members.set([user, user_2])

    def test_get_chats_list(self):
        response = self.client.get(reverse('chats-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_chat_by_id(self):
        chat_id = Chat.objects.first().id
        response = self.client.get(reverse('chat-detail', kwargs={'chat_id': chat_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(chat_id))
        self.assertEqual(response.data['last_message'], None)
