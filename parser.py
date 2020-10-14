import os
import sys
import subprocess
import json
import re
import regex
import platform
import multiprocessing
import get_cpu_count
from hashlib import md5
import time
import textwrap

global javaCallCommand

class function:
    parentFile = None  # Absolute file which has the function
    parentNumLoc = None  # Number of LoC of the parent file
    name = None  # Name of the function
    lines = None  # Tuple (lineFrom, lineTo) that indicates the LoC of function
    funcId = None  # n, indicating n-th function in the file
    parameterList = []  # list of parameter variables
    variableList = []  # list of local variables
    dataTypeList = []  # list of data types, including user-defined types
    funcCalleeList = []  # list of called functions' names
    primaryList = [] # List of all the identifiers
    funcBody = None

    def __init__(self, fileName):
        self.parentFile = fileName
        self.parameterList = []
        self.variableList = []
        self.dataTypeList = []
        self.funcCalleeList = []

    def removeListDup(self):
        # for best performance, must execute this method
        # for every instance before applying the abstraction.
        self.parameterList = list(set(self.parameterList))
        self.variableList = list(set(self.variableList))
        self.dataTypeList = list(set(self.dataTypeList))
        self.funcCalleeList = list(set(self.funcCalleeList))

def normalize(string):
    # Code for normalizing the input string.
    # LF and TAB literals, curly braces, and spaces are removed,
    # and all characters are lowercased.
    return ''.join(string.replace('\n', '').replace('\r', '').replace('\t', '').replace('{', '').replace('}', '').split(' ')).lower()

def removeComment(string, language):
    # Code for removing comments
    c_regex = re.compile(r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)',
        re.DOTALL | re.MULTILINE)
    python_regex = re.compile(r"(?m)^ *#.*\n?|(\"\"\"([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\"\"\")")
    if language == "c" or language == "java" or language == "go" or language == "javascript" or language == "js":
        return ''.join([c.group('noncomment') for c in c_regex.finditer(string) if c.group('noncomment')])
    elif language == "python":
        return python_regex.sub("", string)

def new_abstract(instance, level, language):
    # Applies abstraction on the function instance,
    # and then returns a tuple consisting of the original body and abstracted
    # body.
    originalFunctionBody = instance.funcBody
    print(originalFunctionBody)
    originalFunctionBody = removeComment(originalFunctionBody, language)
    print("REMOVED COMMENTS")
    print(originalFunctionBody)
    abstractBody = originalFunctionBody

    if int(level) >= 0:  # No abstraction.
        abstractBody = originalFunctionBody

    if int(level) >= 1:  # PARAM
        parameterList = instance.parameterList
        for param in parameterList:
            if len(param) == 0:
                continue
            try:
                paramPattern = re.compile("(?!.*\")(^|\(|\s)" + str(param)+ "(\W)(?!.*\")")
                print("Parameters: " + str(paramPattern.search(abstractBody)))
                abstractBody = paramPattern.sub(r"\g<1>FPARAM\g<2>", abstractBody)
            except:
                pass

    if int(level) >= 2:  # DTYPE
        dataTypeList = instance.dataTypeList
        for dtype in dataTypeList:
            print(dtype)
            if len(dtype) == 0:
                continue
            try:
                dtypePattern = re.compile("(?!.*\")(^|\(|\s)" + str(dtype)+ "(\W)(?!.*\")")
                print("Data types: " + str(dtypePattern.search(abstractBody)))
                abstractBody = dtypePattern.sub(r"\g<1>DTYPE\g<2>", abstractBody)
            except:
                pass

    if int(level) >= 3:  # LVAR
        variableList = instance.variableList
        for lvar in variableList:
            if len(lvar) == 0:
                continue
            try:
                lvarPattern = re.compile("(?!.*\")(^|\(|\s)" + str(lvar)+ "(\W)(?!.*\")")
                print("Variables: " + str(lvarPattern.search(abstractBody)))
                abstractBody = lvarPattern.sub(r"\g<1>LVAR\g<2>", abstractBody)
            except:
                pass


    return (originalFunctionBody, abstractBody)


