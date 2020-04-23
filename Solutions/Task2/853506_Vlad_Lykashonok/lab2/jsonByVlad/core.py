JSON_LEFTBRACE, JSON_RIGHTBRACE = '{', '}'
JSON_LEFTBRACKET, JSON_RIGHTBRACKET = '[', ']'
JSON_COMMA, JSON_COLON = ',', ':'
JSON_TAB = '  '

def lex(string):
    tokens, value, str_flag = [], '', False
    i = 0
    while i < len(string):
        # print(string[i])
        if ' \n\t'.find(string[i]) != -1:
            i+=1
            continue
        if '\'\"'.find(string[i]) != -1:
            str_flag = True
            i+=1
            while '\'\"'.find(string[i]) == -1:
                if string[i] == '\\':
                    value += string[i]
                    i+=1
                    value += string[i]
                    i+=1
                value += string[i]
                i+=1
        elif '{},:[]'.find(string[i]) != -1:
            if value:
                if value == 'null':
                    tokens.append(None)
                elif value == 'false':
                    tokens.append(False)
                elif value == 'true': 
                    tokens.append(True)
                elif value.isdigit() and not str_flag:
                    tokens.append(int(value))
                else:
                    tokens.append(value)
            tokens.append(string[i])
            value = ''
            str_flag = False
        else:
            value += string[i]
        i+=1
    return tokens

def parse_array(tokens):
    jsonArray = []
    
    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return jsonArray, tokens[1:]
    
    while True:
        json, tokens = parse(tokens)
        jsonArray.append(json)

        if t == JSON_COMMA and ( tokens[1] == JSON_RIGHTBRACE or tokens[1] == JSON_RIGHTBRACKET ):
            return jsonArray, tokens[2:]
        if tokens[0] == JSON_RIGHTBRACKET:
            return jsonArray, tokens[1:]
        elif tokens[0] != JSON_COMMA:
            raise ValueError('invald array, must be \',\' between elements')
        else:
            tokens = tokens[1:]

def parse_object(tokens):
    jsonObject = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return jsonObject, tokens[1:]
    
    while True:
        jsonKey = tokens[0]
        if type(jsonKey) is str:
            tokens = tokens[1:]
        else:
            raise ValueError('invalid key, must be string, not: \'{}\''.format(jsonKey))
        
        if tokens[0] != JSON_COLON:
            raise ValueError('invalid value after key, must be \':\', not: \'{}\''.format(t))
        
        jsonValue, tokens = parse(tokens[1:])
        jsonObject[jsonKey] = jsonValue

        t = tokens[0]
        if t == JSON_COMMA and ( tokens[1] == JSON_RIGHTBRACE or tokens[1] == JSON_RIGHTBRACKET ):
            return jsonObject, tokens[2:]
        if t == JSON_RIGHTBRACE:
            return jsonObject, tokens[1:]
        elif t != JSON_COMMA:
            raise ValueError('invald object, must be \',\' between elements')
        
        tokens = tokens[1:]

def parse(tokens):
    t = tokens[0]
    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]

def from_json(string):
    # print('str from jsonparse',string)
    tokens = lex(string)
    # print('tokens - ',tokens)
    parsed_object = {}
    parsed_object = parse(tokens)
    # print(parsed_object[0])
    return parsed_object[0]

def get_array(arr):
    string = '['
    if len(arr) == 0:
        return '[]'
    for item in arr:
        if type(item) is dict:
            string += get_object(item)
        elif type(item) is list:
            string += get_array(item)
        elif type(item) is str:
            string += "\"" + item + '\"'
        elif item is None:
            string += "null"
        elif item is True:
            string += "true"
        elif item is False:
            string += "false"
        elif type(item) is int or float:
            string += str(item)
        if arr.index(item) != len(arr) - 1:
            string += ', '
    return string + ']'

def get_object(obj):
    string = '{'

    if len(list(obj.keys())) == 0:
        return '{}'

    for item in obj:
        if type(obj[item]) is dict:
            string += "\"" + str(item) + '\": ' + get_object(obj[item])
        elif type(obj[item]) is list:
            string += "\"" + str(item) + '\": ' + get_array(obj[item])
        elif type(obj[item]) is str:
            string += "\"" + str(item) + '\": ' + "\"" + obj[item] + "\""
        elif obj[item] is None:
            string += "\"" + str(item) + '\": ' + "null"
        elif obj[item] == True:
            string += "\"" + str(item) + '\": ' + "true"
        elif obj[item] == False:
            string += "\"" + str(item) + '\": ' + "false"
        elif type(obj[item]) is int or float:
            string += "\"" + str(item) + '\": ' + str(obj[item])
        if list(obj.keys()).index(item) != len(list(obj.keys())) - 1:
            string += ', '
    return string + '}'

def to_json(obj):
    return get_object(obj)

# For coverage
# print(from_json({"name":None,"age":30,"bool":False,"bool2":True,"tmp":[],"city":"New York","empty":{},"cards":["1234","4321","qwe",False,True,None,[],{}]}))
# print(to_json('{"bool": false,"bool2": true,"string": "string","array": [{"obj":{}},"4321",null]}, "int": 30, "intstr": "30"'))