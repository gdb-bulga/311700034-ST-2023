import unittest
import sys
sys.path.append('/Users/houyi/Desktop/Software_testing/Lab1')

import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        for name in self.user_name:
            self.user_id.append(self.students.set_name(name))
        self.assertEqual(self.students.name, self.user_name)
        
        print('Start set_name test', '\n')
        for i in range(len(self.user_name)):
            print(i, self.students.name[i])
        print('\n')
        print('Finish set_name test', '\n', '\n', '\n')
        
    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        for i in self.user_id:
            self.assertEqual(self.students.get_name(i), self.students.name[i])
        ids = set(self.user_id)
        mex = 0
        while mex in ids:
          mex += 1
        self.assertEqual(self.students.get_name(mex), 'There is no such user')
        
        print('Start get_name test', '\n')
        for i in self.user_id:
            print('id:', i, self.students.get_name(i))
        print('id:', mex, self.students.get_name(mex))
        
        print('\n')
        print('Finish get_name test')

        
if __name__ == '__main__':# pragma: no cover
    unittest.main()
    