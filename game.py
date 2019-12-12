from menu import screen, full_quit, first_time
from constants import *


class Platform:
    length = 20
    chest_img = pygame.image.load('images/chest.png')
    key_img = pygame.image.load('images/key.png')
    platform = pygame.image.load('images/platform.png')

    def __init__(self, x, y, chest=False, key=False):
        self.x = x
        self.y = y

        self.chest = chest
        self.key = key

    def show(self):
        if self.chest:
            picture = self.chest_img
        elif self.key:
            picture = self.key_img
        else:
            picture = self.platform
        screen.blit(picture, (self.x, self.y))


class Cell:
    size = 400

    def __init__(self, platforms, x, y, empty=False):
        self.platforms = platforms.copy()
        self.x = x
        self.y = y
        self.empty = empty

    def show(self):
        for p in self.platforms:
            p.show()

    def move_platforms(self, direction, cell_pos, reverse=1):
        self.x, self.y = cell_pos[0], cell_pos[1]
        for p in self.platforms:
            if direction == "up":
                p.y -= 400 * reverse
            if direction == "down":
                p.y += 400 * reverse
            if direction == "left":
                p.x -= 400 * reverse
            if direction == "right":
                p.x += 400 * reverse


class Player:
    length, height = 20, 30
    stand = pygame.image.load('images/hero.png')
    moving = (pygame.image.load('images/hero_moving_1.png'), pygame.image.load('images/hero_moving_2.png'))

    up = False  # Just stand
    key = False  # No keys
    next_level = False  # Fix it plz
    img_count = 0  # for animation

    cells = []  # All cells
    last_cell = None  # Debug
    cell = None  # Current cell

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Set speed vector of player
        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        """ Move the player. """
        # Gravity
        self.gravity()

        # Move left/right
        self.x += self.x_speed
        # See if we hit anything
        obstacles = self.collide_check()
        for block in obstacles:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.x_speed > 0:
                self.x = block.x - self.length
            elif self.x_speed < 0:
                # Otherwise if we are moving left, do the opposite.
                self.x = block.x + block.length

        # Move up/down
        if self.up:
            self.jump()
        self.y += self.y_speed
        # Check and see if we hit anything
        obstacles = self.collide_check()
        for block in obstacles:
            # Reset our position based on the top/bottom of the object.
            if self.y_speed > 0:
                self.y = block.y - self.height
            elif self.y_speed < 0:
                self.y = block.y + block.length
            # Stop our vertical movement
            self.y_speed = 0

    def gravity(self):
        """ Calculate effect of gravity. """
        self.y_speed += .45

        # See if we are on the end of a screen.
        if self.y > HEIGHT - self.height and self.y_speed >= 0:
            self.y_speed = 0
            self.y = HEIGHT - self.height
        elif self.y <= 0 and self.y_speed <= 0:
            self.y_speed = 0
            self.y = 0

    def jump(self):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        self.y += 2
        obstacles = self.collide_check()
        self.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(obstacles) > 0 or self.y + self.height >= HEIGHT:
            jump_sound.play()
            self.y_speed = -8

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.x_speed = -5

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.x_speed = 5

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.x_speed = 0
    # ========================

    def collide_check(self):
        """ Checking for collision. """
        # find which cell
        self.cell = self.which_cell()
        obstacles = []
        for c in self.cells:
            for p in c.platforms:
                if self.x + self.length > p.x and self.x < p.x + p.length:
                    if self.y + self.height > p.y and self.y < p.y + p.length:
                        obstacles.append(p)
                        if p.chest:
                            if self.key:
                                self.next_level = True
                                pygame.mixer.music.stop()
                                chest_sound.play()
                                pygame.time.delay(int(chest_sound.get_length() * 1000))  # Stop for opening-sound time
                            else:
                                error_sound.play()
                        if p.key:
                            self.key = True
                            c.platforms.remove(p)
                            key_sound.play()
        return obstacles

    def which_cell(self):
        """ Finds current cell. """
        for c in self.cells:
            if c.x <= self.x + 1 <= c.x + c.size and c.y <= self.y + 1 <= c.y + c.size:
                self.last_cell = c
                return c
        return self.last_cell  # Just for sure

    def move(self, direct):
        """ Move a hero when cell moving """
        if direct == 'up':
            self.y -= -400
        elif direct == 'down':
            self.y += -400
        elif direct == 'left':
            self.x -= -400
        elif direct == 'right':
            self.x += -400

    def show(self):
        """ Draws the player. """
        self.img_count += 1
        if self.img_count >= 30:
            self.img_count = 0

        if self.x_speed > 0:
            image = self.moving[self.img_count // 15]
        elif self.x_speed < 0:
            image = pygame.transform.flip(self.moving[self.img_count // 15], True, 0)
        else:
            image = self.stand
        screen.blit(image, (self.x, self.y))

    def add_level(self, cells):
        self.cells = cells
        self.cell = cells[0]


# Prepare Game Objects
clock = pygame.time.Clock()
inf_font = pygame.font.SysFont("Arial", 35)
menu = False
level = 1
#           All sounds
key_sound = pygame.mixer.Sound("sounds/key.ogg")
chest_sound = pygame.mixer.Sound("sounds/chest.ogg")
error_sound = pygame.mixer.Sound("sounds/error.ogg")
jump_sound = pygame.mixer.Sound("sounds/jump.ogg")
pop_sound = pygame.mixer.Sound("sounds/pop.ogg")
win_sound = pygame.mixer.Sound("sounds/win.ogg")

pygame.mixer.music.load("sounds/steps.ogg")
# ====================


# Main Loop
def main():
    global menu, level
    from levels import lvl_for_game
    level = lvl_for_game.number + 1 if lvl_for_game else level

    lvl_amount = os.listdir(os.getcwd() + "/levels")  # 'getcwd' return your directory path
    max_level = len(lvl_amount)  # minus template.png
    menu = False
    while True:
        global first_time
        if first_time:
            game_intro()
            first_time = False
        else:
            game_board()
        if level == max_level:
            # Prints WIN
            win_sound.play()  # All level passed
            screen.fill(BLACK)
            win_font = pygame.font.SysFont('Algerian', 100)
            size = win_font.size("Congratulations!")
            congrats = win_font.render("Congratulations!", True, WHITE, BLACK)
            screen.blit(congrats, (WIDTH // 2 - size[0] // 2, HEIGHT // 2 - size[1] // 2))
            pygame.display.flip()

            pygame.time.delay(2500)
            break
        if menu:
            break


def next_level():
    global level
    level += 1


def game_intro():
    screen.fill(BLACK)
    win_font = pygame.font.SysFont('Agency FB', 50)

    phrases = (win_font.render("Hello friend!", True, WHITE),
               win_font.render("This Game is very simple.", True, WHITE),
               win_font.render("You have to play for SUPER NINJA WARRIOR.", True, WHITE),
               win_font.render("Whose goal is to find all the treasures.", True, WHITE),
               win_font.render("In a strange and changeable world.", True, WHITE),
               win_font.render("Which YOU also control!", True, WHITE),
               win_font.render("Character and Level control: arrows.", True, WHITE),
               win_font.render("Change mode: space.", True, WHITE))

    for phrase in phrases:
        pop_sound.play()
        screen.blit(phrase, (300, 100 + phrases.index(phrase) * 60))
        pygame.display.flip()
        for i in range(800):
            pygame.time.delay(2)
            pygame.event.get()

    intro = True
    crutch = 0
    phrase_render = True
    while intro:
        # Control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_quit()

            if event.type == pygame.KEYDOWN:  # if any key is pressed
                intro = False

        # Switcher
        crutch += 1
        if crutch % 500 == 0:
            phrase_render = not phrase_render

        if phrase_render:
            phrase = win_font.render("Press any key to continue...", True, GREY)
            screen.blit(phrase, (300, 100 + len(phrases) * 60))
        else:
            pygame.draw.rect(screen, BLACK, (300, 100 + len(phrases) * 60, 600, 100 + (len(phrases)+1) * 60))
        pygame.display.flip()


def game_board():
    # Generate level and hero
    image = pygame.image.load('levels/{}.png'.format(level))
    cells, hero = create_level_from_image(image)
    hero.add_level(cells)

    # ====================  MAIN CYCLE  ====================
    game = True
    mix_mode = False
    zooming = 300
    global menu
    while game and not menu:
        # Control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_quit()

            if event.type == pygame.KEYDOWN:  # if any key is pressed
                # Exit
                if event.key == pygame.K_ESCAPE:
                    menu = True
                # Restart
                if event.key == pygame.K_r:
                    game = False

                # Move Left
                if event.key == pygame.K_LEFT:
                    if mix_mode:
                        move_tile(cells, 'left', hero)
                    else:
                        hero.go_left()
                # Move Right
                if event.key == pygame.K_RIGHT:
                    if mix_mode:
                        move_tile(cells, 'right', hero)
                    else:
                        hero.go_right()
                # Move Up
                if event.key == pygame.K_UP:
                    if mix_mode:
                        move_tile(cells, 'up', hero)
                    else:
                        hero.up = True  # bool даёт возможность зажать прыжок
                # Move Down
                if mix_mode:
                    if event.key == pygame.K_DOWN:
                        move_tile(cells, 'down', hero)

                # Change mode
                if event.key == pygame.K_SPACE:
                    mix_mode = not mix_mode
                    pop_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and hero.x_speed < 0:
                    hero.stop()
                if event.key == pygame.K_RIGHT and hero.x_speed > 0:
                    hero.stop()
                if event.key == pygame.K_UP:
                    hero.up = False

        """ ********** LOGIC ********** """
        if not mix_mode:
            if zooming < 300:
                zooming += 15
            #  Hero
            hero.update()
            # print(cells.index(hero.cell) + 1)
            if hero.x_speed:
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.stop()
            if hero.y_speed:
                pygame.mixer.music.stop()
        else:
            if zooming:
                zooming -= 15

        # If the player gets out of a screen
        if hero.x + hero.length >= WIDTH:
            hero.x = WIDTH - hero.length
        elif hero.x <= 0:
            hero.x = 0
        elif hero.y <= 0:
            hero.y = 0
        elif hero.y >= HEIGHT:
            hero.y = HEIGHT - hero.height

        if hero.next_level:
            next_level()
            game = False
        """ ******** END LOGIC ******** """

        """ ********** PAINTING ********** """
        #  Background
        screen.fill(BACKGROUND)

        # Shows blocks
        for c in cells:
            c.show()
            if c.empty and mix_mode:
                # color = (244, 103, 96)
                pygame.draw.rect(screen, BLUE, (c.x, c.y, c.size, c.size), 5)

        # Draw lines
        for row in range(3):
            pygame.draw.line(screen, WHITE, (WIDTH // 3 * row, 0), (WIDTH // 3 * row, HEIGHT))
            for col in range(2):
                pygame.draw.line(screen, WHITE, (0, HEIGHT // 2 * col), (WIDTH, HEIGHT // 2 * col))

        # Draws hero
        hero.show()

        # move and mix mode
        new_screen = camera(screen, hero, zooming)
        screen.blit(new_screen, (0, 0))

        # Prints FPS
        clock.tick(60)
        fps = inf_font.render("fps: " + str(int(clock.get_fps())), 0, WHITE)
        fps.set_alpha(50)
        screen.blit(fps, (WIDTH - 100, HEIGHT - 35))

        # Update all animation
        pygame.display.flip()
        """ ****************************** """


def camera(surf, hero, zoom):
    height = 800-zoom
    width = 1.5 * height
    x = hero.x - width//2
    y = hero.y - height//2
    x = clamp(x, 0, WIDTH - width)
    y = clamp(y, 0, HEIGHT - height)

    surf = surf.subsurface((x, y, width, height)).copy()
    surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
    return surf


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def create_level_from_image(image):
    hero = Player(WIDTH // 2, HEIGHT // 2)  # Create Hero on standard coordinates
    img = pygame.image.tostring(image, 'RGB')
    platform_width = platform_height = 20
    cells = []
    for i in range(2):
        for j in range(3):
            platforms = []
            y = i * 400  # координаты
            for line in range(20):
                x = j * 400
                for row in range(20):
                    index = (row + line * 60 + j * 20 + i * 60 * 20) * 3
                    color = (img[index + 0], img[index + 1], img[index + 2])  # r, g, b
                    if color == BLACK:  # Ground
                        platforms.append(Platform(x, y))
                    elif color == GREEN:  # Finish
                        platforms.append(Platform(x, y, chest=True))
                    elif color == YELLOW:  # Key
                        platforms.append(Platform(x, y, key=True))
                    elif color == BLUE:  # Recreate Hero if needed
                        hero = Player(x, y)  # Creating a Hero
                    else:  # Nothing
                        pass
                    x += platform_width  # перемещаем на ширину блока
                y += platform_height  # то же самое и с шириной
            cells.append(Cell(platforms, j * 400, i * 400))
    cells[5].empty = True
    return cells, hero


def move_tile(cells_list, direction, hero):
    # Searching for empty tile
    empty = [t for t in cells_list if t.empty].pop()
    # searching for necessary tile and 'unpack' a list
    neighbour = None
    if direction == 'left':
        if empty.x > 0:
            neighbour = [t for t in cells_list if t.y == empty.y and t.x == empty.x - empty.size].pop()
    if direction == 'right':
        if empty.x < WIDTH - empty.size:
            neighbour = [t for t in cells_list if t.y == empty.y and t.x == empty.x + empty.size].pop()
    if direction == 'up':
        if empty.y >= empty.size:
            neighbour = [t for t in cells_list if t.x == empty.x and t.y == empty.y - empty.size].pop()
    if direction == 'down':
        if empty.y < HEIGHT - empty.size:
            neighbour = [t for t in cells_list if t.x == empty.x and t.y == empty.y + empty.size].pop()

    if neighbour:  # if you can move it. MOVE IT! (ost 'Madagaskar')
        # Swapping if not moving and not staying at a border
        if hero.x + hero.length <= hero.cell.x + hero.cell.size and hero.x >= hero.cell.x:  # Not border
            if int(hero.y + hero.height) <= hero.cell.y + hero.cell.size and hero.y >= hero.cell.y:
                temp = (empty.x, empty.y)
                empty.move_platforms(direction, (neighbour.x, neighbour.y))
                neighbour.move_platforms(direction, (temp[0], temp[1]), reverse=-1)
                if hero.cell == neighbour:
                    hero.move(direction)
                return True
    error_sound.play()
