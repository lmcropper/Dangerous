import pygame
import sys
import time
import random
import math
import serial 

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

# Serial port settings (adjust the port and baudrate as needed)
ser = serial.Serial('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0', 115200, timeout=1) 

# Game states
TITLE_SCREEN = "title"
CHARACTER_SELECT = "character_select"
FIGHT_SCREEN = "fight"
current_state = TITLE_SCREEN

SELECT_BUTTON = 0
START_BUTTON = 7

# Constants
RETURN_TO_TITLE_DELAY = 3  # Delay in seconds before showing the message to return to the title screen

# Global variable to track the time when the fight ends
fight_end_time = None

# Fonts
font_title_title = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 74)
font_select_fight_banner = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 150)
font_select_title = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 74)
font_select_animal_small = pygame.font.Font("./fonts/WIDEAWAKE.ttf", 36)
font_select_animal_large = pygame.font.Font("./fonts/WIDEAWAKE.ttf", 48)
font_fight_title = pygame.font.Font("./fonts/Platinum Sign Over.ttf", 74)
font_large = pygame.font.Font(None, 72)
font_mid = pygame.font.Font(None, 25)
font_small = pygame.font.Font(None, 20)

# Animals
animals = ["Moose", "Black Widow", "Rattlesnake", "Mountain Lion", "Scorpion", "Mosquito", "Raccoon", "Black Bear", "Coyote", "Gila Monster"]
animal_stats = {
    "Moose": """ 
        Moose are the largest deer species, weighing up to 1,500 lbs and standing 6 feet tall.\n
        Male moose grow antlers that can span up to 6 feet wide from tip to tip.\n
        Moose have poor eyesight but make up for it with a strong sense of smell and hearing.\n
        They are excellent swimmers and can dive up to 20 feet deep in lakes and ponds.\n
        During mating season, bull moose can become aggressive, using antlers to spar.""",
    "Black Widow": """ 
        Black widow venom is 15 times stronger than a rattlesnake's, making them highly toxic.\n
        Female black widows are recognized by the red hourglass mark on their abdomen.\n
        The name comes from the female's habit of consuming the male after mating.\n
        Black widow silk is incredibly strong, comparable to commercial-grade materials.\n
        They spin irregular, tangled webs in dark, undisturbed areas such as basements.""",
    "Rattlesnake": """ 
        Female rattlesnakes carry eggs inside their bodies and give birth to live young.\n
        They have heat-sensitive pits that allow them to detect prey in complete darkness.\n
        Rattlesnakes lack eardrums and "hear" by sensing vibrations through their jaws.\n
        Their rattles grow an extra segment each time they shed their skin.\n
        Rattles are made of keratin, the same material found in human hair and nails.""",
    "Mountain Lion": """ 
        Cougars can jump 18 feet vertically and 40 feet horizontally, making them powerful hunters.\n
        Utah is home to approximately 2,300 cougars, according to wildlife estimates.\n
        The highest altitude cougar was spotted at 19,024 feet above sea level.\n
        Cougars are ambush predators, stalking or waiting to strike their prey.\n
        Cougar cubs stay with their mothers for 18 months to 2 years, learning survival skills.""",
    "Scorpion": """ 
        Newborn scorpions ride on their mother's back until their first molt for protection.\n
        Scorpions have remained largely unchanged for 300 million years, according to fossils.\n
        Modern scorpions can live for up to 25 years in the wild under favorable conditions.\n
        Scorpions engage in a complex mating dance known as the promenade à deux.\n
        Only 25 of the nearly 2,000 scorpion species have venom potent enough to harm humans.""",
    "Mosquito":""" 
        Only female mosquitoes bite to extract the protein from blood needed to produce eggs.\n
        A mosquito's wings beat from 300 to 600 times per second, creating their distinctive buzz.\n
        Female mosquitoes can consume their body weight in blood during a single feeding.\n
        Mosquitoes lay their eggs in standing water and rest in shady, low-airflow areas.\n
        They can detect the carbon dioxide in your breath from up to 75 feet away.""",
    "Raccoon": """ 
        Raccoon paws have very sensitive nerves, and wetting them increases their sensitivity.\n
        Raccoons thrive in urban areas, adapting well to life alongside humans.\n
        Raccoons are the second most frequently reported rabid wildlife species in the U.S.\n
        They are excellent climbers and can descend tree trunks headfirst with ease.\n
        The name "raccoon" comes from an Algonquin word meaning "one who rubs with his hands." """,
    "Black Bear": """ 
        Black bears hibernate from late November to early December to conserve energy in winter.\n
        They typically live in forests and are excellent tree climbers, sometimes sleeping in trees.\n
        Black bear cubs stay with their mother for one to three years, learning survival skills.\n
        These bears are strong swimmers, capable of paddling over a mile in freshwater.\n
        Black bears can sprint at speeds up to 35 miles per hour when threatened.""",
    "Coyote": """ 
        Coyotes are highly adaptable and can be found in nearly every habitat in North America.\n
        Coyotes form strong family bonds, with packs usually consisting of a mated pair and offspring.\n
        They are known for their distinctive vocalizations, including howls, yips, and barks.\n
        Coyotes can run at speeds of up to 40 miles per hour, making them very fast predators.\n
        Their excellent senses of smell, hearing, and sight help them hunt and avoid danger.""",
    "Gila Monster": """ 
        Gila monsters are one of only two venomous lizards in North America, with a painful bite.\n
        They can store fat in their tails, surviving for months on these reserves without food.\n
        Gila monsters use their keen sense of smell to locate nests of eggs and small prey.\n
        Once a Gila monster bites, it tends to hold on, gnawing to inject venom through its teeth.\n
        Due to their slow reproduction and shrinking habitat, they are protected by law.""",
    "Logan Cropper": """ 
        President of the comedy club and drummer in a salsa band, Logan is a multi-talented guy.\n
        Known for his fearless attitude, he can stare down a laser without flinching.\n
        Logan is a skilled gamer, often playing Lucina in Smash Bros tournaments.\n
        With his diverse skills and confidence, Logan is the most dangerous "animal" of all."""
}

