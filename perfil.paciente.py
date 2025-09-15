import getpass  # para esconder senha
import json     # para salvar usuários

print("Bem-vindo ao Nome do local\n"
      "Integre, acompanhe e registre cada etapa com segurança.\n"
      "➡️  Acesse o painel e comece agora.\n")

usuario_encontrado = None  # variável global

#So aceita o numero 1 e 2, se tiver digitado o errado ele volta para as opções disponiveis
while True:
    print("Acesso ao login: Digite 1")
    print("Criar uma conta: Digite 2")
    opcao = input("Escolha uma opção (1 para login, 2 para criar conta): ").strip()

    if opcao in ["1", "2"]:
        break
    else:
        print("❌ Opção inválida! Tente novamente.\n")

# Cadastro
def cadastro():
    if opcao == "2":
        nome = input("Nome completo: ").strip()
        def formatar_cpf(cpf: str) -> str:
            """Formata o CPF no padrão 000.000.000-00"""
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

        while True:
            cpf = input("CPF (11 dígitos): ").strip()
            if cpf.isdigit() and len(cpf) == 11:
                identificador = formatar_cpf(cpf)   # <- aqui já salva formatado
                tipo_usuario = "paciente"
                break
            else:
                print("❌ CPF inválido! Digite apenas 11 números.")

        # Criar senha
        while True:
            senha = getpass.getpass("Crie uma senha: ").strip()
            confirma = getpass.getpass("Confirme a senha: ").strip()
            if senha == confirma:
                break
            else:
                print("❌ As senhas não conferem. Tente novamente!")

        # Salvar usuário
        usuario = {"nome": nome, "id": identificador, "senha": senha, "tipo": tipo_usuario}
        with open("usuarios.json", "a") as f:
            f.write(json.dumps(usuario) + "\n")

        print(f"\n✅ Conta criada com sucesso! Bem-vindo(a), {nome}.\n")
        return usuario

# Login
def login():
    while True:  # 🔄 repete até acertar
        identificador = input("Digite seu CPF ou CRM: ").strip()
        senha = getpass.getpass("Senha: ").strip()

        try:
            with open("usuarios.json", "r") as f:
                for linha in f:
                    usuario = json.loads(linha)
                    if usuario["id"] == identificador and usuario["senha"] == senha:
                        print(f"\n✅ Login realizado com sucesso! Bem-vindo(a), {usuario['nome']}.\n")
                        return usuario
        except FileNotFoundError:
            print("❌ Nenhum usuário cadastrado ainda. Vamos criar uma conta!\n")
            return cadastro()   
        print("❌ Usuário ou senha incorretos. Tente novamente!\n")


# --- Fluxo principal ---
if opcao == "2":
    usuario_encontrado = cadastro()

elif opcao == "1":
    usuario_encontrado = login()
    if not usuario_encontrado:  # se não encontrou usuário, chama cadastro
        usuario_encontrado = cadastro()

