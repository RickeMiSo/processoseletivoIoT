### Identificação do Candidato

- **Nome completo**: Henrique Soares de Souza
- **GitHub**: RickeMiSo (pessoal) / HenriqueSoaresSouza (institucional - UNIVASF)

---

## Visão Geral da Solução

O objetivo do projeto foi simular um ambiente de contagem de pecas, ou outros objetos em uma esteira. Para tanto, o sistema usa um sensor de luz (fotorresistor) para detectar se um objeto passa por sua frente, e realiza a contagem pra cada objeto que passa, e também avisa caso ocorra um gargalo (o objeto permanece na frente do sensor por um tempo extenso). O usuário pode interagir com o sistema simulado de duas formas: Ajustando a "luz" que o sensor detecta (em unidades lux), e ativando o reinício da contagem, zerando a mesma com um botão.

---

## Arquitetura do Sistema Embarcado

O fluxo do programa se dá na seguinte forma:
- Importação das bibliotecas usadas
- Definição de variáveis globais (bandeiras, timer, contador de objetos, tempo de debounce) e configuração dos pinos
- Definição de funções de callback, ISRs, e função de verificação principal
- Loop principal

Os estados relevantes foram categorizados pelas variáveis bandeira, com utilização extensa de callbacks entre os componentes e funções de interrupt para eventos como o botão sendo pressionado e o timer passando de seu limite.

---

## Componentes Utilizados na Simulação

Foram usados:
- Placa de borda ESP32 DevKit C v4 (comum), que realiza a manipulação dos dados obtidos pelo sensor e a lógica sistema.
- Sensor de luminosidade (LDR), que coleta os dados (luminosidade) para ser analisado pela placa.
- Botão pushdown, operando com pull-up, para o usuário realizar o zeramento da contagem realizada pelo sistema.
- Interface UART (Saída Serial), para telemetria e transmissão de dados e logs.

---

## Decisões Técnicas Relevantes

O código foi organizado de forma predominantemente funcional, com o sistema sendo dividido em várias tarefas pequenas e específicas; diversas funções foram definidas, assim como callbacks e ISRs. Usaram-se variáveis globais para armazenar estados de eventos (como o pressionamento do botão, início do timer para identificar gargalo, entre outros). Optou-se por uma abordagem que envolveu callbacks e interrupts para lidar os eventos.

Usou-se apenas a saída digital do sensor LDR, que dá output 1 se lux<=100, e 0 caso lux>=100. Isso serviu o propósito de informar se um objeto passa pela esteira na frente do sensor.

---

## Resultados Obtidos

O projeto funciona satisfatoriamente para os requisitos explorados (contagem de objetos em esteira hipotética e alerta de gargalo). Todos os componentes funcionam corretamente, desde o sensor (permitindo escolhas de valores de iluminação simulados), o botão (com tratamento para bounce), a placa e a interface serial. 

A simulação Wokwi funcionou exatamente como previsto; deslizando lux para valores <=100, o sistema captou a luminosidade baixa, e caso o lux seja deslizado para um valor >100. E se permanecer no valor baixo por pelo menos 5 segundos, manda um alerta por meio da saída serial.

---

## Comentários Adicionais (Opcional)

Dentre as dificuldades encontradas no decorrer do projeto, um desafio que se destacou foi encontrar uma boa abordagem para lidar com eventos, e aplicá-la no código de forma eficiente. A solução que encontrei provavelmente possui redundâncias e um uso muito abrangente de variáveis globais, que seriam questões que eu tentaria melhorar caso usufruísse de mais tempo e um domínio maior.

Apesar dessas limitações, o projeto serviu como um passo importante para verdadeiramente entender políticas de "event handling", como usar callbacks de forma extremamente útil, assim como lidar com múltiplos estados diferentes de eventos.

---
