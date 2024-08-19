import google.generativeai as genai
import os

API_KEY = "SUA_API_GEMINI"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')  # or gemini-1.5-pro
chat = model.start_chat(history=[
    {"role": "user", "parts": "você cria projetos e pode criar arquivos adicionar conteúdo em arquivos e criar pastas, esses são seus comandos que funcionam por que eu programei: crie arquivos usando '!create <filename> ```<content>```' e crie pastas usando '!folder <foldername>'. nota: o !create tambem serve para reescrever o conteudo de um arquivo"},
    {"role": "model", "parts": "hello world em python: !create hello.py ```python\nprint(\"Hello world!\")\n```"}
])

def tokenize_code(response_text):
    tokens = []
    i = 0
    while i < len(response_text):
        if response_text[i] in [' ', '\n']:
            i += 1
            continue
        if response_text[i:i+7] == '!create':
            tokens.append('!create')
            i += 7
        elif response_text[i:i+7] == '!folder':
            tokens.append('!folder')
            i += 7
        elif response_text[i:i+3] == '```':
            i += 3  # Skip the opening ```
            code_start = i
            while i < len(response_text) and response_text[i:i+3] != '```':
                i += 1
            code = response_text[code_start:i]
            tokens.append(code.strip())  # Strip leading/trailing whitespace
            i += 3  # Skip the closing ```
        else:
            start = i
            while i < len(response_text) and response_text[i] not in [' ', '\n']:
                i += 1
            tokens.append(response_text[start:i])
    return tokens

while True:
    question = input("Question > ")
    if question == "exit":
        break
    response = chat.send_message(question)
    tokens = tokenize_code(response.text)

    i = 0
    while i < len(tokens):
        if tokens[i] == "!create":
            filename = tokens[i+1]
            with open(filename, "w") as f:
                if i+2 < len(tokens):
                    code = tokens[i+2]
                    f.write(code)
            i += 3
        elif tokens[i] == "!folder":
            os.mkdir(tokens[i+1])
            i += 2
        else:
            i += 1

    print(response.text)