#Original shallow C\C++ code parser using Antlr
def parse_shallow(files):
    javaCallCommand = "java -Xmx1024m -jar FuncParser-opt.jar " + files + " 1"
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    # this parses function definition plus body.
    functionInstanceList = []

    try:
        astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    funcList = astString.split(delimiter)
    for func in funcList[1:]:
        functionInstance = function(files)

        elemsList = func.split('\n')[1:-1]
        # print elemsList
        if len(elemsList) > 9:
            functionInstance.parentNumLoc = int(elemsList[1])
            functionInstance.name = elemsList[2]
            functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
            functionInstance.funcId = int(elemsList[4])
            functionInstance.funcBody = '\n'.join(elemsList[9:])
            functionInstanceList.append(functionInstance)

    return functionInstanceList

#Original deep C/C++ code parser using Antlr
def parse_deep(files):
    javaCallCommand = "java -Xmx1024m -jar FuncParser-opt.jar " + files + " 1"
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    # this parses function definition plus body.
    functionInstanceList = []

    try:
        astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    funcList = astString.split(delimiter)
    for func in funcList[1:]:
        functionInstance = function(files)

        elemsList = func.split('\n')[1:-1]
        # print elemsList
        if len(elemsList) > 9:
            functionInstance.parentNumLoc = int(elemsList[1])
            functionInstance.name = elemsList[2]
            functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
            functionInstance.funcId = int(elemsList[4])
            functionInstance.parameterList = elemsList[5].rstrip().split('\t')
            functionInstance.variableList = elemsList[6].rstrip().split('\t')
            functionInstance.dataTypeList = elemsList[7].rstrip().split('\t')
            functionInstance.funcCalleeList = elemsList[8].rstrip().split('\t')
            functionInstance.funcBody = '\n'.join(elemsList[9:])
            print(functionInstance.funcBody)
            print("funccalls: " + str(functionInstance.funcCalleeList))
            print("variables: " + str(functionInstance.variableList))
            print("parameters: " + str(functionInstance.parameterList))
            print("data types: " + str(functionInstance.dataTypeList))
            functionInstanceList.append(functionInstance)

    return functionInstanceList

#Shallow JAVA code parser using Universal-Ctags
def parse_java_shallow(file):
    Command = "ctags -f - --kinds-java=* --fields=neK " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    methodList = astString.split('\n')
    method = re.compile(r'(method)')
    number = re.compile(r'(\d+)')
    funcBody = re.compile(r'{([\S\s]*)}')
    string = ""
    funcId = 1
    methodInstanceList = []

    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        methodInstance = function(file)
        methodInstance.funcBody = ''

        if i != '' and method.match(elemList[3]) and len(elemList) >= 6:
            methodInstance.name = elemList[0]
            methodInstance.parentFile = elemList[1]
            methodInstance.lines = (int(number.search(elemList[4]).group(0)),
                                    int(number.search(elemList[5]).group(0)))
            methodInstance.parentNumLoc = len(lines)
            string = ""
            string = string.join(lines[methodInstance.lines[0]-1:methodInstance.lines[1]])
            if funcBody.search(string):
                methodInstance.funcBody = methodInstance.funcBody + funcBody.search(string).group(1)
            else:
                methodInstance.funcBody = " "
            methodInstance.funcId = funcId
            funcId+=1
            methodInstanceList.append(methodInstance)
    return methodInstanceList

#Deep JAVA code parser using Universal-Ctags
def parse_java_deep(file):
    Command = "ctags -f - --kinds-java=* --fields=neKS " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    methodList = astString.split('\n')
    local = re.compile(r'local')
    method = re.compile(r'(method)')
    parameterSpace = re.compile(r'\(\s*([^)]+?)\s*\)')
    word = re.compile(r'\w+')
