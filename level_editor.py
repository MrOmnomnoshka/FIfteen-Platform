from constants import *
from menu import screen, full_quit, Button, inf_font
color = WHITE
done = False
level = None


def change_color(new_c):
    global color
    color = new_c


def save_level(image):
    global level
    level.image = pygame.transform.scale(image, (60, 40))  # Small image
    pygame.image.save(level.image, 'levels/{}.png'.format(level.number+1))
    go_back()


def go_back():
    global done
    done = True


def main(lvl):
    global done, level
    done = False
    level = lvl

    # Canvas
    not_scale = lvl.image if lvl.image else pygame.image.load('levels/template.png')
    image = pygame.transform.scale(not_scale, (6*180, 4*180))  # Full screen

    # Menu buttons
    buttons = [  # Palette
               Button("   ", 150, 10, BLUE, change_color, BLUE),
               Button("   ", 210, 10, BLACK, change_color, BLACK),
               Button("   ", 270, 10, GREEN, change_color, GREEN),
               Button("   ", 330, 10, YELLOW, change_color, YELLOW),
               Button("   ", 390, 10, WHITE, change_color, WHITE),
               # Really buttons
               Button(pygame.image.load('images/back.png'), WIDTH - 100, 300, WHITE, go_back),
               Button(pygame.image.load('images/save.png'), WIDTH - 100, 500, WHITE, save_level, image)]

    # =================== Main cycle =======================
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit
                full_quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        # Show
        screen.fill(BACKGROUND)
        screen.blit(image, (0, 72))

        # Draw lines
        for row in range(4):
            pygame.draw.line(screen, RED, (1080 // 3 * row, 72), (1080 // 3 * row, 720+72))  # Vertical
            for col in range(3):
                pygame.draw.line(screen, RED, (0, (720 // 2) * col + 72), (1080, 720 // 2 * col + 72))  # Horizontal

        # Text
        info = inf_font.render("Color:", 0, WHITE)
        screen.blit(info, (10, 10))

        # Buttons
        for b in buttons:
            b.update()

            highlight = 4  # Default
            if color == BLUE:
                highlight = 0
            elif color == BLACK:
                highlight = 1
            elif color == GREEN:
                highlight = 2
            elif color == YELLOW:
                highlight = 3
            elif color == WHITE:
                highlight = 4
            current_btn = buttons[highlight]
            pygame.draw.rect(screen, PURPLE, [current_btn.x, current_btn.y, current_btn.w, current_btn.h], 5)

        # Print logic
        if pygame.mouse.get_pressed()[0]:  # Left
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(image, color, (x - x % 18, y - y % 18 - 72, 18, 18))

        # Update all animation
        pygame.display.flip()

        # Speed limit
        pygame.time.Clock().tick(60)
