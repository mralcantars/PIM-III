import json     # para salvar usuários
import pwinput  # para esconder senha com '*' 

# Dados dos médicos com horários disponíveis
medicos = [
    {
        "nome": "Dr. Marcos Vieira",
        "especialidade": "Pneumologia",
        "horarios_disponiveis": ["12/09/2025 15:00", "12/09/2025 16:00", "15/09/2025 14:00"]
    },
    {
        "nome": "Dra. Patrícia Mendes",
        "especialidade": "Dermatologia",
        "horarios_disponiveis": ["25/09/2025 19:00", "25/09/2025 15:00"]
    },
    {
        "nome": "Dr. André Moreira",
        "especialidade": "Neurologia",
        "horarios_disponiveis": ["14/09/2025 10:00", "14/09/2025 16:00"]
    },
    {
        "nome": "Dra. Luciana Castro",
        "especialidade": "Gastroenterologia",
        "horarios_disponiveis": ["18/09/2025 11:00", "18/09/2025 17:30"] # Corrigi a lista de strings
    },
    {
        "nome": "Dr. Ricardo Alves",
        "especialidade": "Nefrologia",
        "horarios_disponiveis": ["02/10/2025 14:00", "02/10/2025 11:00"] # Corrigi a lista de strings
    },
    {
        "nome": "Dra. Renata Fonseca",
        "especialidade": "Cardiologia",
        "horarios_disponiveis": ["04/09/2025 14:00"]
    },
]

print("Bem-vindo ao Nome do local\n"
      "Integre, acompanhe e registre cada etapa com segurança.\n"
      "➡️  Acesse o painel e comece agora.\n")

usuario_encontrado = None  # variável global para armazenar o usuário logado

# Menu inicial: login ou cadastro
while True:
    print("Acesso ao login: Digite 1")
    print("Criar uma conta: Digite 2")
    opcao_inicial = input("Escolha uma opção (1 para login, 2 para criar conta): ").strip()

    if opcao_inicial in ["1", "2"]:
        break
    else:
        print("❌ Opção inválida! Tente novamente.\n")

#Cadastro
def formatar_cpf(cpf: str) -> str:
    """Formata o CPF no padrão 000.000.000-00"""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def cadastro():
    nome = input("Nome completo: ").strip()
    while True:
        cpf = input("CPF (11 dígitos): ").strip()
        if cpf.isdigit() and len(cpf) == 11:
            identificador = formatar_cpf(cpf)
            tipo_usuario = "paciente"
            break
        else:
            print("❌ CPF inválido! Digite apenas 11 números.")

    while True:
        senha = pwinput.pwinput("Crie uma senha: ", mask="*").strip()
        confirma = pwinput.pwinput("Confirme a senha: ", mask="*").strip()
        if senha == confirma:
            print("✅ Senha criada com sucesso!")
            break
        else:
            print("❌ As senhas não conferem. Tente novamente!")

    # Inicia com campos de perfil vazios e agenda vazia
    usuario = {
        "nome": nome,
        "id": identificador,
        "senha": senha,
        "tipo": tipo_usuario,
        "perfil": {},
        "agenda": []
    }

    # Salva o usuário no arquivo
    with open("usuarios.json", "a") as f:
        f.write(json.dumps(usuario) + "\n")

    print(f"\n✅ Conta criada com sucesso! Bem-vindo(a), {nome}.\n")
    return usuario

#Login
def login():
    while True:
        identificador = input("Digite seu CPF ou CRM: ").strip()
        senha = pwinput.pwinput("Senha: ", mask ="*").strip()

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

