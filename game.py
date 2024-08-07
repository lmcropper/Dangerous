import pygame
import sys

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
    "Rattlesnake": 
        "Female rattlesnakes carry and incubate their eggs inside of their bodies for around 90 days before giving birth to live young.
        Rattle Snakes have heat-sensitive pits on each side of their heads that transmit signals to the same area of the snake’s brain as the optic nerve. It can “see” the heated image of its prey even in complete darkness.
        Rattlesnakes have an inner ear structure without an eardrum, instead, snakes "hear" by sensing vibrations through their jawbone.
        Once rattlesnakes grow out of their old skin and go through the molting process, their bodies naturally add an extra segment to their rattles each time.
        Their rattle is made up of various interlocking rings of keratin, the same material that human hair, skin, and nails are made of.",
    "Mountain Lion": 
        "Cougars can jump 18ft vertically and 40ft horizontally.
        Utah division of wildlife resources estimates that 2,300 cougars live in Utah.
        Highest cat: cougar spotted at 5,800 m (19,024 ft).
        Cougar is an ambush predator–It either stalks its prey or waits for it to draw close before striking.
        The cubs stay with their mother for between 18 months to 2 years. The cubs drink their mother’s milk for around 3 months, but begin to eat meat after 6 weeks.",
    "Scorpion": 
        "After birth, the newborn scorpions ride on their mother's back, where they remain protected until they molt for the first time.
        Fossil evidence shows that scorpions have remained largely unchanged since the Carboniferous period (350-300 million years ago).
        Modern scorpions can live as long as 25 years.
        Scorpions engage in an elaborate courtship ritual known as the promenade à deux (literally, a walk for two).
        Of the nearly 2,000 known species of scorpions in the world, only 25 are known to produce venom powerful enough to pack a dangerous punch to an adult.",
    "Mosquito": "Stats for Mosquito",
    "Raccoon": "Stats for Raccoon",
    "Black Bear": "Stats for Black Bear",
    "Coyote": "Stats for Coyote",
    "Gila Monster": "Stats for Gila Monster"
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
    "Gila Monster": pygame.image.load("images/gila_monster.png")
}

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

def draw_fight_screen():
    screen.fill(WHITE)
    fight_text = font_large.render("Fight!", True, BLACK)
    screen.blit(fight_text, ((SCREEN_WIDTH - fight_text.get_width()) // 2, 20))

    # Draw dummy sprites for selected animals
    for i, animal in enumerate(selected_animals):
        if animal:
            dummy_sprite = font_large.render(animal[0], True, BLACK)
            screen.blit(dummy_sprite, (200 + i * 400, 300))

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
        draw_fight_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
