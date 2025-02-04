import pygame
import random
import time

class AIPlayer(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface([30, 30], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (15, 15), 15) # Màu xanh dương giống player
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(0, screen_width), random.randrange(0, screen_height)) # Vị trí ngẫu nhiên ban đầu
        self.speed = 5 # Tốc độ giống player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.target_position = self.generate_random_target() # Mục tiêu di chuyển ban đầu
        self.wait_time = 1 # Thời gian đợi (giây)
        self.wait_timer = 0 # Bộ đếm thời gian đợi hiện tại
        self.is_waiting = False # Trạng thái đợi

    def generate_random_target(self):
        """Tạo một vị trí mục tiêu ngẫu nhiên trong màn hình."""
        return (random.randrange(0, self.screen_width), random.randrange(0, self.screen_height))

    def update(self, delta_time):
        if self.is_waiting:
            self.wait_timer -= delta_time
            if self.wait_timer <= 0:
                self.is_waiting = False
                self.target_position = self.generate_random_target() # Chọn mục tiêu mới sau khi đợi
        else:
            # Tính toán vector di chuyển đến mục tiêu
            direction_x = self.target_position[0] - self.rect.centerx
            direction_y = self.target_position[1] - self.rect.centery
            distance = ((direction_x ** 2) + (direction_y ** 2)) ** 0.5 # Khoảng cách

            if distance < 5: # Đến đủ gần mục tiêu
                self.is_waiting = True
                self.wait_timer = self.wait_time
            else:
                # Chuẩn hóa vector di chuyển và di chuyển theo tốc độ
                direction_x = direction_x / distance
                direction_y = direction_y / distance
                self.rect.x += direction_x * self.speed * delta_time * 60 # Nhân với delta_time và 60fps (ước lượng) để di chuyển mượt mà theo thời gian thực
                self.rect.y += direction_y * self.speed * delta_time * 60

        # Giữ AI player trong màn hình (giống player)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def draw(self, screen):
        screen.blit(self.image, self.rect)