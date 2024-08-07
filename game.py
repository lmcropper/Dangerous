import pygame
import sys
import time
import random
import math

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
clock = pygame.time.Clock()
framerate = 60

# Game states
TITLE_SCREEN = "title"
CHARACTER_SELECT = "character_select"
FIGHT_SCREEN = "fight"
current_state = TITLE_SCREEN

SELECT_BUTTON = 0
START_BUTTON = 7

# Fonts

font_title_title = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 74)
font_select_fight_banner = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 150)
font_select_title = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 74)
font_select_animal_small = pygame.font.Font("./fonts/WIDEAWAKE.ttf", 36)
font_select_animal_large = pygame.font.Font("./fonts/WIDEAWAKE.ttf", 48)
font_fight_title = pygame.font.Font("./fonts/Platinum Sign OVer.ttf", 74)
font_large = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 36)

# Animals
animals = ["Moose", "Black Widow", "Rattlesnake", "Mountain Lion", "Scorpion", "Mosquito", "Raccoon", "Black Bear", "Coyote", "Gila Monster"]
animal_stats = {
    "Moose": "Stats for Moose",
    "Black Widow": "Stats for Black Widow",
    "Rattlesnake": 
        """Female rattlesnakes carry and incubate their eggs inside of their bodies for around 90 days before giving birth to live young.
        Rattle Snakes have heat-sensitive pits on each side of their heads that transmit signals to the same area of the snake's brain as the optic nerve. It can “see” the heated image of its prey even in complete darkness.
        Rattlesnakes have an inner ear structure without an eardrum, instead, snakes "hear" by sensing vibrations through their jawbone.
        Once rattlesnakes grow out of their old skin and go through the molting process, their bodies naturally add an extra segment to their rattles each time.
        Their rattle is made up of various interlocking rings of keratin, the same material that human hair, skin, and nails are made of.""",
    "Mountain Lion": 
        """Cougars can jump 18ft vertically and 40ft horizontally.
        Utah division of wildlife resources estimates that 2,300 cougars live in Utah.
        Highest cat: cougar spotted at 5,800 m (19,024 ft).
        Cougar is an ambush predator--It either stalks its prey or waits for it to draw close before striking.
        The cubs stay with their mother for between 18 months to 2 years. The cubs drink their mother's milk for around 3 months, but begin to eat meat after 6 weeks.""",
    "Scorpion": 
        """After birth, the newborn scorpions ride on their mother's back, where they remain protected until they molt for the first time.
        Fossil evidence shows that scorpions have remained largely unchanged since the Carboniferous period (350-300 million years ago).
        Modern scorpions can live as long as 25 years.
        Scorpions engage in an elaborate courtship ritual known as the promenade à deux (literally, a walk for two).
        Of the nearly 2,000 known species of scorpions in the world, only 25 are known to produce venom powerful enough to pack a dangerous punch to an adult.""",
    "Mosquito": "Stats for Mosquito",
    "Raccoon": "Stats for Raccoon",
    "Black Bear": "Stats for Black Bear",
    "Coyote": "Stats for Coyote",
    "Gila Monster": "Stats for Gila Monster",
    "Logan Cropper": "infinity"
}
selected_indices = [0, 1]
selected_animals = [None, None]
animal_selected = [False, False]  # Track if an animal is selected for each player

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
select_background_color = (200, 200, 200)
select_header_height = 100
select_box_height = 300
select_box_width = SCREEN_WIDTH / 5
select_border_weight = 10
select_selected_border_weight = 30

last_input_time = [0,0]  # Last time input was received for each player
debounce_delay = 0.05  # 200 milliseconds debounce delay

joysticks = {}

