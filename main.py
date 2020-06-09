import re
import time
import base64
import getpass
import sqlite3
from watcher import *


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

#cria o banco, a tabela e guarda os dados
def inserirDadosBD():
    try:
        conexao = sqlite3.connect("emailUsuario.sqlite3")
        consulta = conectar.cursor()
        sql = "CREATE TABLE IF NOT EXISTS email(emRemetente VARCHAR(50) NOT NULL, emDestinatario VARCHAR(50) NOT NULL)"
            
        limpatela()
        print(nome)
        
        emRemetente = input("\n [+] Seu e-mail: ").lower()    
        verif = validarEmail(emRemetente)
        emRemetente = bs64(verif)        

        emDestinatario = input(" [+] E-mail destinatário: ").lower()
        verif = validarEmail(emDestinatario)
        emDestinatario = bs64(verif)
                        
        if consulta.execute(sql): pass              
        argumentos = (emRemetente, emDestinatario)                
        sql = """INSERT INTO email(emRemetente, emDestinatario)VALUES (?, ?)"""        
        if consulta.execute(sql, argumentos):
            conexao.commit()
            print("\n [!] Dados inseridos com sucesso!")
            time.sleep(2)
            consulta.close()
            conexao.close()

    except Exception as erro:
        print("\n [x] Um erro ocorreu, consulte o log.")
        Watcher.LOG(" inserirDadosBD ", erro)
        time.sleep(2)
        return False 


if __name__ == "__main__":

    conexao = sqlite3.connect("emailUsuario.sqlite3")
    consulta = conectar.cursor()

    while True:
        
        try:
            consulta.execute("SELECT * FROM email")
        except sqlite3.OperationalError:
            if inserirDadosBD() == False:
                break
            
        limpatela()
        print(nome)        
        print("\n [*] E-mail remetente:", emailAtual(consulta, "emRemetente"))
        print(" [*] E-mail destinatário:", emailAtual(consulta, "emDestinatario"))
        print("\n  >> OPÇÕES:\n\n [+] 1 - Atualizar e-mail remetente\n [+] 2 - Atualizar e-mail destinatário\n [+] 3 - Iniciar detecção de movimentos\n [+] 4 - Sair")
        opcao = input(" [+]---> ")
        
        if opcao not in ["1", "2", "3", "4"]:
            print("\n [x] Opção inválida!")
            time.sleep(2)
                
        elif opcao == "1":
            limpatela()
            print(nome) 
            print("\n [*] E-mail remetente atual:", emailAtual(consulta, "emRemetente"))
            atualizaEmail(conexao, consulta, "emRemetente", "remetente")

        elif opcao == "2":
            limpatela()
            print(nome) 
            print("\n [*] E-mail destinatário atual:", emailAtual(consulta, "emDestinatario"))
            atualizaEmail(conexao, consulta, "emDestinatario", "destinatário")

        elif opcao == "3":
            senha_remetente = ""
            alerta = False          
            if input("\n [+] Deseja ativar o alerta[1-Sim|2-Não]? ") == "1":
                alerta = True
                senha_remetente = getpass.getpass(" [+] Informe a senha do e-mail remetente: ")
                        
            email_remetente = emailAtual(consulta, "emRemetente")
            email_destinatario = emailAtual(consulta, "emDestinatario")

            duracao_exec = input(" [+] Informe por quantas horas a detecção deve ser executada: ")
            try:
                duracao_exec = 3600 * int(duracao_exec) #ex: 1hr * 5 = total em segundos
                inicio_exec = time.time()
                watcher = Watcher(email_remetente, senha_remetente, email_destinatario, alerta, inicio_exec, duracao_exec)
                while int(time.time() - inicio_exec) < duracao_exec:
                    watcher.detectarMovimento()
            except ValueError:
                print("\n [x] Valor inválido informado!")
                time.sleep(2)
            
        elif opcao == "4":
            consulta.close()
            conexao.close()
            break
            
