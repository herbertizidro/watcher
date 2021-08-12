
Necessário:
 - Instale opencv-python e yagmail
 
Execução:
 - Abra o cmd na pasta do script e execute o comando "python main.py"

O que faz:

Inicia a câmera e aguarda um movimento(opção 3 do menu).
Quando detectado, tenta encontrar um rosto(frontal) ou corpo(parte superior/tronco) no frame.
Se encontrar, marca com um retângulo o rosto ou corpo e salva o frame para enviar por e-mail.
Após isso, a câmera deve gravar durante 1 minuto(esse tempo pode ser modificado na variável "cronometro_limite" do método "gravarVideo").
Você define por quanto tempo esse processo será repetido.

Para receber o frame por e-mail é necessário que você salve seu e-mail remetente e seu e-mail destinatário no banco de dados. A senha é pedida antes da detecção começar, se o envio de e-mail for habilitado. O script não salva a senha no banco, armazena em memória.

OBS:
 - A iluminação do ambiente pode afetar o desempenho.
