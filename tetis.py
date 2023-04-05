import pygame
import random

# 初始化 Pygame
pygame.init()

# 定義一些顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定義方塊的大小和數量
BLOCK_SIZE = 30
NUM_BLOCKS_X = 10
NUM_BLOCKS_Y = 20

# 設置視窗大小
WINDOW_SIZE = [BLOCK_SIZE * NUM_BLOCKS_X, BLOCK_SIZE * NUM_BLOCKS_Y]
screen = pygame.display.set_mode(WINDOW_SIZE)

# 定義方塊類別
class Block(pygame.sprite.Sprite):
    """
    定義方塊類別
    """
    def __init__(self, color, width, height):
        """
        初始化方塊
        :param color: 方塊顏色
        :param width: 方塊寬度
        :param height: 方塊高度
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# 定義方塊的顏色
COLORS = [BLUE, GREEN, RED]

# 定義方塊類型
BLOCK_TYPES = [
    # I 方塊
    [[1, 1, 1, 1]],

    # J 方塊
    [[2, 2, 2],
     [0, 0, 2]],

    # L 方塊
    [[3, 3, 3],
     [3, 0, 0]],

    # O 方塊
    [[4, 4],
     [4, 4]],

    # S 方塊
    [[0, 5, 5],
     [5, 5, 0]],

    # T 方塊
    [[0, 6, 0],
     [6, 6, 6]],

    # Z 方塊
    [[7, 7, 0],
     [0, 7, 7]]
]

# 定義方塊的初始位置
BLOCK_START_X = NUM_BLOCKS_X // 2 - 1
BLOCK_START_Y = -2

# 定義方塊群組
all_sprites_group = pygame.sprite.Group()
active_blocks_group = pygame.sprite.Group()

# 定義下一個方塊的顯示區域
next_block_group = pygame.sprite.Group()

# 定義計時器
clock = pygame.time.Clock()
fall_speed = 1
fall_counter = 0
move_counter = 0
move_speed = 5

# 定義遊戲結束標誌
game_over = False

# 定義分數
score = 0

# 生成方塊
def generate_block():
    """
    生成方塊
    """
    global active_blocks_group, next_block_group
# 從方塊類型列表中隨機選擇一個方塊
block_type = random.choice(BLOCK_TYPES)
# 從顏色列表中根據方塊的第一個元素的值選擇方塊的顏色
color = COLORS[block_type[0][0]]
block = []
# 根據方塊的二維列表生成方塊的精靈
for row in range(len(block_type)):
for col in range(len(block_type[row])):
if block_type[row][col] != 0:
block_sprite = Block(color, BLOCK_SIZE, BLOCK_SIZE)
block_sprite.rect.x = (BLOCK_START_X + col) * BLOCK_SIZE
block_sprite.rect.y = (BLOCK_START_Y + row) * BLOCK_SIZE
block.append(block_sprite)
# 把生成的方塊精靈添加到方塊群組和所有精靈群組中
for sprite in block:
active_blocks_group.add(sprite)
all_sprites_group.add(sprite)
# 生成下一個方塊的顯示區域
next_block_group.empty()
for row in range(len(BLOCK_TYPES[block_type.index])):
for col in range(len(BLOCK_TYPES[block_type.index][row])):
if BLOCK_TYPES[block_type.index][row][col] != 0:
block_sprite = Block(COLORS[BLOCK_TYPES[block_type.index][row][col]], BLOCK_SIZE, BLOCK_SIZE)
block_sprite.rect.x = (col + 13) * BLOCK_SIZE
block_sprite.rect.y = (row + 7) * BLOCK_SIZE
next_block_group.add(block_sprite)

# 檢查方塊是否可以移動
def can_move(dx, dy):
"""
# 檢查方塊是否可以移動
:param dx: x 軸移動距離
:param dy: y 軸移動距離
:return: True 表示可以移動，False 表示不能移動
"""
for block in active_blocks_group:
x = block.rect.x + dx
y = block.rect.y + dy
if x < 0 or x >= NUM_BLOCKS_X * BLOCK_SIZE or y >= NUM_BLOCKS_Y * BLOCK_SIZE or
pygame.sprite.spritecollideany(block, all_sprites_group, pygame.sprite.collide_rect) is not None:
return False
return True

# 移動方塊
def move_blocks(dx, dy):
"""
移動方塊
:param dx: x 軸移動距離
:param dy: y 軸移動距離
"""
global score
# 移動方塊精靈
for block in active_blocks_group:
block.rect.x += dx
block.rect.y += dy
# 如果向下移動，檢查是否有行已滿，並且移除滿行
if dy > 0:
rows_removed = remove_complete_rows()
if rows_removed > 0:
score += 10 * rows_removed

# 移除完整的行
def remove_complete_rows():
"""
移除完整的行
:return: 返回被移除的行數
"""
rows_removed = 0
# 檢查每一行是否滿行，如果是，則移除該行的方塊精靈
for row in range(NUM_BLOCKS_Y):
blocks_in_row = [block for block in all_sprites_group if block.rect.y == row * BLOCK_SIZE]
if len(blocks_in_row) == NUM_BLOCKS_X:
rows_removed += 1
for block in blocks_in_row:
block.kill()
# 移除方塊精靈後，需要把上方的方塊精靈下移一行
for block in all_sprites_group:
if block.rect.y < row * BLOCK_SIZE:
block.rect.y += BLOCK_SIZE
return rows_removed

# 旋轉方塊
def rotate_block():
"""
旋轉方塊
"""
global active_blocks_group
rotated_blocks = []
pivot_block = None
# 獲取旋轉軸
for block in active_blocks_group:
x, y = block.rect.x, block.rect.y
col, row = x // BLOCK_SIZE, y // BLOCK_SIZE
relative_x, relative_y = x % BLOCK_SIZE, y % BLOCK_SIZE
new_x = x + (relative_y - relative_x)
new_y = y + (relative_x + relative_y)
new_col, new_row = new_x // BLOCK_SIZE, new_y // BLOCK_SIZE
# 檢查旋轉後的方塊是否超出邊界或與其他方塊重疊
if new_col < 0 or new_col >= NUM_BLOCKS_X or new_row >= NUM_BLOCKS_Y or
pygame.sprite.spritecollideany(block, all_sprites_group, pygame.sprite.collide_rect) is not None:
return
# 確定旋轉軸的位置
if block.rect.x == min([b.rect.x for b in active_blocks_group]):
pivot_block = block
# 生成旋轉後的方塊精靈
rotated_block = Block(block.image.fill, BLOCK_SIZE, BLOCK_SIZE)
rotated_block.rect.x, rotated_block.rect.y = new_x, new_y
rotated_blocks.append(rotated_block)
all_sprites_group.add(rotated_block)
# 刪除原有方塊精靈
for block in active_blocks_group:
block.kill()
# 添加旋轉後的方塊精靈
for block in rotated_blocks:
active_blocks_group.add(block)

# 遊戲主迴圈
generate_block()
while not game_over:
for event in pygame.event.get():
if event.type == pygame.QUIT:
game_over = True
elif event.type == pygame.KEYDOWN:
if event.key == pygame.K_LEFT:
if can_move(-BLOCK_SIZE, 0):
move_blocks(-BLOCK_SIZE, 0)
elif event.key == pygame.K_RIGHT:
if can_move(BLOCK_SIZE, 0):
move_blocks(BLOCK_SIZE, 0)
elif event.key == pygame.K_DOWN:
if can_move(0, BLOCK_SIZE):
move_blocks(0, BLOCK_SIZE)
elif event.key == pygame.K_UP:
rotate_block()
# 計時器
fall_counter += 1
if fall_counter >= 60 // fall_speed:
    if can_move(0, BLOCK_SIZE):
        move_blocks(0, BLOCK_SIZE)
else:
generate_block()
fall_counter = 0
move_counter += 1
if move_counter >= 60 // move_speed:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if can_move(-BLOCK_SIZE, 0):
            move_blocks(-BLOCK_SIZE, 0)
    elif keys[pygame.K_RIGHT]:
        if can_move(BLOCK_SIZE, 0):
            move_blocks(BLOCK_SIZE, 0)
    elif keys[pygame.K_DOWN]:
        if can_move(0, BLOCK_SIZE):
            move_blocks(0, BLOCK_SIZE)
    move_counter = 0

# 畫面更新
screen.fill(WHITE)
all_sprites_group.draw(screen)
pygame.draw.rect(screen, BLACK, [0, 0, BLOCK_SIZE * NUM_BLOCKS_X, BLOCK_SIZE * NUM_BLOCKS_Y], 2)
pygame.draw.rect(screen, BLACK, [13 * BLOCK_SIZE, 7 * BLOCK_SIZE, 6 * BLOCK_SIZE, 6 * BLOCK_SIZE], 2)
font = pygame.font.Font(None, 36)
score_text = font.render("Score: " + str(score), True, BLACK)
screen.blit(score_text, [10, 10])
next_block_text = font.render("Next block:", True, BLACK)
screen.blit(next_block_text, [13 * BLOCK_SIZE, 5 * BLOCK_SIZE])
next_block_group.draw(screen)
pygame.display.flip()

# 遊戲結束判斷
if pygame.sprite.spritecollideany(Block(RED, BLOCK_SIZE, BLOCK_SIZE), active_blocks_group, pygame.sprite.collide_rect):
    game_over = True

# 設定遊戲難度
if score >= 100:
    fall_speed = 2
if score >= 200:
    move_speed = 7

# 設定畫面更新速度
clock.tick(60)

# 退出 Pygame
pygame.quit()

