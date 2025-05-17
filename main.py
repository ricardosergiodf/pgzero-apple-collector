import pgzrun
import random
import math
from pygame import Rect

# Constantes
WIDTH = 800
HEIGHT = 600
TITLE = "Apple Collector"

# Estados do jogo
MENU = "menu"
GAME = "game"
GAME_OVER = "game_over"
game_state = MENU

# Classe de animação para gerenciamento de sprites


class AnimatedSprite:
    def __init__(self, base_name, frames, animation_delay=5):
        self.frames = [f"{base_name}{i}" for i in range(frames)]
        self.current_frame = 0
        self.animation_delay = animation_delay
        self.frame_counter = 0
        self.is_moving = False

    def update(self, is_moving=False):
        self.is_moving = is_moving
        self.frame_counter += 1
        if self.frame_counter >= self.animation_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]

# Configuração do jogador


class Player:
    def __init__(self, x, y):
        self.actor = Actor('hero_idle0')
        self.actor.pos = (x, y)
        self.idle_animation = AnimatedSprite('hero_idle', 4)
        self.run_animation = AnimatedSprite('hero_run', 6)
        self.speed = 5
        self.y_velocity = 0
        self.is_jumping = False
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.facing_right = True

    def update(self, is_moving):
        if is_moving:
            self.run_animation.update(True)
            self.actor.image = self.run_animation.get_current_frame()
        else:
            self.idle_animation.update()
            self.actor.image = self.idle_animation.get_current_frame()

        if not self.facing_right:
            self.actor.flip_x = True
        else:
            self.actor.flip_x = False

# Configuração dos inimigos


class Enemy:
    def __init__(self, x, y, patrol_distance=100, platform=None):
        self.actor = Actor('enemy_idle0')
        self.actor.pos = (x, y)
        self.idle_animation = AnimatedSprite('enemy_idle', 4)
        self.run_animation = AnimatedSprite('enemy_run', 6)
        self.speed = 2
        self.direction = -1
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.facing_right = False
        self.platform = platform  # Guarda referência para a plataforma
        self.y_velocity = 0

    def update(self):
        # Atualiza posição
        next_x = self.actor.x + self.speed * self.direction

        # Verifica se a próxima posição sairia da plataforma
        if self.platform:
            if next_x < self.platform.left + self.actor.width/2:
                next_x = self.platform.left + self.actor.width/2
                self.direction = 1
                self.facing_right = True
            elif next_x > self.platform.right - self.actor.width/2:
                next_x = self.platform.right - self.actor.width/2
                self.direction = -1
                self.facing_right = False

        self.actor.x = next_x

        # Mantém o inimigo na plataforma
        if self.platform:
            self.actor.y = self.platform.top - self.actor.height/2

        # Atualiza animação
        if abs(self.speed * self.direction) > 0:
            self.run_animation.update(True)
            self.actor.image = self.run_animation.get_current_frame()
        else:
            self.idle_animation.update()
            self.actor.image = self.idle_animation.get_current_frame()

        if not self.facing_right:
            self.actor.flip_x = True
        else:
            self.actor.flip_x = False


# Configuração das plataformas
ground = Rect((0, HEIGHT - 20), (WIDTH, 20))
platforms = [
    ground,
    Rect((100, 450), (200, 20)),
    Rect((400, 350), (200, 20)),
    Rect((200, 250), (200, 20)),
    Rect((500, 150), (200, 20)),
]

