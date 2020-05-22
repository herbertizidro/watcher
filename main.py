import time
import getpass
import sqlite3
from watcher import *

#autor: Herbert Izidro

def inserirDadosBD():
    #cria o banco e a tabela, valida as informações e insere
    try:
        conectar = sqlite3.connect("emailUsuario.sqlite3")
        consulta = conectar.cursor()

        sql = """CREATE TABLE IF NOT EXISTS email(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                emRemetente VARCHAR(50) NOT NULL, senRemetente VARCHAR(50) NOT NULL,
                emDestinatario VARCHAR(50) NOT NULL)"""
            
        print(nome)            
        emRemetente = input("\n [+] Seu e-mail: ").lower()
        verif = validarEmail(emRemetente)
        while verif == 0:
            print("  >> E-mail inválido! <<")
            emRemetente = input(" [+] Seu e-mail: ").lower()
            verif = validarEmail(emRemetente)

        emRemetente = bs64(emRemetente)        
                                    
        senRemetente = getpass.getpass(" [+] Sua senha: ")
        if senRemetente != "":            
            senRemetente = bs64(senRemetente)

        emDestinatario = input(" [+] E-mail destinatário: ").lower()
        verif = validarEmail(emDestinatario)
        while verif == 0:
            print("  >> E-mail destinatário inválido! <<")
            emDestinatario = input(" [+] E-mail destinatário: ").lower()
            verif = validarEmail(emDestinatario)

        emDestinatario = bs64(emDestinatario)
                        
        if consulta.execute(sql):
            pass
                
        argumentos = (emRemetente, senRemetente, emDestinatario)
                
        sql = """INSERT INTO email(emRemetente, senRemetente, emDestinatario)VALUES (?, ?, ?)"""        
        if consulta.execute(sql, argumentos):
            conectar.commit()
            print("\n [!] Dados inseridos com sucesso!")
            time.sleep(2)
            consulta.close()
            conectar.close()

    except Exception as erro:
        print("\n [x] Um erro ocorreu, consulte o log.")
        Watcher.LOG(" inserirDadosBD ", erro)
        time.sleep(2)
        return False
        

def menu():
    conectar = sqlite3.connect("emailUsuario.sqlite3")
    consulta = conectar.cursor()

    while True:
        try:
            consulta.execute("SELECT * FROM email")
        except sqlite3.OperationalError:
            if inserirDadosBD() == False:
                break
            
        limpatela()
        print(nome)
        obterDados = consulta.execute("SELECT emRemetente FROM email")
        aux_emR = ""
        for o in obterDados:
            aux_emR = bs64_decode(str(o))

        obterDados = consulta.execute("SELECT emDestinatario FROM email")
        aux_emD = ""
        for o in obterDados:
            aux_emD = bs64_decode(str(o))
            
        print("\n [*] E-mail remetente:", aux_emR)
        print(" [*] E-mail destinatário:", aux_emD)
        print("\n  >> OPÇÕES:\n\n [+] 1 - Atualizar e-mail remetente\n [+] 2 - Atualizar senha remetente\n [+] 3 - Atualizar e-mail destinatário\n [+] 4 - Iniciar detecção de movimentos\n [+] 5 - Sair")
        opcao = input(" [+]---> ")
        
        if opcao not in ["1", "2", "3", "4", "5"]:
            print("\n [x] Opção inválida!")
            time.sleep(2)
                
        elif opcao == "1":
            obterEmRem = consulta.execute("SELECT emRemetente FROM email")
            limpatela()
            print(nome)
            aux = ""
            for o in obterEmRem:
                aux = bs64_decode(str(o))

            print("\n [*] E-mail remetente atual:", aux)
            novoEmRem = input(" [+] Novo e-mail remetente: ").lower()

            verif = validarEmail(novoEmRem)
            while verif == 0:
                print("  >> E-mail inválido! <<")
                novoEmRem = input(" [+] Novo e-mail remetente: ").lower()
                verif = validarEmail(novoEmRem)
            novoEmRem = bs64(novoEmRem)

            consulta.execute("UPDATE email SET emRemetente = ?", (novoEmRem,))
            conectar.commit()
            print("\n [!] E-mail remetente atualizado com sucesso!")
            time.sleep(2)

        elif opcao == "2":
            limpatela()
            print(nome)
            novaSenRem = getpass.getpass("\n [+] Nova senha: ")

            while novaSenRem == "":
                print("  >> Senha inválida! <<")
                novaSenRem = getpass.getpass(" [+] Nova senha: ")
            novaSenRem = bs64(novaSenRem)

            consulta.execute("UPDATE email SET senRemetente = ?", (novaSenRem,))
            conectar.commit()
            print("\n [!] Senha atualizada com sucesso!")
            time.sleep(2)

        elif opcao == "3":
            obterEmDes = consulta.execute("SELECT emDestinatario FROM email")
            limpatela()
            print(nome)
            aux = ""
            for o in obterEmDes:
                aux = bs64_decode(str(o))

            print("\n\n [*] E-mail destinatário atual:", aux)
            novoEmDes = input(" [+] Novo e-mail destinatário: ").lower()
                
            verif = validarEmail(novoEmDes)
            while verif == 0:
                print("  >> E-mail inválido! <<")
                novoEmDes = input(" [+] Novo e-mail destinatário: ").lower()
                verif = validarEmail(novoEmDes)
            novoEmDes = bs64(novoEmDes)

            consulta.execute("UPDATE email SET emDestinatario = ?", (novoEmDes,))
            conectar.commit()
            print("\n [!] E-mail destinatário atualizado com sucesso!")
            time.sleep(2)

        elif opcao == "4":        
            alerta_status = True
            ativarAlerta = input("\n [+] Deseja ativar o alerta[1-Sim|2-Não]? ")
            aux_senR = ""            
            if ativarAlerta == "1":
                obterDados = consulta.execute("SELECT senRemetente FROM email")
                for o in obterDados:
                    if str(o) == "('',)":
                        aux_senR = getpass.getpass(" [+] Informe a senha do e-mail remetente: ")
                    else:
                        aux_senR = bs64_decode(str(o))
            else:
                alerta_status = False
                        
            obterDados = consulta.execute("SELECT emRemetente FROM email")
            aux_emR = ""
            for o in obterDados:
                aux_emR = bs64_decode(str(o))

            obterDados = consulta.execute("SELECT emDestinatario FROM email")
            aux_emD = ""
            for o in obterDados:
                aux_emD = bs64_decode(str(o))

            duracao_exec = input(" [+] Informe por quantas horas a detecção deve ser executada: ")
            try:
                duracao_exec = 3600 * int(duracao_exec) #ex: 1hr * 5 = total em segundos
                inicio_exec = time.time()
                watcher = Watcher(aux_emR, aux_senR, aux_emD, alerta_status, inicio_exec, duracao_exec)
                while int(time.time() - inicio_exec) < duracao_exec:
                    watcher.detectarMovimento()
            except ValueError:
                print("\n [x] Valor inválido informado!")
                time.sleep(2)
            
        elif opcao == "5":
            consulta.close()
            conectar.close()
            break



if __name__ == "__main__":
        menu()
