

if __name__ == "__main__":
    
    import time
    import sqlite3
    import getpass

    from watcher import *
    from cria_db import *
    from funcoes import *

    conexao = sqlite3.connect("emailUsuario.sqlite3")
    consulta = conexao.cursor()

    while True:
        
        try:
            consulta.execute("SELECT * FROM email")
        except sqlite3.OperationalError:
            break
            
        limpatela()
        print(nome)        
        print("\n [*] E-mail remetente:", emailAtual(consulta, "emRemetente"))
        print(" [*] E-mail destinatário:", emailAtual(consulta, "emDestinatario"))
        print("\n  >> OPÇÕES:\n\n [+] 1 - Atualizar e-mail remetente\n [+] 2 - Atualizar e-mail destinatário\n [+] 3 - Iniciar detecção de movimentos\n [+] 4 - Sair")
        opcao = input(" [+]---> ")
                
        if opcao == "1":
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
                limpatela()
                break
            except ValueError:
                print("\n [x] Valor inválido informado!")
                time.sleep(2)
            
        elif opcao == "4":
            limpatela()
            consulta.close()
            conexao.close()
            break
            
        else:
            print("\n [x] Opção inválida!")
            time.sleep(2)