# PAINEL DO PACIENTE (manu)
if usuario_encontrado["tipo"] == "paciente":
    while True:
        print("MENU PACIENTE")
        print("1 - Perfil pessoal")
        print("2 - Agenda")
        print("3 - Resultados e documentos")
        print("4 - Comunicação segura")
        print("5 - Módulos educacionais")
        print("6 - Notificações")
        print("7 - Privacidade")

        escolha = input("\nEscolha uma opção: ").strip()
        if escolha in ["1", "2", "3", "4", "5", "6", "7"]:
            print(f"Você escolheu a opção {escolha}.")
        else:
            print("❌ Opção inválida! Voltando ao menu principal.")
            # aqui você sai do menu atual e retorna para o menu principal

        if escolha == "1":
            # Configuração do perfil do paciente
            print("\nVamos configurar seu perfil. Por favor, preencha os dados a seguir:")
            nome_completo = usuario_encontrado["nome"]
            identificar = usuario_encontrado["id"]
            idade = int(input("Insira a idade: "))
            genero = input("Insira seu gênero: ").strip()
            endereco = input("Insira seu endereço: ").title().strip()

        # contato
            while True:
                contato = input("Insira seu telefone para contato (11 dígitos, ex: 11987654321): ").strip()
                if contato.isdigit() and len(contato) == 11:
                    # formatar (DDD) 98765-4321
                    contato_formatado = f"({contato[:2]}) {contato[2:7]}-{contato[7:]}"
                    break
                else:
                    print("❌ Telefone inválido! Digite apenas números e use 11 dígitos.")

            print("📞 Telefone salvo:", contato_formatado)

            # medicamentos
            medicamentos = input("Faz uso de medicamentos contínuos? (sim ou não): ").strip().lower()
            if medicamentos == "sim":
                medicamentos = input("Quais medicamentos você utiliza? ").strip()
            else:
                medicamentos = "Nenhum"

            # preferência de contato
            preferencia_de_contato = input("Por onde devemos entrar em contato (e-mail, telefone ou app): ").strip().lower()

            if preferencia_de_contato == "e-mail" "email" "EMAIL" "Email":
                while True:
                    email_contato = input("Digite seu e-mail para contato: ").strip()
                    if "@" in email_contato and email_contato.endswith(".com"):
                        meio_contato = f"E-mail: {email_contato}"
                        break
                    else:
                        print("❌ E-mail inválido! Certifique-se de incluir '@' e terminar com '.com'.")
            elif preferencia_de_contato == "telefone":
                meio_contato = f"Telefone: {contato}"
            elif preferencia_de_contato == "app":
                meio_contato = "App (notificações internas)"
            else:
                meio_contato = "Nenhum"

            print("📩 Preferência de contato registrada:", meio_contato)
        
            # termos de privacidade
            while True:
                print("\n🔒 Termos de privacidade: Seus dados serão usados apenas para fins clínicos, conforme a LGPD.\n")
                aceitou_termos = input("Você aceita os termos de privacidade (sim/não): ").strip().lower()
                
                if aceitou_termos == "sim":
                    print("✅ Termos aceitos! Vamos continuar...")
                    break
                else:
                    print("⚠️ Você deve aceitar os termos para continuar.\n")


            # conferindo dados
            while True:
                print(
                    f"\nConfira seus dados:\n"
                    f"Nome: {nome_completo}\n"
                    f"CPF: {identificar}\n"
                    f"Idade: {idade}\n"
                    f"Gênero: {genero}\n"
                    f"Endereço: {endereco}\n"
                    f"Telefone: {contato}\n"
                    f"Medicamentos: {medicamentos}\n"
                    f"Preferência de contato: {meio_contato}"
                )
                arrumar = input("Está correto ou deseja corrigir algo? (digite 'corrigir' ou 'ok'): ").strip().lower()

                if arrumar == "ok":
                    print("\n✅ Perfil finalizado com sucesso!Voltando ao MENNU PACIENTE..." )
                    break
                elif arrumar == "corrigir":
                    campo = input("O que deseja corrigir? ").strip().lower()
                    if campo == "nome".strip().lower():
                        nome_completo = input("Digite novamente o nome: ").strip().lower()
                    elif campo == "cpf".strip().lower():
                        identificar = input("Digite novamente o CPF: ").strip().lower()
                    elif campo == "idade" .strip().lower():
                        idade = int(input("Digite novamente a idade: ")) .strip()
                    elif campo == "genero".strip().lower():
                        genero = input("Digite novamente o gênero: ").strip().lower()
                    elif campo == "endereco" "endereço".strip().lower():
                        endereco = input("Digite novamente o endereço: ").title().strip()
                    elif campo == "telefone".strip().lower():
                        while True:
                            contato = input("Digite novamente o telefone (11 dígitos): ").strip() .lower()
                            if contato.isdigit() and len(contato) == 11:
                                break
                            else:
                                print("Telefone inválido!")
                    elif campo == "medicamentos" "medicamentos".strip().lower():
                        usa_medicamentos = input("Faz uso de medicamentos contínuos? (sim/não): ").strip().lower()
                        if usa_medicamentos == "sim".strip().lower():
                            medicamentos = input("Quais medicamentos você utiliza? ").strip()
                        else:
                            medicamentos = "Nenhum"
                    elif campo == "contato" .strip().lower():
                        preferencia_de_contato = input("E-mail, telefone ou app? ").strip().lower()
                        if preferencia_de_contato == "e-mail".strip().lower():
                            email_contato = input("Digite seu e-mail para contato: ").strip()
                            meio_contato = f"E-mail: {email_contato}"
                        elif preferencia_de_contato == "telefone".strip().lower():
                            meio_contato = f"Telefone: {contato}"
                        elif preferencia_de_contato == "app".strip().lower():
                            meio_contato = "App (notificações internas)"
                        else:
                            meio_contato = "Não informado"
                    else:
                        print("⚠️ Campo inválido. Tente novamente.")
                else:
                    print("⚠️ Digite apenas 'ok' ou 'corrigir'.")

        

