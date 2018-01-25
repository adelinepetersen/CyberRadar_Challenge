#!/usr/bin/env python

import ply.lex as lex

## first define the lexer and acceptable tokens
tokens = (
    'FIRST',
    'PROPERTY',
    'OPERATION',
    'AT',
    'NEST1',
    'PRENEST2'
    'NEST2',
    'COMPARATOR',
    'CONTEXT',
    'VALUE',
)

def t_FIRST(t):
    r' [NP] '
    return t

def t_PROPERTY(t):
    r' \w + \. + \w+'
    return t

def t_OPERATION(t):
    r'^.*\b(upper|count|lower)\b.*$'
    return t

def t_AT(t):
    r'\@'
    return t

def t_NEST1(t):
    r'OPERATION + \( + PROPERTY + \)'
    return t

def t_PRENEST2(t):
    r'OPERATION + \('
    return t

def t_NEST2(t):
    r'OPERATION + \( + PROPERTY + \) + \)'
    return t

def t_COMPARATOR(t):
    r'(?<![!=])[!=]=(?!=)| [>] | [<] | [>=] | [<=] | [has] | [not has] | [in] | [not in] | [contains] | [not contains] | [match] | [not match] | [added] |  [removed] '
    return t

def t_CONTEXT(t):
    r'^(?=.*?\b[a-z]+\b)((?!upper|counter|lower).)*$'
    return t

def t_VALUE(t):
    r'^(.*\b([\w]+|[\d]+)\b)((?!upper|counter|lower).)*$'
    return t

t_ignore = '[ \t\n]'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Opens file provided by user, puts each line of file through the
# syntax checker. Prints statement whether the syntax is correct or not.
def syntaxAnalyzer():
    file_object = open("tests.txt", 'r')
    list_lines = file_object.readlines()
    for i in range(len(list_lines)):
        if (syntaxCheck(list_lines[i])):
            print("Line " + str(i) + ": syntax ok\n")
        else:
            print("Line " + str(i) + ": syntax err\n")
    file_object.close()

def syntaxCheck(ln):
    lexer.input(ln)
    ctr = 1
    if_context = False
    at_one = False
    at_two = False
    at_three = False
    at_four = False
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        print(tok.type)
        if ctr == 1:
            if tok.type != 'FIRST':
                return False
        elif ctr == 2:
            if (tok.type == 'AT'):
                at_one = True
            elif tok.type != 'PROPERTY':
                return False
        elif ctr == 3:
            if at_one and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False
            elif tok.type == 'CONTEXT':
                if_context = True
            elif tok.type != 'COMPARATOR':
                return False
        elif ctr == 4:
            if at_one and tok.type == 'AT':
                at_two = True
            elif at_one and tok.type == 'CONTEXT':
                if_context = True
            elif at_one and tok.type != 'COMPARATOR':
                return False
            elif not at_one and if_context and tok.type != 'COMPARATOR':
                return False
            elif not at_one and not if_context and tok.type == 'AT':
                at_three = True 
            elif not at_one and not if_context and (tok.type != 'VALUE' and tok.type != 'CONTEXT'):
                return False
        elif ctr == 5:
            if at_one and at_two and tok.type != 'NEST2':
                return False
            elif at_one and if_context and tok.type != 'COMPARATOR':
                return False
            elif at_one and not if_context and tok.type == 'AT':
                at_three = True
            elif at_one and not if_context and (tok.type != 'VALUE' and tok.type != 'CONTEXT'):
                return False
            elif not at_one and if_context and tok.type == 'AT':
                at_three = True
            elif not at_one and if_context and (tok.type != 'VALUE' and tok.type != 'CONTEXT'):
                return False
            elif not at_one and not if_context and at_three and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False 
        elif ctr == 6:
            if at_one and at_two and tok.type == 'CONTEXT':
                if_context = True
            elif at_one and at_two and tok.type != 'COMPARATOR':
                return False
            elif at_one and if_context and tok.type == 'AT':
                at_three = True
            elif at_one and if_context and (tok.type != 'VALUE' and tok.type != 'CONTEXT'):
                return False
            elif at_one and not if_context and at_three and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False
            elif not at_one and if_context and at_three and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False
            elif not at_one and not if_context and at_three and tok.type == 'AT':
                at_four = True
        elif ctr == 7:
            if at_one and at_two and if_context and tok.type != 'COMPARATOR':
                return False
            elif at_one and at_two and not if_context and tok.type == 'AT':
                at_three = True
            elif at_one and at_two and not if_context and (tok.type != 'CONTEXT' and tok.type != 'VALUE'):
                return False 
            elif at_one and not at_two and if_context and at_three and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False 
            elif at_one and not at_two and not if_contest and at_three and tok.type == 'AT':
                at_four = True
            elif not at_one and not at_two and if_context and at_three and tok.type == 'AT':
                at_four = True
            elif not at_one and not at_two and not if_context and at_three and at_four and tok.type != 'NEST2':
                return False 
        elif ctr == 8:
            if at_one and at_two and if_context and tok.type == 'AT':
                at_three = True
            elif at_one and at_two and if_context and (tok.type != 'VALUE' and tok.type != 'CONTEXT'):
                return False
            elif at_one and at_two and not if_context and at_three and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False
            elif at_one and not at_two and if_context and at_three and tok.type == 'AT':
                at_four = True 
            elif at_one and not at_two and not if_context and at_three and at_four and tok.type != 'NEST2':
                return False
            elif not at_one and not at_two and if_context and at_three and at_four and tok.type != 'NEST2':
                return False 
        elif ctr == 9:
            if at_one and at_two and if_context and at_three and (tok.type != 'NEST1' and tok.type != 'PRENEST2'):
                return False
            elif at_one and at_two and not if_context and at_three and tok.type == 'AT':
                at_four = True
            elif at_one and not at_two and if_context and at_three and at_four and tok.type != 'NEST2':
                return False 
        elif ctr == 10:
            if at_one and at_two and if_context and at_three and tok.type == 'AT':
                at_four = True 
            elif at_one and at_two and not if_context and at_three and at_four and tok.type != 'NEST2':
                return False
        elif ctr == 11:
            if at_one and at_two and if_context and at_three and at_four and tok.type != 'NEST2':
                return False
        else:
            return False

        ctr = ctr + 1
    return True

syntaxAnalyzer()