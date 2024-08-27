import google.generativeai as genai
import os

def main():
    api_key = input("Digite sua chave de API do Google (Gemini): ")
    genai.configure(api_key=api_key)

    file_path = input("Digite o caminho do arquivo que deseja editar: ")
    with open(file_path, "r") as f:
        file_content = f.read()

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    instructions = f"""
    Você é um assistente de programação. Estamos trabalhando no arquivo {file_path}.
    O conteúdo atual do arquivo é:

    ```
    {file_content}
    ```

    Importante: Realize apenas uma ação por vez. Espere a confirmação do usuário antes de prosseguir para a próxima ação.

    Quando eu pedir para adicionar ou remover código, use o seguinte formato:

    Para adicionar código ao final do arquivo, use:
    **Adicionar:**
    código: <código a ser adicionado>

    Para remover código, use:
    **Remover:**
    linha: <número da linha a ser removida>

    O código pode ter múltiplas linhas após o "código:". Não é recomendado usar ``` e você nunca pode usar.
    Não adicione nenhuma mensagem após o código.

    Lembre-se de sempre usar o formato correto e não usar **Adicionar** ou **Remover** toda vez que for adicionar ou remover código, use apenas
    "codigo:" uma vez para adicionar, e "linha:" para cada linha que deseja remover. Você só pode usar ou **Adicionar** ou **Remover** de cada vez, não pode usar os dois ou os mesmo mais de uma vez.

    Importante: Se for usar **Remover:**, você deve usar apenas "linha:" para cada linha que deseja remover. Por exemplo:
    **Remover:**
    linha: 5
    linha: 6
    linha: 7

    Se for usar o **Adicionar:**, você deve usar apenas "código:" para adicionar o código ao final do arquivo.
    """

    chat.send_message(instructions)
    print("Assistente: Olá! Estou pronto para ajudar com o arquivo. O que você gostaria de fazer? Lembre-se, farei uma ação de cada vez.")

    while True:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            break

        response = chat.send_message(user_input)
        print("Assistente:", response.text)

        if "linha:" in response.text or "código:" in response.text:
            action_description = response.text.split("\n")[0].strip()
            print(f"Ação a ser realizada: {action_description}")

            lines_to_remove = []
            code_to_add = ""
            for line in response.text.split("\n"):
                if line.startswith("linha:"):
                    line_number = int(line.split("linha:")[1].strip())
                    lines_to_remove.append(line_number)
                elif line.startswith("código:"):
                    code_to_add = "\n".join(response.text.split("código:")[1].strip().split("\n"))

            with open(file_path, "r") as f:
                lines = f.readlines()
            
            if "**Adicionar:**" in action_description:
                new_lines = lines + ["\n" + code_to_add + "\n"]
                print("Código adicionado ao final do arquivo")
            elif "**Remover:**" in action_description:
                new_lines = [line for i, line in enumerate(lines, 1) if i not in lines_to_remove]
                print(f"Código removido das linhas {', '.join(map(str, lines_to_remove))}")
            
            with open(file_path, "w") as f:
                f.writelines(new_lines)

            with open(file_path, "r") as f:
                file_content = f.read()
            update_message = f"O arquivo foi atualizado. O novo conteúdo é:\n\n```\n{file_content}\n```\nVocê gostaria de fazer mais alguma alteração?"
            chat.send_message(update_message)

if __name__ == "__main__":
    main()
