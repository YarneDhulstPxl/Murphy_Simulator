import math
import pygame
import numpy as np


class Car(pygame.sprite.Sprite):
    def __init__(self, surface):
        self.bounded_rect = surface.get_rect()

        super(Car, self).__init__()

        self._original_image = pygame.image.load('img/car.png')
        self._original_image = pygame.transform.scale(self._original_image, (50, 30))
        self.image = self._original_image

        global car_x
        global car_y
        
        self.rect = self.image.get_rect()
        car_x = int(self.rect.centerx)
        car_y = int(self.rect.centery)

        # Set the car right in the center of the screen
        self.rect.centery = self.bounded_rect.height / 2
        self.rect.centerx = self.bounded_rect.width - (self.rect.width / 2)

    def set_car_straight(self):
        # Set the car straight by just pointing to the original image
        self.image = self._original_image

    def move(self, x, y):
        if y < 0:
            # If we move down, rotate the image a bit so it looks like it's actually steering down
            self.image = pygame.transform.rotate(self._original_image, -5)
        elif y > 0:
            # If we move up, rotate the image a bit so it looks like it's actually steering up
            self.image = pygame.transform.rotate(self._original_image, 5)
        else:
            # If we don't move up or down, we set the car straight again
            self.set_car_straight()

        # Move the car by changing the sprite positions
        self.rect.centerx = self.rect.centerx + x
        self.rect.centery = self.rect.centery + y
        
        global car_x
        global car_y

        car_x = int(self.rect.centerx)
        car_y = int(self.rect.centery)

        # But make sure that the sprite stays within the game screen
        self.rect.clamp_ip(self.bounded_rect)


