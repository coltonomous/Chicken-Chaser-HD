import pygame
import random

""" This is the source code for a game where you control the lateral movements of a tractor
to avoid chickens. Score is awarded for being on course to hit the chickens without actually hitting them and
is subtracted for hitting and killing chickens. Vehicle movements are controlled with the side arrow keys.
Additionally, the game can be paused by pressing the "p" key. I would like to
specially acknowledge 'sentdex', whose YouTube tutorials helped make this possible."""

########################################################################################################################
################################################## Game Setup ##########################################################
########################################################################################################################

pygame.init()

# Aspect ratio
xDisplay = 800
yDisplay = 600

# Game sounds
squishSound = pygame.mixer.Sound("squish.wav")
crashSound = pygame.mixer.Sound("crash.wav")
gameMusic = pygame.mixer.music.load("chicken_dance.wav")

# Game art
gameDisplay = pygame.display.set_mode((xDisplay, yDisplay))
background = pygame.image.load("cchd.png").convert_alpha()
pygame.display.set_caption("Chicken Chaser")
gameIcon = pygame.image.load("chicken_icon.png")
carSprite = pygame.image.load("tractor_sprite.png").convert_alpha()
chickenSprite = pygame.image.load("zelda_chicken.png").convert_alpha()
bloodSplatter = pygame.image.load("blood.png").convert_alpha()
pygame.display.set_icon(gameIcon)

# Tractor dimensions and scaling
carWidth = int(0.105 * xDisplay)
carHeight = int(0.233 * yDisplay)
carSprite = pygame.transform.scale(carSprite, (carWidth, carHeight))

# Chicken dimensions and scaling
chickenWidth = int(0.0925 * xDisplay)
chickenHeight = int(0.123 * yDisplay)
chickenSprite = pygame.transform.scale(chickenSprite, (chickenWidth, chickenHeight))

# Blood spatter dimensions and scaling
bloodWidth = int(0.1875 * xDisplay)
bloodHeight = int(0.25 * yDisplay)
bloodSplatter = pygame.transform.scale(bloodSplatter, (bloodWidth, bloodHeight))

colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "darkRed": (175, 0, 0),
    "darkGreen": (0, 175, 0)
}

# Insults for crashes in game
lossCount = -1
lossList = [
    "That's what you call driving?",
    "Your mother was a hamster!",
    "Your father smelt of elderberries!"
]

clock = pygame.time.Clock()

########################################################################################################################
############################################ Game Functions ############################################################
########################################################################################################################


def draw_intro_screen():
    """
    Start menu.
    """
    # Animating chicken sprite.
    chick_x = xDisplay * 0.1875
    chick_y = yDisplay * 0.55
    chick_dir = True

    while 1:
        for event in pygame.event.get():
            quit_program(event)

        # Controls chicken's movement
        if chick_x > xDisplay * 0.65:
            chick_dir = False
        elif chick_x < xDisplay * 0.1875:
            chick_dir = True

        if chick_dir:
            chick_x += 5
        else:
            chick_x -= 5

        # Updates display
        gameDisplay.blit(background, (0, 0))
        display_message(xDisplay / 2, yDisplay / 3, 75, "Chicken! Bwak!")

        draw_chicken(chick_x, chick_y)

        draw_button("I'm no chicken!", 0.15 * xDisplay, 0.75 * yDisplay, 175, 50,
                    colors["darkGreen"], colors["green"], "play")
        draw_button("Chicken out...", 0.65 * xDisplay, 0.75 * yDisplay, 175, 50,
                    colors["darkRed"], colors["red"], "quit")

        pygame.display.update()
        clock.tick(60)


