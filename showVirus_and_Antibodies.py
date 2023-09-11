import random
import pygame

class AntivirusSystem:
    def __init__(self, num_antibodies, virus_sequence):
        self.antibodies = []
        self.virus_sequence = virus_sequence
        for i in range(num_antibodies):
            antibody = self.generate_antibody()
            self.antibodies.append(antibody)

    def generate_antibody(self):
        antibody = []
        for i in range(len(self.virus_sequence)):
            base = self.virus_sequence[i]
            if random.random() < 0.1:
                base = self.mutate_base(base)
            antibody.append(base)
        return antibody

    def mutate_base(self, base):
        bases = ['A', 'C', 'G', 'T']
        bases.remove(base)
        return random.choice(bases)

    def detect_virus(self, sequence):
        for antibody in self.antibodies:
            similarity = self.calculate_similarity(sequence, antibody)
            if similarity >= 0.9:
                print("Virus detected!")
                return True
        print("No virus detected.")
        return False

    def calculate_similarity(self, seq1, seq2):
        num_matches = 0
        for i in range(len(seq1)):
            if seq1[i] == seq2[i]:
                num_matches += 1
        similarity = num_matches / len(seq1)
        return similarity

def visualize_antibodies(antibodies, virus_sequence):
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Antibodies")

    # Define colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    # Define font
    font = pygame.font.Font(None, 30)

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(white)

        # Draw virus sequence
        for i in range(len(virus_sequence)):
            base = virus_sequence[i]
            x = i * 40 + 100
            y = 20
            pygame.draw.circle(screen, red, (x, y), 20, 0)
            text = font.render(base, True, black)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

        # Draw antibodies
        for i in range(len(antibodies)):
            antibody = antibodies[i]
            color = blue if i == 0 else green
            for j in range(len(antibody)):
                base = antibody[j]
                x = j * 40 + 100
                y = i * 60 + 100
                pygame.draw.circle(screen, color, (x, y), 20, 0)
                text = font.render(base, True, black)
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

        # Update screen
        pygame.display.flip()

    # Clean up
    pygame.quit()
# Demo
if __name__ == "__main__":
    num_antibodies = int(input("Enter the number of antibodies: "))
    virus_length = int(input("Enter the length of the virus sequence: "))
    bases =virus_sequence = ''.join(random.choices(['A', 'C', 'G', 'T'], k=virus_length))
    antivirus_system = AntivirusSystem(num_antibodies, virus_sequence)

    print("Virus sequence:", virus_sequence)

    visualize_antibodies(antivirus_system.antibodies, virus_sequence)