rooms=[0]*4
n=4
for i in range (n):
  x=int(input("Room "+str(i) +" (Ënter 1 for dirty and 0 for clean): "))
  rooms[i]=x
initial=int(input("Ënter the room the vacuum cleaner is in (0-3): "))
while True:
  action=int(input("Enter 0 for cleaning , 1 for moving left, 2 for moving right: "))
  if action==0:
    rooms[initial]=0
    print("Cleaning the dust in " + str(initial))
    print(rooms)
  elif action==1:
    initial=initial-1
    if initial==-1:
      initial=initial+1
    print("At room " + str(initial))
    print(rooms)
  elif action==2:
    initial=initial+1
    if initial==4:
      initial=initial-1
    print("At room " + str(initial))
    print(rooms)
  else:
    print("Invalid input")

  if sum(rooms)==0:
    print("All rooms are clean")
    break
