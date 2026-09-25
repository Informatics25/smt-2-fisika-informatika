import pygame
import sys
import os
import math

# --- KONFIGURASI FISIKA ---
GRAVITY = 0.5
MASS = 1.0
BOUNCE = 0.7
FRICTION = 0.99
BALL_SPIN_FACTOR = 0.75

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Challenge")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 15)
font_besar = pygame.font.SysFont("Arial", 32, bold=True)
font_title = pygame.font.SysFont("Arial", 68, bold=True)
font_howto = pygame.font.SysFont("Arial", 18)
font_sedang = pygame.font.SysFont("Arial", 22, bold=True)

# Warna
DARK_BG = (18, 18, 28)
ORANGE = (255, 140, 0)
ORANGE_LIGHT = (255, 180, 60)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_BUTTON = (35, 35, 55)
TEXT_DARK = (25, 25, 35)
DEBUG_HITBOX = False

# Warna Background Procedural (fallback)
ARENA_TOP = (22, 24, 38)
ARENA_BOTTOM = (38, 36, 52)
WOOD_LIGHT = (165, 112, 62)
WOOD_DARK = (105, 72, 38)
COURT_LINE = (245, 245, 245)

# ==================== FUNGSI MUAT ASET ====================
def muat_aset(nama_file, ukuran, warna_fallback, bentuk="rect"):
    if os.path.exists(nama_file):
        gambar = pygame.image.load(nama_file).convert_alpha()
        return pygame.transform.scale(gambar, ukuran)
    else:
        permukaan = pygame.Surface(ukuran, pygame.SRCALPHA)
        if bentuk == "circle":
            cx, cy = ukuran[0] // 2, ukuran[1] // 2
            rad = ukuran[0] // 2 - 1
            pygame.draw.circle(permukaan, warna_fallback, (cx, cy), rad)
        else:
            permukaan.fill(warna_fallback)
        return permukaan

def muat_background():
    path = os.path.join(ASSETS_PATH, "background.png")
    if os.path.exists(path):
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    else:
        return None

# ==================== LOAD ASET ====================
BASE_DIR = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_DIR, "assets")

ukuran_bola = (40, 40)
img_ball = muat_aset(os.path.join(ASSETS_PATH, "ball.png"), ukuran_bola, ORANGE, "circle")

ukuran_player = (250, 200)
img_player = muat_aset(os.path.join(ASSETS_PATH, "player.png"), ukuran_player, (50, 50, 150))

ukuran_hoop = (350, 300)
img_hoop = muat_aset(os.path.join(ASSETS_PATH, "hoop.png"), ukuran_hoop, GRAY)

# === BACKGROUND DARI GAMBAR ===
img_background = muat_background()

# ==================== VARIABEL GAME ====================
player_pos = (50, HEIGHT - 250)
HAND_OFFSET_X = 82
HAND_OFFSET_Y = 26

def get_hand_position():
    return [player_pos[0] + HAND_OFFSET_X, player_pos[1] + HAND_OFFSET_Y]

ball_radius = ukuran_bola[0] // 2
ball_pos = list(get_hand_position())
ball_vel = [0, 0]
ball_angle = 0.0
prev_ball_y = ball_pos[1]
dragging = False
score = 0
hoop_x = 500
hoop_y = 300
backboard_rect = pygame.Rect(hoop_x + 166, hoop_y, 15, 120)
sensor_ring = pygame.Rect(hoop_x + 122, hoop_y + 62, 52, 18)

# --- SISTEM BATAS BOLA BARU ---
shots_taken = 0
MAX_SHOTS = 10
TARGET_SCORE = 5
ball_in_flight = False
is_win = False

# State
game_state = "menu"