#Funções de agenda
def mostrar_agenda(usuario):
    if not usuario.get("agenda"): 
        print("📅 Nenhum compromisso agendado.")
        return

    consultas = [c for c in usuario["agenda"] if c["tipo_compromisso"].lower() == "consulta"]
    exames = [c for c in usuario["agenda"] if c["tipo_compromisso"].lower() == "exame"]

    print("\n📌 Consultas")
    if consultas:
        for c in consultas:
            hora = c.get("hora", "") 
            print(f"   {c['data']} {hora} – {c['especialidade']} – Status: {c['status']}")
    else:
        print("   Nenhuma consulta agendada.")

    print("\n📌 Exames")
    if exames:
        for c in exames:
            hora = c.get("hora", "") 
            print(f"   {c['data']} {hora} – {c['especialidade']} – Status: {c['status']}")
    else:
        print("   Nenhum exame agendado.")

def adicionar_compromisso_paciente(usuario):
    print("\n Adicionar Novo Compromisso ")
    while True:
        tipo = input("Tipo de compromisso (Consulta / Exame): ").strip().title()
        if tipo in ["Consulta", "Exame"]:
            break
        else:
            print("❌ Tipo inválido. Escolha 'Consulta' ou 'Exame'.")

    especialidade_exame = input(f"Procurar por especialidade para {tipo} ou nome do exame: ").strip().title()

    if tipo == "Consulta":
        medicos_encontrados = [m for m in medicos if m["especialidade"].lower() == especialidade_exame.lower()]

        if medicos_encontrados:
            print(f"\nMédicos encontrados para {especialidade_exame}:")
            for idx, m in enumerate(medicos_encontrados, 1):
                print(f"{idx} - {m['nome']} ({m['especialidade']})")
            
            while True:
                escolha_medico_idx = input("Escolha o número do médico: ").strip()
                if escolha_medico_idx.isdigit() and 1 <= int(escolha_medico_idx) <= len(medicos_encontrados):
                    medico_escolhido = medicos_encontrados[int(escolha_medico_idx) - 1]
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")

            if not medico_escolhido["horarios_disponiveis"]:
                print("⚠️ Nenhum horário disponível para este médico.")
                return
            
            print("\nHorários disponíveis:")
            for idx, h in enumerate(medico_escolhido["horarios_disponiveis"], 1):
                print(f"{idx} - {h}")

            while True:
                escolha_horario = input("Escolha o número do horário desejado: ").strip()
                if escolha_horario.isdigit() and 1 <= int(escolha_horario) <= len(medico_escolhido["horarios_disponiveis"]):
                    horario_escolhido = medico_escolhido["horarios_disponiveis"].pop(int(escolha_horario)-1)
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")

            # Garante que 'agenda' é uma lista
            if "agenda" not in usuario:
                usuario["agenda"] = []

            usuario["agenda"].append({
                "tipo_compromisso": tipo,
                "data": horario_escolhido.split()[0],
                "hora": horario_escolhido.split()[1],
                "especialidade": medico_escolhido["especialidade"],
                "medico": medico_escolhido["nome"],
                "status": "Confirmada"
            })

            print(f"✅ Consulta agendada com sucesso com {medico_escolhido['nome']} em {horario_escolhido}!")
            # Atualiza o arquivo de usuários após adicionar o compromisso
            atualizar_usuario_no_arquivo(usuario)
        else:
            print("⚠️ Nenhum médico encontrado com essa especialidade.")

    elif tipo == "Exame":
        data_exame = input("Data do exame (DD/MM/YYYY): ").strip()
        status_exame = input("Status do exame (Agendado / Resultado em análise): ").strip().title()

        if "agenda" not in usuario:
            usuario["agenda"] = []

        usuario["agenda"].append({
            "tipo_compromisso": tipo,
            "data": data_exame,
            "hora": "", # Exames geralmente não têm hora específica no agendamento inicial
            "especialidade": especialidade_exame, # Aqui 'especialidade_exame' é o nome do exame
            "status": status_exame
        })
        print(f"✅ Exame de {especialidade_exame} adicionado com sucesso para {data_exame}!")
        # Atualiza o arquivo de usuários após adicionar o compromisso
        atualizar_usuario_no_arquivo(usuario)
