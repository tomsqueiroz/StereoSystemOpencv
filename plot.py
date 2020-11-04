import matplotlib.pyplot as plt
import json
import numpy as np

with open('output.json', 'r') as file:

	data = json.load(file)
	data = json.loads(data)

for elem, i in zip(data, range(len(data))):

	if elem == [[-1], [-1], [-1]]:

		print(f"{i}: miss")

xCoord = []
yCoord = []
zCoord = []

for elem in data:

	xCoord.append(elem[0][0])
	yCoord.append(elem[1][0])
	zCoord.append(elem[2][0])

time = range(0, 19)
plt.plot(time, xCoord, 'ro', label='X')
plt.plot(time, yCoord, 'bo', label='Y')
plt.plot(time, zCoord, 'go', label='Z')
plt.title('Rastreamento de coordenadas')
plt.axis([0, 18, 0, 4])
plt.ylabel('Position')
plt.xlabel('Time (s)')
plt.legend(loc="upper left")
plt.show()