import pygame
import random
import sys
import math

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter One-Bit")

# Define as cores em um esquema one-bit (preto e branco)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.set_colorkey(BLACK)  # Define a cor preta como transparente
        self.image.fill(BLACK)  # Preenche a superfície com preto (será transparente)
        # Desenha o triângulo apontando para cima
        pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 30), (50, 30)])
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, WHITE, self.image.get_rect())  # Retângulo simples para o inimigo
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Remove o inimigo quando sai da tela

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, WHITE, self.image.get_rect())  # Tiro simples como retângulo
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  # Remove o tiro quando sai da tela

def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    text = font.render("Press SPACE to Start", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def show_game_over_screen(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)
    
    pygame.display.flip()
    pygame.time.wait(4000)  # Espera 2 segundos para fechar a tela de game over

def main():
    show_start_screen()
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_start = False

    player = Player()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all_sprites.add(player)

    score = 0  # Inicializa a pontuação
    health = 100  # Inicializa a vida do jogador

    font = pygame.font.Font(None, 36)  # Fonte para exibir a pontuação

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets)

        # Spawna inimigos em intervalos aleatórios
        if random.randint(1, 60) == 1:
            enemy = Enemy(random.randint(0, SCREEN_WIDTH - 50), -30)
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Atualiza todas as sprites
        all_sprites.update()

        # Verifica se inimigos ultrapassaram o jogador (saíram da tela)
        for enemy in enemies:
            if enemy.rect.bottom > SCREEN_HEIGHT:
                health -= 10  # Reduz a vida em 10 para cada inimigo que ultrapassa
                if health < 0:
                    health = 0  # Garante que a vida não seja negativa
                enemy.kill()  # Remove o inimigo

        # Verifica colisões entre balas e inimigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        if hits:
            score += len(hits)  # Aumenta a pontuação conforme o número de inimigos destruídos

        # Desenha todas as sprites
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Desenha a pontuação na tela
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Desenha a barra de vida
        pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 30, SCREEN_WIDTH - 20, 20), 2)  # Moldura da barra
        pygame.draw.rect(screen, WHITE, (12, SCREEN_HEIGHT - 28, (SCREEN_WIDTH - 24) * (health / 100), 16))  # Barra de vida

        pygame.display.flip()

        if health <= 0:
            show_game_over_screen(score)
            running = False

        # FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()