.....
def atualizar_usuario_no_arquivo(usuario_a_atualizar):
    """Sobrescreve o arquivo 'usuarios.json' com as informações atualizadas de todos os usuários."""
    usuarios_existentes = []
    try:
        with open("usuarios.json", "r") as f:
            for linha in f:
                usuarios_existentes.append(json.loads(linha))
    except FileNotFoundError:
        pass # Se o arquivo não existe, a lista permanece vazia

    # Encontra e atualiza o usuário na lista
    for i, u in enumerate(usuarios_existentes):
        if u["id"] == usuario_a_atualizar["id"]:
            usuarios_existentes[i] = usuario_a_atualizar
            break
    else: # Se o usuário não foi encontrado (caso de um novo cadastro sem ter lido antes)
        usuarios_existentes.append(usuario_a_atualizar)

    # Reescreve o arquivo com a lista atualizada de usuários
    with open("usuarios.json", "w") as f:
        for u in usuarios_existentes:
            f.write(json.dumps(u) + "\n")

# --- Funções de Perfil (adaptadas) ---
def configurar_perfil_paciente(usuario):
    print("\n--- Configurar Perfil Pessoal ---")
    # Usa os dados existentes do usuário como padrão
    perfil = usuario.get("perfil", {}) # Pega o perfil existente ou um dicionário vazio
    
    print(f"Nome completo: {usuario['nome']}") # Nome já vem do cadastro
    print(f"CPF: {usuario['id']}") # CPF já vem do cadastro

    idade = input(f"Idade ({perfil.get('idade', 'Não informado')}): ").strip()
    perfil['idade'] = int(idade) if idade.isdigit() else perfil.get('idade', None)

    genero = input(f"Gênero ({perfil.get('genero', 'Não informado')}): ").strip().title()
    perfil['genero'] = genero if genero else perfil.get('genero', None)

    endereco = input(f"Endereço ({perfil.get('endereco', 'Não informado')}): ").strip().title()
    perfil['endereco'] = endereco if endereco else perfil.get('endereco', None)

    while True:
        contato = input(f"Telefone para contato (11 dígitos, ex: 11987654321) ({perfil.get('contato_raw', 'Não informado')}): ").strip()
        if contato.isdigit() and len(contato) == 11:
            perfil['contato_raw'] = contato # Salva o número puro
            perfil['contato_formatado'] = f"({contato[:2]}) {contato[2:7]}-{contato[7:]}"
            print("📞 Telefone salvo:", perfil['contato_formatado'])
            break
        elif not contato: # Permite pular se o usuário não quiser alterar
            print("Telefone não alterado.")
            break
        else:
            print("❌ Telefone inválido! Digite apenas números e use 11 dígitos.")
    
    medicamentos_str = perfil.get('medicamentos', 'Nenhum')
    usa_medicamentos = input(f"Faz uso de medicamentos contínuos? (sim/não) ({'sim' if medicamentos_str != 'Nenhum' else 'não'}): ").strip().lower()
    if usa_medicamentos == "sim":
        medicamentos = input(f"Quais medicamentos você utiliza? ({medicamentos_str}): ").strip()
        perfil['medicamentos'] = medicamentos if medicamentos else medicamentos_str
    else:
        perfil['medicamentos'] = "Nenhum"

    preferencia_de_contato_str = perfil.get('preferencia_de_contato', 'Não informado')
    preferencia_de_contato = input(f"Por onde devemos entrar em contato (e-mail, telefone ou app) ({preferencia_de_contato_str}): ").strip().lower()
    
    if preferencia_de_contato in ["e-mail", "email"]:
        while True:
            email_contato = input(f"Digite seu e-mail para contato ({perfil.get('email_contato', 'Não informado')}): ").strip()
            if "@" in email_contato and "." in email_contato: # Validação básica de e-mail
                perfil['email_contato'] = email_contato
                perfil['meio_contato_detalhado'] = f"E-mail: {email_contato}"
                perfil['preferencia_de_contato'] = "E-mail"
                print("📩 Preferência de contato registrada:", perfil['meio_contato_detalhado'])
                break
            elif not email_contato: # Permite pular
                print("E-mail não alterado.")
                break
            else:
                print("❌ E-mail inválido! Certifique-se de incluir '@' e '.'.")
    elif preferencia_de_contato == "telefone":
        if perfil.get('contato_formatado'):
            perfil['meio_contato_detalhado'] = f"Telefone: {perfil['contato_formatado']}"
            perfil['preferencia_de_contato'] = "Telefone"
            print("📩 Preferência de contato registrada:", perfil['meio_contato_detalhado'])
        else:
            print("⚠️ Telefone não informado no perfil. Por favor, preencha o telefone primeiro.")
    elif preferencia_de_contato == "app":
        perfil['meio_contato_detalhado'] = "App (notificações internas)"
        perfil['preferencia_de_contato'] = "App"
        print("📩 Preferência de contato registrada:", perfil['meio_contato_detalhado'])
    elif not preferencia_de_contato: # Permite pular
        print("Preferência de contato não alterada.")
    else:
        perfil['meio_contato_detalhado'] = "Não informado"
        perfil['preferencia_de_contato'] = "Não informado"
        print("Preferência de contato inválida ou não informada.")

    while True:
        print("\n🔒 Termos de privacidade: Seus dados serão usados apenas para fins clínicos, conforme a LGPD.\n")
        aceitou_termos = input("Você aceita os termos de privacidade (sim/não): ").strip().lower()
        if aceitou_termos == "sim":
            perfil['aceitou_termos'] = True
            print("✅ Termos aceitos! Vamos continuar...")
            break
        else:
            print("⚠️ Você deve aceitar os termos para continuar.\n")
            perfil['aceitou_termos'] = False # Mantém como False se não aceitar

    usuario["perfil"] = perfil # Atualiza o perfil no objeto usuário
    atualizar_usuario_no_arquivo(usuario) # Salva as alterações no arquivo

    print("\n--- Dados do Perfil ---")
    print(f"Nome: {usuario['nome']}")
    print(f"CPF: {usuario['id']}")
    for key, value in perfil.items():
        if key not in ['contato_raw', 'aceitou_termos']: # Não exibe esses campos brutos
            print(f"{key.replace('_', ' ').title()}: {value if value is not None else 'Não informado'}")
    print("\n✅ Perfil finalizado e salvo com sucesso! Voltando ao MENU PACIENTE...")


