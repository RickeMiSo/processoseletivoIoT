import machine
from machine import Pin, Timer
import time

pin_botao = machine.Pin(14, Pin.IN, Pin.PULL_UP)
pin_ldr_do = machine.Pin(34, Pin.IN)

# Variável de bandeira para interrupção
botao_pressionado = False

# Variável de bandeira para gargalo
gargalo = False

# Variável de bandeira para Timer ativo
timer_ativo = False

# Variável de contagem
pecas = 0

# Variáveis para controle de debounce não bloqueante
tempo_ultimo_interrupt = 0
DEBOUNCE_DELAY = 200 # em ms

# Instanciamento do timer para uso na contagem de pecas e detecção de gargalos
timer = Timer(0)


# ISR com tratamento de debounce para o botão de reset
def interruption_handler(pino_interruptor):
    global botao_pressionado
    global tempo_ultimo_interrupt
    tempo_atual = time.ticks_ms()
    if time.ticks_diff(tempo_atual, tempo_ultimo_interrupt) > DEBOUNCE_DELAY:
        if botao_pressionado == False:
            botao_pressionado = True
            tempo_ultimo_interrupt = tempo_atual


# Função que verifica o estado do sensor a cada ciclo do loop
# principal.
def verificar_estado():
    global timer_ativo
    global gargalo
    global pecas

    luminosidade_baixa = (pin_ldr_do.value() == 1)
    
    # Se a luminosidade estiver baixa, o timer é ativado
    # com um tempo de 4 segundos.
    if luminosidade_baixa and not timer_ativo:
        timer.init(
            period = 5000,
            mode = Timer.ONE_SHOT,
            callback = timer_handler
        )
        timer_ativo = True

    # Caso o timer esteja ativo, mas a luminosidade volta, ele é desativado
    # e a peca é contabilizada
    elif not luminosidade_baixa and timer_ativo:
        timer.deinit()
        timer_ativo = False
        pecas += 1
        print("Peca detectada! Total:", pecas)
        

# ISR do timer de luminosidade
def timer_handler(timer_obj):
    global gargalo
    gargalo = True

print("Contador de Producao Inicializado")

pin_botao.irq(trigger=Pin.IRQ_FALLING, handler=interruption_handler)

while True:
    if botao_pressionado:
        pecas = 0
        botao_pressionado = False
        print("Turno resetado com sucesso. Contadores zerados.")
    
    if gargalo:
        print("Alerta: Micro-parada detectada!")
        gargalo = False
    
    verificar_estado()
