import pygame

# pygame initialization:
if __name__ == '__main__':
    pygame.init()
    display = pygame.display.set_mode((500, 500))

    font = pygame.font.Font("./resources/fonts/retro-land-mayhem.ttf", 55)
    text = font.render("LEJEJJE", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.blit(text, (0, 0))

        pygame.display.update()

    pygame.quit()
