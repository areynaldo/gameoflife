import pygame
import random
import copy

#Table functions
def newTable(w,h):
    table = []
    for i in range(0, h):
        table.append([])
        for j in range(0, w):
            table[i].append(False)
    return table

def drawTable(table, screen):
    h = screen.get_height()/len(table)
    w = screen.get_width()/len(table[0])
    for y in range(0, len(table)):
        for x in range(0, len(table[y])):
            if table[y][x]:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(w*x, h*y, w, h))
            elif not table[y][x]:
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(w*x, h*y, w, h))

def countNeighbours(cells, x, y):
    count = 0

    #N
    if y > 0:
        if cells[y-1][x]:
            count +=1
    #S
    if y < len(cells)-1:
        if cells[y+1][x]:
            count +=1
    #E
    if x > 0:
        if cells[y][x-1]:
            count +=1
    #W
    if x < len(cells[0])-1:
        if cells[y][x+1]:
            count +=1
    #NE
    if y > 0 and x < len(cells[0])-1:
        if cells[y-1][x+1]:
            count +=1
    #SE
    if y < len(cells)-1 and x < len(cells[0])-1:
        if cells[y+1][x+1]:
            count +=1
    #SE
    if y < len(cells)-1 and x > 0:
        if cells[y+1][x-1]:
            count +=1
    #NW
    if y > 0 and x > 0:
        if cells[y-1][x-1]:
            count +=1

    return count

#Table class
class Cgol():
    pause = True
    cells = []
    dt    = 0

    def __init__(self, w, h):
        self.pause = True
        self.dt = 0
        self.cells = []
        for i in range(0, h):
            self.cells.append([])
            for j in range(0, w):
                self.cells[i].append(False)

    def draw(self, screen):
        h = screen.get_height()/len(self.cells)
        w = screen.get_width()/len(self.cells[0])
        for y in range(0, len(self.cells)):
            for x in range(0, len(self.cells[y])):
                if self.cells[y][x]:
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(w*x, h*y, w, h))
                elif not self.cells[y][x]:
                    pygame.draw.rect(screen, (255,255,255), pygame.Rect(w*x, h*y, w, h))
                pygame.draw.rect(screen, (200,200,200), pygame.Rect(w*x, h*y, w, h), 1)

    def changeCells(self, screen):
        h = screen.get_height()/len(self.cells)
        w = screen.get_width()/len(self.cells[0])
        for y in range(0, len(self.cells)):
            for x in range(0, len(self.cells[y])):
                rect = pygame.Rect(w*x, h*y, w, h)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.cells[y][x] = False if self.cells[y][x] else True

    def update(self, clock):
        if not self.pause:
            self.dt += clock.get_time()
            print(self.dt)
            if self.dt >= 100:
                self.dt = 0
                self.nextGen()

    def nextGen(self):
        oldcells = [i[:] for i in self.cells]
        for y in range(0, len(oldcells)):
            for x in range(0, len(oldcells[y])):
                neighbours = countNeighbours(oldcells, x, y)
                if oldcells[y][x]:
                    if neighbours > 3 or neighbours < 2:
                        self.cells[y][x] = False
                elif not oldcells[y][x]:
                    if neighbours == 3:
                        self.cells[y][x] = True


def main():
    gol = Cgol(32,18)

    pygame.init()
    gscreen = pygame.display.set_mode((1280, 720))
    grunning = True
    clock = pygame.time.Clock()

    while grunning:
        clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                    grunning = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                gol.changeCells(gscreen)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    gol.pause = False if gol.pause else True
                if ev.key == pygame.K_RIGHT:
                    gol.nextGen()
                if ev.key == pygame.K_RIGHT:
                    pass

        gol.update(clock)
        gol.draw(gscreen)
        pygame.display.flip()

if __name__ == "__main__":
    main()