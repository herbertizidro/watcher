#codifica os dados - só uma 'firula' mesmo
def bs64(param) -> str:
    cod_x = base64.b64encode(param.encode())
    cod_x = str(cod_x).replace("b'","").replace("'","")                       
    return cod_x

#decodifica os dados
def bs64Decode(param) -> str:
    cod_x = base64.b64decode(param.encode())
    cod_x = str(cod_x).replace("b'","").replace("'","")                      
    return cod_x
        
#verifica se o e-mail está de acordo com o padrão
def validarEmail(email) -> str:
    aux = 0
    while aux == 0:
        padrao = re.findall("[^a-zA-Z0-9]", email)
        if "@" in padrao and "." in padrao:
            aux = 1
            return email
        else:            
            print("  >> E-mail inválido! <<")
            email = input(" [+] Informe o e-mail novamente: ").lower()  

#exibe os e-mails - recebe a variável de consulta e a coluna da tabela
def emailAtual(consulta, coluna) -> str:
    email = consulta.execute("SELECT " + coluna + " FROM email")
    aux = ""
    for e in email:
        aux = bs64Decode(str(e))
    return aux

#atualiza os e-mails - recebe as variáveis de conexão e consulta, a coluna da tabela e o tipo de e-mail(remetente ou destinatário)
def atualizaEmail(conexao, consulta, coluna, tipo_email):
    novo_email = input(" [+] Novo e-mail " + tipo_email + ": ").lower()    
    verif = validarEmail(novo_email)
    novo_email = bs64(verif)    
    consulta.execute("UPDATE email SET " + coluna + " = ?", (novo_email,))
    conexao.commit()
    print("\n [!] E-mail " + tipo_email + " atualizado com sucesso!")
    time.sleep(2)
