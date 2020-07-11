

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import random

ACT_UP = 0
ACT_DOWN = 1
ACT_LEFT = 2
ACT_RIGHT = 3

class TripleEnv(gym.Env):

    def __init__(self):
        self.rowMax = 7
        self.columnMax = 7
        self.colourMax = 3
        self.colours = [[0 for i in range(self.rowMax)] for j in range(self.columnMax)]
        self.reset()
        self.score = 0
    

    def step(self, row, column, act):
        done = False
        if (self.CheckActionValid(row, column, act)):
            reward = 1
            colour = self.GetColour(row, column)
            targetRow = -1
            targetColumn = -1

            if act == ACT_UP:
                targetRow = row - 1
                targetColumn = column
            elif act == ACT_DOWN:
                targetRow = row + 1
                targetColumn = column
            elif act == ACT_LEFT:
                targetRow = row
                targetColumn = column - 1
            elif act == ACT_RIGHT:
                targetRow = row
                targetColumn = column + 1
            else:
                return False

            tarGetColour = self.GetColour(targetRow, targetColumn)
            self.SetColour(row, column, tarGetColour)
            self.SetColour(targetRow, targetColumn, colour)
            self.EnsureValid()

            self.score += 1
            if self.score >= 50:
                done = True
                self.score = 50
        else:
            reward = -1
        return self.colours, reward, done, {}

    def reset(self):
        self.ColourReset()
        self.EnsureValid()
        return self.colours

    def render(self):
        print("  ", end='')
        for k in range(0, self.columnMax):
            print(k, end='')
            print(" ", end='')
        
        for i in range(0, self.rowMax):
            print("\n")
            print(i, end='')
            print(" ", end='')
            for j in range(0, self.columnMax):
                colour = self.GetColour(i, j)
                if colour == 1:
                    s = "☆"
                elif colour == 2:
                    s = "○"
                elif colour == 3:
                    s = "□"
                elif colour == 4:
                    s = "△"
                elif colour == 5:
                    s = "●"
                else:
                    s = "X"
                print(s, end='')
        print("\n")



    def GetColour(self, row, column):
        if row < 0 or column <0 or row >= self.rowMax or column >= self.columnMax:
            return -1
        else:
         return self.colours[row][column]

    def SetColour(self, row, column, colour):
        if row < 0 or column <0 or row >= self.rowMax or column >= self.columnMax:     
            return -1
        else:
            self.colours[row][column] = colour
            return colour

    def CheckActionValid(self, row, column, act):
        colour = self.GetColour(row, column)
        if colour == -1:
            return True
        
        if (act == ACT_UP):
            # OOA
            # BBO
            row1 = row - 1
            column1 = column - 2
            column2 = column - 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

            # OAO
            # BOB
            row1 = row - 1
            column1 = column - 1
            column2 = column + 1           
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

            # AOO
            # OBB
            row1 = row - 1
            column1 = column + 1
            column2 = column + 2   
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

            # AOB
            # BOA
            # ABB
            # BOB
            row1 = row - 3
            row2 = row - 2
            column1 = column
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

        elif (act == ACT_DOWN):
            # BBO
            # OOA
            row1 = row + 1
            column1 = column - 1
            column2 = column - 2   
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

            # BOB
            # OAO
            row1 = row + 1
            column1 = column - 1
            column2 = column + 1   
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

            # OBB
            # AOO
            row1 = row + 1
            column1 = column + 2
            column2 = column + 1   
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

            # BOA
            # ABB
            # AOB
            # BOA
            row1 = row + 2
            row2 = row + 3
            column1 = column 
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

        elif (act == ACT_LEFT):
            # OB
            # OB
            # AO
            row1 = row - 1
            row2 = row - 2            
            column1 = column - 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

            # OB
            # AO
            # OB
            row1 = row - 1
            row2 = row + 1            
            column1 = column - 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

            # AO
            # OB
            # OB
            row1 = row + 1
            row2 = row + 2            
            column1 = column - 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

            # OOBO
            row1 = row      
            column1 = column - 3
            column2 = column - 2
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True

        elif (act == ACT_RIGHT):
            # BO
            # BO
            # OA
            row1 = row - 1
            row2 = row - 2            
            column1 = column + 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

            # BO
            # OA
            # BO
            row1 = row + 1
            row2 = row - 1            
            column1 = column + 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

            # OA
            # BO
            # BO
            row1 = row + 1
            row2 = row + 2            
            column1 = column + 1
            if (self.GetColour(row1, column1) == colour and self.GetColour(row2, column1) == colour):
                return True

            # OBOO
            row1 = row     
            column1 = column + 2
            column2 = column + 3
            if (self.GetColour(row1, column1) == colour and self.GetColour(row1, column2) == colour):
                return True
        else:
            return False


    def GetRandomColour(self):
        return random.randint(1, self.colourMax)


    def ColourReset(self):
        for i in range(0, self.rowMax):
            for j in range(0, self.columnMax):
                self.SetColour(i, j, self.GetRandomColour())


    # 直接暴力循环处理已经形成三连的元素(直接以每个元素为中心，判断四周即可)
    def ProcessTriple(self):
        # 保证不存在已经三连的元素
        find = True
        while find:
            find = False
            for i in range(0, self.rowMax):
                for j in range(0, self.columnMax):
                    colour = self.GetColour(i, j)
                    if self.GetColour(i - 1, j) == colour and self.GetColour(i + 1, j) == colour:
                        self.SetColour(i, j, self.GetRandomColour())
                        self.SetColour(i - 1, j, self.GetRandomColour())
                        self.SetColour(i + 1, j, self.GetRandomColour())
                        find = True
                    elif self.GetColour(i, j - 1) == colour and self.GetColour(i, j + 1) == colour:
                        self.SetColour(i, j, self.GetRandomColour())
                        self.SetColour(i, j - 1, self.GetRandomColour())
                        self.SetColour(i, j + 1, self.GetRandomColour())
                        find = True


    # 直接暴力循环检查是否有通过一步即可形成三连的地方
    def CheckTripleValid(self):
        for i in range(0, self.rowMax):
            for j in range(0, self.columnMax):
                for act in range(ACT_UP, ACT_RIGHT):
                    if self.CheckActionValid(i, j, act):
                        return True
        return False


    # 形成既没有已经三连的情况，又有单步可消除的环境
    def EnsureValid(self):
        while True:
            self.ProcessTriple()
            if not self.CheckTripleValid():
                self.ColourReset()
            else:
                break


