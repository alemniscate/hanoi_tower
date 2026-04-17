import random
import js

DISK_COUNT = 4
TOWER_COUNT = 3

game = {
    "towers": [[], [], []],
    "selected_tower": -1,
    "move_count": 0
}

DISK_COLORS = [
    "#FFFF44",
    "#4444FF",
    "#44FF44",
    "#FF4444"
]

#
# utils.py
#
def q(query):
    return js.document.querySelector(query)

def q_text(query, text):
    q(query).innerText = text
    
def set_timeout(f, ms):
    return js.setTimeout(f, ms)

#
# main.py
#

def start_game():

    game["towers"] = [list(range(DISK_COUNT - 1, -1, -1)), [], []]
    game["selected_tower"] = -1
    game["move_count"] = 0
    
    draw_game()
    
def move_disk(from_tower, to_tower):
    if not can_move(from_tower, to_tower):
        return False
    
    disk = game["towers"][from_tower].pop()
    game["towers"][to_tower].append(disk)
    game["move_count"] += 1
    
    if check_clear():
        def show_clear_message():
            q_text("#title", "ハノイの塔をゲームクリア")
            q_text("#info", "おめでとう！")
        set_timeout(show_clear_message, 100)
        
    return True

def can_move(from_tower, to_tower):
    if from_tower < 0 or from_tower >= TOWER_COUNT:
        return False
    if to_tower < 0 or to_tower >= TOWER_COUNT:
        return False
    if from_tower == to_tower:
        return False
    if len(game["towers"][from_tower]) == 0:
        return False
    if len(game["towers"][to_tower]) == 0:
        return True
    from_disk = game["towers"][from_tower][-1]
    to_disk = game["towers"][to_tower][-1]
    return from_disk < to_disk

def check_clear():
    target_order = list(range(DISK_COUNT - 1, -1, -1))
    for tower_index in [1, 2]:
        if game["towers"][tower_index] == target_order:
            return True
    return False
    
#
# draw.py
#

canvas = q("#canvas")
context = canvas.getContext("2d")

TOWER_WIDTH = 8
TOWER_HEIGHT = 200
TOWER_BASE_WIDTH = 100
TOWER_BASE_HEIGHT = 20
DISK_HEIGHT = 20
MAX_DISK_WIDTH = 80
MIN_DISK_WIDTH = 30
PANEL_W = canvas.width // TOWER_COUNT

def draw_game():
    context.clearRect(0, 0, canvas.width, canvas.height)
    draw_move_count()
    draw_selection()
    for i in range(TOWER_COUNT):
        draw_tower(i)
        draw_disks(i)

def draw_tower(index):
    x = PANEL_W * index + PANEL_W // 2
    context.fillStyle = "#8B4513"
    tower_x = x - TOWER_WIDTH // 2
    tower_y = 150
    context.fillRect(tower_x, tower_y, TOWER_WIDTH, TOWER_HEIGHT)
    base_x = x - TOWER_BASE_WIDTH // 2
    base_y = 150 + TOWER_HEIGHT
    context.fillRect(base_x, base_y, TOWER_BASE_WIDTH, TOWER_BASE_HEIGHT)
    
def draw_disks(index):
    tower_x = PANEL_W * index + PANEL_W // 2
    disks = game["towers"][index]
    for disk_idx, disk_size in enumerate(disks):
        disk_width = MIN_DISK_WIDTH + (MAX_DISK_WIDTH - MIN_DISK_WIDTH) * disk_size // (DISK_COUNT - 1)
        disk_x = tower_x - disk_width // 2
        disk_y = 150 + TOWER_HEIGHT - (disk_idx + 1) * DISK_HEIGHT
        context.fillStyle = DISK_COLORS[disk_size]
        context.fillRect(disk_x, disk_y, disk_width, DISK_HEIGHT)
        context.strokeStyle = "#333333"
        context.lineWidth = 2
        context.strokeRect(disk_x, disk_y, disk_width, DISK_HEIGHT)

def draw_selection():
    if game["selected_tower"] < 0:
        return
    x = PANEL_W * game["selected_tower"]
    h = TOWER_HEIGHT + TOWER_BASE_HEIGHT + 15
    context.strokeStyle = "#FF6600"
    context.fillStyle = "rgba(200, 200, 255, 0.3)"
    context.lineWidth = 3
    context.fillRect(x + 10, 140, PANEL_W - 20, h)
    context.strokeRect(x + 10, 140, PANEL_W - 20, h)
    
def draw_move_count():
    context.fillStyle = "#333333"
    context.font = "16px Arial"
    context.textAlign = "center"
    context.fillText(f"移動回数： {game['move_count']}", canvas.width // 2, 30)

#
# click.py
#

def canvas_on_click(event):
    rect = canvas.getBoundingClientRect()
    x = int(event.clientX - rect.left)
    y = int(event.clientY - rect.top)
    
    panel_w = canvas.width // TOWER_COUNT
    clicked_tower = x // panel_w
    if 0 <= clicked_tower < TOWER_COUNT:
        handle_tower(clicked_tower)
        
canvas.addEventListener("click", canvas_on_click)
        
def handle_tower(index):
    q_text("#info", "")
    if game["selected_tower"] == -1:
        if game["towers"][index]:
            game["selected_tower"] = index
            q_text("#info", f"塔{index + 1}の円盤の移動先を選んでください")
    else:
        if move_disk(game["selected_tower"], index):
            q_text("#info", f"円盤を塔{index + 1}に移動しました")
        else:
            q_text("#info", f"塔{index + 1}に移動できません")
        game["selected_tower"] = -1
    draw_game() 
