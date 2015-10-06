import unittest
import os.path
from format import format
from format import Line
from fv2 import CSV


class FormatcsvTest(unittest.TestCase):
    def test_line(self):
        l1 = 'aaaaaaaaaa'
        l2 = 'bbbbbbbbbb'
        l3 = 'cccccc'
        l4 = 'ddddddddddddddddddddddddddddddd'
        obj = Line(l1, 3)
        self.failIf(obj.content() != None)
        obj.feed(l2)
        self.failIf(obj.content() != None)
        obj.feed(l3)
        self.failIf(obj.content() != ', '.join([l1, l2, l3]))
        obj.feed(l4)
        self.failIf(obj.content() != ', '.join([l1, l2, l3]))

    def test_format(self):
        format('data/testdata.csv', 'data/testdata-3dayperline.csv', 3)
        self.failIf(os.path.getsize('data/testdata-3dayperline.csv') <
                    os.path.getsize('data/testdata.csv') * 2)


class CsvTest(unittest.TestCase):
    def test_closeprice(self):
        format('data/testdata.csv', 'data/testdata-10dayperline.csv', 10)
        csv = CSV('data/testdata-10dayperline.csv')
        p = csv.closeprice(date='2015-07-15')
        self.failIf(p != 79.03)

if __name__ == '__main__':
    unittest.main()
