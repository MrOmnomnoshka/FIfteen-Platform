from menu import screen, full_quit, Button, inf_font
from constants import *
import level_editor


class Level:
    empty_text = inf_font.render("Empty", 0, BLACK)

    def __init__(self, image, x, y, number):
        self.image = image
        self.x = x
        self.y = y
        self.number = number

    def show(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:  # empty
            pygame.draw.rect(screen, WHITE, (self.x, self.y, 300, 200))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, 300, 200), 5)
            screen.blit(self.empty_text, (self.x + 110, self.y + 80))
        num_text = inf_font.render("Level: " + str(self.number + 1), 0, WHITE)
        screen.blit(num_text, (self.x + 100, self.y + 200))

    def pressed(self, pos):
        if self.x <= pos[0] <= self.x + 300 and self.y <= pos[1] <= self.y + 200:
            return True


def go_back():
    global done
    done = True


def change_page(way):
    global page, pages
    page += way
    page = max(min(pages, page), 1)


def edit_level():
    if chosen:
        level_editor.main(chosen)
        update()


def add_level():
    global pages, page
    number = 1
    for pg in container:
        for lvl in pg:
            if lvl.image is None:
                return False  # Can create only one empty level
            number += 1
    if number > pages*6:
        pages += 1
        page += 1
        container.append([])

    x, y = 100, 130
    for lvl in range(6):
        if lvl != 0 and lvl % 3 == 0:
            y += 300
            x = 100
        # Find where
        if (number-1) % 6 == lvl:
            container[pages-1].append(Level(None, x, y, number-1))
        x += 350


def del_level():
    global chosen, container
    if chosen and chosen.image:
        os.remove('levels/{}.png'.format(chosen.number+1))
        for p in container:
            for lvl in p:  # Shift others
                if lvl.number > chosen.number and lvl.image:
                    os.rename(f'levels/{lvl.number+1}.png', f'levels/{lvl.number}.png')
        chosen = None
    update()


# Global variables
level_buttons = [Button("Edit level", 300, 700, (25, 65, 65), edit_level),
                 Button("Add level", 530, 700, (25, 65, 65), add_level),
                 Button("Del level", 760, 700, (25, 65, 65), del_level),
                 Button("<-", 50, 700, (25, 65, 65), change_page, -1),
                 Button("->", 1100, 700, (25, 65, 65), change_page, 1),
                 Button(pygame.image.load('images/back.png'), 10, 10, (25, 65, 65), go_back)]
done = False
page = 1  # current page
pages = 1  # all Pages
lvl_amount = 0
container = []
chosen = None
lvl_for_game = None
# =======================


def update():
    global pages, container, lvl_amount
    container = []

    # Read 'levels' folder
    lvl_amount = os.listdir(os.getcwd() + "/levels")  # 'getcwd' return your directory path
    lvl_amount = len(lvl_amount) - 1  # minus template.png

    # Scale images
    pages = (lvl_amount // 6 + 1)  # max_on_screen = 6
    small_images = []
    for lvl in range(lvl_amount):
        small_images.append(pygame.image.load('levels/{}.png'.format(lvl + 1)))
        small_images[lvl] = pygame.transform.scale(small_images[lvl], (6 * 50, 4 * 50))  # 300x200

    # Container(page) filling
    for p in range(pages):
        container.append([])
        x, y = 100, 130
        for lvl in range(6):
            if lvl != 0 and lvl % 3 == 0:
                y += 300
                x = 100
            # Fill class
            if lvl + p * 6 < len(small_images):  # image
                container[p].append(Level(small_images[lvl + p * 6], x, y, lvl + p * 6))
            # else:  # empty
            #     container[p].append(Level(None, x, y, lvl+p*6))
            x += 350


def main():
    update()  # Loading pages
    global done, chosen, lvl_for_game
    done = False
    # =================== Main cycle =======================
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit
                full_quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        #  Background
        screen.fill(BACKGROUND)

        # Show
        for lvl in container[page-1]:
            lvl.show()

        # Buttons
        for b in range(len(level_buttons)):
            level_buttons[b].update()

        # Check
        pressed = pygame.mouse.get_pressed()[0]
        pos = pygame.mouse.get_pos()
        for lvl in container[page-1]:
            # check mouse
            if pressed:
                if lvl.pressed(pos):
                    chosen = lvl
                    if chosen.image:
                        lvl_for_game = chosen
                    break
                else:
                    chosen = None
        # Draws selected
        if chosen and chosen in container[page-1]:
            pygame.draw.rect(screen, GREEN, (chosen.x-2, chosen.y-2, 302, 202), 2)

        # Current and all pages
        page_text = inf_font.render("page " + str(page) + "/" + str(pages), 0, WHITE)
        screen.blit(page_text, (WIDTH - 165, HEIGHT - 60))

        # Update all animation
        pygame.display.flip()

        # Speed limit
        pygame.time.Clock().tick(60)
