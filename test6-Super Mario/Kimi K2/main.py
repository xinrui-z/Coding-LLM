import pygame
import sys
import random
from enum import Enum

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    LEVEL_COMPLETE = 4

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.lives = 3
        self.coins = 0
        
    def update(self, platforms, enemies, coins):
        # 重力
        self.vel_y += GRAVITY
        
        # 移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -MOVE_SPEED
        elif keys[pygame.K_RIGHT]:
            self.vel_x = MOVE_SPEED
        else:
            self.vel_x *= 0.8
            
        # 跳跃
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            
        # 更新位置
        self.rect.x += self.vel_x
        self.check_collisions(platforms, 'x')
        
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collisions(platforms, 'y')
        
        # 检查敌人碰撞
        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in enemy_hits:
            if self.vel_y > 0 and self.rect.bottom < enemy.rect.top + 20:
                enemy.kill()
                self.vel_y = JUMP_STRENGTH / 2
            else:
                self.lives -= 1
                self.rect.x = 100
                self.rect.y = 400
                return True
                
        # 检查金币碰撞
        coin_hits = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_hits:
            self.coins += 1
            
        return False
        
    def check_collisions(self, platforms, direction):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if direction == 'x':
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
                self.vel_x = 0
            elif direction == 'y':
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 2
        
    def update(self, platforms):
        self.rect.x += self.vel_x
        
        # 检查平台边缘
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if not hits:
            self.vel_x *= -1
            
        # 检查墙壁碰撞
        for platform in hits:
            if self.vel_x > 0 and self.rect.right >= platform.rect.right:
                self.vel_x *= -1
            elif self.vel_x < 0 and self.rect.left <= platform.rect.left:
                self.vel_x *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        pygame.draw.circle(self.image, BLACK, (10, 10), 8)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超级玛丽")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.game_state = GameState.MENU
        self.level = 1
        
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        self.player = None
        
    def create_level(self, level):
        # 清空所有精灵组
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.coins.empty()
        
        # 创建玩家
        self.player = Player(100, 400)
        self.all_sprites.add(self.player)
        
        # 创建地面
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # 根据关卡创建平台
        if level == 1:
            platforms = [
                Platform(200, 500, 100, 20),
                Platform(400, 450, 100, 20),
                Platform(600, 400, 100, 20),
                Platform(300, 350, 100, 20),
                Platform(500, 300, 100, 20),
            ]
            
            enemies = [
                Enemy(250, 470),
                Enemy(450, 420),
                Enemy(650, 370),
            ]
            
            coins = [
                Coin(250, 450),
                Coin(450, 400),
                Coin(650, 350),
                Coin(350, 300),
                Coin(550, 250),
            ]
            
        elif level == 2:
            platforms = [
                Platform(150, 500, 100, 20),
                Platform(350, 450, 100, 20),
                Platform(550, 400, 100, 20),
                Platform(250, 350, 100, 20),
                Platform(450, 300, 100, 20),
                Platform(650, 250, 100, 20),
            ]
            
            enemies = [
                Enemy(200, 470),
                Enemy(400, 420),
                Enemy(600, 370),
                Enemy(300, 320),
                Enemy(500, 270),
            ]
            
            coins = [
                Coin(200, 450),
                Coin(400, 400),
                Coin(600, 350),
                Coin(300, 300),
                Coin(500, 250),
                Coin(700, 200),
            ]
            
        # 添加平台、敌人和金币到精灵组
        for platform in platforms:
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
        for enemy in enemies:
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
        for coin in coins:
            self.coins.add(coin)
            self.all_sprites.add(coin)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.game_state = GameState.PLAYING
                        self.create_level(self.level)
                        
                elif self.game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.game_state = GameState.MENU
                        self.level = 1
                        
                elif self.game_state == GameState.LEVEL_COMPLETE:
                    if event.key == pygame.K_SPACE:
                        self.level += 1
                        if self.level > 2:
                            self.game_state = GameState.MENU
                            self.level = 1
                        else:
                            self.create_level(self.level)
                            self.game_state = GameState.PLAYING
                            
        return True
        
    def update(self):
        if self.game_state == GameState.PLAYING:
            # 更新所有精灵
            self.enemies.update(self.platforms)
            died = self.player.update(self.platforms, self.enemies, self.coins)
            
            # 检查游戏结束
            if self.player.lives <= 0:
                self.game_state = GameState.GAME_OVER
                
            # 检查关卡完成
            if len(self.coins) == 0:
                self.game_state = GameState.LEVEL_COMPLETE
                
    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.PLAYING:
            self.all_sprites.draw(self.screen)
            self.draw_hud()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
            
        pygame.display.flip()
        
    def draw_menu(self):
        title = self.font.render("超级玛丽", True, BLACK)
        start_text = self.font.render("按空格键开始游戏", True, BLACK)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
        self.screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 300))
        
    def draw_hud(self):
        lives_text = self.font.render(f"生命: {self.player.lives}", True, BLACK)
        coins_text = self.font.render(f"金币: {self.player.coins}", True, BLACK)
        level_text = self.font.render(f"关卡: {self.level}", True, BLACK)
        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(coins_text, (10, 50))
        self.screen.blit(level_text, (10, 90))
        
    def draw_game_over(self):
        game_over_text = self.font.render("游戏结束", True, BLACK)
        restart_text = self.font.render("按R键重新开始", True, BLACK)
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 250))
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 300))
        
    def draw_level_complete(self):
        complete_text = self.font.render("关卡完成！", True, BLACK)
        next_text = self.font.render("按空格键进入下一关", True, BLACK)
        self.screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, 250))
        self.screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 300))
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
