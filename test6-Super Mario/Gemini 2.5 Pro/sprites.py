# sprites.py

import pygame
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE - 5, TILE_SIZE * 2 - 5)) # 一个瘦高的矩形代表马里奥
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # 只有当脚下有平台时才能跳跃
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = PLAYER_JUMP

    def update(self):
        # 1. 计算加速度
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # 2. 应用摩擦力
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # 3. 运动方程
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # 4. 更新位置
        self.rect.midbottom = self.pos

        # 防止玩家走出屏幕
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Goomba(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE - 5, TILE_SIZE - 5))
        self.image.fill(BLUE) # 蓝色代表Goomba
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = GOOMBA_SPEED

    def update(self):
        self.rect.x += self.vx
        
        # 简单的AI：碰到边缘或平台就返回
        # 注意：这是一个简化的实现，需要更复杂的碰撞检测来防止穿墙
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.vx *= -1
            
        # 模拟重力（简化版，仅用于在平台上移动）
        # 为了让Goomba能掉下去，需要一个更完整的物理系统
        # 这里我们假设它总是在平台上
