import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.lives = 3
        self.score = 0
        
    def update(self, platforms, enemies, coins):
        # 应用重力
        self.vel_y += GRAVITY
        
        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 边界检查
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        # 掉落检测
        if self.y > SCREEN_HEIGHT:
            self.lives -= 1
            self.respawn()
            
        # 平台碰撞检测
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                if self.vel_y > 0:  # 下落
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # 上升
                    self.y = platform.rect.bottom
                    self.vel_y = 0
                    
        # 敌人碰撞检测
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                if self.vel_y > 0 and self.y < enemy.y:  # 从上方踩到敌人
                    self.vel_y = JUMP_STRENGTH // 2
                    enemies.remove(enemy)
                    self.score += 100
                else:  # 被敌人碰到
                    self.lives -= 1
                    self.respawn()
                    
        # 金币收集检测
        for coin in coins[:]:
            if player_rect.colliderect(coin.rect):
                coins.remove(coin)
                self.score += 50
                
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            
    def move_left(self):
        self.vel_x = -PLAYER_SPEED
        
    def move_right(self):
        self.vel_x = PLAYER_SPEED
        
    def stop(self):
        self.vel_x = 0
        
    def respawn(self):
        self.x = 100
        self.y = 400
        self.vel_x = 0
        self.vel_y = 0
        
    def draw(self, screen):
        # 绘制玛丽（简单的红色帽子和蓝色衣服）
        # 帽子
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, 15))
        # 脸
        pygame.draw.rect(screen, (255, 220, 177), (self.x + 5, self.y + 15, 20, 15))
        # 身体
        pygame.draw.rect(screen, BLUE, (self.x + 5, self.y + 30, 20, 10))
        # 腿
        pygame.draw.rect(screen, (0, 0, 139), (self.x + 8, self.y + 40, 6, 10))
        pygame.draw.rect(screen, (0, 0, 139), (self.x + 16, self.y + 40, 6, 10))

class Platform:
    def __init__(self, x, y, width, height, color=BROWN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # 添加纹理
        for i in range(0, self.rect.width, 20):
            pygame.draw.line(screen, BLACK, 
                           (self.rect.x + i, self.rect.y), 
                           (self.rect.x + i, self.rect.y + self.rect.height), 1)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.vel_x = ENEMY_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.direction = 1
        
    def update(self, platforms):
        # 简单的左右移动
        self.x += self.vel_x * self.direction
        self.rect.x = self.x
        
        # 检查是否到达平台边缘
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.bottom == platform.rect.top:
                    on_platform = True
                    # 检查前方是否有平台
                    next_x = self.x + (self.width + 10) * self.direction
                    if not platform.rect.collidepoint(next_x, platform.rect.top):
                        self.direction *= -1
                        break
                        
        if not on_platform:
            self.direction *= -1
            
    def draw(self, screen):
        # 绘制蘑菇怪
        # 身体
        pygame.draw.ellipse(screen, ORANGE, (self.x, self.y + 10, self.width, 20))
        # 头
        pygame.draw.circle(screen, RED, (self.x + self.width // 2, self.y + 10), 15)
        # 白色斑点
        pygame.draw.circle(screen, WHITE, (self.x + 8, self.y + 8), 3)
        pygame.draw.circle(screen, WHITE, (self.x + 22, self.y + 8), 3)
        # 眼睛
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 12), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 12), 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.animation_offset = 0
        
    def update(self):
        # 金币动画
        self.animation_offset += 0.1
        
    def draw(self, screen):
        # 绘制旋转的金币
        y_offset = abs(pygame.math.Vector2(0, 1).rotate(self.animation_offset * 50).y) * 3
        pygame.draw.ellipse(screen, YELLOW, 
                          (self.x - self.radius, self.y - self.radius + y_offset, 
                           self.radius * 2, self.radius * 2 - y_offset * 2))
        pygame.draw.ellipse(screen, ORANGE, 
                          (self.x - self.radius, self.y - self.radius + y_offset, 
                           self.radius * 2, self.radius * 2 - y_offset * 2), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超级玛丽")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(100, 400)
        self.platforms = self.create_platforms()
        self.enemies = self.create_enemies()
        self.coins = self.create_coins()
        self.game_over = False
        self.game_won = False
        
    def create_platforms(self):
        platforms = []
        # 地面
        platforms.append(Platform(0, 550, SCREEN_WIDTH, 50))
        
        # 悬浮平台
        platforms.append(Platform(200, 450, 150, 20))
        platforms.append(Platform(400, 350, 150, 20))
        platforms.append(Platform(600, 250, 150, 20))
        platforms.append(Platform(100, 250, 100, 20))
        platforms.append(Platform(350, 200, 100, 20))
        
        # 管道
        platforms.append(Platform(700, 480, 60, 70, GREEN))
        platforms.append(Platform(50, 480, 60, 70, GREEN))
        
        return platforms
        
    def create_enemies(self):
        enemies = []
        enemies.append(Enemy(250, 520))
        enemies.append(Enemy(450, 320))
        enemies.append(Enemy(650, 220))
        return enemies
        
    def create_coins(self):
        coins = []
        # 在平台上放置金币
        coins.append(Coin(275, 420))
        coins.append(Coin(475, 320))
        coins.append(Coin(675, 220))
        coins.append(Coin(150, 220))
        coins.append(Coin(400, 170))
        coins.append(Coin(550, 200))
        coins.append(Coin(300, 500))
        coins.append(Coin(500, 500))
        return coins
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over or self.game_won:
                        self.reset_game()
                    else:
                        self.player.jump()
                if event.key == pygame.K_r and (self.game_over or self.game_won):
                    self.reset_game()
        return True
        
    def update(self):
        if not self.game_over and not self.game_won:
            # 处理按键
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            elif keys[pygame.K_RIGHT]:
                self.player.move_right()
            else:
                self.player.stop()
                
            # 更新游戏对象
            self.player.update(self.platforms, self.enemies, self.coins)
            
            for enemy in self.enemies:
                enemy.update(self.platforms)
                
            for coin in self.coins:
                coin.update()
                
            # 检查游戏状态
            if self.player.lives <= 0:
                self.game_over = True
            elif len(self.coins) == 0:
                self.game_won = True
                
    def draw(self):
        # 背景
        self.screen.fill((135, 206, 235))  # 天蓝色
        
        # 绘制云朵
        for i in range(3):
            x = 100 + i * 250
            y = 50 + i * 30
            pygame.draw.circle(self.screen, WHITE, (x, y), 30)
            pygame.draw.circle(self.screen, WHITE, (x + 25, y), 35)
            pygame.draw.circle(self.screen, WHITE, (x + 50, y), 30)
            
        # 绘制游戏对象
        for platform in self.platforms:
            platform.draw(self.screen)
            
        for coin in self.coins:
            coin.draw(self.screen)
            
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        self.player.draw(self.screen)
        
        # 绘制UI
        score_text = self.font.render(f"分数: {self.player.score}", True, BLACK)
        lives_text = self.font.render(f"生命: {self.player.lives}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        # 绘制游戏状态
        if self.game_over:
            game_over_text = self.font.render("游戏结束!", True, RED)
            restart_text = self.font.render("按空格键重新开始", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            
        elif self.game_won:
            win_text = self.font.render("恭喜通关!", True, GREEN)
            restart_text = self.font.render("按空格键重新开始", True, BLACK)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(win_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = Game()
    game.run()
