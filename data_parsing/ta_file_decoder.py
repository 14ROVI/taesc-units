class Token:
    R_S_BRACKET = 1
    L_S_BRACKET = 2
    R_C_BRACKET = 3
    L_C_BRACKET = 4
    STRING = 5
    INT = 6
    EQUALS = 7
    SEMICOLON = 8
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
            Token.SEMICOLON: ";",
            Token.NEWLINE: ";"
        }
        
        if self.type in token_map:
            return token_map[self.type]
        else:
            return str(self.value)


def remove_comments(raw: str) -> str:
    cursor = 0
    
    while cursor < len(raw):
        cur_start = cursor
        
        if raw[cursor:cursor+2] == "//":
            while raw[cursor:cursor+1] != "\n":
                cursor += 1
            raw = raw[:cur_start] + raw[cursor:]
            cursor = cur_start
        elif raw[cursor:cursor+2] == "/*":
            while raw[cursor:cursor+2] != "*/":
                cursor += 1
            raw = raw[:cur_start] + raw[cursor+2:]
            cursor = cur_start
        else:
            cursor += 1
            
    return raw
            
        

def tokenise(raw: str) -> list:
    tokens = []
    cursor = 0
    cur_start_point = 0
    
    while cursor < len(raw):
        cur_start_point = cursor
        char = raw[cursor]
        
        if char == "[":
            tokens.append(Token(Token.L_S_BRACKET, None))
            cursor += 1
            while raw[cursor] != "]":
                cursor += 1
            tokens.append(Token(Token.STRING, raw[cur_start_point+1:cursor]))
            tokens.append(Token(Token.R_S_BRACKET, None))
            cursor += 1
        elif char == "{":
            tokens.append(Token(Token.L_C_BRACKET, None))
            cursor += 1
        elif char == "}":
            tokens.append(Token(Token.R_C_BRACKET, None))
            cursor += 1
        elif char == "=":
            tokens.append(Token(Token.EQUALS, None))
            cursor += 1
        elif char == ";":
            tokens.append(Token(Token.SEMICOLON, None))
            cursor += 1
        elif char == "/" and raw[cursor + 1] == "/":
            while raw[cursor] != "\n":
                cursor += 1
        elif char == "/" and raw[cursor + 1] == "*":
            while raw[cursor:cursor+2] != "*/":
                cursor += 1
            cursor += 2
        elif char in "\n\t ":
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
    cur_start_point = 0
    
    while cursor < len(tokens):
        cur_start_point = cursor
        token = tokens[cursor]
        
        if token.type == Token.L_S_BRACKET:
            key = tokens[cursor+1].value
            cursor += 4
            indent = 1
            while indent > 0:
                if tokens[cursor].type == Token.L_C_BRACKET:
                    indent += 1
                elif tokens[cursor].type == Token.R_C_BRACKET:
                    indent -= 1
                cursor += 1
            data[key] = parse(tokens[cur_start_point+4:cursor-1])
        else:
            key = tokens[cursor].value
            cursor += 2
            if tokens[cursor].type != Token.SEMICOLON:
                data[key] = tokens[cursor].value
                cursor += 1
            else:
                data[key] = None
            cursor += 1
    
    return data

        
def decode(raw: str) -> dict:
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    comment_less = remove_comments(raw)
    tokens = tokenise(comment_less)
    return parse(tokens)
