import pygame
import random
 
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
 
# Set the width and height of each snake segment
segment_width = 15
segment_height = 15

# Set the width and height of screen
screen_width = 800
screen_height = 600


# Margin between each segment
segment_margin = 3
 
# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
 
 
class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y, color):
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Score(pygame.sprite.Sprite):
    def __init__(self, score, color, width, height, size = 25):
        # Call the parent class (Sprite) constructor  
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.textSurf = self.font.render("Score: " + str(score), 1, color)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.set_alpha(128)
        self.image.blit(self.textSurf, (W, 0))
        self.rect = self.textSurf.get_rect()

def generateFood(allspriteslist):
    food_segment = None
    
    food_x = random.randint(0, screen_width - segment_width)
    food_y = random.randint(0, screen_height - segment_height)
    if food_x % 18 == 0 and food_y % 18 == 0:
        food_segment = Segment(food_x, food_y, GREEN)
    
    while food_segment == None:
        food_x = random.randint(0, screen_width - segment_width)
        food_y = random.randint(0, screen_height - segment_height)
        if food_x % 18 == 0 and food_y % 18 == 0:
            food_segment = Segment(food_x, food_y, GREEN)
        if (food_x, food_y) in snake_points:
            food_segment = None
    
    allspriteslist.add(food_segment)
    return allspriteslist, (food_x, food_y), food_segment

def foodEaten(snake_points, food_x, food_y):
    if (food_x, food_y) in snake_points:
        return True
    return False

def text_objects(text, font, color = WHITE):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(msg, text):
    largeText = pygame.font.Font('freesansbold.ttf',75)
    smallText = pygame.font.Font('freesansbold.ttf',45)
    msgSurf, msgRect = text_objects(msg, largeText)
    textSurf, textRect = text_objects(text, smallText, RED)
    msgRect.center = ((screen_width/2),(screen_height/2))
    textRect.center = ((screen_width/2),(screen_height/2) + 65)
    screen.blit(msgSurf, msgRect)
    screen.blit(textSurf, textRect)
    pygame.display.update()

def crash(score):
    message_display('You Crashed...', 'Final score: ' + str(score))

def showScore(score):
    scoreText = pygame.font.Font('freesansbold.ttf', 25)
    scoreSurf, scoreRect = text_objects('Score: ' + str(score), scoreText, BLUE)
    scoreRect.center = (screen_width - 70, 25)
    screen.blit(scoreSurf, scoreRect)
    Score(score, BLUE, 70, 30)

# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([screen_width, screen_height])
 
# Set the title of the window
pygame.display.set_caption('Snake in python by Darshan...')
 
allspriteslist = pygame.sprite.Group()
 
# Create an initial snake
snake_segments = []
snake_points = []
for i in range(10):
    x = 270 - (segment_width + segment_margin) * i
    y = 36
    if i == 0: color = RED
    else: color = WHITE
    segment = Segment(x, y, color)
    snake_segments.append(segment)
    snake_points.append((x, y))
    allspriteslist.add(segment)

# Create an initial food
allspriteslist, (food_x, food_y), food_segment = generateFood(allspriteslist)
 
clock = pygame.time.Clock()
done = False
score = 0
sc = None
 
while not done:
    if sc != None: 
        allspriteslist.remove(sc)
        sc = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)
 
    # Get rid of last segment of the snake
    if not foodEaten(snake_points, food_x, food_y):
        old_segment = snake_segments.pop()
        snake_points.pop()
        allspriteslist.remove(old_segment)
 
    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y, RED)
    
    # Check self killing
    if (x, y) in snake_points:
        done = True
        
    # Check borders
    if (x + x_change >= screen_width or x < 0) or (y + y_change >= screen_height or y < 0):
        done = True
        print("Game over!!! Score:", score)
        
    if foodEaten(snake_points, food_x, food_y):
        allspriteslist.remove(food_segment)
        allspriteslist, (food_x, food_y), food_segment = generateFood(allspriteslist)
        score += 1
        #pygame.display.set_caption('Score: ' + str(score))
        
    # Insert new segment into the list
    old_head = snake_segments.pop(0)
    allspriteslist.remove(old_head)
    second_node = Segment(snake_points[0][0], snake_points[0][1], WHITE)
    snake_segments.insert(0, second_node)
    snake_segments.insert(0, segment)
    snake_points.insert(0, (x, y))
    allspriteslist.add(second_node)
    allspriteslist.add(segment)
 
    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)
    
    if sc == None:
        sc = Score(score, BLUE, 670, 30)
        allspriteslist.add(sc)
    allspriteslist.draw(screen)
 
    # Flip screen
    pygame.display.flip()
 
    # Pause
    clock.tick(10)

if done == True: 
    crash(score)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                break