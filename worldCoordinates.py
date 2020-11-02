import numpy as np
import cv2
import json

def readIntrinsics(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["cameraMatrix1"]), np.array(data["cameraMatrix2"])

def readExtrinsics(file):

	with open(file, 'r') as file:

		data = json.load(file)
		data = json.loads(data)

	return np.array(data["tVecs1"]), np.array(data["rotMatrix1"]), \
		   np.array(data["tVecs2"]), np.array(data["rotMatrix2"])

def getWorldCoordinates(coord1, coord2):

	projMatrix1 = computeProjMatrix(mtx1, rotMatrix1, tVecs1)
	projMatrix2 = computeProjMatrix(mtx2, rotMatrix2, tVecs2)

	coordinates = cv2.triangulatePoints(projMatrix1, projMatrix2, coord1, coord2)

	return np.array((coordinates[i]/coordinates[3] for i in range(3)))

def computeProjMatrix(mtx, rotMatrix, tVecs):

	aux = np.concatenate((rotMatrix, tVecs), axis=1)

	return np.matmul(mtx, aux)

'''
O script que determina as coordenadas de mundo deve receber os
vetores dos trackers para ambas as câmeras. Esses terão, nece-
ssariamente, o mesmo número de valores. A função do tracker de-
ve rodar a rotina de sincronizar as câmeras e retornar vetores
sincronizados, logo, com o mesmo comprimento.
'''
def adjustArrays(array1, array2):

	output = []

	for i in range(len(array1)):

		if array1[i] == (-1, -1) or array2[i] == (-1, -1):

			output[i] = (-1, -1, -1)

		else:

			output[i] = getWorldCoordinates(array1[i], array2[i])

	return output

if __name__ == "__main__":

'''
Pra facilitar a declaracao e chamada de funções, removi variáveis
 que não estavam sendo usadas como rVecs, camPos e dist.
'''
	global mtx1
	global mtx2
	global tVecs1
	global tVecs2
	global rotMatrix1
	global rotMatrix2

	mtx1, mtx2 = readIntrinsics('intrinsicsCalibration.json')
	tVecs1, rotMatrix1, tVecs2, rotMatrix2 = readExtrinsics('extrinsicsCalibration.json')
	#arrayCam1, arrayCam2 = readTrackedArrays()

	coord = getWorldCoordinates(arrayCam1, arrayCam2)

	print(f"\n{coord}")