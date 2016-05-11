#   Jerry Paul
#   Concepts of Programming Languages 
#   Project 1 - Recursive Descent Interpreter in Python
#   Source Code credits to Santiago Estens (Recursive Descent Parsing)
#   
#   TO RUN:
#   Use a terminal/command line prompt
#   python conceptsproject.py textfile.txt

stack = []
class Parser:
    def __init__(self, tokens): #initialization function
        self.tokens=tokens
        self.length=len(tokens)
        self.upto=0

    def end(self):
        return self.upto == self.length 

    def peek(self): #look at the current character
        return None if self.end() else self.tokens[self.upto]

    def next(self):     #function to move to the next character in the token
        if not self.end():
            self.upto += 1

    def parse(self):    #return if the boolean expression is valid or not
        if self.parseE() and self.end():
            return True
        else:
            print("Error incorrect input")#print error when not valid
            return False

    def parseE(self):   #rule E of the grammar  
        self.parseB()
        return True

    def parseB(self):   #rule B of the grammar
        if self.parseL():
            if self.parseT():
                return True
            else:
                return False
        else:
            return False

    

    def parseT(self):   #Check for And, Imply and OR
        if self.peek() == '^':
            self.next()
            if self.parseL():
                x=stack.pop()
                y=stack.pop()
                stack.append(x and y)#evaluate expression
                if self.parseT():
                    return True
                else:
                    return False
            else:
                return False
        elif self.peek() == 'v':
            self.next()
            if self.parseL():
                x=stack.pop()
                y=stack.pop()
                stack.append(x or y)#evaluate expression
                if self.parseT():
                    return True
                else:
                    return False
            else:
                return False
        elif self.peek() == '-':
            self.next()
            if self.peek() == '>':
                self.next()
                if self.parseL():
                    x=stack.pop()
                    y=stack.pop()
                    stack.append(x and y)#evaluate expression
                    if self.parseT():
                        return True
                    else:
                        return False
            else:
                return False
        elif self.peek() == ')' or self.peek() == '.':
            return True
        else:
            return False
                    
            

    def parseL(self):   #rule L of the grammar
        if self.parseA():
            return True
        elif self.peek() == '~':
            self.next()
            if self.parseA():
                z=stack.pop()
                stack.append(not z)#apply the complement to the current result
                return True
            else:
                return False
        else:
            return False

    def parseA(self):   #rule L of the grammar
        if self.peek() == 't':
            stack.append(True)#add value to stack
            self.next()
            return True
        elif self.peek() == 'f':
            stack.append(False)#add value to stack
            self.next()
            return True
        elif self.peek() == '(':
            self.next()
            if self.parseB():
                if self.peek() == ')':
                    self.next()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
                


import argparse     #library that implements command line arguments
cmd = argparse.ArgumentParser()
cmd.add_argument("txtfile")     #specify that the program requires a textfile as an input
arguments = cmd.parse_args()    #store the textfile name
file = open(arguments.txtfile,'r')  #open the file in read mode
str = file.readline()
err = "- >"     #This is sort of cheating, but lexing errors for space between -> can be checked efficiently
if err in str:
    print("Error: Incorrect Format")
else:
    print("No Error")
    result=Parser(str.replace(" ","")).parse()  #read the first line of the text, parse it and store the result
    if result:#if the result was valid, print it
        print("Result of expression is: {}".format(stack.pop()))


    
