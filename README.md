Necessário:
 - Instale opencv-python e yagmail
 
Execução:
 - Abra o cmd na pasta do script e execute o comando "python main.py"

O que faz:

Inicia a câmera e aguarda um movimento.
Quando detectado, tenta encontrar um rosto(frontal) ou corpo(parte superior/tronco) no frame.
Se encontrar, marca com um retângulo o rosto ou corpo e salva o frame para enviar por e-mail.
Após isso a câmera deve gravar durante 1 minuto(esse tempo pode ser modificado na variável "cronometro_limite").
Você define por quanto tempo esse processo será repetido.

Para receber o frame por e-mail é necessário que você salve seu e-mail remetente e seu e-mail destinatário no banco de dados. A senha logicamente é opcional. O envio de e-mail também é opcional, antes de iniciar a detecção de movimentos você será questionado se deseja ativá-lo.

Então, em resumo, você salva seus e-mails no banco de dados e escolhe a opção referente à detecção de movimentos(opção 4 do menu), informando logo em seguida se quer receber o frame por e-mail e por quantas horas a detecção deve ser executada.

OBS:
 - A iluminação do ambiente pode afetar o desempenho.