animal_descriptions = {
    "Moose": """         
        Moose are the largest mammals in Utah and can be surprisingly dangerous.\n 
        Moose are often aggressive, especially during mating season and when protecting their young.\n 
        They are known to charge when they feel threatened, and their massive antlers can cause severe injury.\n 
        Moose encounters are common in Utah’s mountainous regions, and it’s best to keep a safe distance if you spot one in the wild.\n
        But if you do run into a moose, you should look out for these signs of aggression: licking their long snouts, their ears pinned back, lowering their head as if to charge.\n""",
    "Black Widow": """
        The infamous black widow spider has distinctive markings one should keep an eye out for.\n 
        The blood red hourglass markings on the spider’s back is a clear sign you should avoid these creatures at all costs.\n
        A black widow sting is one of the worst insect bites a person can ever experience.\n 
        Symptoms include nausea, headaches, vomiting, hallucinations, seizures, muscle spasms, fever, and possibly even shock.\n
        Anyone bitten by a black widow should obtain medical care immediately so they can be administered anti-venom for their bite.\n""",
    "Rattlesnake": """ 
        Like most arid regions, rattlesnakes are rather ubiquitous in Utah.\n 
        Indeed, our state contains up to five different species of the iconic snake.\n 
        If you are unlucky enough to be bitten by this noisy reptiles, you should seek out emergency medical care as soon as possible.\n 
        The venom rattlesnakes produce can cause long-term damage to your brain and to your nervous system.\n 
        A bite from a rattlesnake is not an injury you should just try to walk off.\n
        Thankfully, rattlesnakes are nocturnal animals who prefer to hide beneath the ground to avoid the blazing sun.\n 
        Considering how rattlesnakes, too, have a basic form of heat vision, it’s highly likely they will see you in the dark before you see them.\n 
        And even then, you could probably hear them at night thanks to their characteristic rattle sound.\n 
        If that doesn’t send you running in the opposite direction, you’re either brave or reckless.\n""",
    "Mountain Lion": """ 
        If you encounter a mountain lion in the mountains or deserts of Utah, you should not attempt to run away.\n 
        Mountain lions are capable of incredible bursts of speed (up to 50 miles per hour) and are prolific hunters.\n 
        The best way to stay safe in Utah’s mountain lion territories is to never hike alone, stay close to your group,\n 
        keep your campsite clean and free of litter, and avoid any area with an animal carcass.\n 
        You should treat a mountain lion encounter much the same way you would with a bear by keeping eye contact,\n 
        backing away slowly, and giving the animal time and space to escape your company.\n""",
    "Scorpion": """ 
        No one who has been stung by a scorpion likely wants to repeat the experience ever again.\n 
        The reason why is the venom these tiny insects inject packs quite the punch.\n 
        One scorpion sting can cause excruciating pain, repetitive vomiting, swelling, and numbness all throughout the body.\n
        Symptoms often last 1 to 3 days and some unlucky sting recipients may even find it hard to breath or even move the affected limb.\n 
        Sadly, these pesky bugs are all too common in Mexico with up to 100,000 people stung each and every year.\n 
        The best way to avoid feeling the sting of bark scorpions while you’re out hiking or exploring is to wear a thick pair of boots.\n""",
    "Mosquito":""" 
        Weighing in at a diminutive 5 milligrams, the mosquito is, without a doubt, the smallest creature on this list.\n 
        Not to mention the most common. What makes mosquitos so dangerous are the numerous diseases they can transmit to those they bite.\n 
        These diseases include two forms of encephalitis, St. Louis and Equine, and the West Nile virus.\n 
        The worst of these three viruses is equine encephalitis since it requires medical attention.\n 
        Symptoms include vomiting, headache, and a stiff neck.\n 
        Thankfully, mosquitos are seasonal in Utah, preferring the warmer months to prey on hapless humans outside enjoying the sun.\n""",
    "Raccoon": """ 
        Raccoons may look like cute, furry bandits, but do not doubt the ferocity of these animals.\n 
        Not only do raccoons love to invade urban centers, they will attack humans at the drop of a hat.\n 
        The odds a raccoon attack can prove deadly are low considering how most raccoons are smaller than most domesticated dogs.\n 
        They do remain a lethal threat, however, due to how many of them carry the deadly disease rabies.\n 
        Unfortunately, rabies is often a fatal disease if you have not been vaccinated.\n 
        Like most animals on this list, it’s best to avoid raccoons altogether.\n 
        If they find their way into your house or yard, it’s best to hire a professional to remove the raccoon.\n 
        If you have a close encounter with one it’s best to avoid eye contact and back off from the wild animal.\n""",
    "Black Bear": """ 
        Most Utahans are surprised to learn there are thousands of black bears roaming the state.\n 
        Thankfully, most of these furry beasts are only found deep in the forests or atop one of the state’s many mountains.\n 
        Utah’s largest predator by a wide margin, you should do all you can to avoid a run-in with a black bear if you’re out hiking or camping.\n
        While a black bear won’t attack humans for dietary reasons, it will charge you if it feels threatened or if its cubs are around.\n 
        If you do bump into a black bear do not run. Stand your ground and don’t try to play dead or curl into a ball.\n 
        Just give the bear time and space to flee and you’ll likely walk away with an amazing story to tell your friends and family.\n 
        If a black bear does, for some odd reason, attack you, be sure to fight like your life depends on it, because it does.\n 
        If you packed bear spray, now would be the time to use it.\n""",
    "Coyote": """ 
        Coyotes are a pretty common site in the Utah wilderness.\n 
        While these furry animals may look a lot like their distant cousins, the domesticated dog, the similarities stop there.\n 
        Coyotes are wild animals which will attack you if you give them the chance.\n 
        If you encounter a coyote in the wild, the first thing you should do is stay calm.\n 
        The coyote is likely more nervous than you are.\n 
        The best tactic is to attempt to scare it away by yelling, waving your arms, and backing away.\n 
        Whatever you do avoid turning your back on the animal. This might cause it overcome its fears and chase after you.\n 
        And considering how fast a coyote can run, over 35 mph, you don’t stand a chance in a foot race.\n""",
    "Gila Monster": """ 
        This reptile certainly has the most frightening name on this list of dangerous animals.\n 
        But the infamous Gila Monster is more bark than bite in real life.\n 
        Sluggish and slow, the Gila Monster is easy to avoid if you spot one in the wild.\n 
        And they should be easy to spot since they often grow up to two feet in length.\n
        You don’t want to get bitten by a Gila Monster though.\n 
        Their bite packs quite a wallop of venom, with some victims reporting it as toxic as a rattlesnake strike.\n 
        Thankfully, there have been no reported deaths due to Gila Monster bites in over 100 years.\n 
        This doesn’t mean you should act recklessly around one though.\n 
        The best way to deal with a Gila Monster in the wild is to just back away and find another path.\n 
        Trust us. No one wants to be the first Gila Monster fatality in a century.\n""",
    "Logan Cropper": """ 
        President of the comedy club and drummer in a salsa band, Logan is a multi-talented guy.\n
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
}

animal_full_images = {
    "Moose": pygame.image.load("images/full_images/moose.png"),
    "Black Widow": pygame.image.load("images/full_images/black_widow.png"),
    "Rattlesnake": pygame.image.load("images/full_images/rattlesnake.png"),
    "Mountain Lion": pygame.image.load("images/full_images/mountain_lion.png"),
    "Scorpion": pygame.image.load("images/full_images/scorpion.png"),
    "Mosquito": pygame.image.load("images/full_images/mosquito.png"),
    "Raccoon": pygame.image.load("images/full_images/raccoon.png"),
    "Black Bear": pygame.image.load("images/full_images/black_bear.png"),
    "Coyote": pygame.image.load("images/full_images/coyote.png"),
    "Gila Monster": pygame.image.load("images/full_images/gila_monster.png"),
    #"Logan Cropper": None
}

 # TODO: Add Logan Cropper image
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

# Load animation frames for the blast zone
blast_zone_frames = [
    pygame.image.load(f"images/blast_zone/Blast{i}.gif") for i in range(1, 14)
]

stage_background = pygame.image.load("images/stages/FD_Forest.jpg")

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

def reset_game():
    """Resets game state for a new round."""
    global selected_indices, selected_animals, animal_selected, animation_state, sprite_positions, fight_end_time

    selected_indices = [0, 1]
    selected_animals = [None, None]
    animal_selected = [False, False]
    animation_state = STATE_APPEAR
    sprite_positions = [(200, 300), (SCREEN_WIDTH - 200 - sprite_size[1], 300)]
    fight_end_time = None

# Function to draw multiline text
def draw_multiline_text(text, font, color, surface, x, y, line_height):
    lines = text.split('\n')  # Split the text into lines based on the newline character
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * line_height))

def send_danger_level(index):
    """
    Sends a danger level over serial based on the animal's index.
    The level is scaled between 1 (least dangerous) to 100 (most dangerous).
    """
    danger_level = int(((len(animals) - index) / len(animals)) * 100)
    ser.write(danger_level.to_bytes(1, 'big'))  # Send as a single byte
    print(f"Sent danger level {danger_level} over serial for animal index {index}")


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
STATE_ANIMATION = 5

# Constants for moves
BACK = 0
PUNCH = 1
KICK = 2

# Initialize variables
animation_state = STATE_APPEAR
sprite_positions = [(0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2)]
sprite_home_positions = sprite_positions.copy()
winning_sprite = 0
losing_sprite = 0
sprite_angles = [0, 0]
sprite_attack_state = BACK
step_count = 0
turn_count = 0

animation_frame_index = 0
animation_frame_time = 0.1  # Time between frames in seconds
last_frame_time = 0

def draw_fight_screen():
    global animation_state, step_count, fight_end_time, animation_frame_index, last_frame_time, winning_sprite, losing_sprite
    modifier = 1 if winning_sprite == 0 else -1

    screen.fill(WHITE)
    scaled_background = pygame.transform.scale(stage_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_background, (0, 0))

    fight_text = font_fight_title.render("FIGHT!", True, BLACK)
    screen.blit(fight_text, ((SCREEN_WIDTH - fight_text.get_width()) // 2, 20))

    # Draw sprites for selected animals
    for i, animal in enumerate(selected_animals):
        if animal in animal_sprites.keys():
            sprite = animal_sprites[animal]
            scaled_sprite = pygame.transform.scale(sprite, sprite_size)
            scaled_sprite = pygame.transform.flip(scaled_sprite, True, False)
            if animation_state != STATE_FIGHT or i == winning_sprite:
                screen.blit(scaled_sprite, (sprite_positions[i][0] - sprite_size[0] // 2, sprite_positions[i][1] - sprite_size[1] // 2))
        else:
            dummy_sprite = font_large.render("?", True, BLACK)
            screen.blit(dummy_sprite, (sprite_positions[i][0] - dummy_sprite.get_width() // 2, sprite_positions[i][1] - dummy_sprite.get_height() // 2))

    if animation_state == STATE_FIGHT:
        losing_sprite = 1 - winning_sprite

        if step_count == 0:
            # Winning sprite continues moving forward
            sprite_positions[winning_sprite] = (sprite_positions[winning_sprite][0] + 15, sprite_positions[winning_sprite][1])
            step_count += 1
        else:
            # Losing sprite is propelled up and away
            sprite_positions[losing_sprite] = (sprite_positions[losing_sprite][0], sprite_positions[losing_sprite][1] - 120)
            sprite_positions[losing_sprite] = (sprite_positions[losing_sprite][0] + (250 * modifier), sprite_positions[losing_sprite][1])

            # Apply vertical stretch to the losing sprite
            original_image = animal_sprites[selected_animals[losing_sprite]]
            stretched_image = pygame.transform.scale(original_image, (int(sprite_size[0] * 4), int(sprite_size[1] * 0.6)))
            stretched_image = pygame.transform.rotate(stretched_image, 45 * modifier)
            screen.blit(stretched_image, (sprite_positions[losing_sprite][0] - stretched_image.get_width() // 2, sprite_positions[losing_sprite][1] - stretched_image.get_height() // 2))

        # Check if the losing sprite has gone off the top of the screen
        if sprite_positions[losing_sprite][1] + sprite_size[1] < 0:
            animation_state = STATE_ANIMATION
            step_count = 0
            fight_end_time = time.time()

    if animation_state == STATE_ANIMATION:
        # Update the animation frame
        current_time = time.time()
        if current_time - last_frame_time > animation_frame_time:
            animation_frame_index = (animation_frame_index + 1) % len(blast_zone_frames)
            last_frame_time = current_time

        # Draw the current frame of the animation
        current_frame = blast_zone_frames[animation_frame_index]
        current_frame = pygame.transform.scale(current_frame, (current_frame.get_width() * 10, current_frame.get_height() * 10))
        current_frame = pygame.transform.rotate(current_frame, 130 * modifier)
        screen.blit(current_frame, (SCREEN_WIDTH / 2 + (650 * modifier) - current_frame.get_width() / 2, 300 - current_frame.get_height() / 2))

        # Check if the animation is finished
        if animation_frame_index == len(blast_zone_frames) - 1:
            animation_state = STATE_FINISHED
            fight_end_time = time.time()

    if animation_state == STATE_FINISHED:
        screen.fill(WHITE)
        selected_animal_indices = [animals.index(animal) for animal in selected_animals]
        winning_sprite = selected_animal_indices.index(min(selected_animal_indices))
        # Get the winning animal
        winning_animal = selected_animals[winning_sprite]
        winning_description = f"The {winning_animal} is Utah's number {animals.index(winning_animal) + 1} most dangerous animal!"

        # Display the winning animal's image
        if winning_animal in animal_images.keys():
            winning_image = animal_full_images[winning_animal]
            screen.blit(winning_image, (SCREEN_WIDTH / 2 - 925, SCREEN_HEIGHT / 2 - 200))

        end_banner_height = 200
        end_text = font_select_animal_large.render(winning_description, True, WHITE)
        pygame.draw.rect(screen, (20, 20, 20), (0, SCREEN_HEIGHT / 5 - end_banner_height / 2, SCREEN_WIDTH, end_banner_height), 0)
        screen.blit(end_text, end_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5)))

        animal_description = animal_descriptions[winning_animal]
        draw_multiline_text(animal_description, font_mid, BLACK, screen, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 100, 20)

        # Check if the delay has passed to show the message
        if fight_end_time and time.time() - fight_end_time > RETURN_TO_TITLE_DELAY:
            return_text = font_mid.render("Press any button to return to the title screen", True, BLACK)
            screen.blit(return_text, ((SCREEN_WIDTH - return_text.get_width()) // 2 + 200, SCREEN_HEIGHT - 100))

def update_sprite_positions():
    global animation_state, step_count, turn_count
    global active_sprite, move_count, moves
    global sprite_positions, sprite_home_positions, sprite_attack_state
    global losing_sprite, winning_sprite

    if animation_state == STATE_APPEAR:
        # Initial position setup from edges of the screen
        sprite_positions[0] = (0, SCREEN_HEIGHT // 2)  # Start off-screen left
        sprite_positions[1] = (SCREEN_WIDTH, SCREEN_HEIGHT // 2)     # Start off-screen right
        animation_state = STATE_STEP_CLOSER

    if animation_state == STATE_STEP_CLOSER:
        # Move sprites towards each other
        sprite_positions[0] = (sprite_positions[0][0] + 20, sprite_positions[0][1])  # Slower approach
        sprite_positions[1] = (sprite_positions[1][0] - 20, sprite_positions[1][1])
        
        # Check if they have met in the center
        if sprite_positions[0][0] >= ((SCREEN_WIDTH // 2) - 100) and sprite_positions[1][0] <= ((SCREEN_WIDTH // 2) + 100):
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
            sprite_positions[losing_sprite] = (sprite_positions[losing_sprite][0], sprite_positions[losing_sprite][1] - 80)
            sprite_positions[losing_sprite] = (sprite_positions[losing_sprite][0] + 5, sprite_positions[losing_sprite][1])

            # Apply blur and stretch to the losing sprite
            original_image = animal_sprites[selected_animals[losing_sprite]]
            stretched_image = pygame.transform.scale(original_image, (sprite_size[0] + 20, sprite_size[1] + 40))
            blurred_image = pygame.transform.smoothscale(stretched_image, (sprite_size[0], sprite_size[1]))
            screen.blit(blurred_image, sprite_positions[losing_sprite])

        # Check if the losing sprite has gone off the top of the screen
        if sprite_positions[losing_sprite][1] + sprite_size[1] < 0:
            animation_state = STATE_FINISHED
            send_danger_level(animals.index(selected_animals[winning_sprite]))  # Send danger level over serial
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
    global current_state, fight_end_time
    if animation_state == STATE_FINISHED:
        # If the fight is finished and the delay has passed, check for any input
        if fight_end_time and time.time() - fight_end_time > RETURN_TO_TITLE_DELAY:
            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                # Return to the title screen
                current_state = TITLE_SCREEN
                reset_game()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connected")

        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")

        if current_state == TITLE_SCREEN:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play(-1)
            handle_title_screen_events(event)
        elif current_state == CHARACTER_SELECT:
            handle_character_select_events(event)
        elif current_state == FIGHT_SCREEN:
            pygame.mixer.music.stop()
            handle_fight_screen_events(event)

    if current_state == TITLE_SCREEN:
        draw_title_screen()
    elif current_state == CHARACTER_SELECT:
        draw_character_select()
    elif current_state == FIGHT_SCREEN:
        if animation_state == STATE_FINISHED and fight_end_time is None:
            fight_end_time = time.time()  # Record the time when the fight ends
        update_sprite_positions()
        draw_fight_screen()

    pygame.display.flip()
    clock.tick(framerate)

pygame.quit()
sys.exit()
