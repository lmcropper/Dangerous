import pygame
import sys

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