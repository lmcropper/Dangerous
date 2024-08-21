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
font_fight_title = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 74)
font_large = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 24)

# Animals
animals = ["Moose", "Black Widow", "Rattlesnake", "Mountain Lion", "Scorpion", "Mosquito", "Raccoon", "Black Bear", "Coyote", "Gila Monster"]
animal_stats = {
    "Moose": 
        """\nMoose are the largest deer species, weighing up to 1,500 lbs and standing 6 feet tall.\n
        Male moose grow antlers that can span up to 6 feet wide from tip to tip.\n
        Moose have poor eyesight but make up for it with a strong sense of smell and hearing.\n
        They are excellent swimmers and can dive up to 20 feet deep in lakes and ponds.\n
        During mating season, bull moose can become aggressive, using antlers to spar.""",
    "Black Widow": 
        """\nBlack widow venom is 15 times stronger than a rattlesnake's, making them highly toxic.\n
        Female black widows are recognized by the red hourglass mark on their abdomen.\n
        The name comes from the female's habit of consuming the male after mating.\n
        Black widow silk is incredibly strong, comparable to commercial-grade materials.\n
        They spin irregular, tangled webs in dark, undisturbed areas such as basements.""",
    "Rattlesnake": 
        """\nFemale rattlesnakes carry eggs inside their bodies and give birth to live young.\n
        They have heat-sensitive pits that allow them to detect prey in complete darkness.\n
        Rattlesnakes lack eardrums and "hear" by sensing vibrations through their jaws.\n
        Their rattles grow an extra segment each time they shed their skin.\n
        Rattles are made of keratin, the same material found in human hair and nails.""",
    "Mountain Lion": 
        """\nCougars can jump 18 feet vertically and 40 feet horizontally, making them powerful hunters.\n
        Utah is home to approximately 2,300 cougars, according to wildlife estimates.\n
        The highest altitude cougar was spotted at 19,024 feet above sea level.\n
        Cougars are ambush predators, stalking or waiting to strike their prey.\n
        Cougar cubs stay with their mothers for 18 months to 2 years, learning survival skills.""",
    "Scorpion": 
        """\nNewborn scorpions ride on their mother's back until their first molt for protection.\n
        Scorpions have remained largely unchanged for 300 million years, according to fossils.\n
        Modern scorpions can live for up to 25 years in the wild under favorable conditions.\n
        Scorpions engage in a complex mating dance known as the promenade à deux.\n
        Only 25 of the nearly 2,000 scorpion species have venom potent enough to harm humans.""",
    "Mosquito":
        """\nOnly female mosquitoes bite to extract the protein from blood needed to produce eggs.\n
        A mosquito's wings beat from 300 to 600 times per second, creating their distinctive buzz.\n
        Female mosquitoes can consume their body weight in blood during a single feeding.\n
        Mosquitoes lay their eggs in standing water and rest in shady, low-airflow areas.\n
        They can detect the carbon dioxide in your breath from up to 75 feet away.""",
    "Raccoon": 
        """\nRaccoon paws have very sensitive nerves, and wetting them increases their sensitivity.\n
        Raccoons thrive in urban areas, adapting well to life alongside humans.\n
        Raccoons are the second most frequently reported rabid wildlife species in the U.S.\n
        They are excellent climbers and can descend tree trunks headfirst with ease.\n
        The name "raccoon" comes from an Algonquin word meaning "one who rubs with his hands." """,
    "Black Bear": 
        """\nBlack bears hibernate from late November to early December to conserve energy in winter.\n
        They typically live in forests and are excellent tree climbers, sometimes sleeping in trees.\n
        Black bear cubs stay with their mother for one to three years, learning survival skills.\n
        These bears are strong swimmers, capable of paddling over a mile in freshwater.\n
        Black bears can sprint at speeds up to 35 miles per hour when threatened.""",
    "Coyote": 
        """\nCoyotes are highly adaptable and can be found in nearly every habitat in North America.\n
        Coyotes form strong family bonds, with packs usually consisting of a mated pair and offspring.\n
        They are known for their distinctive vocalizations, including howls, yips, and barks.\n
        Coyotes can run at speeds of up to 40 miles per hour, making them very fast predators.\n
        Their excellent senses of smell, hearing, and sight help them hunt and avoid danger.""",
    "Gila Monster": 
        """\nGila monsters are one of only two venomous lizards in North America, with a painful bite.\n
        They can store fat in their tails, surviving for months on these reserves without food.\n
        Gila monsters use their keen sense of smell to locate nests of eggs and small prey.\n
        Once a Gila monster bites, it tends to hold on, gnawing to inject venom through its teeth.\n
        Due to their slow reproduction and shrinking habitat, they are protected by law.""",
    "Logan Cropper": 
        """\nPresident of the comedy club and drummer in a salsa band, Logan is a multi-talented guy.\n
        Known for his fearless attitude, he can stare down a laser without flinching.\n
        Logan is a skilled gamer, often playing Lucina in Smash Bros tournaments.\n
        With his diverse skills and confidence, Logan is the most dangerous "animal" of all."""
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
    #"Logan Cropper": None

 # TODO: Add Logan Cropper image
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

background_image = pygame.image.load("images/brick.jpg")

# Load and play background music for character select
pygame.mixer.music.load("music/Megafauna.mp3")

# Load sound effects
sound_title_start = pygame.mixer.Sound("sounds/title_start.wav")
sound_playerselect_start = pygame.mixer.Sound("sounds/playerselect_start.wav")
sound_playerselect_move = pygame.mixer.Sound("sounds/playerselect_move.wav")
sound_playerselect_select = pygame.mixer.Sound("sounds/playerselect_select.wav")
sound_smash_attack = pygame.mixer.Sound("sounds/smash_attack.wav")

# Animal Select global params
select_background_color = (200, 200, 200)
select_header_height = 100
select_box_height = 300
select_box_width = SCREEN_WIDTH / 5
select_border_weight = 10
select_selected_border_weight = 30

last_input_time = [0,0]  # Last time input was received for each player
debounce_delay = 0.15  # 200 milliseconds debounce delay

joysticks = {}

# Key mappings
KEYBOARD_KEYS = {
    "P1_SELECT": pygame.K_RETURN,    # Player 1 selects an animal
    "P2_SELECT": pygame.K_SPACE,     # Player 2 selects an animal
    "P1_START": pygame.K_r,          # Player 1 starts the game
    "P2_START": pygame.K_t,          # Player 2 starts the game
    "P1_UP": pygame.K_w,             # Player 1 moves up
    "P1_DOWN": pygame.K_s,           # Player 1 moves down
    "P1_LEFT": pygame.K_a,           # Player 1 moves left
    "P1_RIGHT": pygame.K_d,          # Player 1 moves right
    "P2_UP": pygame.K_UP,            # Player 2 moves up
    "P2_DOWN": pygame.K_DOWN,        # Player 2 moves down
    "P2_LEFT": pygame.K_LEFT,        # Player 2 moves left
    "P2_RIGHT": pygame.K_RIGHT       # Player 2 moves right
}

# Function to draw multiline text
def draw_multiline_text(text, font, color, surface, x, y, line_height):
    lines = text.split('\n')  # Split the text into lines based on the newline character
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * line_height))

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

    screen.blit(background_image, (0, 0))

    title_text = font_select_title.render("CHARACTER SELECT", True, WHITE)
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
            animal_text = font_select_animal_large.render(animal, True, WHITE)
            screen.blit(animal_text, origin)
            draw_multiline_text(animal_stats[animal], font_small, WHITE, screen, origin[0], origin[1] + 50, font_small.get_height())

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
STATE_BUMP = 4

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
            if i == 0:  # Mirror the sprite on the left
                scaled_sprite = pygame.transform.flip(scaled_sprite, True, False)
            screen.blit(scaled_sprite, sprite_positions[i])
        else:
            dummy_sprite = font_large.render("?", True, BLACK)
            screen.blit(dummy_sprite, sprite_positions[i])

    if animation_state == STATE_FINISHED:
        selected_animal_indices = [animals.index(animal) for animal in selected_animals]
        winning_sprite = selected_animal_indices.index(min(selected_animal_indices))
        # Get the winning animal
        winning_animal = selected_animals[winning_sprite]
        winning_description = f"The {winning_animal} is the number {animals.index(winning_animal) + 1} most dangerous animal!"

        # Display the winning animal's name
        end_banner_height = 200
        end_text = font_select_animal_large.render(winning_description, True, WHITE)
        pygame.draw.rect(screen, (20, 20, 20), (0, SCREEN_HEIGHT / 2 - end_banner_height / 2, SCREEN_WIDTH, end_banner_height), 0)
        screen.blit(end_text, end_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        # Display the winning animal's image
        #if winning_animal in animal_images.keys():
        #    winning_image = animal_images[winning_animal]
        #    scaled_image = pygame.transform.scale(winning_image, (200, 200))
        #    screen.blit(scaled_image, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100))


def update_sprite_positions():
    global animation_state, step_count, turn_count
    global active_sprite, move_count, moves
    global sprite_positions, sprite_home_positions, sprite_attack_state
    global losing_sprite, winning_sprite

    if animation_state == STATE_APPEAR:
        # Initial position setup from edges of the screen
        sprite_positions[0] = (-sprite_size[0], sprite_positions[0][1])  # Start off-screen left
        sprite_positions[1] = (SCREEN_WIDTH, sprite_positions[1][1])     # Start off-screen right
        animation_state = STATE_STEP_CLOSER

    if animation_state == STATE_STEP_CLOSER:
        # Move sprites towards each other
        sprite_positions[0] = (sprite_positions[0][0] + 20, sprite_positions[0][1])  # Slower approach
        sprite_positions[1] = (sprite_positions[1][0] - 20, sprite_positions[1][1])
        
        # Check if they have met in the center
        if sprite_positions[0][0] >= (SCREEN_WIDTH // 2) - sprite_size[0] and sprite_positions[1][0] <= (SCREEN_WIDTH // 2):
            animation_state = STATE_BUMP
            sprite_home_positions = sprite_positions.copy()
            step_count = 0
            turn_count = 0
            # Determine the winner based on which selected animal appears first in the 'animals' array
            selected_animal_indices = [animals.index(animal) for animal in selected_animals]
            winning_sprite = selected_animal_indices.index(min(selected_animal_indices))
            losing_sprite = 1 - winning_sprite

    if animation_state == STATE_BUMP:
        # Sprites bump into each other a few times
        bump_distance = 10  # Smaller bump distance for smoother animation
        if step_count % 2 == 0:
            sprite_positions[0] = (sprite_home_positions[0][0] - bump_distance, sprite_positions[0][1])
            sprite_positions[1] = (sprite_home_positions[1][0] + bump_distance, sprite_positions[1][1])
        else:
            sprite_positions = sprite_home_positions.copy()

        step_count += 1

        if step_count >= 12:  # Increase the number of steps for smoother bumps
            animation_state = STATE_FIGHT
            sound_smash_attack.play()
            step_count = 0

    if animation_state == STATE_FIGHT:
        if step_count == 0:
            # Winning sprite continues moving forward
            sprite_positions[winning_sprite] = (sprite_positions[winning_sprite][0] + 15, sprite_positions[winning_sprite][1])
            step_count += 1
        else:
            # Losing sprite is propelled up and away
            sprite_positions[losing_sprite] = (sprite_positions[losing_sprite][0], sprite_positions[losing_sprite][1] - 70)
            sprite_positions[losing_sprite] = (sprite_positions[losing_sprite][0] + 5, sprite_positions[losing_sprite][1])

        # Check if the losing sprite has gone off the top of the screen
        if sprite_positions[losing_sprite][1] + sprite_size[1] < 0:
            animation_state = STATE_FINISHED
            step_count = 0


    if animation_state == STATE_FINISHED:
        # Get the winning animal
        winning_animal = selected_animals[winning_sprite]
        winning_description = "The " + winning_animal + " is the number " + str(animals.index(winning_animal)) + " most dangerous animal!"

        # Display the winning animal's name
        end_banner_height = 200
        end_text = font_select_fight_banner.render(winning_description, True, WHITE)
        pygame.draw.rect(screen, (20, 20, 20), (0, SCREEN_HEIGHT / 2 - end_banner_height / 2, SCREEN_WIDTH, end_banner_height), 0)
        screen.blit(end_text, end_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

        # Display the winning animal's image
        if winning_animal in animal_images.keys():
            winning_image = animal_images[winning_animal]
            scaled_image = pygame.transform.scale(winning_image, (200, 200))
            screen.blit(scaled_image, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100))

    time.sleep(0.05)  # Smoother animation with shorter sleep




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
debounce_delay = 0.0

# Dictionary to store the last direction for each joystick
last_direction = {0: [0, 0], 1: [0, 0]}

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
        player = 0 if jid == 0 else 1
        print(f"Player {player+1} pressed button {button}")

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
                # Check if the current direction is different from the last direction
                if axes[1] != last_direction[player][1]:
                    if axes[1]:
                        selected_indices[player] = (selected_indices[player] - axes[1]) % 10
                        sound_playerselect_move.play()
                    # Update the last direction for the Y-axis
                    last_direction[player][1] = axes[1]

                if axes[0] != last_direction[player][0]:
                    if axes[0]:
                        selected_indices[player] = (selected_indices[player] + axes[0] * 5) % 10
                        sound_playerselect_move.play()
                    # Update the last direction for the X-axis
                    last_direction[player][0] = axes[0]

    # Handle keyboard inputs
    if event.type == pygame.KEYDOWN:
        # Player 1 key events
        if event.key == KEYBOARD_KEYS["P1_SELECT"]:
            animal_selected[0] = not animal_selected[0]
            sound_playerselect_select.play()
        elif event.key == KEYBOARD_KEYS["P1_START"]:
            if all(animal_selected):
                sound_playerselect_start.play()
                current_state = FIGHT_SCREEN
        elif event.key == KEYBOARD_KEYS["P1_UP"]:
            if not animal_selected[0]:
                selected_indices[0] = (selected_indices[0] - 5) % 10
                sound_playerselect_move.play()
        elif event.key == KEYBOARD_KEYS["P1_DOWN"]:
            if not animal_selected[0]:
                selected_indices[0] = (selected_indices[0] + 5) % 10
                sound_playerselect_move.play()
        elif event.key == KEYBOARD_KEYS["P1_LEFT"]:
            if not animal_selected[0]:
                selected_indices[0] = (selected_indices[0] - 1) % 10
                sound_playerselect_move.play()
        elif event.key == KEYBOARD_KEYS["P1_RIGHT"]:
            if not animal_selected[0]:
                selected_indices[0] = (selected_indices[0] + 1) % 10
                sound_playerselect_move.play()

        # Player 2 key events
        if event.key == KEYBOARD_KEYS["P2_SELECT"]:
            animal_selected[1] = not animal_selected[1]
            sound_playerselect_select.play()
        elif event.key == KEYBOARD_KEYS["P2_START"]:
            if all(animal_selected):
                sound_playerselect_start.play()
                current_state = FIGHT_SCREEN
        elif event.key == KEYBOARD_KEYS["P2_UP"]:
            if not animal_selected[1]:
                selected_indices[1] = (selected_indices[1] - 5) % 10
                sound_playerselect_move.play()
        elif event.key == KEYBOARD_KEYS["P2_DOWN"]:
            if not animal_selected[1]:
                selected_indices[1] = (selected_indices[1] + 5) % 10
                sound_playerselect_move.play()
        elif event.key == KEYBOARD_KEYS["P2_LEFT"]:
            if not animal_selected[1]:
                selected_indices[1] = (selected_indices[1] - 1) % 10
                sound_playerselect_move.play()
        elif event.key == KEYBOARD_KEYS["P2_RIGHT"]:
            if not animal_selected[1]:
                selected_indices[1] = (selected_indices[1] + 1) % 10
                sound_playerselect_move.play()
    #print(selected_indices)
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
