
if __name__ != "__main__":

    import os
    import cv2
    import time
    import yagmail
    import numpy as np
    from PIL import Image
    
    from funcoes import limpatela
   
    global nome
    nome = "\n | W A T C H E R |\n"

    #detecção de movimentos, envio de e-mail, captura de vídeo e registro de erros
    class Watcher():
        #inicialização dos atributos
        def __init__(self, email, senha, emailD, alerta_status, inicio_exec, duracao_exec):
            self.__email_remetente = email
            self.__senha_remetente = senha
            self.__email_destinatario = emailD
            self.__alerta_status = alerta_status
            self.inicio_exec = inicio_exec
            self.duracao_exec = duracao_exec

        @staticmethod
        def LOG(local, erro):  #gera o log com os erros para facilitar a manutenção
            data_hora = time.strftime('%d/%m/%Y - %H:%M:%S')
            with open("logErros.txt", "a") as arq:
                arq.write("\n\n" + data_hora + local + str(erro))
                
        #envia uma amostra(imagem) da detecção por e-mail
        def __emitirAlerta(self):
            try:
                deteccao_img = [yagmail.inline("./amostra.jpg")]
                yag = yagmail.SMTP(self.__email_remetente, self.__senha_remetente)
                yag.send(self.__email_destinatario, "WATCHER - Frontal ou corpo detectado", deteccao_img)
                os.remove("./amostra.jpg")
            except Exception as erro:
                Watcher.LOG(" Watcher.emitirAlerta ", erro)

        
        def __gravarVideo(self): #grava vídeos de 1 minuto
            try:
                print(" [*] Gravando ...")
                cronometro_limite = 60 #60 segundos - modificar aqui para aumentar ou diminuir
                cap = cv2.VideoCapture(0)
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                nome_video = time.strftime("%d%m%Y%H%M%S") + ".avi"
                video = cv2.VideoWriter(nome_video, fourcc, 20.0, (640,480))
                cronometro_inicio = time.time()
                while int(time.time() - cronometro_inicio) < cronometro_limite:
                    ret, frame = cap.read()
                    if ret == True:
                        video.write(frame)
                cap.release()
                video.release()
            except Exception as erro:
                Watcher.LOG(" Watcher.gravarVideo ", erro)

        #detecta os movimentos e identifica o frontal ou corpo no frame
        def detectarMovimento(self):
            try:
                limpatela()
                print(nome)
                print(" [*] Detecção de movimentos iniciada.")
                cap = cv2.VideoCapture(0)
                sub_fundo = cv2.createBackgroundSubtractorMOG2(300, 400, True)
                cont_frame = 0
                while int(time.time() - self.inicio_exec) < self.duracao_exec:
                    ret, frame = cap.read()
                    cont_frame += 1	
                    frame_redimensionado = cv2.resize(frame, (0, 0), fx = 0.90, fy = 0.90)
                    masc = sub_fundo.apply(frame_redimensionado)
                    cont_pixel = np.count_nonzero(masc)
                    # cont_pixel > 10 - determina quantos pixels são considerados "movimento"
                    if(cont_frame > 1 and cont_pixel > 50):
                        #detecção de frontal e corpo a seguir
                        frontal_face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                        corpo_sup_cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")
                        frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        
                        frontal = frontal_face_cascade.detectMultiScale(frame_cinza, 1.3, 5)
                        corpo_sup = corpo_sup_cascade.detectMultiScale(frame_cinza, 1.3, 5)
                        
                        #configuração para a inserção de texto e marcação de face ou corpo
                        fonte = cv2.FONT_HERSHEY_SIMPLEX
                        coordenadas = (00, 50)
                        escala_fonte = 1
                        cor = (0, 255, 0)
                        espessura_linha = 2
                        
                        if len(frontal) > 0:
                            cap.release()
                            print(" [*] Frontal detectado!")
                            if self.__alerta_status == True:
                                for(x, y, w, h) in frontal:
                                    cv2.rectangle(frame, (x,y), (x+w, y+h), cor, espessura_linha) #desenha o retangulo no rosto encontrado
                                cv2.putText(frame, "frontal", coordenadas, fonte, escala_fonte, cor, espessura_linha)
                                cv2.imwrite("amostra.jpg", frame)
                                self.__emitirAlerta()
                            self.__gravarVideo()
                            
                        elif len(corpo_sup) > 0:
                            cap.release()
                            print(" [*] Corpo detectado!")
                            if self.__alerta_status == True:
                                for(x, y, w, h) in corpo_sup:
                                    cv2.rectangle(frame, (x,y), (x+w, y+h), cor, espessura_linha) #desenha o retangulo no corpo encontrado
                                cv2.putText(frame, "corpo(superior)", coordenadas, fonte, escala_fonte, cor, espessura_linha)
                                cv2.imwrite("amostra.jpg", frame)
                                self.__emitirAlerta()
                            self.__gravarVideo()
                           
                        else:
                            continue

            except Exception as erro:
                if "(-215:Assertion failed) !ssize.empty() in function 'cv::resize'" in str(erro):
                    pass
                else:
                    Watcher.LOG(" Watcher.detectarMovimentos ", erro)


