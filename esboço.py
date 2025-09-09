import getpass  # para esconder senha
import json     # para salvar usuários
import datetime #marcar consulta

print("Bem-vindo ao Nome do local\n"
      "Integre, acompanhe e registre cada etapa com segurança.\n"
      "➡️ Acesse o painel e comece agora.\n"
      "Acesso ao login: Digite 1\n"
      "Criar uma conta: Digite 2")

opcao = input("Escolha uma opção (1 para login, 2 para criar conta): ").strip()

#Cadastro
if opcao == "2":
    print("\nVocê deseja se cadastrar como:\n1 - Paciente\n2 - Especialista")
    tipo = input("Digite 1 ou 2: ").strip()

    nome = input("Nome completo: ").strip()

    #Cadastro Paciente 
    if tipo == "1":
        while True:  # fica repetindo até digitar corretamente
            cpf = input("CPF (11 dígitos): ").strip()
            if cpf.isdigit() and len(cpf) == 11:  # só números e 11 dígitos
                identificador = cpf
                tipo_usuario = "paciente"
                break
            else:
                print("❌ CPF inválido! Digite apenas 11 números.")

    #Cadastro Especialista 
    elif tipo == "2":
        while True:
            crm = input("CRM (6 dígitos): ").strip()
            if crm.isdigit() and len(crm) == 6:  # só números e 6 dígitos
                identificador = crm
                tipo_usuario = "especialista"
                break
            else:
                print("❌ CRM inválido! Digite apenas 6 números.")

    else:
        print("Opção inválida. Cadastro cancelado.")
        exit()

    #Criar senha com confirmação
    while True:
        senha = getpass.getpass("Crie uma senha: ").strip()
        confirma = getpass.getpass("Confirme a senha: ").strip()
        if senha == confirma:
            break
        else:
            print("❌ As senhas não conferem. Tente novamente!")

    #Salvar usuário no arquivo
    usuario = {"nome": nome, "id": identificador, "senha": senha, "tipo": tipo_usuario}
    with open("usuarios.json", "a") as f: #Abre o arquivo chamado usuarios.json, "a" é de append entao ele adiciona ao final do documento
        f.write(json.dumps(usuario) + "\n") #esse json.dumps converte o objeto usuario (geralmente um dicionário Python) em uma string no formato JSON// 
        #o f.write escreve a string JSON dentro do arquivo.O "\n" adiciona uma quebra de linha no final, para que cada registro de usuário fique em uma linha separada.

    print(f"\n✅ Conta criada com sucesso! Bem-vindo(a), {nome}.\n")

    # Mostrar menu certo depois do cadastro
    if tipo_usuario == "paciente":
        print("MENU PACIENTE")
        print("1 - Perfil pessoal")
        print("2 - Agenda")
        print("3 - Resultados e documentos")
        print("4 - Comunicação segura")
        print("5 - Módulos educacionais")
        print("6 - Notificações")
        print("7 - Privacidade")
    else:
        print("MENU ESPECIALISTA")
        print("1 - Dashboard inicial")
        print("2 - Perfil do especialista")
        print("3 - Agenda")
        print("4 - Estudos clínicos")
        print("5 - Resultados e relatórios")
        print("6 - Comunicação")
        print("7 - Configurações")


#Login
elif opcao == "1":
    identificador = input("Digite seu CPF ou CRM: ").strip()
    senha = getpass.getpass("Senha: ").strip()

    usuario_encontrado = None

    #procurar usuário no arquivo
    try:
        with open("usuarios.json", "r") as f: #Abre o arquivo usuarios.json no modo leitura ("r"). Se o arquivo não existir, será lançado um erro FileNotFoundError.
            for linha in f:#Lê o arquivo linha por linha.
                usuario = json.loads(linha)
                if usuario["id"] == identificador and usuario["senha"] == senha: #Verifica se o id e a senha do usuário lido são iguais aos valores fornecidos.
                    usuario_encontrado = usuario #Se encontrou, guarda o dicionário do usuário em usuario_encontrado.
                    break
    except FileNotFoundError:
        print("Nenhum usuário cadastrado ainda.")
        exit()

    if usuario_encontrado:
        print(f"\n✅ Login realizado com sucesso! Bem-vindo(a), {usuario_encontrado['nome']}.\n")

        if usuario_encontrado["tipo"] == "paciente":
            print("MENU PACIENTE")
            print("1 - Perfil pessoal")
            print("2 - Agenda")
            print("3 - Resultados e documentos")
            print("4 - Comunicação segura")
            print("5 - Módulos educacionais")
            print("6 - Notificações")
            print("7 - Privacidade")
        else:
            print("MENU ESPECIALISTA")
            print("1 - Dashboard inicial")
            print("2 - Perfil do especialista")
            print("3 - Agenda")
            print("4 - Estudos clínicos")
            print("5 - Resultados e relatórios")
            print("6 - Comunicação")
            print("7 - Configurações")
    else:
        print("❌ Usuário ou senha incorretos.")

#Nehuma das opções acima
else:
    print("Opção inválida. Encerrando...")
