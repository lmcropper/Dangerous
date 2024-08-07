import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top 10 Dangerous Animals")

# Game states
TITLE_SCREEN = "title"
CHARACTER_SELECT = "character_select"
FIGHT_SCREEN = "fight"
current_state = TITLE_SCREEN

# Fonts
font_huge = pygame.font.Font(None, 150)
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Animals
animals = ["Moose", "Black Widow", "Rattlesnake", "Mountain Lion", "Scorpion", "Mosquito", "Raccoon", "Black Bear", "Coyote", "Gila Monster"]
animal_stats = {
    "Moose": "Stats for Moose",
    "Black Widow": "Stats for Black Widow",
    "Rattlesnake": "Stats for Rattlesnake",
    "Mountain Lion": "Stats for Mountain Lion",
    "Scorpion": "Stats for Scorpion",
    "Mosquito": "Stats for Mosquito",
    "Raccoon": "Stats for Raccoon",
    "Black Bear": "Stats for Black Bear",
    "Coyote": "Stats for Coyote",
    "Gila Monster": "Stats for Gila Monster",
    "Logan Cropper": "infinity"
}
selected_indices = [0, 1]
selected_animals = [None, None]
# Load images for animals (ensure these files exist)
animal_images = {
    "Moose": pygame.image.load("images/moose.png"),
    "Black Widow": pygame.image.load("images/black_widow.png"),
    "Rattlesnake": pygame.image.load("images/rattlesnake.png"),
    "Mountain Lion": pygame.image.load("images/mountain_lion.png"),
    "Scorpion": pygame.image.load("images/scorpion.png"),
    "Mosquito": pygame.image.load("images/mosquito.png"),
    "Raccoon": pygame.image.load("images/raccoon.png"),
    "Black Bear": pygame.image.load("images/black_bear.png"),
    "Coyote": pygame.image.load("images/coyote.png"),
    "Gila Monster": pygame.image.load("images/gila_monster.png"),
    #"Logan Cropper": None # TODO: Add Logan Cropper image
}
animal_sprites = {
    "Moose": pygame.image.load("sprites/moose.png"),
    "Black Widow": pygame.image.load("sprites/black_widow.png"),
    "Rattlesnake": pygame.image.load("sprites/snake.png"),
    "Mountain Lion": pygame.image.load("sprites/cougar.png"),
    "Scorpion": pygame.image.load("sprites/scorpion.png"),
    "Mosquito": pygame.image.load("sprites/mosquito.png"),
    "Raccoon": pygame.image.load("sprites/raccoon.png"),
    "Black Bear": pygame.image.load("sprites/bear.png"),
    "Coyote": pygame.image.load("sprites/coyote.png"),
    "Gila Monster": pygame.image.load("sprites/gila_monster.png"),
    #"Logan Cropper": None # TODO: Add Logan Cropper sprite
}
sprite_size = (300, 300) # y, x

# Load and play background music for character select
pygame.mixer.music.load("music/Megafauna.mp3")

# Load sound effects
sound_title_start = pygame.mixer.Sound("sounds/title_start.wav")
sound_playerselect_start = pygame.mixer.Sound("sounds/playerselect_start.wav")
sound_playerselect_move = pygame.mixer.Sound("sounds/playerselect_move.wav")
sound_playerselect_select = pygame.mixer.Sound("sounds/playerselect_select.wav")

# Animal Select global params
select_header_height = 100
select_box_height = 300
select_box_width = SCREEN_WIDTH / 5
select_border_weight = 10

joysticks = {}

