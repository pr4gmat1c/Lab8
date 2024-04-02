import pygame
import sys
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    drawingmode = "point"
    points = []
    circles = []
    rectangles = []
    drawing = False
    start_pos = None
    while True:

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # determine if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # determine if a letter key was pressed
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                #     yellow color
                elif event.key == pygame.K_y:
                    mode = 'yellow'
                # pink color
                elif event.key == pygame.K_p:
                    mode = 'pink'
                # mode to draw circle
                elif event.key == pygame.K_c:
                    drawingmode = 'circle'
                # key to return to drawing mode
                elif event.key == pygame.K_v:
                    drawingmode = 'point'
                # mode to draw rectangle
                elif event.key == pygame.K_t:
                    drawingmode = 'rectangle'
                elif event.key == pygame.K_e:
                    screen.fill((0,0,0))
                    points = []
                    rectangles = []
                    circles = []


            if drawingmode == "point":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click grows radius
                        radius = min(200, radius + 1)
                    elif event.button == 3:  # right click shrinks radius
                        radius = max(1, radius - 1)

                if event.type == pygame.MOUSEMOTION:
                    # if mouse moved, add point to list
                    position = event.pos
                    points = points + [position]
                    points = points[-256:]

            if drawingmode == 'circle':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        drawing = True
                        start_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        drawing = False
                        end_pos = event.pos
                        radius_circle = math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2)
                        circles.append((start_pos, int(radius_circle)))
                        start_pos = None
                # Draw a preview circle while mouse is being held
                if drawing and start_pos is not None:
                    end_pos = pygame.mouse.get_pos()
                    radius_circle = math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2)
                    pygame.draw.circle(screen, WHITE, start_pos, int(radius_circle), 2)

            if drawingmode == 'rectangle':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        drawing = True
                        start_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        drawing = False
                        end_pos = event.pos
                        # Construct rectangle from any start and end positions
                        rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                           abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                        rectangles.append(rect)
                        start_pos = None
                # Draw a preview rectangle while mouse is being held
                if drawing and start_pos is not None:
                    end_pos = pygame.mouse.get_pos()
                    # Construct temporary rectangle for preview
                    temp_rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                            abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                    pygame.draw.rect(screen, WHITE, temp_rect, 2)

        screen.fill((0, 0, 0))

        # draw all points
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1
            # Draw all stored circles
        for circle in circles:
            pygame.draw.circle(screen, WHITE, circle[0], circle[1], 2)

        for rect in rectangles:
            pygame.draw.rect(screen, WHITE, rect, 2)

        pygame.display.flip()

        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = ((0,0,255))
    elif color_mode == 'red':
        color = ((255,0,0))
    elif color_mode == 'green':
        color = ((0,255,0))
    elif color_mode == 'yellow':
        color = ((255,255,0))
    elif color_mode == 'pink':
        color = ((245, 66, 182))

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


main()