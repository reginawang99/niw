# coding: utf-8

class Util(object):

    # ## Utility Functions
    
    # In[ ]:
    
    # find first opening quote
    def findFirstQuote(self,st):
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
    
    # used after findFirstQuote
    # find closing quote
    def findRealQuote(self,q,st):
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
    
    # # Cleaning up the notebook cells
    # Count the number of spaces in a string.
        
    def spaces(self,s):
        k = 0
        while k < len(s) and s[k] == " ":
            k=k+1
        return k 
    
    
    def getFileName(self,st):
        t = st[st.index("(")+1:st.rfind(")")]
        ind = st.index("(")+1
        t = t.replace(" ","")
        if not t[0] == 's':
            ind = ind + t.find("file=")+5
            t = t[t.find("file=")+5:]
        t = t[:t.find("]")+2]
        if st.count("=")==0 or st.find("=")>st.find("("):
            return [t,ind,st[:st.index("(")]+st[st.index("("):st.rfind(")")].replace(" ","")+st[st.rfind(")"):],False]
        else:
            return[t,ind,st[:st.index("(")]+st[st.index("("):st.rfind(")")].replace(" ","")+st[st.rfind(")"):],               True,st[:st.find("=")].replace(" ","")]
    
    def getMode(self,st,fileName):
        t = st[st.index("(")+1:st.rfind(")")]
        t = t.replace(" ",""); t = t.replace(fileName,"")
        a = t.split(",")
        numDouble = 0
        for i in range(0,len(a)):
            if "sys.agrv[]" in a[i]:
                return a[i][a[i].find("sys.agrv[]"):a[i].find("sys.agrv[]")+11]
        return 'r' 
    
    def buffering(self,st):
        t = st[st.index("(")+1:st.rfind(")")]
        a = t.split(",");i = 0
        while i < len(a):
            if not "sys.agrv[" in a[i]:
                return a[i]
            i+=1
        return -1
    
    def addZeros(self,num):
        st = str(num)
        while len(st) < 5:
            st = "0" + st
        return st  
    
    # check if string is a call to print function
    # why i as an argument?
    def isPrinting(self,st,i):
        st = st.replace('"',"'")
        if st.find("print(") > -1 and (st.find("'") == -1 or st.find("'") > st.find("print(")):
            return True  
        
    # what kind of check?
    def checkForVariable(self,i,j,k,s):
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
    
    # check if character is a number
    def isNumber(self,char):
        try:
            int(char)
            return True
        except ValueError:
            return False
            
    # add zeros up to 5 digits
    def addZeros(self,num):
        st = str(num)
        while len(st) < 5:
            st = "0"+st
        return st
    
    def inCode(self,methName,lineCode):
        lineCode.replace('"',"'")
        while methName in lineCode:
            pre = ord(lineCode[lineCode.find(methName)-1])
            post = ord(lineCode[lineCode.find(methName)+len(methName)])
            if not(pre > 64 and pre < 91 or post > 64 and post < 91 or pre < 123 and pre > 96 or post < 123 and post > 96):
                if lineCode[:lineCode.find(methName)].count("'") % 2 == 0:
                    return True
            lineCode = lineCode[:lineCode.find(methName)] + lineCode[lineCode.find(methName) + len(methName)+1:]
        return False         