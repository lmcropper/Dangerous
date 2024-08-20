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
font_small = pygame.font.Font(None, 36)

# Animals
animals = ["Moose", "Black Widow", "Rattlesnake", "Mountain Lion", "Scorpion", "Mosquito", "Raccoon", "Black Bear", "Coyote", "Gila Monster"]
animal_stats = {
    "Moose": 
        """Moose are the largest members of the deer family: weighing up to 1,500 pounds and standing about 6 feet tall at the shoulder.\n
        Male moose grow massive, broad antlers that can span up to 6 feet from tip to tip.\n
        Moose have relatively poor eyesight, but they make up for it with a strong sense of smell and acute hearing.\n
        Moose are excellent swimmers and often feed on aquatic plants. They can dive up to 20 feet deep in lakes and ponds.\n
        During the mating season, bull moose can become quite aggressive, using their antlers to spar with rivals and establish dominance.""",
    "Black Widow": 
        """Black widow spiders are famous for their potent venom, which is 15 times stronger than that of a rattlesnake.\n
        Female black widows are easily recognized by the red or orange hourglass-shaped marking on the underside of their shiny black abdomen.\n
        The species gets its name from the female's tendency to consume the male after mating, although this behavior is not as common as once believed.\n
        The silk produced by black widows is extremely strong and durable, comparable to the strength of some commercial-grade materials.\n
        Black widows spin irregular, tangled webs in dark, undisturbed areas""",
    "Rattlesnake": 
        """Female rattlesnakes carry and incubate their eggs inside of their bodies for around 90 days before giving birth to live young.\n
        Rattle Snakes have heat-sensitive pits on each side of their heads that transmit signals to the same area of the snake's brain as the optic nerve. It can “see” the heated image of its prey even in complete darkness.\n
        Rattlesnakes have an inner ear structure without an eardrum, instead, snakes "hear" by sensing vibrations through their jawbone.\n
        Once rattlesnakes grow out of their old skin and go through the molting process, their bodies naturally add an extra segment to their rattles each time.\n
        Their rattle is made up of various interlocking rings of keratin, the same material that human hair, skin, and nails are made of.""",
    "Mountain Lion": 
        """Cougars can jump 18ft vertically and 40ft horizontally.\n
        Utah division of wildlife resources estimates that 2,300 cougars live in Utah.\n
        Highest cat: cougar spotted at 5,800 m (19,024 ft).\n
        Cougar is an ambush predator--It either stalks its prey or waits for it to draw close before striking.\n
        The cubs stay with their mother for between 18 months to 2 years. The cubs drink their mother's milk for around 3 months, but begin to eat meat after 6 weeks.""",
    "Scorpion": 
        """After birth, the newborn scorpions ride on their mother's back, where they remain protected until they molt for the first time.\n
        Fossil evidence shows that scorpions have remained largely unchanged since the Carboniferous period (350-300 million years ago).\n
        Modern scorpions can live as long as 25 years.\n
        Scorpions engage in an elaborate courtship ritual known as the promenade à deux (literally, a walk for two).\n
        Of the nearly 2,000 known species of scorpions in the world, only 25 are known to produce venom powerful enough to pack a dangerous punch to an adult.""",
    "Mosquito":
        """Only female mosquitoes bite because they need the protein from blood to produce their eggs.\n
        A mosquito's wings beat from 300 to 600 times per second.\n
        Some female mosquitoes can drink their entire body weight in blood during a meal.\n
        Mosquitoes lay their eggs in standing water and like to rest in shady spots and areas with low air flow\n
        A mosquito can smell the carbon dioxide you exhale from about 60 to 75 feet away.""",
    "Raccoon": 
        """Raccoons have very sensitive nerves on the fingers of their front paws: wetting the skin is believed to increase the responsiveness of those nerves.\n
        Although so many animal populations have been diminished because of human urbanization, raccoons have readily adapted to living alongside people.\n
        After bats, raccoons are the second most frequently reported rabid wildlife species, according to the CDC.\n
        Raccoons are great climbers: they're one of the few mammals that can descend vertical tree trunks headfirst.\n
        The name Raccoon is from the Algonquin word arukhkun, meaning “he who rubs, scrubs and scratches with his hands.""",
    "Black Bear": 
        """In late November and early December, black bears head to their dens to sleep away the winter, or hibernate.\n
        They typically live in forests and are excellent tree climbers, even sleeping in trees during the summer.\n
        Black bear cubs stay with Mom for one to three years while she teaches them how to live in the wild.\n
        Excellent swimmers: black bears can paddle at least a mile and a half in freshwater.\n
        They can sprint up to 35 miles per hour.""",
    "Coyote": 
        """Coyotes are found in nearly every type of habitat in North America, from deserts and forests to urban areas.\n
        Coyotes often forms strong family bonds: A pack typically consists of a mated pair and their offspring.\n
        They are known for their distinctive vocalizations, including howls, yips, and barks - which they use to communicate.\n
        Coyotes can run at speeds of up to 40 miles per hour: making them one of the fastest animals in North America.\n
        They have excellent senses of smell, hearing, and sight, which help them hunt and avoid danger.""",
    "Gila Monster": 
        """The Gila monster is one of only two venomous lizards in North America. While not typically fatal to humans, its bite can be very painful.\n
        They can store fat in their tails and live off these reserves for months.\n
        Gila monsters use their keen sense of smell to locate nests of eggs or young birds and mammals, which form a large part of their diet.\n
        Once a Gila monster bites, it tends to hold on, gnawing to help inject through grooves in its teeth.\n
        Due to their slow reproductive rate and shrinking habitat, Gila monsters are protected by law in several states""",
    "Logan Cropper": 
        """President of the comedy club\n
        Plays the drums in the salsa band\n
        Can stare down the barrell of a laser and be fine\n
        Plays Lucina in smash bros\n
        Easily the most dangerous animal of them all"""
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

background_image = pygame.image.load("images/brick.jpg")

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
            stats_text = font_small.render(animal_stats[animal], True, WHITE)
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
