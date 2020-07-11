
from tripleGame import TripleGame

game = TripleGame(True, 7, 7, 4)
game.Start()

while True:
  print("enter: 'rowIndex columnIndex act' (act: up=0, down=1, left=2, right=3)")
  row, column, act = input()
  game.DoAction(row, column, act)


