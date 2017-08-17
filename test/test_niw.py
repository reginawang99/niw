# coding: utf-8
from niw import NiW
import unittest

class TestNiW(unittest.TestCase):
 
    def test_setWorkflowName(self):
        niw = NiW()
        initial_dir_path = niw.dirPath
        niw.setWorkflowName("Test notebook name.ipynb")
        self.assertEqual("TestNotebookName", niw.workflowName)
        self.assertEqual(initial_dir_path+"/TestNotebookName", niw.dirPath)
      
    def test_setNotebook(self):
        niw = NiW()
        with self.assertRaises(Exception) as context:
            niw.setNotebook("test.ipynb")
        self.assertTrue('File does not exist: test.ipynb', context.exception)
        niw.setNotebook("../notebook/Disease+Analysis.ipynb")
        self.assertTrue(len(niw.code) > 0)
          
if __name__ == '__main__':     
    unittest.main()