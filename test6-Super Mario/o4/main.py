import pygame
import sys

# —— 常量定义 —— #
WIDTH, HEIGHT = 800, 600      # 窗口大小
FPS = 60                      # 帧率
TILESIZE = 40                 # 格子大小
GRAVITY = 0.5                 # 重力加速度
JUMP_SPEED = -10              # 跳跃初速度
PLAYER_SPEED = 5              # 水平移动速度

# 简单关卡地图，'X' 表示砖块，'P' 表示玩家起点，其它空格
LEVEL_MAP = [
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "         P                                                                      ",
    "    XXXXXXXXXXXXX                                  XXXXXXX                     ",
    "                                                                                ",
    "                                          XXXX                                  ",
    "                           XXXX                                               ",
    "           XXXX                                                               ",
    "                                                                                ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# —— 精灵定义 —— #
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, blocks_group):
        super().__init__()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((200, 50, 50))  # 红色方块代表马里奥
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.blocks = blocks_group
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_SPEED

    def update(self):
        # 水平移动
        self.rect.x += self.vel_x
        self.collide(self.vel_x, 0)

        # 重力
        self.vel_y += GRAVITY
        if self.vel_y > TILESIZE:  # 限制最大下落速度
            self.vel_y = TILESIZE
        self.rect.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y)

    def collide(self, dx, dy):
        # 与所有砖块检测碰撞并修正位置
        for block in self.blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0:    # 向右撞
                    self.rect.right = block.rect.left
                if dx < 0:    # 向左撞
                    self.rect.left = block.rect.right
                if dy > 0:    # 向下撞（落地）
                    self.rect.bottom = block.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if dy < 0:    # 向上撞（顶头）
                    self.rect.top = block.rect.bottom
                    self.vel_y = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((100, 70, 40))  # 棕色方块代表砖块
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("简易超级玛丽 - Pygame")
    clock = pygame.time.Clock()

    # —— 精灵组 —— #
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    # —— 根据地图实例化砖块 & 玩家 —— #
    player = None
    for row_idx, row in enumerate(LEVEL_MAP):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * TILESIZE, row_idx * TILESIZE
            if cell == 'X':
                block = Block(x, y)
                all_sprites.add(block)
                blocks.add(block)
            elif cell == 'P':
                player = Player(x, y, blocks)
                all_sprites.add(player)

    # 初始没有显式放置 P，也可手动指定
    if not player:
        player = Player(100, HEIGHT - 2 * TILESIZE, blocks)
        all_sprites.add(player)

    # 视口横向滚动偏移
    scroll_x = 0

    # —— 游戏主循环 —— #
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 输入 & 更新
        player.handle_input()
        all_sprites.update()

        # 计算滚动：保持玩家始终在窗口左侧三分之一位置
        scroll_x = player.rect.x - WIDTH // 3
        if scroll_x < 0:
            scroll_x = 0

        # 绘制
        screen.fill((135, 206, 235))  # 天空蓝背景
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - scroll_x, sprite.rect.y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
