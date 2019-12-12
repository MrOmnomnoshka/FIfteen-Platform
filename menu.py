from constants import *


class Button:
    active = False
    # small_text = pygame.font.SysFont('сambria', 50)
    from constants import inf_font

    def __init__(self, surface, bx, by, b_color, action=None, par=None):
        self.surface = surface
        self.x = bx
        self.y = by
        self.color = b_color
        self.action = action
        self.par = par

        if type(self.surface) is str:
            # color under the mouse
            self.color_active = [self.color[0]+20, self.color[1]+20, self.color[2]+20]
            self.color_active[0] = 255 if self.color_active[0] > 255 else self.color_active[0]  # red
            self.color_active[1] = 255 if self.color_active[1] > 255 else self.color_active[1]  # green
            self.color_active[2] = 255 if self.color_active[2] > 255 else self.color_active[2]  # blue

        if type(self.surface) is str:
            x_i = self.inf_font.size(surface)[0] // 2
            y_i = self.inf_font.size(surface)[1] // 2
            # x_i = 30
            # y_i = 30
            self.w = x_i*2 + 20
            self.h = 50
            self.tx = bx + self.w // 2 - x_i
            self.ty = by + self.h // 2 - y_i
        else:
            self.w, self.h = self.surface.get_rect()[2:]

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0] == 0:  # if mouse up
            self.active = False

        # print(click)
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            if type(self.surface) is str:
                pygame.draw.rect(screen, self.color_active, (self.x, self.y, self.w, self.h))
            else:
                screen.blit(pygame.transform.scale(self.surface, (self.w-10, self.h-10)), (5+self.x, 5+self.y))

            if click[0] == 1 and self.action and not self.active:
                pop_sound.play()
                self.active = True
                if self.par:
                    self.action(self.par)
                else:
                    self.action()
        else:
            if type(self.surface) is str:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            else:
                screen.blit(self.surface, (self.x, self.y))

        if type(self.surface) is str:
            text = self.inf_font.render(self.surface, 0, WHITE)
            screen.blit(text, (self.tx, self.ty))
            pass


# Initialization
pygame.init()  # Работу себе найди
pygame.mixer.init()  # Рабта со звуком
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Fifteen Platform')


def change_mode(new_mode):
    global mode
    mode = new_mode


def full_quit():
    pygame.quit()
    quit()


# Prepare Game Objects
mode = "menu"
first_time = True
# All sounds
key_sound = pygame.mixer.Sound("sounds/key.ogg")
pop_sound = pygame.mixer.Sound("sounds/pop.ogg")
# Menu buttons
buttons = list()
buttons.append(Button("Play", 565, 300, (25, 65, 65), change_mode, 'game'))
buttons.append(Button("Levels", 550, 400, (25, 65, 65), change_mode, 'levels'))
buttons.append(Button("Exit", 570, 500, (25, 65, 65), full_quit))
# ====================


# Main Loop
def main():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit
                full_quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                full_quit()
        draw(mode)
        # Speed limit
        pygame.time.Clock().tick(60)


def draw(mode):
    if mode == "menu":
        draw_menu()

    elif mode == "game":
        import game
        game.main()
        change_mode('menu')
    elif mode == "levels":
        import levels
        levels.main()
        change_mode('menu')


def draw_menu():
    #  Background
    screen.fill(BACKGROUND)

    for b in buttons:
        b.update()

    # Draws current level
    from levels import lvl_for_game
    from game import level
    inf_level = lvl_for_game.number + 1 if lvl_for_game else level
    index = inf_font.render("(Level-" + str(inf_level)+")", 0, WHITE, BACKGROUND)
    index.set_alpha(50)
    screen.blit(index, (665, 290))

    # Update all animation
    pygame.display.flip()


if __name__ == "__main__":
    main()
