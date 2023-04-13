import unittest
from unittest.mock import patch
from course_scheduling_system import CSS

class TestCSS(unittest.TestCase):

    def setUp(self):
        self.css = CSS()

    def test_q1_1(self):
        course = ('Math', 'Monday', 2, 4)
        with patch.object(CSS, 'check_course_exist', return_value=True):
            result = self.css.add_course(course)
            self.assertTrue(result)
            self.assertIn(course, self.css.get_course_list())

    def test_q1_2(self):
        course1 = ('Math', 'Monday', 2, 4)
        course2 = ('Physics', 'Monday', 3, 5)
        with patch.object(CSS, 'check_course_exist', return_value=True):
            self.css.add_course(course1)
            result = self.css.add_course(course2)
            self.assertFalse(result)
            self.assertNotIn(course2, self.css.get_course_list())

    def test_q1_3(self):
        course = ('Math', 'Monday', 2, 4)
        with patch.object(CSS, 'check_course_exist', return_value=False):
            result = self.css.add_course(course)
            self.assertFalse(result)
            self.assertNotIn(course, self.css.get_course_list())

    def test_q1_4(self):
        course = 'Math'
        with patch.object(CSS, 'check_course_exist', return_value=True):
            with self.assertRaises(TypeError):
                self.css.add_course(course)

    def test_q1_5(self):
        course1 = ('Math', 'Monday', 2, 4)
        course2 = ('Physics', 'Tuesday', 3, 5)
        course3 = ('Chemistry', 'Wednesday', 5, 7)
        with patch.object(CSS, 'check_course_exist', return_value=True):
            self.css.add_course(course1)
            self.css.add_course(course2)
            self.css.add_course(course3)
            result = self.css.remove_course(course2)
            self.assertTrue(result)
            self.assertNotIn(course2, self.css.get_course_list())
            self.assertEqual(4, self.css.check_course_exist.call_count)
            expected_str = 'Monday    Tuesday   Wednesday Thursday  Friday    \n\
|         |         |         |         |         \n\
Math      |         |         |         |         \n\
Math      |         |         |         |         \n\
Math      |         |         |         |         \n\
|         |         Chemistry |         |         \n\
|         |         Chemistry |         |         \n\
|         |         Chemistry |         |         \n'
            self.assertEqual(expected_str, str(self.css))
            
    def test_q1_6(self):
        with patch.object(CSS, 'check_course_exist', return_value=True):
            # Add more test cases here to achieve 100% code coverage
            pass
    
if __name__ == '__main__':
    unittest.main()
