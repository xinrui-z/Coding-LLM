import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("超级玛丽游戏")
clock = pygame.time.Clock()

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
        self.speed = 5
        self.jump_power = -15
        self.on_ground = False
        self.score = 0
        
    def update(self):
        # 处理重力
        if not self.on_ground:
            self.vel_y += 0.8
        
        # 限制下落速度
        if self.vel_y > 15:
            self.vel_y = 15
            
        # 更新位置
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True
    
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
    
    def move_left(self):
        self.vel_x = -self.speed
    
    def move_right(self):
        self.vel_x = self.speed
    
    def stop(self):
        self.vel_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1
        
    def update(self):
        self.rect.x += self.speed * self.direction
        
        # 边界反弹
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.player = Player(100, 300)
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        self.all_sprites.add(self.player)
        
        # 创建平台
        self.create_platforms()
        
        # 创建敌人
        self.create_enemies()
        
        # 创建金币
        self.create_coins()
        
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.win = False
        
    def create_platforms(self):
        # 地面平台
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # 其他平台
        platforms_data = [
            (200, 500, 100, 20),
            (400, 400, 100, 20),
            (600, 300, 100, 20),
            (300, 250, 100, 20),
            (100, 200, 100, 20),
            (500, 150, 100, 20),
        ]
        
        for x, y, width, height in platforms_data:
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
    
    def create_enemies(self):
        enemies_data = [
            (300, SCREEN_HEIGHT - 70),
            (500, 370),
            (200, 170),
        ]
        
        for x, y in enemies_data:
            enemy = Enemy(x, y)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
    
    def create_coins(self):
        coins_data = [
            (250, 470),
            (450, 370),
            (650, 270),
            (350, 220),
            (150, 170),
            (550, 120),
        ]
        
        for x, y in coins_data:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
    
    def handle_collisions(self):
        # 平台碰撞检测
        self.player.on_ground = False
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for hit in hits:
            if self.player.vel_y > 0:  # 下降时碰到平台
                self.player.rect.bottom = hit.rect.top
                self.player.vel_y = 0
                self.player.on_ground = True
            elif self.player.vel_y < 0:  # 上升时碰到平台
                self.player.rect.top = hit.rect.bottom
                self.player.vel_y = 0
        
        # 敌人碰撞检测
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            # 简单的碰撞处理：游戏结束
            self.game_over = True
        
        # 金币收集检测
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            self.player.score += 10
        
        # 检查是否获胜（收集所有金币）
        if len(self.coins) == 0:
            self.win = True
    
    def update(self):
        if not self.game_over and not self.win:
            self.all_sprites.update()
            self.handle_collisions()
    
    def draw(self):
        # 绘制背景
        screen.fill(SKY_BLUE)
        
        # 绘制所有精灵
        self.all_sprites.draw(screen)
        
        # 绘制UI
        score_text = self.font.render(f"分数: {self.player.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        coins_left = len(self.coins)
        coins_text = self.font.render(f"剩余金币: {coins_left}", True, BLACK)
        screen.blit(coins_text, (10, 50))
        
        # 游戏结束画面
        if self.game_over:
            game_over_text = self.font.render("游戏结束! 按R重新开始", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)
        
        # 获胜画面
        if self.win:
            win_text = self.font.render("恭喜获胜! 按R重新开始", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(win_text, text_rect)
    
    def restart(self):
        # 重置游戏状态
        self.__init__()

def main():
    game = Game()
    running = True
    
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game.game_over or game.win):
                    game.restart()
                elif event.key == pygame.K_SPACE:
                    game.player.jump()
            
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    game.player.stop()
        
        # 处理持续按键
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.player.move_right()
        
        # 更新游戏状态
        game.update()
        
        # 绘制游戏
        game.draw()
        
        # 更新显示
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