# Objetos do jogo
player = Player(WIDTH // 2, HEIGHT - 50)

# Cria inimigos em plataformas específicas
enemies = [
    Enemy(WIDTH - 100, HEIGHT - 50, 200, ground),  # Inimigo no chão
    Enemy(200, 450, 150, platforms[1]),  # Inimigo da plataforma 1
    Enemy(500, 350, 100, platforms[2])   # Inimigo da plataforma 2
]

# Configuração da fruta
fruit = Actor('apple')
fruit_positions = [
    (100, 400),
    (400, 300),
    (200, 200),
    (500, 100),
    (300, HEIGHT - 50)
]
fruit.pos = random.choice(fruit_positions)

# Variáveis do jogo
player_lives = 3
player_score = 0
sound_on = True
bg_blue = 180
bg_blue_direction = 1

# Inicia música de fundo
music.play('bg_music')


def draw():
    screen.fill((100, 150, bg_blue))

    if game_state == MENU:
        draw_menu()
    elif game_state == GAME:
        draw_game()
    elif game_state == GAME_OVER:
        draw_game_over()


def draw_menu():
    screen.draw.text("Apple Collector", center=(WIDTH//2, 150),
                     fontsize=60, color="white", shadow=(1, 1))
    screen.draw.text("Press ENTER to Start", center=(
        WIDTH//2, 300), fontsize=40, color="yellow")
    screen.draw.text("Press ESC to Exit", center=(
        WIDTH//2, 400), fontsize=40, color="yellow")

    sound_status = "ON" if sound_on else "OFF"
    screen.draw.text(f"Sound: {sound_status} (Press M to toggle)", center=(
        WIDTH//2, 350), fontsize=30, color="white")


def draw_game():
    # Desenha plataformas
    for platform in platforms:
        screen.draw.filled_rect(platform, (0, 100, 0))

    # Desenha jogador (piscando se invulnerável)
    if not player.is_invulnerable or (player.invulnerable_timer * 10) % 2 == 0:
        player.actor.draw()

    # Desenha inimigos
    for enemy in enemies:
        enemy.actor.draw()

    # Desenha fruta
    fruit.draw()

    # Desenha pontuação
    screen.draw.text(f"Score: {player_score}", topleft=(
        20, 20), fontsize=30, color="white")

    # Desenha vidas usando heart.png
    for i in range(player_lives):
        heart = Actor('heart')
        heart.pos = (35 + i * 40, 60)
        heart.draw()


def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH//2, 200),
                     fontsize=60, color="red", shadow=(2, 2))
    screen.draw.text(f"Final Score: {player_score}", center=(
        WIDTH//2, 280), fontsize=40, color="white")
    screen.draw.text("Press R to Restart", center=(
        WIDTH//2, 350), fontsize=30, color="yellow")
    screen.draw.text("Press M for Menu", center=(
        WIDTH//2, 400), fontsize=30, color="yellow")


def update():
    global bg_blue, bg_blue_direction

    # Atualiza cor de fundo
    if bg_blue_direction == 1:
        bg_blue += 0.5
        if bg_blue >= 255:
            bg_blue_direction = -1
    else:
        bg_blue -= 0.5
        if bg_blue <= 180:
            bg_blue_direction = 1

    if game_state == GAME:
        update_game()


def update_game():
    global player_lives, game_state, player_score

    # Atualiza movimento e animação do jogador
    is_moving = False
    if keyboard.left and player.actor.x > 30:
        player.actor.x -= player.speed
        player.facing_right = False
        is_moving = True
    if keyboard.right and player.actor.x < WIDTH - 30:
        player.actor.x += player.speed
        player.facing_right = True
        is_moving = True

    player.update(is_moving)

    # Atualiza movimento vertical do jogador
    player.y_velocity += 0.5  # gravidade
    player.actor.y += player.y_velocity

    # Verifica colisões com plataformas
    on_platform = False
    for platform in platforms:
        if player.actor.colliderect(platform) and player.y_velocity > 0:
            player.actor.y = platform.top - player.actor.height / 2
            player.y_velocity = 0
            player.is_jumping = False
            on_platform = True

    # Pular
    if keyboard.up and not player.is_jumping and on_platform:
        player.y_velocity = -10
        player.is_jumping = True
        if sound_on:
            sounds.jump.play()

    # Atualiza inimigos
    for enemy in enemies:
        enemy.update()

        # Verifica colisão com inimigo
        if player.actor.colliderect(enemy.actor) and not player.is_invulnerable:
            player_lives -= 1
            player.is_invulnerable = True
            if sound_on:
                sounds.hit.play()

            if player_lives <= 0:
                game_state = GAME_OVER

    # Atualiza invulnerabilidade
    if player.is_invulnerable:
        player.invulnerable_timer += 1
        if player.invulnerable_timer > 60:  # 2 segundos a 30 FPS
            player.invulnerable_timer = 0
            player.is_invulnerable = False

    # Verifica coleta da fruta
    if player.actor.colliderect(fruit):
        player_score += 10
        place_fruit()
        if sound_on:
            sounds.coin.play()


def place_fruit():
    current_pos = fruit.pos
    new_pos = current_pos

    while new_pos == current_pos:
        new_pos = random.choice(fruit_positions)

    fruit.pos = new_pos


def on_key_down(key):
    global game_state, sound_on, player_lives, player_score

    if game_state == MENU:
        if key == keys.RETURN:
            reset_game()
            game_state = GAME
        elif key == keys.M:
            sound_on = not sound_on
            if sound_on:
                music.play('bg_music')
            else:
                music.stop()
        elif key == keys.ESCAPE:
            exit()

    elif game_state == GAME_OVER:
        if key == keys.R:
            reset_game()
            game_state = GAME
        elif key == keys.M:
            game_state = MENU

    elif game_state == GAME:
        if key == keys.M:
            sound_on = not sound_on
            if sound_on:
                music.play('bg_music')
            else:
                music.stop()


def reset_game():
    global player_lives, player_score

    player.actor.pos = (WIDTH // 2, HEIGHT - 50)
    player.y_velocity = 0
    player.is_jumping = False
    player.is_invulnerable = False
    player.invulnerable_timer = 0

    # Reseta inimigos para suas posições nas plataformas
    enemies[0].actor.pos = (WIDTH - 100, ground.top -
                            enemies[0].actor.height/2)  # Inimigo no chão
    # Inimigo da plataforma 1
    enemies[1].actor.pos = (200, platforms[1].top - enemies[1].actor.height/2)
    # Inimigo da plataforma 2
    enemies[2].actor.pos = (500, platforms[2].top - enemies[2].actor.height/2)

    place_fruit()
    player_lives = 3
    player_score = 0


pgzrun.go()
