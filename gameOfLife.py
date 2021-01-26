import cv2
import numpy as np
from time import time, sleep


class GameOfLife:
    def __init__(
            self,
            height=512,
            width=1024,
            generationNumber=None,
            fps=60,
            resizeFactor=8):
        self.__resizeFactor = resizeFactor
        self.height = height // self.__resizeFactor
        self.width = width // self.__resizeFactor
        self.generationNumber = generationNumber
        self.boundaries = [[0, 0], [self.height, self.width]]
        self.world = np.zeros((self.height, self.width, 1), np.uint8)
        self.newStates = []
        self.frameUpdateGap = 1 / fps

    def examplePoints(self, ):
        i, j = self.height // 2, self.width // 2
        points = [(i, j)]

        for k in range(10):
            points.append((i + k, j))
        for k in range(1, 5):
            points.append((i, j + k))
            points.append((i + 4, j + k))
        return points

    def startWithText(self, text):
        position = (self.height // 4, self.width // 4)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 1
        world = cv2.putText(
            self.world,
            text,
            position,
            0,
            fontScale,
            color,
            thickness,
            cv2.LINE_AA)
        _, self.world = cv2.threshold(world, 127, 255, cv2.THRESH_BINARY)

        cv2.imshow(
            'Game of Life',
            cv2.resize(
                self.world,
                (self.width * self.__resizeFactor,
                 self.height * self.__resizeFactor),
                interpolation=cv2.INTER_AREA))
        cv2.waitKey(0)

    def setPoints(self, points):
        self.boundaries = [list(points[0]), list(points[0])]
        for i, j in points:
            self.world[i % self.height][j % self.width] = 255
            self.updateBoundaries(i, j)

    def updateBoundaries(self, i, j):
        # change boundaries
        if i <= self.boundaries[0][0]:
            self.boundaries[0][0] = i - 1
        elif i >= self.boundaries[1][0]:
            self.boundaries[1][0] = (i + 1) % self.width
        if j <= self.boundaries[0][1]:
            self.boundaries[0][1] = (j - 1) % self.height
        elif j >= self.boundaries[1][1]:
            self.boundaries[1][1] = j + 1

    def run(self):
        gen = 0
        preUpdateTime = time()
        while True:
            cv2.imshow(
                'Game of Life',
                cv2.resize(
                    self.world,
                    (self.width * self.__resizeFactor,
                     self.height * self.__resizeFactor),
                    interpolation=cv2.INTER_AREA))
            # cv2.waitKey(0)
            if cv2.waitKey(1) == ord('q'):
                break
            self.move()
            self.changeStates()
            gen += 1
            print('\r[*] Generation %d' % gen, end='')
            timeDiff = time() - preUpdateTime
            if timeDiff < self.frameUpdateGap:
                sleep(self.frameUpdateGap - timeDiff)
            if self.generationNumber is None:
                continue
            elif gen == self.generationNumber:
                break

    def move(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.doesChange(self.world, i, j):
                    self.newStates.append((i, j))
                    self.updateBoundaries(i, j)

    def changeStates(self):
        for i, j in self.newStates:
            if self.world[i % self.height][j % self.width] == 0:
                self.world[i % self.height][j % self.width] = 255
            else:
                self.world[i % self.height][j % self.width] = 0
        self.newStates = []

    def doesChange(self, world, i, j) -> bool:
        count = self.neighboursCount(world, i, j)
        if count == 2:
            return False
        if count == 3:
            return not world[i % self.height][j % self.width] == 255
        return not world[i % self.height][j % self.width] == 0

    def neighboursCount(self, world, i, j):
        count = 0
        count += 1 if world[i - 1][j - 1] else 0
        count += 1 if world[i - 1][j % self.width] else 0
        count += 1 if world[i - 1][(j + 1) % self.width] else 0
        count += 1 if world[i % self.height][j - 1] else 0
        count += 1 if world[i % self.height][(j + 1) % self.width] else 0
        count += 1 if world[(i + 1) % self.height][j - 1] else 0
        count += 1 if world[(i + 1) % self.height][j % self.width] else 0
        count += 1 if world[(i + 1) % self.height][(j + 1) % self.width] else 0
        return count


if __name__ == '__main__':
    game = GameOfLife(
        height=1024,
        width=2048)
    game.startWithText('Qifan Deng')
    # game.setPoints(game.examplePoints())
    game.run()
