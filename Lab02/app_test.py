import unittest
import app
from unittest.mock import Mock
from unittest.mock import patch

class ApplicationTest(unittest.TestCase):
    def setUp(self):
        """
        people = ['William', 'Oliver', 'Henry', 'Liam']
        selected = ['William', 'Oliver', 'Henry']
        return (people, selected)"""
        return ['William', 'Oliver', 'Henry', 'Liam'], ['William', 'Oliver', 'Henry']

    def test_app(self):  
        def fake_mail(name):
            context = 'Congrats, ' + name + '!'
            print(context)
            return context

        @patch('app.Application.get_names')
        @patch('app.Application.get_random_person')
        def test_select_next_person(self, mock_get_random_person, mock_get_names):
            mock_get_names.return_value = self.setUp()
            mock_get_random_person.side_effect = ['William', 'Oliver', 'Henry', 'Liam']
            App = app.Application()
            whom =App.select_next_person()
            print(whom, 'selected')
            self.assertEqual(whom, 'Liam')

            MailSystem = Mock()
            MailSystem.write.side_effect = fake_mail
            App.mailSystem = MailSystem
            App.notify_selected()
            
            print(MailSystem.write.call_args_list)
            print(MailSystem.send.call_args_list)
            self.assertEqual(MailSystem.write.call_count, len(App.selected))
            self.assertEqual(MailSystem.send.call_count, len(App.selected))
        test_select_next_person(self)
 
if __name__ == "__main__":
    unittest.main()
