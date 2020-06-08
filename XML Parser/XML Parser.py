# Gabriel R. Potestades
# 1192_CSC515C_G01 - Theory of Computation and Automata

import sys

# ================Lexical Analyzer================ #

is_valid = True

# Tag States
OT = False
BT = False
CT = False
DT = False
NT = False
VT = False

# Attribute States
AT = False
ATV = False
DQM = False
SQM = False

# Declare containers
attrib_values = []
attributes = []
tokenized = []
operators = []
sequence = []
comments = []
symbols = []
values = []
tags = []

# Declare temporary strings
attrib_val_temp = ''
comment_temp = ''
attrib_temp = ''
tag_temp = ''
val_temp = ''
prev_val = ''

xml_file = open("XML Sample.xml", "r")
#xml_file = sys.stdin

contents = xml_file.read()

for char in contents:

    if char == '<':

        if val_temp.strip() and VT:
            values.append(val_temp.strip())
            tokenized.append(val_temp.strip())
            sequence.append('value')
            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            val_temp = ''
            VT = False
            OT = True
        elif DQM or SQM:
            attrib_val_temp += char
        elif not OT:
            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            OT = True
            VT = False
        else:
            is_valid = False
        
    elif char == '>':

        if VT:
            if char not in ['\n', '\t']:
                if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                    val_temp += char 
        elif DQM or SQM:
            attrib_val_temp += char
        elif DT:
            if NT:
                tags.append(tag_temp.strip())
                tokenized.append(tag_temp.strip())
                sequence.append('tag')
                tag_temp = ''
                NT = False

            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            VT = True
            OT = False
            DT = False

        else:
            if CT:
                tags.append(tag_temp.strip())
                tokenized.append(tag_temp.strip())
                sequence.append('tag')
                tag_temp = ''
                CT = False
            elif BT:
                BT = False
            elif AT:
                AT = False
                if attrib_temp.strip():
                    attributes.append(attrib_temp.strip())
                    tokenized.append(attrib_temp.strip())
                    sequence.append('attribute')
                    attrib_temp = ''
            elif NT:
                tags.append(tag_temp.strip())
                tokenized.append(tag_temp.strip())
                sequence.append('tag')
                tag_temp = ''
                NT = False
            elif OT and tag_temp.strip():
                tags.append(tag_temp.strip())
                tokenized.append(tag_temp.strip())
                sequence.append('tag')
                tag_temp = ''
                OT = False
            else:
                is_valid = False

            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            VT = True       

    elif char == '?':

        if VT:
            if char not in ['\n', '\t']:
                if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                    val_temp += char
        elif DQM or SQM:
            attrib_val_temp += char
        elif OT:
            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            DT = True
            OT = False
            NT = True
        elif DT:
        
            if attrib_temp.strip() and AT:
                attributes.append(attrib_temp.strip())
                tokenized.append(attrib_temp.strip())
                sequence.append('attribute')
                attrib_temp = ''
                AT = False
                symbols.append(char)
                tokenized.append(char)
                sequence.append('symbol')
                DT = False
            elif NT:
                tag_temp += char
            else:
                symbols.append(char)
                tokenized.append(char)
                sequence.append('symbol')
                DT = False
        else:
            is_valid = False

    elif char == ' ':

        if VT:
            if char not in ['\n', '\t']:
                if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                    val_temp += char
        elif DQM or SQM:
            attrib_val_temp += char
        elif NT and tag_temp.strip():
            NT = False
            AT = True
            tags.append(tag_temp.strip())
            tokenized.append(tag_temp.strip())
            sequence.append('tag')
            tag_temp = ''
        elif OT:
            NT = True
            OT = False
        elif AT:
            if attrib_temp.strip():
                attributes.append(attrib_temp.strip())
                tokenized.append(attrib_temp.strip())
                sequence.append('attribute')
                attrib_temp = ''
        elif DT and not ATV:
            NT = True

    elif char == '=':

        if VT:
            if char not in ['\n', '\t']:
                if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                    val_temp += char
        elif DQM or SQM:
            attrib_val_temp += char
        elif AT:
            if attrib_temp.strip():
                attributes.append(attrib_temp.strip())
                tokenized.append(attrib_temp.strip())
                sequence.append('attribute')
                attrib_temp = ''
            operators.append(char)
            tokenized.append(char)
            sequence.append('operator')
            AT = False
            ATV = True
        elif NT:
            tag_temp += char
        elif OT:
            tag_temp += char
            OT = False
            NT = True
        else:
            is_valid = False

    elif char == '"':

        if VT:
            if char not in ['\n', '\t']:
                if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                    val_temp += char
        elif ATV:
            attrib_val_temp += char
            if not DQM and not SQM:
                DQM = True
            elif DQM and not SQM:
                DQM = False
                ATV = False  
                AT = True
                attrib_values.append(attrib_val_temp)
                tokenized.append(attrib_val_temp)
                sequence.append('attribute value')
                attrib_val_temp = ''
        elif not ATV:
            attrib_val_temp += char
            ATV = True
            AT = True
            DQM = True
        else:
            is_valid = False

    elif char == "'":
    
        if VT:
            if char not in ['\n', '\t']:
                if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                    val_temp += char
        elif ATV:
            attrib_val_temp += char
            if not SQM and not DQM:
                SQM = True
            elif SQM and not DQM:
                SQM = False
                ATV = False  
                AT = True   
                attrib_values.append(attrib_val_temp)
                tokenized.append(attrib_val_temp)
                sequence.append('attribute value')
                attrib_val_temp = ''
        elif not ATV:
            attrib_val_temp += char
            ATV = True
            AT = True
            SQM = True
        else:
            is_valid = False

    elif char == '/':

        if VT:
            val_temp += char
        elif DQM or SQM:
            attrib_val_temp += char
        elif NT:
            tags.append(tag_temp.strip())
            tokenized.append(tag_temp.strip())
            sequence.append('tag')
            tag_temp = ''

            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            BT = True
            NT = False 
        elif OT:
            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
            CT = True
            OT = False
        elif AT:
            if attrib_temp:
                attributes.append(attrib_temp)
                tokenized.append(attrib_temp)
                sequence.append('attribute')
                attrib_temp = ''
            symbols.append(char)
            tokenized.append(char)
            sequence.append('symbol')
        else:
            is_valid = False

    elif OT:
        tag_temp += char
        OT = False
        NT = True
    elif NT:
        if char in ['\n', '\t'] and tag_temp.strip():   
            NT = False
            AT = True
            tags.append(tag_temp.strip())
            tokenized.append(tag_temp.strip())
            sequence.append('tag')
            tag_temp = ''
        else:
            tag_temp += char
    elif CT:
        tag_temp += char
    elif DQM or SQM:
        attrib_val_temp += char
    elif AT:
        attrib_temp += char 
    elif VT:
        if char not in ['\n', '\t']:
            if not (prev_val in ['\n', '\t', ' '] and char == ' '):
                 val_temp += char

    if not is_valid:
        sys.stdout.write('NO')
        #break
        exit(0)

    prev_val = char

