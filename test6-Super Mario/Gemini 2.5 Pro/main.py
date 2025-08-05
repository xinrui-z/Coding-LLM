# main.py

import pygame
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # 初始化Pygame和窗口
        pygame.init()
        pygame.mixer.init() # 如果要加声音的话
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_offset_x = 0

    def new(self):
        # 开始一个新游戏
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # 从地图创建世界
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if tile == 'P':
                    p = Platform(x, y)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
                elif tile == 'G':
                    g = Goomba(self, x, y)
                    self.all_sprites.add(g)
                    self.enemies.add(g)
        
        self.player = Player(self, TILE_SIZE * 5, SCREEN_HEIGHT - TILE_SIZE * 5)
        self.run()

    def run(self):
        # 游戏循环
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # 游戏循环 - 更新部分
        self.all_sprites.update()

        # 玩家与平台的碰撞检测 (垂直方向)
        if self.player.vel.y > 0: # 只有在下落时才检测
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # 找到玩家脚下最高的平台
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                
                # 如果玩家脚的位置在平台顶部以下
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0

        # 玩家与平台的碰撞检测 (水平方向)
        # 这个简化版本没有做水平碰撞，可以作为扩展功能添加

        # 玩家与敌人的碰撞检测
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            # 如果玩家在敌人上方且正在下落（踩踏）
            if self.player.vel.y > 0 and self.player.rect.bottom < enemy_hits[0].rect.centery:
                enemy_hits[0].kill() # 踩死敌人
            else:
                self.playing = False # 游戏结束

        # 摄像机跟随
        # 如果玩家移动到屏幕右侧 1/3 处，则移动摄像机
        if self.player.rect.right >= SCREEN_WIDTH * 2 / 3:
            self.camera_offset_x = self.player.rect.right - SCREEN_WIDTH * 2 / 3
            self.player.pos.x -= abs(self.player.vel.x) # 让玩家在屏幕上看起来相对静止
            
            # 移动所有其他精灵
            for sprite in self.all_sprites:
                if sprite != self.player:
                    sprite.rect.x -= abs(self.player.vel.x)

    def events(self):
        # 游戏循环 - 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()

    def draw(self):
        # 游戏循环 - 绘制部分
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Health: 1", 22, WHITE, SCREEN_WIDTH / 2, 15)
        pygame.display.flip()

    def show_start_screen(self):
        # 显示开始界面
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("方向键移动, 空格键跳跃", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text("按任意键开始", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # 显示游戏结束/继续界面
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("按任意键重新开始", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(pygame.font.match_font('arial'), size) # 使用系统默认字体
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

# --- 游戏主程序 ---
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
