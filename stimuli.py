import pygame
import random
import math
import time
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Dot parameters
dot_radius = 1
dot_color = (255, 255, 255)  # White

# Experiment parameters [1, 3, 6, 9, 12, 15, 18, 20, 25, 30, 40, 50, 60, 80, 100]
coherences = [1, 3, 6, 9, 12, 15, 18, 20, 25, 30, 40, 50]
trials_per_coherence = 1
frames_per_trial = 120
coherent_dot_speed = 1
incoherent_dot_speed = 1
participant_id = 1


# Save results to separate file
def save_results_to_file(results):
    file_name = "results{}.txt".format(participant_id)
    with open(file_name, "w") as file:
        # Write the results to the file
        file.write(results)

# Function to generate random dot positions within a square
def generate_dot_positions(num_dots):
    positions = []
    field_size = 300
    field_left = (screen_width - field_size) // 2
    field_top = (screen_height - field_size) // 2
    for _ in range(num_dots):
        x = random.randint(field_left + dot_radius, field_left + field_size - dot_radius)
        y = random.randint(field_top + dot_radius, field_top + field_size - dot_radius)
        angle = random.uniform(0, 2*math.pi)  # Random angle between 0 and 2*pi
        direction_x = math.cos(angle)  # Calculate x-component of the direction vector
        direction_y = math.sin(angle)  # Calculate y-component of the direction vector
        positions.append((x, y, direction_x, direction_y))
    return positions



# Function to update dot positions
def update_dot_positions(positions, coherence, endpoint_x, endpoint_y):
    coherent_dots = round(len(positions) * coherence / 100)
    field_size = 300
    field_left = (screen_width - field_size) // 2
    field_top = (screen_height - field_size) // 2

    for i in range(coherent_dots):
        x, y, _, _ = positions[i]

        # Calculate direction towards the endpoint
        direction_x = (endpoint_x - x) / field_size
        direction_y = (endpoint_y - y) / field_size

        # Check if direction length is zero
        direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if direction_length == 0:
            direction_x = 0
            direction_y = 0
        else:
            # Normalize the direction vector
            direction_x /= direction_length
            direction_y /= direction_length

        # Rest of the code remains the same...


        # Move coherent dots
        x += direction_x * coherent_dot_speed
        y += direction_y * coherent_dot_speed

        # Check if coherent dots go beyond the field boundaries
        if x < field_left + dot_radius or x > field_left + field_size - dot_radius:
            x -= direction_x * coherent_dot_speed
        if y < field_top + dot_radius or y > field_top + field_size - dot_radius:
            y -= direction_y * coherent_dot_speed

        positions[i] = (x, y, direction_x, direction_y)

    for i in range(coherent_dots, len(positions)):
        x, y, direction_x, direction_y = positions[i]

        # Update direction for incoherent dots
        direction_x += random.uniform(-0.1, 0.1)
        direction_y += random.uniform(-0.1, 0.1)

        # Normalize the direction vector
        direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
        direction_x /= direction_length
        direction_y /= direction_length

        # Move incoherent dots
        x += direction_x * incoherent_dot_speed
        y += direction_y * incoherent_dot_speed

        # Check if incoherent dots go beyond the field boundaries
        if x < field_left + dot_radius or x > field_left + field_size - dot_radius:
            direction_x *= -1
            x += direction_x * incoherent_dot_speed
        if y < field_top + dot_radius or y > field_top + field_size - dot_radius:
            direction_y *= -1
            y += direction_y * incoherent_dot_speed

        positions[i] = (x, y, direction_x, direction_y)