#    dataType = re.compile()
    number = re.compile(r'(\d+)')
    funcBody = re.compile(r'{([\S\s]*)}')
    string = ""
    funcId = 1
    methodInstanceList = []
    variables = []
    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        if i != '' and local.match(elemList[3]) and len(elemList) >= 6:
            variables.append(elemList)
    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        methodInstance = function(file)
        methodInstance.funcBody = ''
        if i != '' and method.match(elemList[3]) and len(elemList) >= 6:
            #Parameters and data types
            if (parameterSpace.search(elemList[5])):
                for i in parameterSpace.search(elemList[5])[1].split(", "):
                    methodInstance.parameterList.append(word.findall(i)[1])
                    methodInstance.dataTypeList.append(word.findall(i)[0])
            #Method body
            methodInstance.name = elemList[0]
            methodInstance.parentFile = elemList[1]
            methodInstance.lines = (int(number.search(elemList[4]).group(0)),
                                    int(number.search(elemList[6]).group(0)))
            methodInstance.parentNumLoc = len(lines)
            string = ""
            string = string.join(lines[methodInstance.lines[0]-1:methodInstance.lines[1]])
            if funcBody.search(string):
                methodInstance.funcBody = methodInstance.funcBody + funcBody.search(string).group(1)
            else:
                methodInstance.funcBody = " "
            #Variables
            for var in variables:
                if methodInstance.lines[0] <= int((number.search(var[4]).group(0))) <= methodInstance.lines[1]:
                    varDtype = re.compile(r'\w+(?=\s+' + str(var[0]) + ')')
                    methodInstance.dataTypeList.append(varDtype.search(var[2]).group(0))
                    methodInstance.variableList.append(var[0])
            methodInstance.funcId = funcId
            funcId+=1
            print(methodInstance.funcBody)
            print("Variables: " + str(methodInstance.variableList))
            print("Parameters: " + str(methodInstance.parameterList))
            print("Data types: " + str(methodInstance.dataTypeList))
            methodInstanceList.append(methodInstance)
    return methodInstanceList

#Shallow PYTHON code parser using Universal-Ctags
def parse_python_shallow(file):
    Command = "ctags -f - --kinds-python=* --fields=neK " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    methodList = astString.split('\n')
    member = re.compile(r'(member)')
    func = re.compile(r'(function)')
    number = re.compile(r'(\d+)')
    methodInstanceList = []

    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        methodInstance = function(file)
        methodInstance.funcBody = ''
        if i != '' and (member.match(elemList[3]) or func.match(elemList[3])):
            methodInstance.name = elemList[0]
            methodInstance.parentFile = elemList[1]
            methodInstance.lines = (int(number.search(elemList[4]).group(0)),
                                    int(number.search(elemList[5]).group(0)))
            methodInstance.parentNumLoc = len(lines)
            for line in range(methodInstance.lines[0], methodInstance.lines[1]):
                methodInstance.funcBody = methodInstance.funcBody + (lines[line])
            methodInstanceList.append(methodInstance)

    return methodInstanceList

#Deep PYTHON code parser using Universal-Ctags
def parse_python_deep(file):
    Command = "ctags -f - --kinds-python=* --fields=neK " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    methodList = astString.split('\n')
    member = re.compile(r'(member)')
    func = re.compile(r'(function)')
    local = re.compile(r'(local)')
    parameter = re.compile(r'(parameter)')
    number = re.compile(r'\d+')
    methodInstanceList = []
    variables = []
    parameters = []
    funcId = 1

    #Variables list
    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        if i != '' and local.match(elemList[3]):
            variables.append(elemList)

    #Parameters list
    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        if i != '' and elemList[0] != 'self' and parameter.match(elemList[3]):
            parameters.append(elemList)

    #Function
    for i in methodList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        methodInstance = function(file)
        methodInstance.funcBody = ''
        if i != '' and (member.match(elemList[3]) or func.match(elemList[3])) and len(elemList) >= 6:
            methodInstance.name = elemList[0]
            methodInstance.parentFile = elemList[1]
            methodInstance.lines = (int(number.search(elemList[4]).group(0)),
                                    int(number.search(elemList[5]).group(0)))
            methodInstance.parentNumLoc = len(lines)
            for line in range(methodInstance.lines[0], methodInstance.lines[1]):
                methodInstance.funcBody = methodInstance.funcBody + (lines[line])
            methodInstance.funcId = funcId
            funcId += 1
            #Variables
            for var in variables:
                if methodInstance.lines[0] <= int(number.search(var[4]).group(0)) <= methodInstance.lines[1]:
                    methodInstance.variableList.append(var[0])
                    #Parameters
            for param in parameters:
                if methodInstance.lines[0] <= int(number.search(param[4]).group(0)) <= methodInstance.lines[1]:
                    methodInstance.parameterList.append(param[0])

            methodInstanceList.append(methodInstance)

            print(methodInstance.funcBody)
            print("Variables: " + str(methodInstance.variableList))
            print("Parameters: " + str(methodInstance.parameterList))
    return methodInstanceList