class CarGame(object):

    # How "fast" will the game go.
    SPEED = 1

    # Length of the line
    MIDDLE_LINE_LENGTH = 20

    # The length of the gap between the lines
    MIDDLE_LINE_GAP = 40

    def __init__(self, width=640, height=400):
        # Initialize the game
        pygame.init()
        pygame.display.set_caption("Murphy simulator")

        # Create the screen and background for the game
        self.width = width
        self.height = height

        global screen
        screen = pygame.display.set_mode((self.width , self.height), pygame.DOUBLEBUF)

        self.background = pygame.Surface(screen.get_size()).convert()

        self.font =  pygame.font.Font(None, 24)

        # Create car and add it to a "spritegroup"
        self.car = Car(screen)
        self.sprites = pygame.sprite.RenderPlain((self.car))

        # Initialize middle line
        self.paint_middle_line = 0 - self.MIDDLE_LINE_GAP

        # Create arrays for center and size on the whole width
        self.road_center = np.repeat(height / 2, width)
        self.road_size = np.repeat(200, width).astype(float)

        self.points = 0

        # Paint initial road (it will be a straight road since we don't update the road)
        for i in range(self.width):
            self.paint_road()

        # Create our angles for curving the road
        self.angle1 = 0
        self.angle2 = 0
        self.angle3 = 0

        # Key variables
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        # Is the game running or not
        self.running = False

    def handle_events(self):
        """
        Handles PyGame events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.left = True
                elif event.key == pygame.K_RIGHT:
                    self.right = True
                elif event.key == pygame.K_UP:
                    self.up = True
                elif event.key == pygame.K_DOWN:
                    self.down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                elif event.key == pygame.K_RIGHT:
                    self.right = False
                elif event.key == pygame.K_UP:
                    self.up = False
                elif event.key == pygame.K_DOWN:
                    self.down = False

    def calculate_distance(self, p2):
        p1 = [car_x, car_y]
        distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
        print(distance)

    def check_collission(self):
        global collision15
        global collisionmin15
        global collision40
        global collisionmin40

        for x in range(1, self.width):
            top = self.road_center[x] - (self.road_size[x] / 2)
            bottom = self.road_center[x] + (self.road_size[x] / 2)
            if self.car.rect.collidepoint(x, top):
                self.running = False
                return
            if self.car.rect.collidepoint(x, bottom):
                self.running = False
                return
            
            if angle40rect.collidepoint(x, top):
                collision40 = True
                # print("angle 40 hit top")
                print("x: " + str(x) +" y: " + str(top))
                self.calculate_distance((x, top))
            if angle40rect.collidepoint(x, bottom):
                collision40 = True
                # print("angle 40 hit bottom")
            if angle15rect.collidepoint(x, top):
                collision15 = True
                # print("angle 15 hit top")
            if angle15rect.collidepoint(x, bottom):
                collision15 = True
                # print("angle 15 hit bottom")
            if anglemin15rect.collidepoint(x, top):
                collisionmin15 = True
                # print("angle -15 hit top")
            if anglemin15rect.collidepoint(x, bottom):
                collisionmin15 = True
                # print("angle -15 hit bottom")
            if anglemin40rect.collidepoint(x, top):
                collisionmin40 = True
                # print("angle -40 hit top")
            if anglemin40rect.collidepoint(x, bottom):
                collisionmin40 = True
                # print("angle -40 hit bottom")

        pass

    def run(self):
        self.running = True

        global collision15
        global collisionmin15
        global collision40
        global collisionmin40

        collision15 = False
        collisionmin15 = False
        collision40 = False
        collisionmin40 = False

        # Iterate while running
        while self.running:
            # Increase your points
            self.points += 1

            # Handle events
            self.handle_events()

            # Check if we need to move the car
            if self.left:
                self.car.move(-1, 0)
            elif self.right:
                self.car.move(+1, 0)
            elif self.up:
                self.car.move(0, -1)
            elif self.down:
                self.car.move(0, +1)
            else:
                # We're not moving, so put our car straight again
                self.car.set_car_straight()

            # call update for all our sprites (if they need it)
            self.sprites.update()

            # Update and paint the road on our background
            for i in range(self.SPEED):
                self.update_road()
                self.paint_road()

            self.update_screen()

            self.check_collission()

        pygame.quit()
        print("Game over. You've scored %s points" % self.points)

    def update_screen(self):
        # Paint background
        screen.blit(self.background, (0, 0))

        # Plot texts
        self.plot_text(10, 10, "Road size: {:3}".format(int(self.road_size[0])))
        self.plot_text(10, 25, "Points: {:3}".format(self.points))

        # Draw the sprites
        self.sprites.draw(screen)

        self.draw_detectors()

        # Flip the buffer to the screen
        pygame.display.flip()

    def draw_detectors(self):
        global car_x
        global car_y
        global collision15
        global collisionmin15
        global collision40
        global collisionmin40

        detector_range = 100
        detector_color = (0, 255, 255)

        pygame.draw.line(screen, detector_color, (car_x, car_y) , (car_x - 100, car_y))

        # angle + 180 because the car goes to the left
        # angle of 15 degrees
        global angle15rect
        detector_color = (0, 255, 255)
        if collision15:
            detector_color = (255, 0, 0)
            collision15 = False
        x2 = detector_range * math.cos(math.radians(195)) + car_x
        y2 = detector_range * math.sin(math.radians(195)) + car_y
        angle15rect = pygame.draw.line(screen, detector_color, (car_x, car_y) , (x2, y2))

        # angle of -15 degrees
        global anglemin15rect
        detector_color = (0, 255, 255)
        if collisionmin15:
            detector_color = (255, 0, 0)
            collisionmin15 = False
        x2 = detector_range * math.cos(math.radians(-195)) + car_x
        y2 = detector_range * math.sin(math.radians(-195)) + car_y
        anglemin15rect = pygame.draw.line(screen, detector_color, (car_x, car_y) , (x2, y2))

        # angle of 40 degrees
        global angle40rect
        detector_color = (0, 255, 255)
        if collision40:
            detector_color = (255, 0, 0)
            collision40 = False
        x2 = detector_range * math.cos(math.radians(220)) + car_x
        y2 = detector_range * math.sin(math.radians(220)) + car_y
        angle40rect = pygame.draw.line(screen, detector_color, (car_x, car_y) , (x2, y2))

        # angle of -40 degrees
        global anglemin40rect
        detector_color = (0, 255, 255)
        if collisionmin40:
            detector_color = (255, 0, 0)
            collisionmin40 = False
        x2 = detector_range * math.cos(math.radians(-220)) + car_x
        y2 = detector_range * math.sin(math.radians(-220)) + car_y
        anglemin40rect = pygame.draw.line(screen, detector_color, (car_x, car_y) , (x2, y2))
        



    def update_road(self):
        # rotate center and sizes
        self.road_center = np.roll(self.road_center, 1)
        self.road_size = np.roll(self.road_size, 1)

        # Set the new road size by decreasing a bit from the previous one
        self.road_size[0] = self.road_size[1] - 0.01

        # Update our angles with different speeds
        self.angle1 = self.angle1 + 0.1
        self.angle1 = self.angle1 % 360

        self.angle2 = self.angle2 + 0.041
        self.angle2 = self.angle2 % 360

        self.angle3 = self.angle3 - 0.152
        self.angle3 = self.angle3 % 360

        # Calculate the new road center, with the angles, this will nicely curve on the screen
        self.road_center[0] = (self.height / 2) - \
                  ((self.height / 6) * math.sin(math.radians(self.angle1))) - \
                  ((self.height / 6) * math.sin(math.radians(self.angle2))) - \
                  ((self.height / 6) * math.sin(math.radians(self.angle3)))

        # Increase middle line counter and wrap on the given length (it doesn't paint anything here)
        self.paint_middle_line = self.paint_middle_line + 1
        if self.paint_middle_line == self.MIDDLE_LINE_LENGTH:
            self.paint_middle_line = 0 - self.MIDDLE_LINE_GAP


    def paint_road(self):
        # Move whole background one pixel to the left
        self.background.scroll(1, 0)

        # Find the top and bottom of the road in pixels
        top = int(self.road_center[0] - (self.road_size[0] / 2))
        bottom = int(self.road_center[0] + (self.road_size[0] / 2))

        # Iterate the whole height of the game screen
        for i in range(self.height):
            if i > bottom:
                # Print a green pixel at the bottom
                c = (0, 200, 0)
            elif i == bottom:
                # Print the road edge
                c = (255, 255, 255)
            elif i > top:
                # Print the actual road
                c = (40, 40, 40)
            elif i == top:
                # Print an edge again
                c = (255, 255, 255)
            else:
                # Print the top green pixels
                c = (0, 200, 0)
            self.background.set_at((0, i), c)

        # Check if the middle line is positive, if so we can just paint a middle line
        if self.paint_middle_line > 0:
            c = (255, 255, 0)
            self.background.set_at((0, int(self.road_center[0]-1)), c)
            self.background.set_at((0, int(self.road_center[0])), c)
            self.background.set_at((0, int(self.road_center[0]+1)), c)


    def plot_text(self, x, y, text):
        surface = self.font.render(text, True, (0, 0, 0))
        screen.blit(surface, (x, y))


if __name__ == '__main__':
    CarGame(640, 480).run()