# Functions
def draw_title_screen():
    screen.fill(WHITE)
    title_text = font_title_title.render("TOP 10 DANGEROUS ANIMALS", True, BLACK)
    subtitle_text = font_small.render("Press any button to continue", True, BLACK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 3))
    screen.blit(subtitle_text, ((SCREEN_WIDTH - subtitle_text.get_width()) // 2, SCREEN_HEIGHT // 2))

def draw_character_select():
    global selected_animals
    selected_animals = [animals[selected_indices[0]], animals[selected_indices[1]]]
    screen.fill(select_background_color)
    title_text = font_select_title.render("CHARACTER SELECT", True, BLACK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 5))

    # Time-based factor for pulsing effect
    pulse_factor = (1.05 + 0.05 * math.sin(time.time() * 6))  # Adjust the multiplier and frequency as needed

    # Draw animal selection boxes
    for i, animal in enumerate(animals):
        p1_selection = animal == selected_animals[0]
        p2_selection = animal == selected_animals[1]
        color = (255, 0, 0) if p1_selection else (0, 0, 255) if p2_selection else (100, 100, 100)
        box_rect = pygame.Rect((i % 5) * SCREEN_WIDTH / 5, select_header_height + (i // 5) * select_box_height, select_box_width, select_box_height)

        # Draw the animal image
        image = animal_images[animal]
        if p1_selection or p2_selection:
            scaled_width = int(select_box_width * pulse_factor)
            scaled_height = int(select_box_height * pulse_factor)
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))
            offset_x = (scaled_width - select_box_width) // 2
            offset_y = (scaled_height - select_box_height) // 2
        else:
            scaled_image = pygame.transform.scale(image, (int(select_box_width), int(select_box_height)))
            offset_x = offset_y = 0
            
        # Set the clipping rectangle to prevent spilling over boundaries
        screen.set_clip(box_rect)
        screen.blit(scaled_image, (box_rect.x - offset_x, box_rect.y - offset_y))
        screen.set_clip(None)

        # Draw black bar along the bottom of each selection box
        pygame.draw.rect(screen, BLACK, (box_rect.x, box_rect.y + box_rect.height - 55, box_rect.width, 55))

        # Draw animal name and player indicators
        animal_text = font_select_animal_small.render(animal, True, WHITE)
        if p1_selection:
            p1_text = font_select_animal_small.render("P1", True, WHITE)
            p1_loc = ((i % 5) * SCREEN_WIDTH / 5 + select_box_width - 40, select_header_height + (i // 5) * select_box_height + 40)
            pygame.draw.circle(screen, color, p1_loc, 30)
            screen.blit(p1_text, p1_text.get_rect(center=p1_loc))
        if p2_selection:
            p2_text = font_select_animal_small.render("P2", True, WHITE)
            p2_loc = ((i % 5) * SCREEN_WIDTH / 5 + 40, select_header_height + (i // 5) * select_box_height + 40)
            pygame.draw.circle(screen, color, p2_loc, 30)
            screen.blit(p2_text, p2_text.get_rect(center=p2_loc))
        screen.blit(animal_text, ((i % 5) * SCREEN_WIDTH / 5 + 20, select_header_height + (i // 5) * select_box_height + select_box_height - 50))

        # Draw border around selection box
        pygame.draw.rect(screen, color, box_rect, select_selected_border_weight if (p1_selection and animal_selected[0] or p2_selection and animal_selected[1]) else select_border_weight)

    # Show selected animals' stats and images
    for i, animal in enumerate(selected_animals):
        if animal:
            origin = (20 + SCREEN_WIDTH / 2 * i, select_header_height + select_box_height * 2 + 20)
            animal_text = font_select_animal_large.render(animal, True, BLACK)
            stats_text = font_small.render(animal_stats[animal], True, BLACK)
            screen.blit(animal_text, origin)
            screen.blit(stats_text, (origin[0], origin[1] + 50))

            # Draw the selected animal image next to the stats
            image = animal_images[animal]
            scaled_image = pygame.transform.scale(image, (SCREEN_HEIGHT - select_box_height * 2 - select_header_height, SCREEN_HEIGHT - select_box_height * 2 - select_header_height))  # Scale to fit next to stats
            screen.blit(scaled_image, (SCREEN_WIDTH / 2 - (SCREEN_HEIGHT - select_box_height * 2 - select_header_height) + SCREEN_WIDTH / 2 * i, origin[1] - 20))  # Adjust position next to stats

    # Draw stat border rectangles
    pygame.draw.rect(screen, (100, 100, 100), (0, select_header_height + select_box_height * 2, int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - select_box_height * 2 - select_header_height), select_border_weight)
    pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH / 2, select_header_height + select_box_height * 2, int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - select_box_height * 2 - select_header_height), select_border_weight)

    # Draw start button if both animals are selected
    if all(animal_selected):
        start_banner_height = 200
        start_text = font_select_fight_banner.render("FIGHT", True, WHITE)
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
    fight_text = font_fight_title.render("FIGHT!", True, BLACK)
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
    
    time.sleep(0.1)

def handle_title_screen_events(event):
    global current_state
    if event.type == pygame.KEYDOWN:
        sound_title_start.play()
        current_state = CHARACTER_SELECT
    elif event.type == pygame.JOYBUTTONDOWN:
        sound_title_start.play()
        current_state = CHARACTER_SELECT

import time

# Debounce delay in seconds
debounce_delay = 0.2

# Dictionary to store the last processed time for each joystick
last_processed_time = {}

def handle_character_select_events(event):
    global current_state, selected_animals, animal_selected
    current_time = time.time()
    
    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
        jid = event.joy
        if jid not in last_processed_time:
            last_processed_time[jid] = 0
        
        # Check if enough time has passed since the last processed input
        if current_time - last_processed_time[jid] < debounce_delay:
            return
        
        # Update the last processed time
        last_processed_time[jid] = current_time

    if event.type == pygame.JOYBUTTONDOWN:
        # Detect which joystick button was pressed
        button = event.button
        player = 1 if jid == 0 else 0

        # Toggle selection for the current player
        if button == SELECT_BUTTON:
            animal_selected[player] = not animal_selected[player]
            sound_playerselect_select.play()

        # Check if both players have selected animals and the specific button is pressed
        if all(animal_selected) and button == START_BUTTON:
            sound_playerselect_start.play()
            current_state = FIGHT_SCREEN

    if event.type == pygame.JOYAXISMOTION:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()
            axes = [round(joystick.get_axis(0)), round(joystick.get_axis(1))]
            player = 0 if jid == 0 else 1
            if not animal_selected[player]:
                if axes[1]:
                    selected_indices[player] = (selected_indices[player] - axes[1]) % 10
                    sound_playerselect_move.play()
                if axes[0]:
                    selected_indices[player] = (selected_indices[player] + axes[0] * 5) % 10
                    sound_playerselect_move.play()
    print(selected_indices)
    pygame.event.clear()

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
            print(f"Joystick {joy.get_instance_id()} connected")

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
    clock.tick(framerate)

pygame.quit()
sys.exit()
