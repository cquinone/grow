import pygame
import pygame_gui


# 20 * image buttons
# Network drive: Auto Image loading time taken: 14-17 seconds.

pygame.init()


pygame.display.set_caption('Image Loading Test')
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))
clock = pygame.time.Clock()
load_time_1 = clock.tick()
manager = pygame_gui.UIManager((800, 600), 'data/themes/image_loading_test.json')

load_time_2 = clock.tick()

print('Image loading time taken:', load_time_2 / 1000.0, 'seconds.')

button_row_width = 200
button_row_height = 150
spacing = 0
num_buttons = 1
for j in range(1, 5):
    for i in range(1, 5):
        position = (i * spacing + ((i - 1) * button_row_width),
                    (j * spacing + ((j - 1) * button_row_height)))
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,
                                                               (button_row_width,
                                                                button_row_height)),
                                     text=str(num_buttons),
                                     manager=manager,
                                     object_id='#'+str(num_buttons))
        num_buttons += 1


hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)

is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()