# Display instruction text
instruction_font = pygame.font.Font(None, 20)
instruction_text_content = """
Šiame eksperimente matysie atsitiktinių taškų kinematogramą. \n
Tam tikra dalis taškų judės koherentiškai (į tą pačią pusę). \n
Jūsų užduotis - įvertinti į kurią pusę taškai juda ir paspausti atitinkamą atsakymą. \n
Jei atrodo, kad taškai juda į dešinę - klaviatūroje spauskite rodyklę į dešine. \n
Jei atrodo, kad taškai juda į kairę - klaviatūroje spauskite rodyklę į kairę.\n
Kiekvienas stimulas bus rodomas 2s, atsakymą spauskite, kai stimulas sustoja. \n
Sėkmės.
"""
instruction_text = instruction_font.render(instruction_text_content, True, (255, 255, 255))
instruction_text_lines = instruction_text_content.split("\n")
instruction_text_surfaces = [instruction_font.render(line, True, (255, 255, 255)) for line in instruction_text_lines]
line_height = instruction_text_surfaces[0].get_height()
instruction_text_height = len(instruction_text_surfaces) * line_height
instruction_text = pygame.Surface((screen_width // 2, instruction_text_height))
for i, surface in enumerate(instruction_text_surfaces):
    instruction_text.blit(surface, (0, i * line_height))
instruction_text_rect = instruction_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.fill((0, 0, 0))  # Black
screen.blit(instruction_text, instruction_text_rect)
pygame.display.flip()

# Wait for SPACEBAR to start the experiment or ESCAPE to exit
start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

# Main experiment loop
results = []
previous_endpoints = []
for coherence in coherences:
    results.append(f'{coherence}%:')
    for trial in range(trials_per_coherence):
        # Generate dot positions for the trial
        dot_positions = generate_dot_positions(250)

        # Calculate the direction towards the endpoint
        field_size = 300
        field_left = (screen_width - field_size) // 2
        field_top = (screen_height - field_size) // 2
        # Calculate the direction towards the endpoint
        field_left = (screen_width - field_size) // 2
        field_top = (screen_height - field_size) // 2
        if trial < 2 or previous_endpoints[trial-1] != previous_endpoints[trial-2]:
            endpoint_side = random.choice(['left', 'right'])
        else:
            endpoint_side = 'left' if previous_endpoints[trial-1] == 'right' else 'right'

        # Calculate the endpoint coordinates based on the chosen side
        if endpoint_side == 'left':
            endpoint_x = field_left
        else:
            endpoint_x = field_left + field_size

        endpoint_y = random.randint(field_top + dot_radius, field_top + field_size - dot_radius)

        # Store the current endpoint for future reference
        previous_endpoints.append(endpoint_side)

        angle = math.atan2(endpoint_y - field_top, endpoint_x - field_left)
        direction_x = math.cos(angle)
        direction_y = math.sin(angle)

        # Show stimuli
        for frame in range(frames_per_trial):
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Update dot positions
            update_dot_positions(dot_positions, coherence, endpoint_x, endpoint_y)


            # Clear the screen
            screen.fill((0, 0, 0))  # Black

            # Draw dots
            for position in dot_positions:
                x, y, _, _ = position  # Unpack the x and y values from the position tuple
                pygame.draw.circle(screen, dot_color, (x, y), dot_radius)

            # Update the screen
            pygame.display.flip()

            # Limit the frame rate
            clock.tick(30)  # Adjust the frame rate to control the dot speed

        # Pause for response during the stimuli or after
        response = None
        while response is None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if endpoint_side == 'left':
                            response = 1
                        else:
                            response = -1
                    elif event.key == pygame.K_RIGHT:
                        if endpoint_side == 'right':
                            response = 1
                        else:
                            response = -1
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        # Save the response to results
        results.append(response)

        # Pause for half a second before showing the next stimuli
        pygame.time.wait(500)


# Display thank you message
thank_you_font = pygame.font.Font(None, 36)
thank_you_text = thank_you_font.render("Ačiū už dalyvavimą!", True, (255, 255, 255))
thank_you_text_rect = thank_you_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.fill((0, 0, 0))  # Black
screen.blit(thank_you_text, thank_you_text_rect)
pygame.display.flip()


# Save results to file
save_results_to_file(str(results))

# Wait for a few seconds before closing the program or ESCAPE to exit
end_time = time.time() + 3  # Display thank you message for 3 seconds
while time.time() < end_time:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

# Quit Pygame
pygame.quit()
sys.exit()