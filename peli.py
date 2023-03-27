import pygame

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get(): # Loop through events
            if event.type == pygame.QUIT:
                running = False
        print("kierros")

        screen.fill("purple")

        pygame.display.flip()



        clock.tick(60) # Wait until refresh rate is 60fps

    pygame.quit()


if __name__=="__main__":
    main()