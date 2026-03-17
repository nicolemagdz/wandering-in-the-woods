from ui.ui_k2 import UI_K2
from ui.ui_35 import UI_35
from ui.ui_68 import UI_68
import config
import pygame
from ui.ui_grade_select import GradeSelectUI
from core.simulation import SimulationEngine
    
def main():
    pygame.init()

    # Temporary window for grade selection
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Wandering in the Woods - Select Grade Level")

    # Grade selection screen
    selector = GradeSelectUI(screen)
    grade = selector.run() # returns "K2", "35", or "68"

    # Create simulation engine
    simulation = SimulationEngine()

    # Load correct UI based on grade
    if grade == "K2":
        ui = UI_K2(simulation)
    elif grade == "35":
        ui = UI_35(simulation)
    else:
        ui = UI_68(simulation)

    # Attach UI to simulation (needed for celebration animation)
    simulation.ui = ui

    # Run the selected UI
    ui.run()

if __name__ == "__main__":
    main()