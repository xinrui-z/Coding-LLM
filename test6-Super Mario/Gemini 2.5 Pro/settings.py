# settings.py

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "超级玛丽 (Pygame版)"

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)
SKY_BLUE = (135, 206, 235)

# 玩家属性
PLAYER_ACC = 0.5  # 加速度
PLAYER_FRICTION = -0.12 # 摩擦力
PLAYER_GRAVITY = 0.8 # 重力
PLAYER_JUMP = -20 # 跳跃力度

# 敌人属性
GOOMBA_SPEED = 2

# 平台尺寸
TILE_SIZE = 40

# 关卡地图
# P: Platform (平台)
# G: Goomba (敌人)
LEVEL_MAP = [
    "                                        ",
    "                                        ",
    "                                        ",
    "                                        ",
    "                                        ",
    "                                        ",
    "                                        ",
    "    PPPPPPP          PPPPP              ",
    "                                        ",
    "                   PPPPPPPPP            ",
    "                                        ",
    "  PPPP       G                          ",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
]