# --- Fluxo principal de login/cadastro ---
if opcao_inicial == "2":
    usuario_encontrado = cadastro()
elif opcao_inicial == "1":
    usuario_encontrado = login()
    # Se o login falhar e o usuário decidir cadastrar, `login()` já cuida disso.
    # Se o login falhar e o usuário não cadastrar (e retornar None), isso será tratado no loop do menu principal.

# --- Menu do paciente ---
if usuario_encontrado and usuario_encontrado["tipo"] == "paciente":
    while True:
        print("\n--- MENU PACIENTE ---")
        print("1 - Perfil pessoal")
        print("2 - Agenda")
        print("3 - Resultados e documentos ")
        print("4 - Comunicação segura ")
        print("5 - Módulos educacionais")
        print("6 - Notificações")
        print("7 - Privacidade")
        print("0 - Sair")

        escolha_menu_principal = input("\nEscolha uma opção: ").strip()

        if escolha_menu_principal == "1":
            configurar_perfil_paciente(usuario_encontrado)
        elif escolha_menu_principal == "2":
            while True:
                print("\n--- AGENDA DO PACIENTE ---")
                print("1 - Ver agenda")
                print("2 - Adicionar compromisso")
                print("0 - Voltar ao menu principal")

                opcao_agenda = input("Escolha uma opção: ").strip()
                if opcao_agenda == "1":
                    mostrar_agenda(usuario_encontrado)
                elif opcao_agenda == "2":
                    adicionar_compromisso_paciente(usuario_encontrado)
                elif opcao_agenda == "0":
                    break
                else:
                    print("❌ Opção inválida! Tente novamente.")
        elif escolha_menu_principal == "0":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida! Por favor, escolha uma opção válida do menu.")