#Shallow GO code parser using Universal-Ctags
def parse_go_shallow(file):
    Command = "ctags -f - --kinds-go=* --fields=neK " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    functionInstanceList = []

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    functionList = astString.split('\n')
    func = re.compile(r'(func)')
    number = re.compile(r'(\d+)')
    funcBody = re.compile(r'{([\S\s]*)}')
    string = " "
    funcId = 1

    for i in functionList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        functionInstance = function(file)
        functionInstance.funcBody = ''
        if i != '' and func.fullmatch(elemList[3]) and len(elemList) >= 6:
            functionInstance.name = elemList[0]
            functionInstance.parentFile = elemList[1]
            functionInstance.parentNumLoc = len(lines)
            functionInstance.lines = (int(number.search(elemList[4]).group(0)),
                                    int(number.search(elemList[5]).group(0)))
            string = " "
            if len(lines)-1 >= functionInstance.lines[0]:
                if func.search(lines[functionInstance.lines[0]]):
                    string = string.join(lines[functionInstance.lines[0]:functionInstance.lines[1]])
            if func.search(lines[functionInstance.lines[0]-1]):
                string = string.join(lines[functionInstance.lines[0]-1:functionInstance.lines[1]])
            elif func.search(lines[functionInstance.lines[0]-2]):
                string = string.join(lines[functionInstance.lines[0]-2:functionInstance.lines[1]])
            print(string)
            if funcBody.search(string):
                functionInstance.funcBody = functionInstance.funcBody + funcBody.search(string).group(1)
            else:
                functionInstance.funcBody = " "
            print("FUNCTION BODY")
            print(functionInstance.funcBody)
            functionInstance.funcId = funcId
            funcId += 1
            functionInstanceList.append(functionInstance)

    return functionInstanceList

#Deep GO code parser using Universal-Ctags
def parse_go_deep(file):
    Command = "ctags -f - --kinds-go=* --fields=neKSt " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    functionInstanceList = []

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    functionList = astString.split('\n')
    varRe = re.compile(r'(var)')
    dataType = re.compile(r'')
    func = re.compile(r'(func)')
    number = re.compile(r'(\d+)')
    funcBody = re.compile(r'{([\S\s]*)}')
    string = " "
    funcId = 1
    for i in functionList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        functionInstance = function(file)
        functionInstance.funcBody = ''
        if i != '' and (func.fullmatch(elemList[3]) or func.fullmatch(elemList[4])) and len(elemList) >= 6:
            functionInstance.name = elemList[0]
            functionInstance.parentFile = elemList[1]
            functionInstance.parentNumLoc = len(lines)
            functionInstance.lines = (int(number.search(elemList[4]).group(0)),
                                      int(number.search(elemList[7]).group(0)))
            string = " "

            if func.search(lines[functionInstance.lines[0]]):
                string = string.join(lines[functionInstance.lines[0]:functionInstance.lines[1]])
            elif func.search(lines[functionInstance.lines[0]-1]):
                string = string.join(lines[functionInstance.lines[0]-1:functionInstance.lines[1]])
            elif func.search(lines[functionInstance.lines[0]-2]):
                string = string.join(lines[functionInstance.lines[0]-2:functionInstance.lines[1]])
            print("STRING")
            print(string)
            if funcBody.search(string):
                functionInstance.funcBody = functionInstance.funcBody + funcBody.search(string).group(1)
            else:
                functionInstance.funcBody = " "
            print("FUNCTION BODY")
            functionInstance.funcId = func
            funcId += 1
            #Data types
            elemList[5] = re.sub("(typeref:typename:)", "", elemList[5])
            if re.search(r'\(\s*([^)]+?)\s*\)', elemList[5]):
                for dType in re.search(r'\(\s*([^)]+?)\s*\)', elemList[5])[1].split(", "):
                    functionInstance.dataTypeList.append(re.search("\S+$", dType).group(0))
                    dType = re.sub("\S+$", "", dType)
                    if dType:
                        functionInstance.variableList.append(re.search("\S+", dType).group(0))
            elif re.match(r'^\S+$', elemList[5]):
                functionInstance.dataTypeList.append(re.match(r'^\S+$', elemList[5]).group(0))

            parameter = re.compile(r"^(\S+)")
            parameterSpace = []
            #Parameters
            elemList[6] = re.sub("(signature:)", "", elemList[6])
            if re.search(r'\(\s*([^)]+?)\s*\)', elemList[6]):
                parameterSpace = re.search(r'\(\s*([^)]+?)\s*\)', elemList[6])[1].split(", ")
                for elem in parameterSpace:
                    elem = re.sub("(,)", "", elem)
                    functionInstance.parameterList.append(parameter.search(elem).group(0))
                    elem = re.sub(parameter, "", elem)
                    if re.search("\S+", elem):
                        functionInstance.dataTypeList.append(re.search("\S+", elem).group(0))

            #Variables
            filee = open("function.go", "w+")
            filee.write(functionInstance.funcBody)
            filee.close()
            Command1 = "ctags -f - --kinds-go=* --fields=neKS function.go"
            shellOutput = subprocess.check_output(Command1, stderr=subprocess.STDOUT, shell=True).decode()
            varList = []
            varList = shellOutput.split('\n')
            for var in varList:
                elemsList = re.sub(r'[\t\s ]{2,}', '', var)
                elemsList = elemsList.split("\t")
                if var != '' and (varRe.match(elemsList[3]) or varRe.match(elemsList[4])):
                    functionInstance.variableList.append(elemsList[0])
                    print("//// " +str(elemsList))
            print(functionInstance.funcBody)
            print("Parameters: " + str(functionInstance.parameterList))
            print("Variables: " + str(functionInstance.variableList))
            print("Data types: " + str(functionInstance.dataTypeList))
            functionInstanceList.append(functionInstance)

    return functionInstanceList

