import pygame
import player
import ai_player
from assets.Game import dead_area as dead_area_module
import random

# Khởi tạo Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init() # Khởi tạo Pygame mixer (cho âm thanh)

# Thiết lập màn hình (giữ nguyên)
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Squid Game X")

# Màu sắc (giữ nguyên)
gray_color = (100, 100, 100)
blue_color = (0, 0, 255)
green_color = (0, 255, 0)
white_color = (255, 255, 255)

# Player, AI Players, Sprite groups, Font, Player lists, Clock (giữ nguyên)
player_sprite = player.Player(screen_width, screen_height)
num_ai_players = 29
ai_players = []
for _ in range(num_ai_players):
    ai_players.append(ai_player.AIPlayer(screen_width, screen_height))
all_sprites = pygame.sprite.Group()
all_sprites.add(player_sprite)
for ai in ai_players:
    all_sprites.add(ai)
font = pygame.font.Font(None, 36)
player_count = 1 + num_ai_players
alive_players = [player_sprite] + ai_players
dead_players = []
clock = pygame.time.Clock()

# Biến Dead Area và độ khó (giữ nguyên)
dead_area_event_timer = 0
dead_area_interval = 10
active_dead_areas = []
dead_area_probability = 0.5
no_event_probability_increase = 0.25
dead_area_duration = 5
dead_area_duration_decrease = 2
num_dead_areas_to_create = 3
num_dead_areas_increase = 1
dead_area_event_count = 0

# --- LOAD ÂM THANH ---
warning_sound = pygame.mixer.Sound("assets/audio/warning_in_game_1.wav") # Load sound effect

# Vòng lặp game (sửa logic Dead Area)
running = True
warning_sound_playing = False # Biến trạng thái âm thanh

while running:
    delta_time = clock.tick(60) / 1000.0

    # Xử lý sự kiện (giữ nguyên)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Cập nhật game (giữ nguyên)
    player_sprite.update()
    for ai in ai_players:
        ai.update(delta_time)

    # Logic Dead Area
    dead_area_event_timer += delta_time
    if dead_area_event_timer >= dead_area_interval:
        dead_area_event_timer = 0 # Reset timer

        # Kiểm tra xác suất Dead Area
        if random.random() < dead_area_probability:
            print("Dead Area event triggered!")

            num_dead_areas_to_create = max(1, num_dead_areas_to_create)
            area_radius = 80

            # --- PHÁT ÂM THANH CẢNH BÁO KHI DEAD AREA XUẤT HIỆN ---
            if not warning_sound_playing: # Check if sound is not already playing
                warning_sound.play(-1) # Play warning sound, -1 for loop (play infinitely until stopped)
                warning_sound_playing = True # Set state to playing

            # Tạo các Dead Area vòng tròn
            for _ in range(num_dead_areas_to_create):
                random_x = random.randrange(area_radius, screen_width - area_radius)
                random_y = random.randrange(area_radius, screen_height - area_radius)
                dead_area_instance = dead_area_module.DeadArea((random_x, random_y), area_radius, dead_area_duration)
                active_dead_areas.append(dead_area_instance)

            # Cập nhật độ khó (giữ nguyên)
            dead_area_probability = max(0, dead_area_probability - no_event_probability_increase)
            dead_area_duration = max(1, dead_area_duration - dead_area_duration_decrease)
            num_dead_areas_to_create += num_dead_areas_increase
            dead_area_event_count += 1

            print(f"Dead Area Probability: {dead_area_probability:.2f}")
            print(f"Dead Area Duration: {dead_area_duration:.2f} seconds")
            print(f"Number of Dead Areas: {num_dead_areas_to_create}")
            print(f"Event Count: {dead_area_event_count}")
        else:
            print("No Dead Area event this time.")

    # Cập nhật Dead Areas đang hoạt động và xử lý loại bỏ player
    for area in list(active_dead_areas):
        area.update(delta_time)
        if not area.active: # Nếu Dead Area hết thời gian
            # Kiểm tra player bên trong Dead Area và loại bỏ (giữ nguyên)
            players_to_remove = []
            for player_obj in list(alive_players):
                if area.is_player_inside(player_obj.rect):
                    players_to_remove.append(player_obj)

            for removed_player in players_to_remove:
                if removed_player in alive_players:
                    alive_players.remove(removed_player)
                    dead_players.append(removed_player)
                    all_sprites.remove(removed_player)
                    if removed_player == player_sprite:
                        print("You are eliminated!")
                    else:
                        print("AI player eliminated!")

            active_dead_areas.remove(area) # Xóa Dead Area sau khi xử lý loại bỏ

            # --- DỪNG ÂM THANH CẢNH BÁO KHI DEAD AREA KẾT THÚC ---
            if warning_sound_playing:
                warning_sound.stop() # Stop warning sound
                warning_sound_playing = False # Reset sound state


    # Cập nhật player count, Vẽ màn hình, UI, Sprites, Cập nhật hiển thị (giữ nguyên)
    player_count = len(alive_players)
    screen.fill(gray_color)
    for area in active_dead_areas:
        area.draw(screen)
    text_surface = font.render(f"Players: {player_count}", True, white_color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text_surface, text_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

# Thoát Pygame (sửa để quit mixer)
pygame.quit()
pygame.font.quit()
pygame.mixer.quit() # Quit pygame mixer when exiting