# ==================== SISTEM UKURAN TOMBOL DINAMIS ====================
# Fungsi ini membuat ukuran tombol mengepas otomatis mengikuti panjang teks
def buat_rect_tengah(y_pos, teks, font_obj, padding_x=80, tinggi=62):
    lebar_teks = font_obj.size(teks)[0]
    lebar_tombol = lebar_teks + padding_x
    return pygame.Rect(WIDTH // 2 - lebar_tombol // 2, y_pos, lebar_tombol, tinggi)

# Tombol Menu Utama
button_start = buat_rect_tengah(210, "START GAME", font_besar)
button_how   = buat_rect_tengah(295, "HOW TO PLAY", font_besar)
button_quit  = buat_rect_tengah(380, "QUIT GAME", font_besar)

# Tombol How to Play
button_back_howto = buat_rect_tengah(520, "BACK", font_besar, tinggi=50)

# Tombol Game Over
button_play_again    = buat_rect_tengah(380, "MAIN LAGI", font_besar)
button_back_gameover = buat_rect_tengah(460, "KEMBALI KE MENU", font_sedang)

# Tombol In-Game (di pojok kiri atas, jadi manual posisinya tapi lebar dinamis)
w_menu = font_sedang.size("MENU")[0] + 40
button_menu = pygame.Rect(30, 18, w_menu, 42)


def reset_game():
    global score, ball_angle, dragging, prev_ball_y, shots_taken, ball_in_flight, is_win
    hand = get_hand_position()
    ball_pos[0], ball_pos[1] = hand[0], hand[1]
    ball_vel[0], ball_vel[1] = 0, 0
    ball_angle = 0.0
    score = 0
    shots_taken = 0
    dragging = False
    ball_in_flight = False
    is_win = False
    prev_ball_y = ball_pos[1]

def reset_ball():
    global ball_angle, dragging, prev_ball_y, ball_in_flight
    hand = get_hand_position()
    ball_pos[0], ball_pos[1] = hand[0], hand[1]
    ball_vel[0], ball_vel[1] = 0, 0
    ball_angle = 0.0
    dragging = False
    ball_in_flight = False
    prev_ball_y = ball_pos[1]

def check_score(ball_pos, prev_ball_y, sensor_ring, score):
    if (prev_ball_y < sensor_ring.top <= ball_pos[1] and
            sensor_ring.left - 3 <= ball_pos[0] <= sensor_ring.right + 3):
        return score + 1, True
    return score, False

# ==================== BACKGROUND PROCEDURAL ====================
def draw_court_background():
    for y in range(0, 430):
        ratio = y / 430
        r = int(ARENA_TOP[0] + (ARENA_BOTTOM[0] - ARENA_TOP[0]) * ratio)
        g = int(ARENA_TOP[1] + (ARENA_BOTTOM[1] - ARENA_TOP[1]) * ratio)
        b = int(ARENA_TOP[2] + (ARENA_BOTTOM[2] - ARENA_TOP[2]) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    
    floor_y = 430
    for y in range(floor_y, HEIGHT):
        ratio = (y - floor_y) / (HEIGHT - floor_y)
        r = int(WOOD_LIGHT[0] - (WOOD_LIGHT[0] - WOOD_DARK[0]) * ratio)
        g = int(WOOD_LIGHT[1] - (WOOD_LIGHT[1] - WOOD_DARK[1]) * ratio)
        b = int(WOOD_LIGHT[2] - (WOOD_LIGHT[2] - WOOD_DARK[2]) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    for i in range(6):
        plank_y = floor_y + i * 28
        if plank_y < HEIGHT:
            pygame.draw.line(screen, (85, 58, 30), (0, plank_y), (WIDTH, plank_y), 1)

    pygame.draw.line(screen, COURT_LINE, (15, HEIGHT - 6), (WIDTH - 15, HEIGHT - 6), 4)
    key_x = hoop_x + 95
    key_width = 115
    key_top = 395
    pygame.draw.rect(screen, COURT_LINE, (key_x, key_top, key_width, HEIGHT - key_top - 5), 2)
    ft_y = key_top + 85
    pygame.draw.line(screen, COURT_LINE, (key_x, ft_y), (key_x + key_width, ft_y), 3)
    pygame.draw.line(screen, COURT_LINE, (WIDTH // 2, floor_y), (WIDTH // 2, HEIGHT - 6), 2)

def draw_menu_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(15 + ratio * 12)
        g = int(15 + ratio * 10)
        b = int(25 + ratio * 18)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# ==================== TOMBOL & DRAW ====================
def draw_rounded_button(screen, rect, text, is_hovered, custom_font=None):
    if custom_font is None:
        custom_font = font_besar
        
    shadow = rect.move(5, 5)
    pygame.draw.rect(screen, (10, 10, 18), shadow, border_radius=14)
    bg_color = ORANGE_LIGHT if is_hovered else DARK_BUTTON
    text_color = TEXT_DARK if is_hovered else ORANGE
    border_color = (255, 220, 150) if is_hovered else (180, 100, 0)
    pygame.draw.rect(screen, bg_color, rect, border_radius=14)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=14)
    
    text_surf = custom_font.render(text, True, text_color)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))

def draw_menu():
    draw_menu_background()
    pygame.draw.rect(screen, (30, 30, 45), (0, 0, WIDTH, 8))
    
    title_shadow = font_title.render("BASKETBALL", True, (10, 10, 18))
    screen.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 3, 53))
    title = font_title.render("BASKETBALL", True, ORANGE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    subtitle = font.render("CHALLENGE", True, (200, 200, 210))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 125))
    pygame.draw.line(screen, ORANGE, (200, 165), (600, 165), 2)
    
    mouse_pos = pygame.mouse.get_pos()
    draw_rounded_button(screen, button_start, "START GAME", button_start.collidepoint(mouse_pos))
    draw_rounded_button(screen, button_how, "HOW TO PLAY", button_how.collidepoint(mouse_pos))
    draw_rounded_button(screen, button_quit, "QUIT GAME", button_quit.collidepoint(mouse_pos))