#Shallow JavaScript code parser using Universal-Ctags
def parse_js_shallow(file):
    Command = "ctags -f - --kinds-javascript=* --fields=neK " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    functionInstanceList = []

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    functionList = astString.split('\n')
    func = re.compile(r'(function)')
    method = re.compile(r'(method)')
    number = re.compile(r'(\d+)')
    new_line = re.compile(r'(\n)')

    string = " "
    funcId = 1
    lines_count = 0

    for i in functionList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        functionInstance = function(file)
        functionInstance.funcBody = ''
        if i != '' and len(elemList) >= 5 and (func.fullmatch(elemList[3]) or method.fullmatch(elemList[3])):
            functionInstance.name = elemList[0]
            functionInstance.parentFile = elemList[1]
            functionInstance.parentNumLoc = len(lines)
            string = " "
            string = string.join(lines[int(number.search(elemList[4]).group(0))-1:])
            funcString = ""
            ctr = 0
            flag = 0
            for c in string:
                if c == "{":
                    ctr = ctr + 1
                    flag = 1
                elif c == "}":
                    ctr = ctr - 1
                if ctr == 0 and flag == 1:
                    break
                elif ctr != 0 and flag == 1 and c != "{" and c != "}":
                    funcString = funcString + c

            functionInstance.funcBody = functionInstance.funcBody + funcString
            functionInstance.lines = (int(number.search(elemList[4]).group(0)),
                                      int(number.search(elemList[4]).group(0)) + functionInstance.funcBody.count("\n"))
            functionInstance.funcId = funcId
            funcId += 1
            functionInstanceList.append(functionInstance)

    return functionInstanceList