# Checking purposes
print("********************************************")

for i in range(0, len(tokenized)):
    print (i, '. ', tokenized[i], ' - ' , sequence[i])

# open_symbol = 0
# close_symbol = 0
# values_count = len(values)
# attribute_count = len(attributes)
# attrib_val_count  = len(attrib_values)
# tags_count = len(tags)
# backslash = 0

# for sym in symbols:

#     if sym == '<':
#         open_symbol += 1
#     elif sym == '>':
#         close_symbol += 1
#     elif sym == '/':
#         backslash += 1

# print('Number of < : ', open_symbol)
# print('Number of > : ', close_symbol)
# print('Number of / : ', backslash)
# print('Number of tags : ', tags_count)
# print('Number of values : ', values_count)
# print('Number of attributes : ', attribute_count)
# print('Number of attribute values : ', attrib_val_count)

#exit(0)

# ================Lexical Analyzer================ #

# ==============Syntactical Analyzer============== #

stack = []
is_valid = True
has_header = False

# Header states
SA_HT = False

#Tag states
SA_OT = False
SA_CT = False
SA_NT = False
SA_INT = False

#Attribute states
SA_AT = False
SA_OP = False

for i in range(0, len(tokenized)):

    item = tokenized[i]
    item_type = sequence[i]

    if item_type == 'symbol':
        
        if item == '<':
            
            stack.append(item)

            if not SA_OT:
                SA_OT = True
            else:
                is_valid = False

        elif item == '>':
            
            if SA_HT:
                if stack[len(stack)-1] == '<':
                    stack.pop()
                    has_header = True
                    SA_HT = False
                    SA_AT = False
                else:
                    is_valid = False
            elif SA_CT:
                if stack[len(stack)-1] == '<':
                    stack.pop()
                    SA_CT = False
                else:
                    is_valid = False
            elif SA_NT or SA_AT:
                stack.append(item)
                SA_NT = False
                SA_AT = False
            elif SA_INT:
                if stack[len(stack)-1] == '<':
                    stack.pop()
                    SA_INT = False
                else:
                    is_valid = False
            else:
                is_valid = False

        elif item == '/':
            
            if SA_OT:
                if stack[len(stack)-1] == '<':
                    stack.pop()
                    if stack[len(stack)-1] == '>':
                        stack.pop()
                        SA_OT = False
                        SA_CT = True 
                    else:
                        is_valid = False
                else:
                    is_valid = False
            elif SA_NT or SA_AT:
                stack.pop()
                SA_INT = True
                SA_NT = False
                SA_AT = False
            else:
                is_valid = False
                
        elif item == '?':
            
            if has_header:
                is_valid = False

            if SA_OT:
                stack.append(item)
                SA_OT = False
                SA_HT = True
            elif SA_HT:
                if stack[len(stack)-1] == '?':
                    stack.pop()
                else:
                    is_valid = False  
                   
    elif item_type == 'attribute':

        if not item.replace('_', '').isalnum():
            if item != '_':
                is_valid = False

        if SA_NT or SA_AT:
            
            SA_NT = False
            SA_AT = True
        else:
            is_valid = False
    
    elif item_type == 'operator':
        
        if SA_AT:
            SA_AT = False
            SA_OP = True
        else:
            is_valid = False

    elif item_type == 'attribute value':
        
        # if item == "''" or item == '""':
        #     is_valid = False

        if SA_OP:
            SA_OP = False
            SA_AT = True
        else:
            is_valid = False
        
    elif item_type == 'tag':
        
        if SA_CT:
            if item.replace('_', '').isalnum():
                if stack[len(stack)-1] == item:
                    stack.pop()
                else:
                    is_valid = False  
            else:
                if item != '_':
                    is_valid = False  
        elif SA_OT:   
            if item.replace('_', '').isalnum():
                stack.append(item)
                SA_OT = False
                SA_NT = True           
            else:
                if item != '_':
                    is_valid = False               
        elif SA_HT:
            if item != 'xml':
                is_valid = False
            else:
                SA_NT = True
        else:
            is_valid = False
  
    if not is_valid:
        break

if not has_header or not is_valid or len(stack) > 0:
    sys.stdout.write('NO')
else:
    sys.stdout.write('YES')
    
# ==============Syntactical Analyzer============== #