import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface([30, 30], pygame.SRCALPHA) # Tạo bề mặt trong suốt cho hình tròn
        pygame.draw.circle(self.image, (0, 255, 0), (15, 15), 15) # Vẽ hình tròn xanh lá cây (đã sửa màu)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2) # Bắt đầu ở giữa màn hình
        self.speed = 5  # Giảm tốc độ xuống còn 2
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Phím A (sang trái)
            self.rect.x -= self.speed
        if keys[pygame.K_d]:  # Phím D (sang phải)
            self.rect.x += self.speed
        if keys[pygame.K_w]:  # Phím W (lên trên)
            self.rect.y -= self.speed
        if keys[pygame.K_s]:  # Phím S (xuống dưới)
            self.rect.y += self.speed

        # Giữ nhân vật trong màn hình
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