#Shallow JavaScript code parser using Universal-Ctags
def parse_js_deep(file):
    Command = "ctags -f - --kinds-javascript=* --fields=neKS " + file
    global delimiter
    delimiter = "\r\0?\r?\0\r"
    functionInstanceList = []

    try:
        astString = subprocess.check_output(Command, stderr=subprocess.STDOUT, shell=True).decode()

    except subprocess.CalledProcessError as e:
        print("Parser Error:", e)
        astString = ""

    f = open(file, 'r')
    lines = f.readlines()
    functionList = astString.split('\n')
    func = re.compile(r'(function)')
    varRe = re.compile(r'(var)')
    parameter = re.compile(r'\(\s*([^)]+?)\s*\)')
    variableRe = re.compile(r'(variable)')
    method = re.compile(r'(method)')
    number = re.compile(r'(\d+)')
    new_line = re.compile(r'(\n)')

    string = " "
    funcId = 1
    lines_count = 0
    for i in functionList:
        elemList = re.sub(r'[\t\s ]{2,}', '', i)
        elemList = elemList.split("\t")
        functionInstance = function(file)
        functionInstance.funcBody = ''
        if i != '' and len(elemList) >= 5 and (func.fullmatch(elemList[3]) or method.fullmatch(elemList[3])):
            #Parameters
            if parameter.search(elemList[5]):
                functionInstance.parameterList.append(parameter.search(elemList[5]).group(1))
            functionInstance.name = elemList[0]
            functionInstance.parentFile = elemList[1]
            functionInstance.parentNumLoc = len(lines)
            string = " "
            string = string.join(lines[int(number.search(elemList[4]).group(0))-1:])
            funcString = ""
            ctr = 0
            flag = 0
            for c in string:
                if c == "{":
                    ctr = ctr + 1
                    flag = 1
                elif c == "}":
                    ctr = ctr - 1
                if ctr == 0 and flag == 1:
                    break
                elif ctr != 0 and flag == 1 and c != "{" and c != "}":
                    funcString = funcString + c
            functionInstance.funcBody = functionInstance.funcBody + funcString
            functionInstance.lines = (int(number.search(elemList[4]).group(0)),
                                      int(number.search(elemList[4]).group(0)) + functionInstance.funcBody.count("\n"))
            functionInstance.funcId = funcId
            funcId += 1

            #Variables
            filee = open("function.js", "w+")
            filee.write(functionInstance.funcBody)
            filee.close()
            Command1 = "ctags -f - --kinds-javascript=* --fields=neKS function.js"
            shellOutput = subprocess.check_output(Command1, stderr=subprocess.STDOUT, shell=True).decode()
            varList = []
            varList = shellOutput.split('\n')
            for var in varList:
                elemsList = re.sub(r'[\t\s ]{2,}', '', var)
                elemsList = elemsList.split("\t")
                if var != '' and (varRe.fullmatch(elemsList[3]) or variableRe.fullmatch(elemsList[3])):
                    functionInstance.variableList.append(elemsList[0])
            functionInstanceList.append(functionInstance)
    return functionInstanceList


def loadSource(rootDirectory):
    # returns the list of .src files under the specified root directory.
    maxFileSizeInBytes = None
    maxFileSizeInBytes = 2 * 1024 * 1024  # remove this line if you don't want to restrict
    # the maximum file size that you process.
    walkList = os.walk(rootDirectory)
    srcFileList = []
    for path, dirs, files in walkList:
        for fileName in files:
            ext = fileName.lower()
            if ext.endswith('.c') or ext.endswith('.cpp') or ext.endswith('.cc') or ext.endswith('.c++') or ext.endswith('.cxx') or ext.endswith('.java') or ext.endswith('.py') or ext.endswith('.go') or ext.endswith('.js'):
                absPathWithFileName = path.replace('\\', '/') + '/' + fileName
                if os.path.getsize(absPathWithFileName) < maxFileSizeInBytes:
                    if maxFileSizeInBytes is not None:
                        srcFileList.append(absPathWithFileName)
                    else:
                        srcFileList.append(absPathWithFileName)
    return srcFileList

#old
def parseFile_deep_multi(f):
    functionInstanceList = parse_deep(f)
    return (f, functionInstanceList)
def parseFile_shallow_multi(f):
    functionInstanceList = parse_shallow(f)
    return (f, functionInstanceList)


#new
def parseFile_java_shallow(f):
    methodInstanceList = parse_java_shallow(f)
    return (f, methodInstanceList)

def parseFile_java_deep(f):
    methodInstanceList = parse_java_deep(f)
    return (f, methodInstanceList)

def parseFile_python_shallow(f):
    methodInstanceList = parse_python_shallow(f)
    return (f, methodInstanceList)

def parseFile_python_deep(f):
    methodInstanceList = parse_python_deep(f)
    return (f, methodInstanceList)

def parseFile_go_shallow(f):
    functionInstanceList = parse_go_shallow(f)
    return (f, functionInstanceList)

def parseFile_go_deep(f):
    functionInstanceList = parse_go_deep(f)
    return (f, functionInstanceList)

def parseFile_js_shallow(f):
    functionInstanceList = parse_js_shallow(f)
    return (f, functionInstanceList)