# Functions
def draw_title_screen():
    screen.fill(WHITE)
    title_text = font_large.render("Top 10 Dangerous Animals", True, BLACK)
    subtitle_text = font_small.render("Press any button to continue", True, BLACK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 3))
    screen.blit(subtitle_text, ((SCREEN_WIDTH - subtitle_text.get_width()) // 2, SCREEN_HEIGHT // 2))

def draw_character_select():

    global selected_animals
    selected_animals = [animals[selected_indices[0]], animals[selected_indices[1]]]
    screen.fill(WHITE)
    title_text = font_large.render("Character Select", True, BLACK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 20))

    # Draw animal selection boxes
    for i, animal in enumerate(animals):
        p1_selection = animal == selected_animals[0]
        p2_selection = animal == selected_animals[1]
        color = (0, 0, 255) if (p1_selection) else (255, 0, 0) if (p2_selection) else (100, 100, 100)
        box_rect = ((i % 5) * SCREEN_WIDTH / 5, select_header_height + (i // 5) * select_box_height, select_box_width, select_box_height)
        

        # Draw the animal image
        image = animal_images[animal]
        scaled_image = pygame.transform.scale(image, (int(select_box_width), int(select_box_height)))
        screen.blit(scaled_image, (box_rect[0], box_rect[1]))
        pygame.draw.rect(screen, color, box_rect, select_border_weight)  
        
        animal_text = font_small.render(animal, True, WHITE, (100, 100, 100))
        if p1_selection:
            p1_text = font_small.render("P1", True, (0, 0, 255))
            screen.blit(p1_text, ((i % 5) * SCREEN_WIDTH / 5 + select_box_width - 50, select_header_height + (i // 5) * select_box_height + 20))
        if p2_selection:
            p2_text = font_small.render("P2", True, (255, 0, 0))
            screen.blit(p2_text, ((i % 5) * SCREEN_WIDTH / 5 + select_box_width - 50, select_header_height + (i // 5) * select_box_height + 20))
        screen.blit(animal_text, ((i % 5) * SCREEN_WIDTH / 5 + 20, select_header_height + (i // 5) * select_box_height + select_box_height - 40))

    # Show selected animals' stats and images
    for i, animal in enumerate(selected_animals):
        if animal:
            origin = (20 + SCREEN_WIDTH / 2 * i, select_header_height + select_box_height * 2 + 20)
            animal_text = font_large.render(animal, True, BLACK)
            stats_text = font_small.render(animal_stats[animal], True, BLACK)
            screen.blit(animal_text, origin)
            screen.blit(stats_text, (origin[0], origin[1] + 50))

            # Draw the selected animal image next to the stats
            image = animal_images[animal]
            scaled_image = pygame.transform.scale(image, (SCREEN_HEIGHT - select_box_height * 2 - select_header_height, SCREEN_HEIGHT - select_box_height * 2 - select_header_height))  # Scale to fit next to stats
            screen.blit(scaled_image, (SCREEN_WIDTH / 2 - (SCREEN_HEIGHT - select_box_height * 2 - select_header_height) + SCREEN_WIDTH / 2 * i, origin[1] - 20))  # Adjust position next to stats
    #Draw stat border rectangles
    pygame.draw.rect(screen, (100, 100, 100), (0, select_header_height + select_box_height * 2, int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - select_box_height * 2 - select_header_height), select_border_weight)
    pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH / 2, select_header_height + select_box_height * 2, int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - select_box_height * 2 - select_header_height), select_border_weight)
    
    
    # Draw start button if both animals are selected
    if all(selected_animals):
        start_banner_height = 200
        start_text = font_huge.render("FIGHT", True, WHITE)
        pygame.draw.rect(screen, (20, 20, 20), (0, SCREEN_HEIGHT / 2 - start_banner_height / 2, SCREEN_WIDTH, start_banner_height), 0)
        screen.blit(start_text, start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

# Constants for animation states
STATE_APPEAR = 0
STATE_STEP_CLOSER = 1
STATE_FIGHT = 2
STATE_FINISHED = 3

# Constants for moves
BACK = 0
PUNCH = 1
KICK = 2

# Initialize variables
animation_state = STATE_APPEAR
sprite_positions = [(200, 300), (SCREEN_WIDTH - 200 - sprite_size[1], 300)]
sprite_home_positions = sprite_positions.copy()
sprite_angles = [0, 0]
sprite_attack_state = BACK
step_count = 0
turn_count = 0

def draw_fight_screen():
    screen.fill(WHITE)
    fight_text = font_large.render("Fight!", True, BLACK)
    screen.blit(fight_text, ((SCREEN_WIDTH - fight_text.get_width()) // 2, 20))

    # Draw sprites for selected animals
    for i, animal in enumerate(selected_animals):
        if animal in animal_sprites.keys():
            sprite = animal_sprites[animal]
            scaled_sprite = pygame.transform.scale(sprite, sprite_size)
            screen.blit(scaled_sprite, sprite_positions[i])
        else:
            dummy_sprite = font_large.render("?", True, BLACK)
            screen.blit(dummy_sprite, sprite_positions[i])

def update_sprite_positions():
    global animation_state, step_count, turn_count
    global active_sprite, move_count, moves
    global sprite_positions, sprite_home_positions, sprite_attack_state
    if animation_state == STATE_APPEAR:
        if step_count > 5:
            animation_state = STATE_STEP_CLOSER
            step_count = 0
        step_count += 1

    if animation_state == STATE_STEP_CLOSER:
        sprite_positions[0] = (sprite_positions[0][0] + 100, sprite_positions[0][1])
        sprite_positions[1] = (sprite_positions[1][0] - 100, sprite_positions[1][1])
        step_count += 1
        if step_count > 3:  # Number of steps to take
            animation_state = STATE_FIGHT
            sprite_home_positions = sprite_positions.copy()
            step_count = 0

    if animation_state == STATE_FIGHT:
        if turn_count < 4:
            if step_count == 0:
                # Choose next move set
                active_sprite = random.choice([0, 1])
                move_count = random.randint(1, 3)
                moves = [random.choice([PUNCH, KICK]) for _ in range(move_count)]
                step_count += 1

            elif step_count < move_count:
                if sprite_attack_state == BACK:
                    # Perform next move
                    if moves[step_count] == PUNCH:
                        sprite_positions[active_sprite] = (sprite_positions[active_sprite][0] + 150, sprite_positions[active_sprite][1])
                        sprite_attack_state = PUNCH
                    elif moves[step_count] == KICK:
                        sprite_positions[active_sprite] = (sprite_positions[active_sprite][0] + 150, sprite_positions[active_sprite][1] + 150)
                        sprite_attack_state = KICK
                    step_count += 1
                else:
                    # Return to home position
                    sprite_positions[active_sprite] = sprite_home_positions[active_sprite]
                    sprite_attack_state = BACK

            else: 
                step_count = 0
                turn_count += 1

        else:
            turn_count = 0
            animation_state = STATE_FINISHED

    if animation_state == STATE_FINISHED:
        pass

def handle_title_screen_events(event):
    global current_state
    if event.type == pygame.KEYDOWN:
        sound_title_start.play()
        current_state = CHARACTER_SELECT
    elif event.type == pygame.JOYBUTTONDOWN:
        sound_title_start.play()
        current_state = CHARACTER_SELECT
        

def handle_character_select_events(event):
    global current_state
    # print(selected_animals)
    if all(selected_animals) and (event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN):
        sound_playerselect_start.play()
        current_state = FIGHT_SCREEN


    if event.type == pygame.JOYAXISMOTION:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()
            axes = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            player = 0 if jid == 0 else 1
            if axes[1]:
                selected_indices[player] = (selected_indices[player] - axes[1]) % 10
            if axes[0]:
                selected_indices[player] = (selected_indices[player] + axes[0] * 5) % 10

def handle_fight_screen_events(event):
    pass

# Main loop
running = True
while running:
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            running = False
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connencted")

        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")

        if current_state == TITLE_SCREEN:
            # Start playing music when entering character select
            if pygame.mixer.music.get_busy() == False:  # Check if music is already playing
                pygame.mixer.music.play(-1)  # Loop music indefinitely
            handle_title_screen_events(event)
        elif current_state == CHARACTER_SELECT:
            handle_character_select_events(event)
        elif current_state == FIGHT_SCREEN:
            pygame.mixer.music.stop()  # Stop music when leaving character select
            handle_fight_screen_events(event)

    if current_state == TITLE_SCREEN:
        draw_title_screen()
    elif current_state == CHARACTER_SELECT:
        draw_character_select()
    elif current_state == FIGHT_SCREEN:
        update_sprite_positions()
        draw_fight_screen()

    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
sys.exit()