def draw_how_to_play():
    draw_menu_background()
    pygame.draw.rect(screen, (30, 30, 45), (0, 0, WIDTH, 8))
    
    title = font_title.render("HOW TO PLAY", True, ORANGE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    pygame.draw.line(screen, ORANGE, (220, 105), (580, 105), 2)
    
    instructions = [
        "1. Klik dan tahan bola di tangan pemain untuk mengarahkan.",
        "2. Seret mouse untuk menentukan arah dan kekuatan lemparan.",
        "3. Lepaskan tombol mouse untuk menembakkan bola.",
        "4. Kamu dibekali maksimal 10 kesempatan menembak bola.",
        "5. Cetak minimal 5 poin sebelum bola habis untuk menang!",
        "6. Jika tembakan ke-10 meleset atau bola habis = GAME OVER."
    ]
    y_pos = 160
    for line in instructions:
        if line:
            text = font_howto.render(line, True, (230, 230, 240))
            screen.blit(text, (80, y_pos))
        y_pos += 40
    
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_back_howto.collidepoint(mouse_pos)
    draw_rounded_button(screen, button_back_howto, "BACK", is_hovered)

# --- TAMPILAN LAYAR AKHIR DINAMIS ---
def draw_game_over():
    draw_menu_background()
    pygame.draw.rect(screen, (30, 30, 45), (0, 0, WIDTH, 8))
    
    if is_win:
        title_text = "YOU WIN!"
        title_color = ORANGE
        sub_text = f"Luar biasa! Kamu berhasil mencapai target {score} poin!"
    else:
        title_text = "GAME OVER"
        title_color = (240, 70, 70)  # Merah peringatan
        sub_text = f"Bola habis! Tembakan ke-10 meleset. Skor akhir: {score} / {TARGET_SCORE}"
        
    title_shadow = font_title.render(title_text, True, (10, 10, 18))
    screen.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 4, 124))
    title = font_title.render(title_text, True, title_color)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
    
    msg = font_besar.render(sub_text, True, WHITE)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 220))
    
    mouse_pos = pygame.mouse.get_pos()
    draw_rounded_button(screen, button_play_again, "MAIN LAGI", button_play_again.collidepoint(mouse_pos))
    draw_rounded_button(screen, button_back_gameover, "KEMBALI KE MENU", button_back_gameover.collidepoint(mouse_pos), custom_font=font_sedang)

