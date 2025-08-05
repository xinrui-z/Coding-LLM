import pygame
import sys
import random
import math

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 颜色定义 (红白机风格)
BACKGROUND = (0, 0, 170)  # 深蓝色背景
GRID_COLOR = (0, 0, 100)  # 更深的蓝色网格线
SNAKE_COLOR = (0, 255, 0)  # 绿色蛇身
SNAKE_HEAD_COLOR = (0, 200, 0)  # 稍深的绿色蛇头
FOOD_COLOR = (255, 0, 0)  # 红色食物
TEXT_COLOR = (255, 255, 255)  # 白色文字
GAME_OVER_BG = (0, 0, 0, 180)  # 半透明黑色游戏结束背景

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("红白机风格贪吃蛇")
clock = pygame.time.Clock()

# 字体设置
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_to = 3
        self.last_move_time = 0
        self.move_delay = 150  # 毫秒
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self, current_time):
        if current_time - self.last_move_time > self.move_delay:
            self.last_move_time = current_time
            
            head = self.get_head_position()
            x, y = self.direction
            new_x = (head[0] + x) % GRID_WIDTH
            new_y = (head[1] + y) % GRID_HEIGHT
            new_position = (new_x, new_y)
            
            # 检查是否撞到自己
            if new_position in self.positions[1:]:
                return False  # 游戏结束
                
            self.positions.insert(0, new_position)
            
            if len(self.positions) > self.grow_to:
                self.positions.pop()
                
        return True  # 游戏继续
    
    def change_direction(self, direction):
        # 防止蛇反向移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def grow(self):
        self.grow_to += 1
        self.score += 10
        # 提高游戏速度
        self.move_delay = max(50, self.move_delay - 2)
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # 绘制蛇身
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            if i == 0:  # 蛇头
                pygame.draw.rect(surface, SNAKE_HEAD_COLOR, rect)
                pygame.draw.rect(surface, (0, 100, 0), rect, 1)  # 边框
            else:  # 蛇身
                pygame.draw.rect(surface, SNAKE_COLOR, rect)
                pygame.draw.rect(surface, (0, 150, 0), rect, 1)  # 边框
                
            # 在蛇头上画眼睛
            if i == 0:
                # 确定眼睛位置
                eye_size = GRID_SIZE // 5
                # 左眼
                left_eye_x = p[0] * GRID_SIZE + GRID_SIZE // 3
                left_eye_y = p[1] * GRID_SIZE + GRID_SIZE // 3
                # 右眼
                right_eye_x = p[0] * GRID_SIZE + 2 * GRID_SIZE // 3
                right_eye_y = p[1] * GRID_SIZE + GRID_SIZE // 3
                
                # 根据方向调整眼睛位置
                if self.direction == (1, 0):  # 右
                    left_eye_x += GRID_SIZE // 6
                    right_eye_x += GRID_SIZE // 6
                elif self.direction == (-1, 0):  # 左
                    left_eye_x -= GRID_SIZE // 6
                    right_eye_x -= GRID_SIZE // 6
                elif self.direction == (0, 1):  # 下
                    left_eye_y += GRID_SIZE // 6
                    right_eye_y += GRID_SIZE // 6
                elif self.direction == (0, -1):  # 上
                    left_eye_y -= GRID_SIZE // 6
                    right_eye_y -= GRID_SIZE // 6
                
                pygame.draw.circle(surface, (0, 0, 0), (left_eye_x, left_eye_y), eye_size)
                pygame.draw.circle(surface, (0, 0, 0), (right_eye_x, right_eye_y), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, FOOD_COLOR, rect)
        pygame.draw.rect(surface, (150, 0, 0), rect, 1)  # 边框
        
        # 在食物上画一个笑脸
        center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 3
        
        # 眼睛
        eye_offset = GRID_SIZE // 6
        pygame.draw.circle(surface, (0, 0, 0), (center_x - eye_offset, center_y - eye_offset//2), GRID_SIZE//10)
        pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_offset, center_y - eye_offset//2), GRID_SIZE//10)
        
        # 嘴巴
        mouth_rect = pygame.Rect(center_x - radius//1.5, center_y + eye_offset//2, radius, radius//2)
        pygame.draw.arc(surface, (0, 0, 0), mouth_rect, 0, math.pi, 2)

def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

def draw_score(surface, score):
    score_text = font.render(f"得分: {score}", True, TEXT_COLOR)
    surface.blit(score_text, (10, 10))

def draw_game_over(surface, score):
    # 半透明覆盖层
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(GAME_OVER_BG)
    surface.blit(overlay, (0, 0))
    
    # 游戏结束文字
    game_over_text = font.render("游戏结束", True, TEXT_COLOR)
    score_text = font.render(f"最终得分: {score}", True, TEXT_COLOR)
    restart_text = small_font.render("按空格键重新开始", True, TEXT_COLOR)
    
    surface.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
    surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
    surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))

def draw_title(surface):
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("贪吃蛇", True, TEXT_COLOR)
    subtitle_text = font.render("红白机风格", True, TEXT_COLOR)
    
    surface.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    surface.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 130))
    
    # 绘制控制说明
    controls = [
        "控制说明:",
        "↑ ↓ ← → 方向键控制移动",
        "空格键暂停/继续",
        "按 R 键重新开始"
    ]
    
    for i, text in enumerate(controls):
        ctrl_text = small_font.render(text, True, TEXT_COLOR)
        surface.blit(ctrl_text, (SCREEN_WIDTH//2 - ctrl_text.get_width()//2, 200 + i*30))

def main():
    snake = Snake()
    food = Food()
    game_over = False
    paused = False
    show_title = True
    
    # 确保食物不在蛇身上
    while food.position in snake.positions:
        food.randomize_position()
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if show_title:
                    show_title = False
                    continue
                    
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    
                if event.key == pygame.K_r:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                    paused = False
                    
                if not game_over and not paused:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
        
        if show_title:
            screen.fill(BACKGROUND)
            draw_grid(screen)
            draw_title(screen)
            pygame.display.update()
            clock.tick(10)
            continue
            
        if not paused and not game_over:
            # 更新蛇的位置
            if not snake.update(current_time):
                game_over = True
                
            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # 确保食物不在蛇身上
                while food.position in snake.positions:
                    food.randomize_position()
        
        # 绘制游戏画面
        screen.fill(BACKGROUND)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        
        if paused:
            # 绘制暂停文字
            pause_text = font.render("游戏暂停", True, TEXT_COLOR)
            screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))
        
        if game_over:
            draw_game_over(screen, snake.score)
        
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