def parseFile_js_deep(f):
    functionInstanceList = parse_js_deep(f)
    return (f, functionInstanceList)

#for i in parse_go_deep("testcode1/system.go"):
#    orig, abst = new_abstract(i, 4, 'go')
#    print("______________________")
#    print(orig)
#    print("######################")
#    print(abst)
#    print("______________________")
#parse_python_deep("hmark.py")
#parse_go_deep("testcode1/system.go")
#parse_js_deep("testcode1/nginx-conf-master/src/conf.js")
#parse_go_deep("testcode1/system.go")


#start = time.time()
#parse_c_deep("testcode/trace.c")
for i in parse_js_deep("testcode1/nginx-conf-master/src/conf.js"):
    print("FUNC BODY")
    print(i.funcBody)
    print("ORIGINALIS")
    orig, abst = new_abstract(i, 4, 'js')
    print("ORIGINAL")
    print(orig)
    print("ABSTRACT")
    print(abst)
#end = time.time()
#print(end - start)
#start = time.time()
#end = time.time()
#print(end - start)
#parse_java_deep("testcode/sample_java/javatest/sample1.java")
#parse_python_deep("hmark.py")
#parse_java_deep("testcode/spring-framework-master")
#fileList = loadSource("testcode/react-master")
#directory = "testcode/react-master"
#cpu_count = get_cpu_count.get_cpu_count()
#if cpu_count != 1:
#    cpu_count -= 1
#fileList = loadSource("testcode1/nginx-conf-master")
#directory = "testcode1"
#numFunc = 0
#projDic = {}
#hashFileMap = {}
#proj = directory.replace('\\', '/').split('/')[-1]

#pool = multiprocessing.Pool(processes=cpu_count)

#start = time.time()
#count = 0
#for idx, tup in enumerate(pool.imap_unordered(parse_js_shallow, fileList)):
#    print(tup)
#    count+=1
#    f = tup[0]
#    methodInstanceList = tup[1]
##    numFunc += len(methodInstanceList)
#end = time.time()
#print(end - start)
#    for f in methodInstanceList:
##        origBody, absBody = abstract(f, 0)

#        absBody = normalize(absBody)
#        funcLen = len(absBody)
#        if funcLen > 50:
#            hashValue = md5(absBody.encode('utf-8')).hexdigest()
#
#            try:
#                projDic[funcLen].append(hashValue)
#            except KeyError:
#                projDic[funcLen] = [hashValue]
#            try:
#                hashFileMap[hashValue].extend([pathOnly, f.funcId])
#            except KeyError:
#                hashFileMap[hashValue] = [pathOnly, f.funcId]
#        else:
#            numFunc -= 1  # decrement numFunc by 1 if funclen is under threshold


################################################################################
#cpu_count = get_cpu_count.get_cpu_count()
#if cpu_count != 1:
#    cpu_count -= 1
#
#fileList = loadSource("testcode1")
#directory = "testcode1"
#numFunc = 0
#absLevel = 4
#projDic = {}
#hashFileMap = {}
#proj = directory.replace('\\', '/').split('/')[-1]
#
#pool = multiprocessing.Pool(processes=cpu_count)
#for idx, tup in enumerate(pool.imap_unordered(parseFile_sha_multi, fileList)):
#    f = tup[0]
#
#    functionInstanceList = tup[1]
#    pathOnly = f.split(proj, 1)[1][1:]
#    numFunc += len(functionInstanceList)
#    for f in functionInstanceList:
#        f.removeListDup()
#        path = f.parentFile
#        origBody, absBody = abstract(f, absLevel)
#        print(origBody)
#        print("**********************************")
#        print(absBody)
#        print("**********************************")
#        absBody = normalize(absBody)
#        print(absBody)
#        funcLen = len(absBody)
#
#        if funcLen > 50:
#            hashValue = md5(absBody.encode('utf-8')).hexdigest()
#            print(hashValue)
#
#            try:
#                projDic[funcLen].append(hashValue)
#            except KeyError:
#                projDic[funcLen] = [hashValue]
#            try:
#                hashFileMap[hashValue].extend([pathOnly, f.funcId])
#            except KeyError:
#                hashFileMap[hashValue] = [pathOnly, f.funcId]
#        else:
#            numFunc -= 1  # decrement numFunc by 1 if funclen is under threshold