def draw_game():
    screen.blit(img_player, player_pos)
    screen.blit(img_hoop, (hoop_x, hoop_y))
    
    if dragging:
        screen.blit(img_ball, (ball_pos[0] - ball_radius, ball_pos[1] - ball_radius))
    else:
        rotated_ball = pygame.transform.rotate(img_ball, ball_angle)
        ball_rect = rotated_ball.get_rect(center=(int(ball_pos[0]), int(ball_pos[1])))
        screen.blit(rotated_ball, ball_rect.topleft)
    
    # Panel Skor
    score_panel = pygame.Rect(135, 12, 160, 68)
    pygame.draw.rect(screen, (25, 25, 38), score_panel, border_radius=12)
    pygame.draw.rect(screen, ORANGE, score_panel, width=3, border_radius=12)
    label_score = font.render("SCORE", True, ORANGE)
    screen.blit(label_score, (score_panel.centerx - label_score.get_width() // 2, 18))
    score_num = font_besar.render(f"{score} / {TARGET_SCORE}", True, WHITE)
    screen.blit(score_num, (score_panel.centerx - score_num.get_width() // 2, 38))
    
    # Panel Sisa Bola Baru
    ball_panel = pygame.Rect(310, 12, 160, 68)
    pygame.draw.rect(screen, (25, 25, 38), ball_panel, border_radius=12)
    pygame.draw.rect(screen, (130, 130, 140), ball_panel, width=3, border_radius=12)
    label_ball = font.render("SISA BOLA", True, GRAY)
    screen.blit(label_ball, (ball_panel.centerx - label_ball.get_width() // 2, 18))
    ball_num = font_besar.render(f"{MAX_SHOTS - shots_taken}", True, WHITE)
    screen.blit(ball_num, (ball_panel.centerx - ball_num.get_width() // 2, 38))
    
    mouse_pos = pygame.mouse.get_pos()
    is_hovered_menu = button_menu.collidepoint(mouse_pos)
    draw_rounded_button(screen, button_menu, "MENU", is_hovered_menu, custom_font=font_sedang)
    
    hint = font.render("Drag ball → Release to shoot | Press R to reset ball", True, (180, 180, 190))
    screen.blit(hint, (30, 95))

# ==================== LOOP UTAMA ====================
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "playing"
                elif button_how.collidepoint(mouse_pos):
                    game_state = "how_to_play"
                elif button_quit.collidepoint(mouse_pos):
                    running = False
        
        elif game_state == "how_to_play":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back_howto.collidepoint(mouse_pos):
                    game_state = "menu"
        
        elif game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play_again.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "playing"
                elif button_back_gameover.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "menu"
        
        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_menu.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "menu"
                else:
                    dist = ((mouse_pos[0] - ball_pos[0])**2 + (mouse_pos[1] - ball_pos[1])**2)**0.5
                    if dist < ball_radius * 2:
                        dragging = True
            
            # Deteksi ketika bola dilepas (Tembakan terhitung)
            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    ball_in_flight = True
                    shots_taken += 1
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_ball()  # Reset bola ke tangan saja tanpa menghapus skor total
    
    # ==================== DRAW ====================
    if game_state == "playing":
        if img_background:
            screen.blit(img_background, (0, 0))
        else:
            draw_court_background()
    elif game_state == "menu":
        draw_menu()
    elif game_state == "how_to_play":
        draw_how_to_play()
    elif game_state == "game_over":
        draw_game_over()
    
    if game_state == "playing":
        if dragging:
            hand = get_hand_position()
            ball_pos[0], ball_pos[1] = hand[0], hand[1]
            multiplier = 0.15
            ball_vel[0] = (mouse_pos[0] - hand[0]) * multiplier
            ball_vel[1] = (mouse_pos[1] - hand[1]) * multiplier
            
            temp_x, temp_y = hand[0], hand[1]
            temp_vx, temp_vy = ball_vel[0], ball_vel[1]
            for i in range(45):
                temp_vy += GRAVITY
                temp_x += temp_vx
                temp_y += temp_vy
                temp_vx *= FRICTION
                temp_vy *= FRICTION
                pygame.draw.circle(screen, ORANGE_LIGHT, (int(temp_x), int(temp_y)), 3)
        else:
            ball_vel[1] += GRAVITY
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            
            if ball_pos[1] + ball_radius > HEIGHT:
                ball_pos[1] = HEIGHT - ball_radius
                ball_vel[1] *= -BOUNCE
            if ball_pos[0] + ball_radius > WIDTH:
                ball_pos[0] = WIDTH - ball_radius
                ball_vel[0] *= -BOUNCE
            elif ball_pos[0] - ball_radius < 0:
                ball_pos[0] = ball_radius
                ball_vel[0] *= -BOUNCE
            
            ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ukuran_bola[0], ukuran_bola[1])
            if backboard_rect.colliderect(ball_rect):
                ball_pos[0] = backboard_rect.left - ball_radius
                ball_vel[0] *= -BOUNCE
            
            score, did_score = check_score(ball_pos, prev_ball_y, sensor_ring, score)
            if did_score:
                ball_in_flight = False
                reset_ball()
            prev_ball_y = ball_pos[1]
            
            ball_vel[0] *= FRICTION
            ball_vel[1] *= FRICTION
            
            perubahan_sudut = (ball_vel[0] / ball_radius) * (180 / math.pi)
            ball_angle -= perubahan_sudut
            
            speed = (ball_vel[0]**2 + ball_vel[1]**2) ** 0.5
            if speed < 0.6:
                ball_in_flight = False
                reset_ball()
        
        draw_game()

        # --- LOGIKA PENGECEKAN KEMENANGAN / KEKALAHAN ---
        if score >= TARGET_SCORE:
            is_win = True
            game_state = "game_over"
        elif not ball_in_flight and not dragging and shots_taken >= MAX_SHOTS:
            is_win = False
            game_state = "game_over"
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()