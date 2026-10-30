import random
import math
import sys
try:
    import pygame
    from pygame import mixer
except ImportError:
    print("Pygame not installed. Install with: pip install pygame")
    sys.exit()

# Initialize Pygame
try:
    import pygame
    from pygame import mixer
    pygame.init()
    mixer.init()
except ImportError:
    print("Pygame not installed. Install with: pip install pygame")
    sys.exit()

# Screen setup
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter | kanak Dovloper")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 150, 50)
PURPLE = (150, 50, 255)
CYAN = (50, 255, 255)

# Fonts
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 35)
font_tiny = pygame.font.Font(None, 25)

# Game variables
score = 0
lives = 3
level = 1
game_over = False
paused = False

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        # Draw player ship
        points = [(25, 0), (0, 45), (15, 35), (25, 50), (35, 35), (50, 45)]
        pygame.draw.polygon(self.image, CYAN, points)
        pygame.draw.polygon(self.image, WHITE, points, 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 8
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill(YELLOW)
        pygame.draw.rect(self.image, WHITE, (0, 0, 4, 5))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -12
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45), pygame.SRCALPHA)
        points = [(22, 45), (0, 10), (10, 15), (22, 0), (34, 15), (45, 10)]
        color = random.choice([RED, ORANGE, PURPLE])
        pygame.draw.polygon(self.image, color, points)
        pygame.draw.polygon(self.image, WHITE, points, 2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 7)
        self.speedx = random.randrange(-3, 3)
        self.shoot_delay = random.randrange(1500, 3000)
        self.last_shot = pygame.time.get_ticks()
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx *= -1
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 7)
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

# Enemy Bullet
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 8
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame > 8:
                self.kill()
            else:
                self.image = pygame.Surface((self.size + self.frame*2, self.size + self.frame*2), pygame.SRCALPHA)
                radius = (self.size + self.frame*2) // 2
                pygame.draw.circle(self.image, ORANGE, (radius, radius), radius)
                pygame.draw.circle(self.image, YELLOW, (radius, radius), radius - 3)
                pygame.draw.circle(self.image, WHITE, (radius, radius), radius - 8)
                self.rect = self.image.get_rect(center=self.rect.center)

# Star background
class Star:
    def __init__(self):
        self.x = random.randrange(0, WIDTH)
        self.y = random.randrange(0, HEIGHT)
        self.speed = random.randrange(1, 4)
        self.size = random.randrange(1, 3)
        
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randrange(0, WIDTH)
        
    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

# Create groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
def create_enemies(num):
    for i in range(num):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

create_enemies(8)

# Stars
stars = [Star() for _ in range(100)]

# UI functions
def draw_text(text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_ui():
    draw_text(f"SCORE: {score}", font_small, WHITE, 10, 10)
    draw_text(f"LIVES: {lives}", font_small, WHITE, WIDTH-150, 10)
    draw_text(f"LEVEL: {level}", font_small, WHITE, WIDTH//2-60, 10)
    
    # Shield bar
    shield_width = 150
    shield_height = 10
    pygame.draw.rect(screen, RED, (10, HEIGHT-25, shield_width, shield_height))
    pygame.draw.rect(screen, GREEN, (10, HEIGHT-25, shield_width * (player.shield/100), shield_height))
    draw_text("SHIELD", font_tiny, WHITE, 10, HEIGHT-45)

def draw_start_screen():
    screen.fill(BLACK)
    for star in stars:
        star.draw()
    draw_text("SPACE SHOOTER", font_large, CYAN, WIDTH//2, HEIGHT//2-150, center=True)
    draw_text("kanak Dovloper", font_medium, YELLOW, WIDTH//2, HEIGHT//2-70, center=True)
    draw_text("ARROW KEYS - MOVE", font_small, WHITE, WIDTH//2, HEIGHT//2+20, center=True)
    draw_text("SPACEBAR - SHOOT", font_small, WHITE, WIDTH//2, HEIGHT//2+60, center=True)
    draw_text("PRESS ENTER TO START", font_small, GREEN, WIDTH//2, HEIGHT//2+150, center=True)
    pygame.display.flip()

def draw_game_over_screen():
    screen.fill(BLACK)
    for star in stars:
        star.draw()
    draw_text("GAME OVER", font_large, RED, WIDTH//2, HEIGHT//2-100, center=True)
    draw_text(f"FINAL SCORE: {score}", font_medium, YELLOW, WIDTH//2, HEIGHT//2-20, center=True)
    draw_text("PRESS ENTER TO RESTART", font_small, GREEN, WIDTH//2, HEIGHT//2+80, center=True)
    draw_text("PRESS ESC TO QUIT", font_small, WHITE, WIDTH//2, HEIGHT//2+120, center=True)
    pygame.display.flip()

# Game loop
show_start = True
running = True
while running:
    if show_start:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_start = False
                    # Reset game
                    score = 0
                    lives = 3
                    level = 1
                    player.shield = 100
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()
                    enemy_bullets.empty()
                    player = Player()
                    all_sprites.add(player)
                    create_enemies(8)
        continue
    
    if game_over:
        draw_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    show_start = True
                if event.key == pygame.K_ESCAPE:
                    running = False
        continue
    
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update
    for star in stars:
        star.update()
    
    all_sprites.update()
    
    # Enemy shooting
    for enemy in enemies:
        enemy.shoot()
    
    # Bullet-enemy collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        expl = Explosion(hit.rect.center, 40)
        all_sprites.add(expl)
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Enemy bullet-player collision
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.shield -= 10
        if player.shield <= 0:
            lives -= 1
            player.shield = 100
            expl = Explosion(player.rect.center, 60)
            all_sprites.add(expl)
            if lives <= 0:
                game_over = True
    
    # Enemy-player collision
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        lives -= 1
        player.shield = 100
        expl = Explosion(hit.rect.center, 40)
        all_sprites.add(expl)
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if lives <= 0:
            game_over = True
    
    # Level up
    if len(enemies) == 0:
        level += 1
        create_enemies(8 + level*2)
    
    # Draw
    screen.fill(BLACK)
    for star in stars:
        star.draw()
    all_sprites.draw(screen)
    draw_ui()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
