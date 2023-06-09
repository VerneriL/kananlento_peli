import pygame

def main():
    game = Game()
    game.run()

class Game():    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = False
        self.init_graphics()
        self.init_objects()

    def init_graphics(self):
        self.bird_frame = 0
        bird_imgs = [
            pygame.image.load(f"images/chicken/flying/frame-{i}.png")
            for i in [1, 2, 3, 4]
        ]
        self.bird_imgs = [
            pygame.transform.rotozoom(x, 0, 1/16)
            for x in bird_imgs
        ]
        original_bird_dead_imgs = [
            pygame.image.load(f"images/chicken/got_hit/frame-{i}.png")
            for i in [1, 2]
        ]

        bg_imgs = [
            pygame.image.load(f"images/background/layer_{i}.png")
            for i in [1, 2, 3]
        ]
        self.bg_imgs = [
            pygame.transform.rotozoom(x, 0, 600 / x.get_height()).convert_alpha()
            for x in bg_imgs
        ]

        self.bg_widths = [x.get_width() for x in self.bg_imgs]

    def init_objects(self):
        self.bird_alive =  True
        self.bird_y_speed = 0
        self.bird_pos = (800/3, 600/2)
        self.bird_angle = 0
        self.bird_lift = False
        self.bg_pos = [0, 0, 0]
        
    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.handle_events()
            self.handle_game_logic()
            self.update_screen()
            clock.tick(60) # Wait until refresh rate is 60fps
        pygame.quit()

    def handle_events(self):
        # Loop through events
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird_lift = False

    def handle_game_logic(self):
        if self.bird_alive:
            # Background speeds
            self.bg_pos[0] -= 0.25
            self.bg_pos[1] -= 0.5
            self.bg_pos[2] -= 2

        # Bird y coordinate
        bird_y = self.bird_pos[1] 
        
        if self.bird_alive and self.bird_lift:
            # Lift bird y-pixel per frame
            self.bird_y_speed -= 0.5
            # Acceleration
            self.bird_frame += 1
        else:
            # Gravity
            self.bird_y_speed += 0.2

        # Move bird based on bird speed
        bird_y += self.bird_y_speed
                
        if self.bird_alive: # Jos lintu elossa
            # Determine bird angle
            self.bird_angle = -90 * 0.04 * self.bird_y_speed
            self.bird_angle = max(min(self.bird_angle, 60), -60)

        # Tarkista onko lintu pudonnut maahan
        if bird_y > 600 - 140:
            bird_y = 600 - 140
            self.bird_y_speed = 0
            self.bird_alive = False

        if bird_y < 10:
            pass

        # Aseta linnut x-y-koordinaatit self.bird_pos muuttujaan
        self.bird_pos = (self.bird_pos[0], bird_y)

    def update_screen(self):    
        # self.screen.fill((230, 230, 255)) # Light blue
        # Background display
        for i in [0, 1, 2]:
            # Piissä vasen tausta
            self.screen.blit(self.bg_imgs[i], (self.bg_pos[i], 0))
            # Jos vasen ei riitä peittämään koko ruutua, niin...
            if self.bg_pos[i] + self.bg_widths[i] < 800:
                # piirrä sama tausta vielä oikealle puolelle
                self.screen.blit(
                    self.bg_imgs[i],
                    (self.bg_pos[i] + self.bg_widths[0], 0)
                )
            # Jos taustaa on siirretty sen leveyden verran...
            if self.bg_pos[i] < -self.bg_widths[0]:
                # ...niin aloita alusta
                self.bg_pos[i] += self.bg_widths[0]

        
        # Draw bird from images depending on frames up to 3
        if self.bird_alive:
            bird_img_i = self.bird_imgs[(self.bird_frame // 3) % 4]
        else:
            bird_img = pygame.transform.rotozoom(bird_img_i, self.bird_angle, 1)
            self.screen.blit(bird_img, self.bird_pos)

        # Display
        pygame.display.flip()


if __name__=="__main__":
    main()
