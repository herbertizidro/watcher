
#cria o banco, a tabela e guarda os dados
def inserirDadosBD():
    try:
        conexao = sqlite3.connect("emailUsuario.sqlite3")
        consulta = conexao.cursor()
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
