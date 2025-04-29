class Token:
    R_S_BRACKET = 1
    L_S_BRACKET = 2
    R_C_BRACKET = 3
    L_C_BRACKET = 4
    STRING = 5
    INT = 6
    EQUALS = 7
    COMMENT = 9
    START_MULTILINE_COMMENT = 10
    END_MULTILINE_COMMENT = 11
    FLOAT = 12
    NEWLINE = 13
    
    def __init__(self, tt, tv) -> None:
        self.type = tt
        self.value = tv
        
    def __repr__(self) -> str:
        return f"<Token type={self.type} value={self.value}>"
    
    def __str__(self) -> str:
        token_map = {
            Token.R_S_BRACKET: "]",
            Token.L_S_BRACKET: "[",
            Token.R_C_BRACKET: "}",
            Token.L_C_BRACKET: "{",
            Token.EQUALS: "=",
            Token.NEWLINE: ";"
        }
        
        if self.type in token_map:
            return token_map[self.type]
        else:
            return str(self.value)
            
        

def tokenise(raw: str) -> list:
    tokens = []
    cursor = 0
    cur_start_point = 0
    
    while cursor < len(raw):
        cur_start_point = cursor
        
        if raw[cursor] == "[":
            tokens.append(Token(Token.L_S_BRACKET, None))
            cursor += 1
            while raw[cursor] != "]":
                cursor += 1
            tokens.append(Token(Token.STRING, raw[cur_start_point+1:cursor]))
            tokens.append(Token(Token.R_S_BRACKET, None))
            cursor += 1
        elif raw[cursor] == "{":
            tokens.append(Token(Token.L_C_BRACKET, None))
            cursor += 1
        elif raw[cursor] == "}":
            tokens.append(Token(Token.R_C_BRACKET, None))
            cursor += 1
        elif raw[cursor] == "=":
            tokens.append(Token(Token.EQUALS, None))
            cursor += 1
        elif raw[cursor] in ";\n\r":
            tokens.append(Token(Token.NEWLINE, None))
            cursor += 1
        elif raw[cursor:cursor+2] == "//":
            while raw[cursor] not in "\n\r":
                cursor += 1
        elif raw[cursor:cursor+2] == "/*":
            while raw[cursor:cursor+2] != "*/":
                cursor += 1
            cursor += 2
        elif raw[cursor] in "\t ":
            cursor += 1
        else:
            while raw[cursor] not in "{}[]=;" and raw[cursor:cursor+2] not in {"//", "/*"}:
                cursor += 1
            value = raw[cur_start_point:cursor]
            try:
                tokens.append(Token(Token.INT, int(value)))
            except:
                try:
                    tokens.append(Token(Token.FLOAT, float(value)))
                except:
                    tokens.append(Token(Token.STRING, value))
    
    return tokens
    

def parse(tokens: list[Token]) -> dict:
    data = {}
    cursor = 0
    
    while cursor < len(tokens):
        token = tokens[cursor]
        
        if token.type == Token.L_S_BRACKET: # start of object
            key = tokens[cursor+1].value
            indent = 0
            child_start = 0
            while indent > 0 or child_start == 0:
                if tokens[cursor].type == Token.L_C_BRACKET:
                    if child_start == 0:
                        child_start = cursor
                    indent += 1
                elif tokens[cursor].type == Token.R_C_BRACKET:
                    indent -= 1
                cursor += 1
            data[key] = parse(tokens[child_start+1:cursor-1])
        elif token.type == Token.NEWLINE:
            cursor += 1
        else:
            key = tokens[cursor].value
            cursor += 2
            if tokens[cursor].type != Token.NEWLINE:
                data[key] = tokens[cursor].value
            else:
                data[key] = None
            cursor += 1
    
    return data

        
def decode(raw: str) -> dict:
    tokens = tokenise(raw)
    return parse(tokens)
