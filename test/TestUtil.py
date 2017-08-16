# coding: utf-8
from util import Util
import unittest
class TestUtil(unittest.TestCase):
 
    def test_findFirstQuote(self):
        util = Util()
        self.assertEqual([17, '"'], util.findFirstQuote("with open(mode = \"r+\",file = \"d\") as d:"))
        self.assertEqual([10, "'"], util.findFirstQuote("m=s.split('')"))

    def test_findRealQuote(self):
        util = Util()
        self.assertEqual(2, util.findRealQuote('"',"with open(mode = \"r+\",file = \"d\") as d:"[18:]))
        #self.assertRaises(Exception, add, 4.0, 5.0)
 
    def test_isOpeningFile(self):
        util = Util()
        self.assertIs(util.isOpeningFile("with open(mode = \"r+\",file = \"d\") as d:"), True)
        self.assertIs(util.isOpeningFile("openess = []"), False)
        
    def test_spaces(self):
        self.assertEqual(3, Util().spaces("   "))
        self.assertEqual(0, Util().spaces(""))
        
    def test_addZeros(self):
        self.assertEqual("00002",Util().addZeros(2))
        self.assertEqual("00020",Util().addZeros(20))
        
    def test_isNumber(self):
        self.assertIs(Util().isNumber(0), True)
        self.assertIs(Util().isNumber(""), False)
        self.assertIs(Util().isNumber("0"), True)
        self.assertIs(Util().isNumber(1.1), True)
        self.assertIs(Util().isNumber("house"), False)
        
    def test_isPrinting(self):
        self.assertIs(Util().isPrinting("print", None), False)
        self.assertIs(Util().isPrinting("print('')", None), True)
        self.assertIs(Util().isPrinting("print()", None), True)
        self.assertIs(Util().isPrinting("print(\"\")", None), True)
        self.assertIs(Util().isPrinting("variable = print", None), False)
        self.assertIs(Util().isPrinting("print 'hello world'", None), False) 
        
    def test_getFileName(self):   
        self.assertEqual(['sys.agrv[]2', 32, 'with open(mode=sys.agrv[]1,file=sys.agrv[]2) as d:', False],Util().getFileName("with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d:"))
        self.assertEqual(['sys.agrv[]2', 32, 'with open(mode=sys.agrv[]1,file=sys.agrv[]2) as d:', False],Util().getFileName("with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d:"))

if __name__ == '__main__':     
    unittest.main()