# coding: utf-8
import os

class Util(object):
    
    def getWorkflowName(self, filepath):
        '''
        @param filepath: str
        @return filename: str
        
        - create the workflow name based on the notebook filename
        - create the folder for the workflow files
        '''        
        import re
        filename = filepath.split("/")[-1]
        filename = filename.replace(u".ipynb","")
        filename = filename.title()
        filename = re.sub('[^A-Za-z0-9]+', '', filename)
        return filename  
        
    def createFolder(self, folder):
        '''
        @param folder: str
        @return None
        
        Create folder or remove contents of the existing folder
        '''
        if os.path.exists(folder):                                
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        else:
            os.mkdir(folder) 
                    
    def findFirstQuote(self,st):
        '''
        @param st: str
        @return [int,str] index and quotation mark
        
        Find the first opening quote.
        '''
        if not "'" in st and not '"' in st:
            return [-1]
        elif "'" in st and '"' in st:
            if st.find('"') > st.find("'"):
                return [st.find("'"),"'"]
            return [st.find('"'),'"']
        elif "'" in st:
            return [st.find("'"),"'"]
        elif '"' in st:
            return [st.find('"'),'"']
        
    def findRealQuote(self,q,st):
        '''
        @param q: str Quotation mark " or '
        @param st: str
        @return int: index TODO: what is this?
        
        - used after findFirstQuote
        - find closing quote
        '''
        n = 0
        # why "\\" ?
        while not st[:st.find(q)+1].count("\\"+q) == 0:
            while not st[:st.find(q)+1].count("\\\\") == 0:
                st = st[:st.find("\\\\")]+st[st.find("\\\\")+2:]
                n+=2
            if not st[:st.find(q)+1].count("\\"+q)==0:
                st = st[:st.find("\\"+q)]+st[st.find("\\"+q)+2:]
                n+=2
        return st.find(q)+n
    
    def isOpeningFile(self,st):
        '''
        @param st: str
        @return Boolean
        
        Check if string contains a open statement.
        '''
        if st.replace(" ","").find("open(") != -1:
            t = st[:st.index("(")]
            # the last index
            lastChar = t[t.rfind("open")-1]
            # TODO: what is it checking?
            if lastChar == '.' or lastChar == '=' or lastChar == " ":
                # TODO: unused variable
                s = st[st.index("(")+1:st.rfind(")")].replace(" ","")
                return True   
        return False 
    
    def spaces(self,s):
        '''
        @param s: str
        @return int
        
        Count the number of spaces in a string.
        '''
        k = 0
        while k < len(s) and s[k] == " ":
            k=k+1
        return k 
        
    def getFileName(self,st):    
        '''
        @param st: str
        TODO: why all these values on the list?
        @return [str,int,str,Boolean]: fileName,index,st[],Boolean,st[]
        
        Get the file name in open() statement.
        
        Example:
        str = with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d: 
        return [u'sys.agrv[]2', 32, u'with open(mode=sys.agrv[]1,file=sys.agrv[]2) as d:', False]
        
        str =       with open (sys.agrv[]3,sys.agrv[]4) as da: 
        return [u'sys.agrv[]3', 15, u'    with open (sys.agrv[]3,sys.agrv[]4) as da:', False]
        
        str = with open(sys.agrv[]5,sys.agrv[]6) as w: 
        return [u'sys.agrv[]5', 10, u'with open(sys.agrv[]5,sys.agrv[]6) as w:', False]
        '''
        t = st[st.index("(")+1:st.rfind(")")]
        ind = st.index("(")+1
        t = t.replace(" ","")
        # what is 's'?
        if not t[0] == 's':
            ind = ind + t.find("file=")+5
            t = t[t.find("file=")+5:]
        t = t[:t.find("]")+2]
        # TODO: what is it for?
        if st.count("=") == 0 or st.find("=") > st.find("("):
            return [t,ind,st[:st.index("(")]+st[st.index("("):st.rfind(")")].replace(" ","")+st[st.rfind(")"):],False]
        else:
            return[t,ind,st[:st.index("(")]+st[st.index("("):st.rfind(")")].replace(" ","")+st[st.rfind(")"):],True,st[:st.find("=")].replace(" ","")]
    
    def getMode(self,st,fileName):
        '''
        @param st: str
        @param fileName: str
        @return str
        
        Returns the mode use in a open(mode="r") statement.
        
        Examples:
        
        st = with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d: 
        filename = sys.agrv[]2
        return: sys.agrv[]1
        
        st = with open (sys.agrv[]3,sys.agrv[]4) as da: 
        filename = sys.agrv[]3
        return: sys.agrv[]4
        
        st = with open(sys.agrv[]5,sys.agrv[]6) as w: 
        filename = sys.agrv[]5 
        return: sys.agrv[]6        
        '''
        t = st[st.index("(")+1:st.rfind(")")]
        t = t.replace(" ","")
        t = t.replace(fileName,"")
        a = t.split(",")
        for i in range(0,len(a)):
            # what is this condition for?
            if "sys.agrv[]" in a[i]:
                # return i in sys.argv[]i
                return a[i][a[i].find("sys.agrv[]"):a[i].find("sys.agrv[]")+11]
        return 'r' 
    
    def buffering(self,st):
        '''
        @param st: str
        @return int
        
        Example
        st = with open(mode = sys.agrv[]1,file = sys.agrv[]2) as d: 
        return -1
        
        st =    with open (sys.agrv[]3,sys.agrv[]4) as da: 
        return -1
        
        st = with open(sys.agrv[]5,sys.agrv[]6) as w: 
        return -1
        
        TODO: description
        '''
        t = st[st.index("(")+1:st.rfind(")")]
        a = t.split(",")
        i = 0
        while i < len(a):
            if not "sys.agrv[" in a[i]:
                return a[i]
            i+=1
        return -1
    
    def addZeros(self,num):
        '''
        @param num: int
        @return st: str
        
        Add zeros "0" up to 5 digits.
        '''
        st = str(num)
        while len(st) < 5:
            st = "0" + st
        return st  
        
    def isPrinting(self,st,i):
        '''
        @param st: str
        @param i: TODO: remove?
        @return Boolean
        
        Check if string is a call to print function
        TODO: why i as an argument?
        '''
        st = st.replace('"',"'")
        if st.find("print(") > -1 and (st.find("'") == -1 or st.find("'") > st.find("print(")):
            return True 
        return False 
            
    def checkForVariable(self,i,j,k,s):
        '''
        TODO: Describe @param and @return
        @param i
        @param j
        @param k
        @param s
        @return [Boolean,Boolean,int,int]
        
        Example
        i,j,k,s
        0 0 8 temp = []
        return [False, False, 0, 9] 
        
        0 1 0 s =
        return [True, u's', [1, 0], 2] 
        
        0 1 2 s =
        return [False, False, 0, 3] 
        
        0 1 3 s =
        return [False, False, 0, 4] 
        
        0 2 0 ga = sys.arg[]2!
        return [True, u'ga', [2, 0], 3]
        
        0 2 3 ga = sys.arg[]2!
        return [False, False, 0, 4]
        
        TODO: what kind of check?
        '''
        if s[k].isalpha():
            for x in range(k,len(s)):
                if not s[x].isalpha() and not self.isNumber(s[x]):
                    try:
                        if not s[x] == "(" and not s[x:x+2] == " (":
                            if not (s[x] == "=" or s[x:x+2] == " =") or s.find("(")==-1 or                            s.find("(") > k or s[:k].count("(") == s[:k].count(")"):
                                    if not s[:k-1].replace(" ","") == "for":
                                        return [True,s[k:x].replace(" ",""),[j,k],x+1]
                                    else:
                                        return [False,True,s[k:x].replace(" ",""),x+1,s[:k-4]+"    "]
                        return [False,False,0,k+1]
                    except ValueError:
                        return [True,s[k:].replace(" ",""),[j,k],x+1]
            return [True,s[k:].replace(" ",""),[j,k],x+1]
        return [False,False,0,k+1]
    
    
    def isNumber(self,char):
        '''
        @param char: str
        @return Boolean
        Check if character is a number
        '''
        try:
            int(char)
            return True
        except ValueError:
            return False            
    
    def inCode(self,methName,lineCode):
        '''
        @param methName: str
        @param lineCode: str
        @return Boolean
        TODO: description
        '''
        lineCode.replace('"',"'")
        while methName in lineCode:
            pre = ord(lineCode[lineCode.find(methName)-1])
            post = ord(lineCode[lineCode.find(methName)+len(methName)])
            if not(pre > 64 and pre < 91 or post > 64 and post < 91 or pre < 123 and pre > 96 or post < 123 and post > 96):
                if lineCode[:lineCode.find(methName)].count("'") % 2 == 0:
                    return True
            lineCode = lineCode[:lineCode.find(methName)] + lineCode[lineCode.find(methName) + len(methName)+1:]
        return False   
    
          