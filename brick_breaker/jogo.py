import pygame

# Inicialização
pygame.init()

# Configurações da tela
tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

# Configurações de desempenho
clock = pygame.time.Clock()
FPS = 60  # Limitar a 60 FPS

# Elementos do jogo
tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(0, 750, tamanho_jogador, tamanho_bola)

qtde_blocos_linha = 8
qtde_linhas_bloco = 5
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_bloco

# Cores
cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0),
}

# Variáveis do jogo
fim_jogo = False
pontuacao = 0
movimento_bola = [10, -5]

# Otimização: Criar superfícies para desenho estático
fundo = pygame.Surface(tamanho_tela)
fundo.fill(cores["preta"])

# Função para criar blocos (mantida igual)
def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10
    blocos = []
    
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), 
                               j * distancia_entre_linhas, 
                               largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos

# Funções otimizadas
def movimentar_jogador():
    keys = pygame.key.get_pressed()  # Verifica estado das teclas continuamente
    if keys[pygame.K_RIGHT] and (jogador.x + tamanho_jogador) < tamanho_tela[0]:
        jogador.x += 10
    if keys[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= 10

def movimentar_bola(bola):
    global pontuacao
    
    bola.x += movimento_bola[0]
    bola.y += movimento_bola[1]

    # Colisão com paredes
    if bola.left <= 0 or bola.right >= tamanho_tela[0]:
        movimento_bola[0] = -movimento_bola[0]
    if bola.top <= 0:
        movimento_bola[1] = -movimento_bola[1]
    if bola.bottom >= tamanho_tela[1]:
        return False  # Fim de jogo

    # Colisão com jogador
    if bola.colliderect(jogador):
        movimento_bola[1] = -abs(movimento_bola[1])  # Garante que a bola suba

    # Colisão com blocos (otimizada)
    for bloco in blocos[:]:  # Cria cópia para poder remover itens
        if bola.colliderect(bloco):
            blocos.remove(bloco)
            movimento_bola[1] = -movimento_bola[1]
            pontuacao += 1
            break  # Sai após primeira colisão

    return True

def desenhar_tela():
    tela.blit(fundo, (0, 0))  # Limpa tela com superfície pré-renderizada
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)
    
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)
    
    # Pontuação
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", True, cores["amarela"])
    tela.blit(texto, (10, 760))
    
    pygame.display.flip()

# Inicialização dos blocos
blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_bloco)

# Game loop principal
while not fim_jogo:
    # Controle de FPS
    clock.tick(FPS)
    
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True
    
    # Atualizações
    movimentar_jogador()
    
    if not movimentar_bola(bola):
        fim_jogo = True
    
    if pontuacao >= qtde_total_blocos:
        fim_jogo = True
    
    # Desenho
    desenhar_tela()

pygame.quit()