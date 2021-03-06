from random import randint
import pygame

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 3000)

W = 400
H = 400
WHITE = (255, 255, 255)
CARS = ('red', 'yellow', 'brown')
CARS_SURF = []  # для хранения готовых машин-поверхностей

# надо установить видео режим до вызова image.load()
sc = pygame.display.set_mode((W, H))

for i in range(len(CARS)):
    a = pygame.Surface((20, 40))
    a.fill(pygame.Color(CARS[i]))
    CARS_SURF.append(a)


class Car(pygame.sprite.Sprite):
    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.add(group)  # добавляем в группу
        self.speed = randint(1, 3)  # у машин будет разная скорость

    def update(self):
        if self.rect.y < H:
            self.rect.y += self.speed
        else:
            # теперь не перебрасываем вверх,
            # а удаляем из всех групп
            self.kill()


cars = pygame.sprite.Group()

# добавляем первую машину, которая появляется сразу
Car(randint(1, W), CARS_SURF[randint(0, 2)], cars)

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.USEREVENT:
            Car(randint(1, W), CARS_SURF[randint(0, 2)], cars)

    sc.fill(WHITE)
    cars.draw(sc)
    pygame.display.update()
    pygame.time.delay(20)
    cars.update()
