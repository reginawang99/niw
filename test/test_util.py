# coding: utf-8
from util import Util
import unittest
class test_util(unittest.TestCase):
 
    def test_getWorkflowName(self):
        self.assertEqual("DiseaseAnalysis", Util().getWorkflowName("notebook/disease_analysis.ipynb"))
        self.assertEqual("DiseaseAnalysis2", Util().getWorkflowName("notebook/example/disease_analysis_2.ipynb"))
        self.assertEqual("TestNotebookName", Util().getWorkflowName("notebook/Test notebook name.ipynb"))
        
    def test_createFolder(self):
        import os
        folder1 = "notebook"
        self.assertFalse(os.path.exists(folder1))
        
        # test creation of the folder
        Util().createFolder(folder1);
        
        self.assertTrue(os.path.exists(folder1))
        self.assertTrue(os.listdir(folder1) == [])
        open(os.path.join(folder1, "name.txt"), 'a').close()
        self.assertTrue(os.listdir(folder1) != [])
        
        # test removing content of the existing folder
        Util().createFolder(folder1);
        
        self.assertTrue(os.listdir(folder1) == [])
        self.assertTrue(os.path.exists(folder1))
        os.rmdir(folder1)
        
    def test_findFirstQuote(self):
        util = Util()
        self.assertEqual([17, '"'], util.findFirstQuote("with open(mode = \"r+\",file = \"d\") as d:"))
        self.assertEqual([10, "'"], util.findFirstQuote("m=s.split('')"))

    def test_findRealQuote(self):
        util = Util()
        self.assertEqual(2, util.findRealQuote('"',"with open(mode = \"r+\",file = \"d\") as d:"[18:]))

    def test_isOpeningFile(self):
        util = Util()
        self.assertIs(util.isOpeningFile("with open(mode = \"r+\",file = \"d\") as d:"), True)
        self.assertIs(util.isOpeningFile("openess = []"), False)
        
    def test_spaces(self):
        self.assertEqual(3, Util().spaces("   "))
        self.assertEqual(0, Util().spaces(""))
        
    def test_getFileName(self):   
        self.assertEqual(['sys.agrv[]2', 32, 'with open(mode=sys.agrv[]1,file=sys.agrv[]2) as d:', False],Util().getFileName("with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d:"))
        self.assertEqual(['sys.agrv[]2', 32, 'with open(mode=sys.agrv[]1,file=sys.agrv[]2) as d:', False],Util().getFileName("with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d:"))
     
    def test_getMode(self):
        #self.assertEqual('r', Util().getMode("with open(mode = \"r+\",file = \"sys.agrv[]2\") as d:","d.txt"))
        #self.assertEqual('r', Util().getMode("with open(mode = \"w+\",file = \"sys.agrv[]3\") as d:","d.txt"))
        pass
    
    def test_getBuffering(self):
        pass
    
    
    def test_addZeros(self):
        self.assertEqual("00002",Util().addZeros(2))
        self.assertEqual("00020",Util().addZeros(20))
        
    def test_isPrinting(self):
        self.assertIs(Util().isPrinting("print", None), False)
        self.assertIs(Util().isPrinting("print('')", None), True)
        self.assertIs(Util().isPrinting("print()", None), True)
        self.assertIs(Util().isPrinting("print(\"\")", None), True)
        self.assertIs(Util().isPrinting("variable = print", None), False)
        self.assertIs(Util().isPrinting("print 'hello world'", None), False) 
        
    def test_checkForVariable(self):
        pass
        
    def test_isNumber(self):
        self.assertIs(Util().isNumber(0), True)
        self.assertIs(Util().isNumber(""), False)
        self.assertIs(Util().isNumber("0"), True)
        self.assertIs(Util().isNumber(1.1), True)
        self.assertIs(Util().isNumber("house"), False)
        
    def test_inCode(self):
        pass        
        
if __name__ == '__main__':     
    unittest.main()
    