def draw_button(message, x, y, width, height, inactive_color, active_color, action):
    """
    Generates button at x, y of width and height. Color changes from inactive_color
    to active_color on hovor. Action can be either 'Play' or 'Quit'.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    buttonRect = pygame.Rect(x, y, width, height)

    if buttonRect.collidepoint(mouse):
        pygame.draw.rect(gameDisplay, colors["black"], (x, y, width, height))
        pygame.draw.rect(gameDisplay, active_color, (x + 2, y + 2, width - 4, height - 4))

        if click[0]:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, colors["black"], (x, y, width, height))
        pygame.draw.rect(gameDisplay, inactive_color, (x + 2, y + 2, width - 4, height - 4))

    display_message(x + (width / 2), y + (height / 2), 20, message)


def draw_tractor(tractor_x, tractor_y):
    """
    Draws the tractor at tractor_x, tractor_y.
    """
    gameDisplay.blit(carSprite, (tractor_x, tractor_y))


def draw_chicken(chick_x, chick_y):
    """
    Draws a chicken at chick_x and chick_y.
    """
    gameDisplay.blit(chickenSprite, (chick_x, chick_y))


def blood_splatter(blood_x, blood_y):
    """
    Draws blood at coordinates based on blood_x, blood_y.
    Coordinates are manually adjusted to center blood over chicken.
    """
    gameDisplay.blit(bloodSplatter, (blood_x - (chickenWidth / 2),
                                     blood_y - (chickenHeight / 2)))


def display_message(horiz, vert, font_size, text):
    """
    Writes text of font_size to display at horiz, vert.
    """
    print_text = pygame.font.Font("fixedsys.ttf", font_size)
    text_surface = print_text.render(text, True, colors["black"])
    text_rect = text_surface.get_rect()
    text_rect.center = (horiz, vert)
    gameDisplay.blit(text_surface, text_rect)


def count(game_count, chicken_count):
    """
    Displays updating game_count and chicken_count.
    """
    score_text = "Score: " + str(game_count)
    chicken_text = "Remaining: " + str(chicken_count)
    display_message(xDisplay * 0.9, yDisplay * 0.025, 25, score_text)
    display_message(xDisplay * 0.15, yDisplay * 0.025, 25, chicken_text)


def crash():
    """
    Game over menu.
    """
    global lossCount

    if lossCount < len(lossList) - 1:
        lossCount += 1
    else:
        lossCount = 0

    while 1:
        for event in pygame.event.get():
            quit_program(event)

        display_message(xDisplay / 2, yDisplay / 3, 30, lossList[lossCount])

        draw_button("Play Again?", 0.2125 * xDisplay, 0.75 * yDisplay, 130, 50, colors["darkGreen"],
                    colors["green"], "play")
        draw_button("Chicken out...", 0.65 * xDisplay, 0.75 * yDisplay, 175, 50, colors["darkRed"], colors["red"], "quit")

        pygame.display.update()
        clock.tick(60)


def paused(pause):
    """
    Pauses and unpauses the game and the music.
    """
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():
            quit_program(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    pygame.mixer.music.unpause()

        display_message(xDisplay / 2, yDisplay / 3, 75, "Paused")
        pygame.display.update()
        clock.tick(60)


def win(score, chickens):
    """
    Win menu.
    """
    pygame.mixer.music.fadeout(2000)

    while 1:
        for event in pygame.event.get():
            quit_program(event)

        display_message(xDisplay / 2, yDisplay / 4, 40, "Winner winner chicken dinner!")
        display_message(xDisplay / 2, yDisplay / 2, 30, "Final score: " + str(score))
        average = round(float(score) / float(chickens), 1)
        display_message(xDisplay / 2, 3 * yDisplay / 5, 30, "Average per chicken: " + str(average))

        draw_button("Play again?", 0.15 * xDisplay, 0.75 * yDisplay, 175, 50,
                    colors["darkGreen"], colors["green"], "play")
        draw_button("Chicken out...", 0.65 * xDisplay, 0.75 * yDisplay, 175, 50, colors["darkRed"], colors["red"], "quit")

        pygame.display.update()
        clock.tick(15)


def quit_program(event):
    """
    Terminates the program if the event is quit.
    """
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()


########################################################################################################################
############################################# Main Game Loop ###########################################################
########################################################################################################################

def game_loop():
    score = 0
    chickenCount = 30
    passed = 0
    hit = False

    # Starting coordinates for tractor
    x_pos = xDisplay * 0.455
    y_pos = yDisplay * 0.75
    x_change = 0

    # Starting coordinates and speed for chicken
    chicken_speed = 0.00833 * yDisplay
    chicken_x = random.randrange(25, int(xDisplay - (chickenWidth + 25)))
    chicken_y = -yDisplay

    # Moves the background up and down
    scroll_count = 0

    pygame.mixer.music.play(-1)

    while chickenCount > 0:

        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -0.011 * xDisplay
                elif event.key == pygame.K_RIGHT:
                    x_change = 0.011 * xDisplay
                elif event.key == pygame.K_p:
                    paused(True)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x_pos += x_change

        # Handles crashing into boundaries
        if x_pos + carWidth >= xDisplay + 10 or x_pos <= -10:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(crashSound)
            crash()

        # Handles crashing into chickens
        if y_pos + 0.03 * yDisplay < chicken_y + chickenHeight and \
                (x_pos + (0.03 * xDisplay) < chicken_x < x_pos + carWidth - (0.03 * xDisplay) or
                 x_pos + (0.03 * xDisplay) < chicken_x + chickenWidth < x_pos + carWidth - (0.03 * xDisplay) or
                 x_pos < chicken_x + (chickenWidth / 2) < x_pos + carWidth) and not hit:
            pygame.mixer.Sound.play(squishSound)
            hit = True
            if score >= 50:
                score -= 50
            else:
                score = 0

        # Updates score while on path to crash into chickens.
        elif (x_pos + (0.03 * xDisplay) < chicken_x < x_pos + carWidth - (0.03 * xDisplay) or
              x_pos + (0.03 * xDisplay) < chicken_x + chickenWidth < x_pos + carWidth - (
              0.03 * xDisplay) or x_pos < chicken_x + (chickenWidth / 2) < x_pos + carWidth) and not hit:
            score += int(30 ** (1 / (y_pos - (chicken_y + chickenHeight))))

        # Handles drawing of chickens
        if chicken_y > yDisplay:
            chicken_y = 0 - chickenHeight
            chicken_x = random.randrange(25, int(xDisplay - (chickenWidth + 25)))
            chickenCount -= 1
            passed += 1
            hit = False
            # Updates difficulty
            if chicken_speed < 0.02 * yDisplay:
                chicken_speed += 0.00075 * yDisplay

        # Background scrolling "animation"
        if scroll_count == 0:
            scroll_count = -10

        # Updates display
        gameDisplay.blit(background, (0, scroll_count))
        scroll_count += 1

        if hit:
            blood_splatter(chicken_x, chicken_y)
        else:
            draw_chicken(chicken_x, chicken_y)

        draw_tractor(x_pos, y_pos)
        chicken_y += chicken_speed
        count(score, chickenCount)

        pygame.display.update()
        clock.tick(60)

    win(score, passed)


draw_intro_screen()
