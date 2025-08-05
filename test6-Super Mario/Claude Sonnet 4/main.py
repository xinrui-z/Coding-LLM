import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

# 物理常数
GRAVITY = 0.8
JUMP_SPEED = -15
MARIO_SPEED = 5

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.on_ground = False
        self.lives = 3
        self.score = 0
        
    def update(self):
        # 重力
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # 检查是否落到地面
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_SPEED
            
    def move_left(self):
        self.rect.x -= MARIO_SPEED
        
    def move_right(self):
        self.rect.x += MARIO_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = pygame.Rect(x, y, width, height)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, 3)
        self.direction = random.choice([-1, 1])
        
    def update(self):
        self.rect.x += self.speed * self.direction
        
        # 边界反弹
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            
        # 重力（简单版）
        if self.rect.bottom < SCREEN_HEIGHT - 50:
            self.rect.y += 5
        elif self.rect.bottom > SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("超级玛丽")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # 创建玛丽
        self.mario = Mario()
        self.all_sprites.add(self.mario)
        
        # 创建平台
        self.create_platforms()
        
        # 创建金币
        self.create_coins()
        
        # 创建敌人
        self.create_enemies()
        
    def create_platforms(self):
        platform_data = [
            (200, 400, 150, 20),
            (400, 300, 120, 20),
            (600, 450, 100, 20),
            (300, 200, 100, 20),
            (500, 150, 150, 20),
        ]
        
        for x, y, width, height in platform_data:
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
    def create_coins(self):
        coin_positions = [
            (220, 360), (430, 260), (630, 410),
            (320, 160), (550, 110), (150, 500),
            (700, 350), (250, 500), (450, 500)
        ]
        
        for x, y in coin_positions:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
            
    def create_enemies(self):
        enemy_positions = [(350, 520), (600, 520), (200, 520)]
        
        for x, y in enemy_positions:
            enemy = Enemy(x, y)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
    def handle_collisions(self):
        # 玛丽与平台碰撞
        hits = pygame.sprite.spritecollide(self.mario, self.platforms, False)
        for hit in hits:
            if self.mario.velocity_y > 0:  # 向下移动时
                if self.mario.rect.bottom <= hit.rect.top + 10:
                    self.mario.rect.bottom = hit.rect.top
                    self.mario.velocity_y = 0
                    self.mario.on_ground = True
                    
        # 玛丽与金币碰撞
        hits = pygame.sprite.spritecollide(self.mario, self.coins, True)
        for hit in hits:
            self.mario.score += 100
            
        # 玛丽与敌人碰撞
        hits = pygame.sprite.spritecollide(self.mario, self.enemies, False)
        for hit in hits:
            # 如果玛丽从上方踩到敌人
            if self.mario.velocity_y > 0 and self.mario.rect.bottom <= hit.rect.centery:
                hit.kill()
                self.mario.velocity_y = JUMP_SPEED // 2
                self.mario.score += 200
            else:
                # 玛丽受伤
                self.mario.lives -= 1
                # 简单的击退效果
                if self.mario.rect.centerx < hit.rect.centerx:
                    self.mario.rect.x -= 50
                else:
                    self.mario.rect.x += 50
                    
                # 移除敌人（避免连续伤害）
                hit.kill()
                
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mario.jump()
                elif event.key == pygame.K_r and self.mario.lives <= 0:
                    self.restart_game()
                    
        # 持续按键检测
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.mario.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.mario.move_right()
            
        return True
    
    def restart_game(self):
        # 重置游戏状态
        self.mario.lives = 3
        self.mario.score = 0
        self.mario.rect.x = 100
        self.mario.rect.y = SCREEN_HEIGHT - 100
        self.mario.velocity_y = 0
        
        # 清除所有精灵
        self.all_sprites.empty()
        self.platforms.empty()
        self.coins.empty()
        self.enemies.empty()
        
        # 重新创建
        self.all_sprites.add(self.mario)
        self.create_platforms()
        self.create_coins()
        self.create_enemies()
        
    def draw(self):
        self.screen.fill(BLUE)  # 天空背景
        
        # 绘制地面
        pygame.draw.rect(self.screen, GREEN, 
                        (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # 绘制所有精灵
        self.all_sprites.draw(self.screen)
        
        # 绘制UI信息
        score_text = self.font.render(f"得分: {self.mario.score}", True, WHITE)
        lives_text = self.font.render(f"生命: {self.mario.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        # 游戏结束界面
        if self.mario.lives <= 0:
            game_over_text = self.font.render("游戏结束! 按R键重新开始", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 20))
            self.screen.blit(game_over_text, text_rect)
            
        # 胜利条件（收集所有金币）
        if len(self.coins) == 0:
            win_text = self.font.render("恭喜过关! 按R键重新开始", True, WHITE)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, GREEN, text_rect.inflate(20, 20))
            self.screen.blit(win_text, text_rect)
            
        # 显示操作说明
        if self.mario.score == 0:  # 游戏开始时显示
            instructions = [
                "操作说明:",
                "A/D 或 方向键: 移动",
                "空格键: 跳跃",
                "收集金币, 避开/踩死敌人!"
            ]
            for i, instruction in enumerate(instructions):
                text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH - 250, 10 + i * 25))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            # 只有在游戏进行中才更新
            if self.mario.lives > 0:
                self.all_sprites.update()
                self.handle_collisions()
                
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
