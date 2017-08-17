# coding: utf-8
'''
NiW: Notebooks into Workflows
Converting Jupyter Notebooks into Wings Workflows
'''
import nbformat as nbf
from  nbformat.v4.nbbase import (new_code_cell, new_markdown_cell)
import os
import zipfile
from util import Util
import sys

class NiW(object):
    ''' 
    Data
     
    arr: is a list that includes all cells, markdown and code and their info.
    code: is a list that only includes code cells info and their relative position in the notebook.
    '''
    def __init__(self):
 
        '''TODO: What is this?'''
        self.arr = []
        self.code = []
        self.input = []
        self.output = []
        '''TODO: What is this?'''
        self.parameters = []
        self.param = None
        '''TODO: what is it??'''
        self.banned = [[]]
        '''TODO: What is this?'''
        self.b = []
        self.newVariables = []
        self.passedOnVariables = []
        '''TODO: What is this?'''
        self.strings = []
        self.files = []
        self.methods = None
        self.stdIn = None
        self.allVar = None
        '''TODO: What is this?'''
        self.index = None
        self.runFiles = None
        self.dirPath = "workflow"
        self.workflowName = None        
    
    def setNotebook(self, filepath):
        '''         
        @param filepath: str  
        @return arr: list
        @return code: list
                   
        - set the notebook file
        
        Grab notebook cells information         
        - open notebook with the nbconvert API
            - Get all of the cells (code and markdown) in the specified notebook.
            - Grab cells, put back code to cells to notebook, run code, and save result to a notebook.
            - Check if the code cells' language is in Python.
        '''        
        if not os.path.exists(filepath):
            raise Exception("File does not exist: "+filepath)
        
        self.workflowName = Util().getWorkflowName(filepath)
        self.dirPath = os.path.join(self.dirPath, self.workflowName)
        Util().createFolder(self.dirPath)
        
        # inform notebook file
        with open(filepath,"r") as r:
            # nbconvert format version = 3
            nb = nbf.read(r,as_version=3)
            # worksheets?
            for x in nb.worksheets:
                for cell in x.cells:
                    if cell.cell_type == "markdown" or cell.cell_type == "heading":
                        # source code
                        self.arr.append([cell.source,"markdown"])
                    elif cell.cell_type =="code":
                        if not cell.language == 'python':
                            raise ValueError('Code must be in python!')
                        # input x output in code cells
                        self.arr.append([cell.input,"code"])
                        # split("\n") the string in the code cell
                        # get relative position number of the cell
                        self.code.append([cell.input.split("\n"),len(self.arr)]) 

    def preProcessing(self):
        '''
        @return files: list
        @return strings: list
        
        - Deal w strings by putting all in an array.
        - Deal w comments by putting in an array and adding it back later.
        '''        
        strings = []
        files = []
        code = self.code
        for i in range(0,len(code)):
            # foreach line of code after split("\"), 
            # create a new dimension in the code array with value ""
            for j in range(0,len(code[i][0])):
                code[i][0][j] = [code[i][0][j],""]
            j = 0
            while j < len(code[i][0]):
                dealt = False
                if '"""' == code[i][0][j][0].replace(" ","")[:3]:
                    code[i][0][j][1]= code[i][0][j][0]
                    code[i][0][j][0]= ''
                    j +=1
                    while not '"""' in code[i][0][j][0] and not dealt:
                        code[i][0][j][1]= code[i][0][j][0]
                        code[i][0][j][0]= ''
                        j +=1
                        if '"""' in code[i][0][j][0]:
                            code[i][0][j][1]= code[i][0][j][0]
                            code[i][0][j][0]= ''
                            dealt = True
                if "'''" == code[i][0][j][0].replace(" ","")[:3]:
                    code[i][0][j][1]= code[i][0][j][0]
                    code[i][0][j][0]= ''
                    while not "'''" in code[i][0][j][0]:
                        j = j+1
                        code[i][0][j][1]= code[i][0][j][0]
                        code[i][0][j][0]= ''
                    code[i][0][j][1]= code[i][0][j][0]
                    code[i][0][j][0]= ''
                    dealt = True        
                fstQt = Util().findFirstQuote(code[i][0][j][0])
                if not fstQt[0] == -1 and code[i][0][j][0][:fstQt[0]].count("#")==0 and not dealt:
                    string = code[i][0][j][0][fstQt[0]+1:Util().findRealQuote(fstQt[1],code[i][0][j][0][fstQt[0]+1:])+fstQt[0]+1]
                    if len(string.replace(" ","")) > 0:
                        if not Util().isOpeningFile(code[i][0][j][0]):
                            strings.append(string)
                            code[i][0][j][0]=code[i][0][j][0][:fstQt[0]]+"sys.arg[]"+str(len(strings))+"!"+code[i][0][j][0][Util().findRealQuote(fstQt[1],code[i][0][j][0][fstQt[0]+1:])+fstQt[0]+2:]
                        else:
                            files.append(string)
                            code[i][0][j][0]=code[i][0][j][0][:fstQt[0]]+"sys.agrv[]"+str(len(files))+code[i][0][j][0][Util().findRealQuote(fstQt[1],code[i][0][j][0][fstQt[0]+1:])+fstQt[0]+2:]
                        dealt = True
                if not dealt and  not code[i][0][j][0].find("#")==-1:
                    code[i][0][j][1]= code[i][0][j][0][code[i][0][j][0].find("#"):]
                    code[i][0][j][0]= code[i][0][j][0][:code[i][0][j][0].find("#")]
                if not dealt:
                    j +=1
        self.files = files
        self.strings = strings
        return files

    def comments(self):
        '''
        @param code: list
        @return code: list
        - Deal w comments by putting in an array and adding it back later.
        - If a "\" is at the end of a line, then combine with the next line.
        '''        
        code = self.code
        for i in range (0,len(code)):
            j = 0
            while j < len(code[i][0]):
                if len(code[i][0][j][0]) > 0 and code[i][0][j][0][-1] == "\\": 
                    k = 0
                    while code[i][0][j+1][0][k] == " ":
                        k+=1
                    code[i][0][j][0]= code[i][0][j][0][:-1] + " " + code[i][0][j+1][0][k:]
                    code[i][0][j][1]= code[i][0][j+1][1]
                    del code[i][0][j+1]
                else:
                    j+=1

    def newLines(self):
        '''
        @param code: list
        @return code: list
        
        Make a new line where there is a semicolon, except if it is in a string.
        Justification: Sometimes Jupyter API inserts ";" between assigment statements, instead of "\n".
        Example:
            temp = "";i = 3
        becomes:
            temp = ""
            i = 3
        '''
        code = self.code
        for i in range(0,len(code)):
            j = 0 
            while j < len(code[i][0]):
                if ";" in code[i][0][j][0]:
                    fake = code[i][0][j][0].split(";")
                    code[i][0][j][0]= fake[0]
                    s = fake[0][:Util().spaces(fake[0])]
                    for g in range(1,len(fake)):
                        code[i][0].insert(j+1,[s+fake[len(fake)-g][Util().spaces(fake[len(fake)-g]):],''])
                j = j+1

    def cleaningUp(self):
        '''
        @param code: list
        - remove unnecessary spaces and new lines in code.
        - all single quotes ' are changed to double quotes ".
        - run under assumption that there are no single quotes ' or double quotes " in strings.
        '''
        code = self.code
        for i in range(0,len(code)):
            j = 0
            while j < len(code[i][0]):
                if len(code[i][0][j][0].replace(" ","")) == 0 and len(code[i][0][j][1])==0:
                    del code[i][0][j]
                else:
                    j = j+1
        for i in range(0,len(code)):
            for j in range(0,len(code[i][0])):
                k = Util().spaces(code[i][0][j][0])
                code[i][0][j][0]= code[i][0][j][0][:k] + " ".join(code[i][0][j][0][k:].split())
    

    def imports(self):
        '''
        @param code: list
        @return imports: list
        @return b: list
        
        Imports
        - get all of the imported libraries, puts them together, and sets up heading for code of workflow component.
        - add "matplotlib.use(\"Agg\")" if 'import matplotlib' is an imported library so that the output figure can be saved.
        - save the imported library nicknames or names so that they will not be confused as variables.
        '''
        code = self.code    
        imports= "import sys\n"
        b = ['sys']
        for i in range(0,len(code)):
            j= 0
            while j < len(code[i][0]): 
                if (code[i][0][j][0][:7] == 'import ' or  code[i][0][j][0][:5] == 'from '):
                    if not code[i][0][j][0] in imports:            
                        imports = imports + code[i][0][j][0] +"\n"
                        if not " as " in code[i][0][j][0]:
                            b.append(code[i][0][j][0][code[i][0][j][0].find("import")+7:])
                        else:
                            b.append(code[i][0][j][0][code[i][0][j][0].find(" as ")+4:])
                    del code[i][0][j]
                elif "matplotlib.use(" in code[i][0][j][0]:
                    del code[i][0][j]
                else:
                    j= j+1
        if 'import matplotlib' in imports:
            imports = imports.replace("import matplotlib\n","")
            imports = 'import matplotlib' + "\nmatplotlib.use(\"Agg\")\n" + imports
        imports = "#!/usr/bin/env python\n" +imports
        self.b = b
        return imports

    def magicCommands(self):
        '''
        @param code: list
        @
        Magic Commands
        - Clean up cell magic
        - No cell magic allowed (other than for matplotlib allowed) or a value error will be thrown
        - All cell magic deleted
        '''
        code = self.code    
        for i in range(0,len(code)):
            j=0
            while j <len(code[i][0]):
                if code[i][0][j][0][:1] == "%":
                    if not "matplotlib" in code[i][0][j][0]:
                        raise ValueError('No cell magic allowed (other than for matplotlib allowed)')     
                    else:
                        del code[i][0][j]
                else:
                    j = j+1
 
    def organizeMethods(self):
        '''
        @param code: list
        @return methods: list
        @return code: list
        
        Methods
        - Grab all defined methods and puts in array <b>methods</b>.
        - Save name and code.
        - Remove from code cell.
        - Run under assumption that no methods have been overriden.
        '''
        code = self.code
        methods = []
        for i in range(0,len(code)):
            j = 0
            while j < len(code[i][0]):
                if code[i][0][j][0][:4] == "def ":
                    t = code[i][0][j][0]
                    mName = t[t.index(' ')+1:t.index('(')]
                    mCode = [t,code[i][0][j][1]]
                    k = j
                    del code[i][0][j]
                    while k <len(code[i][0]):
                        if code[i][0][k][0][:4]=="    ":
                            mCode[0] = mCode[0] +"\n" + code[i][0][k][0]
                            mCode[1] = mCode[1]+"\n"+code[i][0][k][1]
                            del code[i][0][k]
                        else:
                            k = len(code[i][0])
                    methods.append([mName,mCode])
                else:
                    j = j+1
        self.methods = methods
    
    def checkOpenFiles(self):
        '''
        @param code: list
        @return code: list
        
        Relocate code in code cell if it uses a file opened from another cell. (Merge??)
        '''
        code = self.code
        for i in range(0,len(code)):
            for j in range (0,len(code[i][0])):
                if Util().isOpeningFile(code[i][0][j][0]) and "sys.agrv[]" in code[i][0][j][0]:
                    name = Util().getFileName(code[i][0][j][0])
                    if name[3]:#whether the file is opened "with open(...):"
                        di= i
                        dj=j
                        closed = False
                        lastSeen = i
                        while not closed and di < len(code):
                            while not closed and dj < len(code[i][0]):
                                if name[4] in code[di][0][dj]:
                                    if "close(" in code[di][dj]:
                                        closed = True 
                                        lastSeen = di
                                    else:
                                        lastSeen = di
                                dj+=1
                            di+=1
                        if not lastSeen == di:
                            for a in range(i,lastSeen):
                                for b in range(0,len(code[a][0])):
                                    code[i][0].append(code[i+1][0][0])
                                    del code[i+1][0][0]
    
    def cleanAndMerge(self):
        '''
        @param code: list
        @param arr: list
        @return code: list
        @return arr: list
        
        Cleaning up Code cells and Merge Cells
        - Remove code cells with no substantial code & merge cells if start indented.
        - If there is no running code in the notebook, a value error will be raised.
        '''
        code = self.code
        arr = self.arr
        dif = 0
        i = 0
        while i < len(code):
            if len(code[i][0]) == 0:            
                dif = dif + 1
                del arr[code[i][1] - dif]
                del code[i]
            elif code[i][0][0][0][:4] == "    ":
                for j in range(0,len(code[i][0])):
                    code[i-1][0].append(code[i][0][j])
                dif = dif + 1
                del arr[code[i][1] - dif]
                del code[i]
            else:
                code[i][1]= code[i][1] - dif
                i= i+1
        if len(code) == 0:
            raise ValueError("There is no running code in this notebook!")    

    def inputsAndOuputs(self, files):
        '''
        @param code: list
        @return input: list
        @return output: list
        @return code: list
        
        Input and Outputs
        - Get list of input data or output data needed for each component.
        - If an input data is opened across cells, the cells are merged.
        - Cells will be merged until the file is closed, the variable name for the input data is no longer mentioned or until the end of the notebook.
        - Put data into form, e.g., "I.1.data.txt".
        - Put "sys.argv[ ]" in code.
        '''
        code = self.code    
        input = []
        output = []
        for i in range(0,len(code)):
            input.append([])
            output.append([])
            for j in range (0,len(code[i][0])):
                if Util().isOpeningFile(code[i][0][j][0]) and "sys.agrv[]" in code[i][0][j][0]:
                    name = Util().getFileName(code[i][0][j][0])
                    indexOfName = int(name[0][10:])
                    mode = files[int(Util().getMode(code[i][0][j][0],name[0])[10:])-1]
                    if 'r' in mode or '+' in mode:
                        input[i].append(["D"+Util().addZeros(len(input[i])+1)+files[indexOfName-1],files[indexOfName-1]])
                        code[i][0][j][0] = code[i][0][j][0][:code[i][0][j][0].find("(")+1]+"sys.argv[" + str(len(input[i])) + "]"+                 ",\""+mode+"\""+","+str(Util().buffering(code[i][0][j][0]))+code[i][0][j][0][code[i][0][j][0].rfind(")"):]
                    else:
                        code[i][0][j][0] = code[i][0][j][0][:code[i][0][j][0].find("(")+1]+"sys.argv[],\""+mode+"\","+str(Util().buffering(code[i][0][j][0]))+code[i][0][j][0][code[i][0][j][0].rfind(")"):]   
                        output[i].append(["O"+Util().addZeros(len(output[i])+1)+files[indexOfName-1],[j,name[1]+9]])
                    if "+" in mode:
                        code[i][0].append(["with open(sys.argv["+str(len(input[i]))+"],'r') as r1928gbdh:",""])
                        output[i].append(["O"+Util().addZeros(len(output[i])+1)+files[indexOfName-1],[len(code[i][0]),23]])
                        code[i][0].append(["    with open(sys.argv[],'w') as w29384ia9ehv:",""])
                        code[i][0].append(["        w29384ia9ehv.write(r1928gbdh.read())",""])
        self.input = input
        self.output = output
    
    def documentation(self):
        '''
        @param arr: list
        @return doc: list
        Documentation /  Markdown cells
        - Make the documentation of first code cell (all markdown combined).
        - Format: "Cell ("+cell number+"): "+source+"\n".
        '''
        arr = self.arr
        doc = ""
        for i in range(0,len(arr)):
            if arr[i][1] == 'markdown':
                doc = doc + "Cell (" + str(i+1) + "): " + arr[i][0] +"\n"
                
        # remove last new line
        if not doc == "":
            doc = doc[:len(doc)-1]
    
        return doc

    def findAllVariables(self,num):
        ''' 
        @param num: TODO: what is it??
        @param code
        @param input
        @param output
        @param banned
        @param b: TODO: what is it??
        @return array: TODO: what is it??
        @return index: TODO: what is it??
        @return banned: TODO: what is it??
        
        TODO: description
        '''
        code = self.code
        input = self.input
        output = self.output
        banned = self.banned
        b = self.b
        # exclude special keywords
        excluded = ["if","try","for","while","with","def","as","else","elif","and","not","del","True", "False","in","return","assert"           ,"break","class","continue","except","exec","finally","from","global","import","is","lambda","or","pass","print",           "raise","yield"]
        array = []
        for j in range(0,len(code[num][0])):
            a = code[num][0][j][0].split('"')
            st = ""
            for amt in range(0,len(a)):
                if amt % 2 == 0:
                    st = st + a[amt]
                else:
                    for q in range(0,len(a[amt])):
                        st +=" "
            index = 0
            while index < len(st):
                char = st[index-1]
                if index == 0 or char == " " or char == "=" or char == "(" or char == "," or char == "[" or char == ";":
                    total = Util().checkForVariable(num,j,index,st)                    
                    if total[0]:
                        notInclude = False
                        for q in range(0,len(input[num])):
                            if input[num][q][1]== total[1]:
                                notInclude = True
                        for q in range(0,len(output[num])):
                            if output[num][q][1] == total[1]:
                                notInclude = True
                        if not total[1] in array and not notInclude:
                            if not total[1] in excluded and not total[1] in banned[num]:
                                if not total[1] in b:
                                    array.append(total[1])#total[1] is the name of the variable
                                    array.append(total[2])#total[2] is the index of the variable
                                else:
                                    while index < len(st) and not (st[index] == "(" or st[index] == "=" or st[index] == "[" or st[index] == ":" or st[index] == " "):
                                        index +=1
                                    index -=1
                    elif total[1]:
                        banned[num].append(total[2])
                        banned[num].append(total[4])
                    index +=1
                    index = total[3]
                else:
                    index +=1
        return array  
        
    def variables(self):
        '''
        - Find all variables used in each cell (cannot have same name as an imported libarary or the excluded below).
        - Split into passed on variables and newly created variables.
        - Check if a variable that a for loop is using.
        '''
        code = self.code    
        banned = self.banned
        newVariables = [self.findAllVariables(0)]
        passedOnVariables = [[]]
        for i in range(1,len(code)):
            banned.append([])
            variables = self.findAllVariables(i)
            newVariables.append([])
            passedOnVariables.append([])
            for m in range(0,int(len(variables)/2)):
                a = 0 
                indentFound = False
                line = code[i][0][variables[2*m+1][0]][0]
                while a < len(line) and not indentFound:
                    if line[a] == " ":
                        a = a+1
                    else: indentFound = True
                if variables[2*m+1][1] == a and "=" in line and line.find("=") < (len(variables[2*m])+variables[2*m+1][1]+2):
                    lineAfterVar = line[line.find("="):]+" "
                    inString = False
                    passed = False
                    while not passed and variables[2*m]in lineAfterVar:
                        if not lineAfterVar[:1] == " ":
                            lineAfterVar = " "+ lineAfterVar
                        if not lineAfterVar[lineAfterVar.find(variables[2*m])-1].isalpha() \
                                and not Util().isNumber(lineAfterVar[lineAfterVar.find(variables[2*m])-1]) \
                                and not Util().isNumber(lineAfterVar[lineAfterVar.find(variables[2*m])+len(variables[2*m])+1]) \
                                and not lineAfterVar[lineAfterVar.find(variables[2*m])+len(variables[2*m])+1].isalpha():
                            passedOnVariables[i].append(variables[2*m])
                            passedOnVariables[i].append(variables[2*m+1])
                            lineAfterVar = " "
                            passed = True
                        lineAfterVar = lineAfterVar[lineAfterVar.find(variables[2*m])+1:]
                    if not passed:
                        newVariables[i].append(variables[2*m])
                        newVariables[i].append(variables[2*m+1])
                else:
                    passedOnVariables[i].append(variables[2*m])
                    passedOnVariables[i].append(variables[2*m+1])

        self.banned = banned
        self.newVariables = newVariables
        self.passedOnVariables = passedOnVariables
            
    def splitVariables(self):
        '''
        - Split newly created variables into created internally or to be set by the user.
        - The set methods are methods that can be used in the process of creating the variable and still be set by the user.
        '''
        code = self.code
        banned = self.banned
        newVariables = self.newVariables
        passedOnVariables = self.passedOnVariables
        allVar = []
        for i in range(0,len(code)):
            allVar.append([])
            for j in range(0,int(len(newVariables[i])/2)):
                allVar[i].append(newVariables[i][j*2])
            for j in range(0,int(len(passedOnVariables[i])/2)):
                allVar[i].append(passedOnVariables[i][j*2])
        setMethods = ["date"]
        
        for i in range(0,len(code)):
            var = 0
            while var*2+1 < len(newVariables[i]):
                deleted = False
                line = code[i][0][newVariables[i][var*2+1][0]][0].replace(" ","")
                if "\"\"" in line:
                    deleted = True
                    del newVariables[i][var*2]
                    del newVariables[i][var*2]
                while '"' in line:
                    line2 = line[:line.find('"')]
                    line = line[line.find('"')+1:] 
                    line = line[line.find('"')+1:] 
                    line = line2 + line
                line = line + " "
                if "+" in line:
                    deleted = True
                    del newVariables[i][var*2]
                    del newVariables[i][var*2]
                k = line.find("=")+1
                if line[k].isalpha() and (line[-2].isalpha() or Util().isNumber(line[-2])):
                    if not line[k:-1] == 'True' and not line[k:-1] == 'False':
                        deleted = True
                        del newVariables[i][var*2]
                        del newVariables[i][var*2]
                while k < len(line) and not deleted:
                    if line[k].isalpha():
                        n = k+1
                        while line[n].isalpha():
                            n = n+1
                        
                        word = line[k:n]
                        if word in allVar or word in banned[i]:
                            deleted = True
                            del newVariables[i][var*2]
                            del newVariables[i][var*2]
                        else:
                            k = n+1
                    else:
                        k = k+1
                while '(' in line and not deleted:
                    if line[line.find('(')-1].isalpha():
                        n = line.find('(')-2
                        while line[n].isalpha():
                            n = n-1
                        fullString = line[n+1:line.find('(')]
                        if not fullString in setMethods:
                            line ="("
                            del newVariables[i][var*2]
                            del newVariables[i][var*2]
                            deleted = True
                    line = line[:line.find("(")]+line[line.find("(")+1:]
                if not deleted:
                    var = var+1
        self.allVar = allVar

    def divideVariablesInParametersAndStdIn(self):
        '''
        Divide newly created variables (to be passed in by the user) to parameter or standard input.
        '''
        parameters = []
        stdIn = []
        code = self.code
        strings = self.strings
        newVariables = self.newVariables
        for i in range(0,len(code)):
            parameters.append([])
            stdIn.append([])
            var = 0
            while var*2+1 < len(newVariables[i]):
                line = code[i][0][newVariables[i][var*2+1][0]][0].replace(" ","")
                line = line[line.find("=")+1:]
                if line[0]=='"' or line[:9]=="sys.arg[]":
                    if line[0] == '"':
                        parameters[i].append([newVariables[i][2*var],newVariables[i][2*var+1],"str",line[1:line.rfind('"')]])
                    else:
                        parameters[i].append([newVariables[i][2*var],newVariables[i][2*var+1],"str","\""+strings[int(line[line.find("sys.arg[]")+9:-1])-1]+"\""])
                elif Util().isNumber(line[0]):
                    if "." in line:
                        parameters[i].append([newVariables[i][2*var],newVariables[i][2*var+1],"float",line])
                    else:
                        parameters[i].append([newVariables[i][2*var],newVariables[i][2*var+1],"int",line])
                elif line == "True" or line == "False":
                    parameters[i].append([newVariables[i][2*var],newVariables[i][2*var+1],"bool",line])
                elif line[:5] == "date(":
                    parameters[i].append([newVariables[i][2*var],newVariables[i][2*var+1],"date",line])
                else:
                    fName = 0
                    while os.path.isfile("./" + self.dirPath + newVariables[i][2*var]+str(fName)):
                        fName+=1
                    with open(self.dirPath+'/'+newVariables[i][2*var]+str(fName)+".txt","w") as write:
                        write.write(line)
                    stdIn[i].append([newVariables[i][2*var],newVariables[i][2*var+1],newVariables[i][2*var]+str(fName)])
                var = var+1
                
        self.stdIn = stdIn
        self.parameters = parameters
            
    def insert(self):
        ''' 
        Add parameters, standard inputs and intermediates to the array <em>inputs</em> 
        and change the line of code with the variable accordingly.
        '''
        code = self.code
        stdIn = self.stdIn
        input = self.input
        output = self.output
        passedOnVariables = self.passedOnVariables
        parameters = self.parameters
        allVar = self.allVar
        toBeInserted = []
        toInsert=[]
        for i in range(0,len(code)):
            toBeInserted.append([])
            toInsert.append([])
            for j in range(0,len(stdIn[i])):
                input[i].append(['I'+Util().addZeros(len(input[i])+1)+stdIn[i][j][0],stdIn[i][j][2]])
                lineNum = stdIn[i][j][1][0]
                line = code[i][0][lineNum][0]
                numSpaces = line[:stdIn[i][j][1][1]]
                toBeInserted[i].append([lineNum,numSpaces + "with open(sys.argv["+str(len(input[i]))+"],\"r\") as r3920n5:"])
                code[i][0][lineNum][0]=numSpaces+"    "+stdIn[i][j][0]+" = eval(r3920n5.read())"
            for j in range(0,len(parameters[i])): #to class
                input[i].append(['P'+Util().addZeros(len(input[i])+1)+parameters[i][j][0],parameters[i][j][2],parameters[i][j][3]])
                lineNum = parameters[i][j][1][0]
                line = code[i][0][lineNum][0]
                if not parameters[i][j][2] == 'bool':
                    code[i][0][lineNum][0]=line[:parameters[i][j][1][1]]+parameters[i][j][0]+" ="+parameters[i][j][2]+"(sys.argv["+str(len(input[i]))+"])"
                else:
                    code[i][0][lineNum][0]=line[:parameters[i][j][1][1]]+parameters[i][j][0]+" =sys.argv["+str(len(input[i]))+"]=='true'"
            for j in range(0,int(len(passedOnVariables[i])/2)): #to class
                foundVar = False
                index = i-1
                while not foundVar:
                    if passedOnVariables[i][j*2] in allVar[index]:
                        foundVar = True
                    else:
                        index -=1
                if index >-1:
                    code[index][0].append(["with open(sys.argv[],\"w\") as w392075:",""])
                    code[index][0].append(["    try:",""])
                    code[index][0].append(["        w392075.write(str(type("+passedOnVariables[i][j*2]+"))+'\\n')",""])
                    code[index][0].append(["        w392075.write(str("+passedOnVariables[i][j*2]+"))",""])
                    code[index][0].append(["    except: pass",""])
                    outputVariable = "O"+Util().addZeros(len(output[index])+1)+passedOnVariables[i][j*2]
                    output[index].append([outputVariable,[len(code[index][0])-5,19]])
                    input[i].append(['V'+Util().addZeros(len(input[i])+1)+passedOnVariables[i][j*2],index,outputVariable])
                    p = passedOnVariables[i][2*j]
                    toInsert[i].append("    arr = r.read()\n    if arr[7:10]== 'int':\n        "+p+" = int(arr[arr.find('>')+1:])\n    elif arr[7:10] == 'str':\n        "+p+" = arr[arr.find('>')+1:]\n    elif arr[7:11] == 'bool':\n        if arr.replace(' ','')[-4:] == 'True':\n            "+p+" = True\n        else:\n            "+p+" = False\n    elif arr[7:12] == 'float':\n        "+p+" = float(arr[arr.find('>')+1:])\n    else:\n        "+p+" = eval(arr[arr.find('>')+1:])")
                    toInsert[i].append("with open(sys.argv["+str(len(input[i]))+"],\"r\") as r:")
                #if all var in get from 
            toBeInserted[i].sort(key = lambda inserted: inserted[0])
            for j in range(0,len(toBeInserted[i])):
                code[i][0].insert(toBeInserted[i][j][0]+j,[toBeInserted[i][j][1],""])
                for g in range(0,len(output[i])):
                    if output[i][g][1][0] >=toBeInserted[i][j][0]+j:
                        output[i][g][1][0]+=1
            for j in range(0,len(toInsert[i])):
                code[i][0].insert(0,[toInsert[i][j],""])
                for g in range(0,len(output[i])):
                        output[i][g][1][0]+=1
        self.index = index
    
    def insertMethods(self):
        '''
        @param code
        @param methods
        @param output
        @return output
        @return code
        @param code
        @param methods
        @param output
        @return code
        @return output
        
        Methods
        - Insert method in code cell if used in that particular code cell.
        '''
        code = self.code
        methods = self.methods
        output = self.output
        for i in range (0,len(code)):
            for m in range (0,len(methods)):
                l=0
                while l <len(code[i][0]):
                    if Util().inCode(methods[m][0],code[i][0][l][0]):
                        t = methods[m][1][0].split("\n")
                        for g in range(0,len(output[i])):
                            output[i][g][1][0] += len(t)
                        t2 = methods[m][1][1].split("\n")
                        for a in range(0,len(t)):
                            code[i][0].insert(0,[t[len(t)-a-1],t2[len(t)-a-1]])
                        l = len(code[i][0])+1
                    else:
                        l= l+1
    
    def figures(self):
        '''
        @param code
        @param output
        @param strings
        @param index
        @return code
        @return output
        
        Figures
        - If a call to save a figure, save it. 
        - If a figure and no save fig call in cell, save the last one.
        '''
        code = self.code
        output = self.output
        strings = self.strings
        index = self.index
        for i in range(0,len(code)):
            figSaved = False
            hasFig = False
            for j in range(0,len(code[i][0])):
                st = " " + code[i][0][j][0].replace(" ","")
                if "figure(" in st and not st[st.find("figure(")-1].isalpha() and not Util().isNumber(st[st.find("figure(")-1]):
                    hasFig = True
                elif "savefig(" in st and not st[st.find("savefig(")-1].isalpha() and not Util().isNumber(st[st.find("savefig(")-1]) and not "savefig()" in st:
                    hasFig = True
                    figSaved = True
                    line = code[i][0][j][0]
                    if "," in line[line.find("savefig("):]:
                        oV="O"+Util().addZeros(len(output[index])+1)+strings[int(line[line.find("savefig(")+17:line.find("savefig(")+                                                                         line[line.find("savefig("):].find(",")-1])-1]
                        code[i][0][j][0]=line[:line.find("savefig(")+8]+"sys.argv[]"+line[line[line.find("savefig("):].find(",")+line.find("savefig("):]
                    else:
                        oV="O"+Util().addZeros(len(output[index])+1)+strings[int(line[line.find("savefig(")+17:line.find("savefig(")+                                                                         line[line.find("savefig("):].find(")")-1])-1]
                        code[i][0][j][0]=line[:line.find("savefig(")+8]+"sys.argv[]"+line[line[line.find("savefig("):].find(")")                                                                                  +line.find("savefig("):]
                    output[i].append([oV,[j,line.find("savefig(")+17]])
                elif "savefig()" in st:
                    hasFig = True
                    figSaved = True
                    
            if hasFig and not figSaved:
                code[i][0].append(["try:savefig(sys.argv[])",""])
                output[i].append(["O"+Util().addZeros(len(output[i])+1)+"figure",[len(code[i][0]),21]])
                code[i][0].append(["except:pass",""])

    
    def addOtherStrings(self):
        '''
        @param code
        @param strings
        @return code
        
        Add other strings that are not new variables.
        '''
        code = self.code
        strings = self.strings
        stringNumber = 0
        index = 0
        for i in range(0,len(code)):
            for j in range(0,len(code[i][0])):
                while "sys.arg[]" in code[i][0][j][0][index:]:
                    line = code[i][0][j][0]
                    code[i][0][j][0] = line[:line.find("sys.arg[]")]+'"'+strings[int( line[line.find("sys.arg[]")+9:line[line.                                find("sys.arg[]"):].find("!")+line.find("sys.arg[]")])-1]+'"'+line[line[line.                                find("sys.arg[]"):].find("!")+1+line.find("sys.arg[]"):]
                    stringNumber+=1
    
    def addNumberArray(self):
        '''
        @param code
        @param input
        @param output
        @return code
        
        Add in the number inarray for sys.argv for outputs.
        '''
        code = self.code
        input = self.input
        output = self.output
        for i in range(0,len(code)):
            for j in range(0,len(output[i])):
                lineToChange = code[i][0][output[i][j][1][0]][0]
                code[i][0][output[i][j][1][0]][0] = lineToChange[:output[i][j][1][1]]+str(len(input[i])+j+1)+lineToChange[output[i][j][1][1]:]
        
    def printing(self):
        '''
        @param code
        @param output
        @param input
        @return code
        @return output
        
        Something becomes an output if it is printed.
        '''
        code = self.code
        output = self.output
        input = self.input
        for i in range (0,len(code)):
            j = 0
            while j < len(code[i][0]):
                if Util().isPrinting(code[i][0][j][0],i):
                    code[i][0].insert(0,["sys.stdout = open(sys.argv["+str(len(output)+1+len(input))+"], 'w')",""])
                    code[i][0].append(["sys.stdout.close()",""])
                    output[i].append(["O"+Util().addZeros(len(output[i])+1)+"stdOut",[i,j]])
                    j = len(code[i][0])
                else: 
                    j+=1
    
    def createNotebook(self):
        ''' 
        @param code
        @param imports
        @param doc
        @param c
        @return code
        
        Change method strings to normal.        
        - Create Workflow / new Notebook    
        - Place back into a new notebook (refer to http://nbconvert.readthedocs.io/en/latest/execute_api.html)
        - Combine each code cell into one big string.
        '''
        doc = self.documentation()
        imports = self.imports()
        code = self.code 
        c = [new_markdown_cell(doc)]
        for i in range(0,len(code)):
            code[i].append(imports)
            for j in range(0,len(code[i][0])):
                code[i][2] += code[i][0][j][0] + code[i][0][j][1]+"\n"
            code[i][2] = code[i][2][:len(code[i][2])-1]
            c.append(new_code_cell(code[i][2]))
        nb = nbf.v4.new_notebook()
        nb['cells'] = c

        # create new restructured notebook file
        with open(self.dirPath+'/' + self.workflowName + ".ipynb",'w') as w:
            nbf.write(nb,w)

    def createIoAndRun(self):
        '''
        @param code
        @param input
        @param output
        @return param
        @return runFiles
        
        Create io.sh file.
        '''
        code = self.code 
        input = self.input
        output = self.output
        param = []
        runFiles = []
        for i in range(0,len(code)):
            param.append([])
            j = 0
            while j < len(input[i]):
                if input[i][j][0][0] == "P" or input[i][j][0][0] == "Z":
                    param[i].append(input[i][j])
                    del input[i][j]
                else: j +=1
            run = '#!/bin/bash\n\ncheckExitCode() {\n if [ $? -ne 0 ]; then \n     echo "Error"\n     exit 1; \n fi\n}\n\nBASEDIR=`dirname $0`\n. $BASEDIR/io.sh '
            run += str(len(input[i]))+" "+str(len(param[i]))+" "+str(len(output[i]))+' "$@"\n\n'
            for j in range(0,len(input[i])):
                run +='echo "Input'+str(j+1)+': $INPUTS'+str(j+1)+'"\n'
            for j in range(0,len(param[i])):
                run +='echo "Param'+str(j+1)+': $PARAMS'+str(j+1)+'"\n'
            for j in range(0,len(output[i])):
                del output[i][j][1]
                run +='echo "Output'+str(j+1)+': $OUTPUTS'+str(j+1)+'"\n'
            run += '\n\n$BASEDIR/Component'+str(i+1)+'.py'
            for j in range(0,len(input[i])):
                run += ' $INPUTS'+str(j+1)
            for j in range(0,len(param[i])):
                run += ' $PARAMS'+str(j+1)
            for j in range(0,len(output[i])):
                run += ' $OUTPUTS'+str(j+1)
            run += '\ncheckExitCode'
            runFiles.append(run)
        
        self.runFiles = runFiles
        self.param = param
            
        with open(self.dirPath+"/io.sh","w") as io:
            io.write('#!/bin/bash\n\n# -----------------------------------------------\n# Option Parsing function for:\n# -i<1..n> [files.. ] -o<1..n> [files.. ]\n# \n# **** IMPORTANT ****\n# - Please pass 2 Arguments to this script\n#   - Arg1: Number of Input Data expected\n#   - Arg1: Number of Input Parameters expected\n#   - Arg2: Number of Output Data expected\n#\n# (c) Varun Ratnakar\n# -----------------------------------------------\n\nINUM=$1; shift\nPNUM=$1; shift\nONUM=$1; shift\n\nset_variables()\n{\n    for ((i=1; i<=INUM; i++)); do typeset ICOUNT$i=0; done\n    for ((i=1; i<=PNUM; i++)); do typeset PCOUNT$i=0; done\n    for ((i=1; i<=ONUM; i++)); do typeset OCOUNT$i=0; done\n}\n\nIFLAG=();\nPFLAG=();\nOFLAG=();\nreset_flags()\n{\n    for ((j=1; j<=INUM; j++)); do IFLAG[$j]=\'0\'; done\n    for ((k=1; k<=PNUM; k++)); do PFLAG[$k]=\'0\'; done\n    for ((l=1; l<=ONUM; l++)); do OFLAG[$l]=\'0\'; done\n}\n\nset_variables\nreset_flags\n\nwhile [ $# -gt 0 ]\ndo\n    case "$1" in\n        -i*) in=$(echo $1 | cut -di -f2); reset_flags; IFLAG[$in]=\'1\';;\n        -p*) ip=$(echo $1 | cut -dp -f2); reset_flags; PFLAG[$ip]=\'1\';;\n        -o*) op=$(echo $1 | cut -do -f2); reset_flags; OFLAG[$op]=\'1\';;\n        --) shift; break;;\n        -*)\n            echo >&2 \\\n            "usage: $0 -i<1..$INUM> [files.. ] -o<1..$ONUM> [files.. ]"\n            exit 1;;\n        *)  for((ind=1; ind<=INUM; ind++)); do\n                if [ "${IFLAG[$ind]}" = "1" ] \n                then \n                    x=""\n                    if [ "${INPUTS[$ind]}" != "" ]; then x="|"; fi\n                    INPUTS[$ind]="${INPUTS[$ind]}$x$1"\n                fi\n            done\n            for((ind=1; ind<=PNUM; ind++)); do\n                if [ "${PFLAG[$ind]}" = "1" ] \n                then \n                    x=""\n                    if [ "${PARAMS[$ind]}" != "" ]; then x="|"; fi\n                    PARAMS[$ind]="${PARAMS[$ind]}$x$1"\n                fi\n            done\n            for((ind=1; ind<=ONUM; ind++)); do\n                if [ "${OFLAG[$ind]}" = "1" ] \n                then \n                    x=""\n                    if [ "${OUTPUTS[$ind]}" != "" ]; then x="|"; fi\n                    OUTPUTS[$ind]="${OUTPUTS[$ind]}$x$1"\n                fi\n            done;;\n    esac\n    shift\ndone\n\nIFS=\'|\'\nfor ((i=1; i<=INUM; i++)); do typeset INPUTS$i=$(echo ${INPUTS[$i]}); done\nfor ((i=1; i<=PNUM; i++)); do typeset PARAMS$i=$(echo ${PARAMS[$i]}); done\nfor ((i=1; i<=ONUM; i++)); do typeset OUTPUTS$i=$(echo ${OUTPUTS[$i]}); done\nIFS=\' \'')

    def inputs(self):
        '''
        @param input
        @param code
        @return input
        
        TODO: Description
        '''
        input = self.input
        code = self.code
        for i in range(0,len(code)):
            for j in range(0,len(input[i])):
                k = 0
                while k < len(input[i][j][0]):
                    if not input[i][j][0][k].isalpha() and not Util().isNumber(input[i][j][0][k]) and not input[i][j][0][k] == ".":
                        input[i][j][0]=input[i][j][0][:k] + input[i][j][0][k+1:]
                    else: 
                        k +=1

    def createZipFile(self):
        '''
        @param code
        @param runFiles
        
        Create run and component zip files.
        '''
        code = self.code
        runFiles = self.runFiles
        for i in range(0,len(code)):
            with open (self.dirPath+'/run','w') as runf:
                runf.write(runFiles[i])
            with open(self.dirPath+'/Component'+str(i+1)+'.py',"w") as codef:
                codef.write(code[i][2])
            zipf = zipfile.ZipFile(self.dirPath+'/Component'+str(i+1)+'.zip', 'w', zipfile.ZIP_DEFLATED)
            zipf.write(self.dirPath+'/io.sh')
            zipf.write(self.dirPath+'/run') 
            zipf.write(self.dirPath+'/Component'+str(i+1)+'.py')
            zipf.close()
            #remove unnecessary files
            os.remove(self.dirPath+'/Component'+str(i+1)+'.py')
        #remove unnecessary files
        os.remove(self.dirPath+'/io.sh')
        os.remove(self.dirPath+'/run')

    def createMetadata(self):
        '''
        @param input
        @param output
        @param param
        
        Create file with workflow inputs, outputs and parameters.
        '''
        input = self.input
        output = self.output
        param = self.param
        # Create inputs metadata files.
        with open(self.dirPath+'/inputs.txt',"w") as w:
            w.write(str(input))
                
        # Params metadata files.        
        with open(self.dirPath+"/params.txt","w") as w:
            w.write(str(param))
                
        # Outputs metadata files.            
        out=[]
        for i in range(0,len(output)):
            out.append([])
            for j in range(0,len(output[i])):
                out[i].append(output[i][j][0])
                
        with open(self.dirPath+'/outputs.txt',"w") as w:
            w.write(str(out))
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "example/Disease+Analysis.ipynb"
        
    mfp = NiW()
    mfp.setNotebook(file_path)
    files = mfp.preProcessing()
    mfp.comments()
    mfp.newLines()
    mfp.cleaningUp()
    mfp.imports()
    mfp.magicCommands()
    mfp.organizeMethods()
    mfp.checkOpenFiles()
    mfp.cleanAndMerge()
    mfp.inputsAndOuputs(files)
    mfp.documentation()
    #mfp.findAllVariables()
    mfp.variables()
    mfp.splitVariables()
    mfp.divideVariablesInParametersAndStdIn()
    mfp.insert()
    mfp.insertMethods()
    mfp.figures()
    mfp.addOtherStrings()
    mfp.addNumberArray()
    mfp.printing()
    mfp.createNotebook()
    mfp.createIoAndRun()
    mfp.inputs()
    mfp.createZipFile()
    mfp.createMetadata()