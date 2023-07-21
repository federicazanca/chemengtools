def bandgap(filename):
    file = open(filename,"r")
    dataReps = []
    while True:
	line = file.readline()
        if "CAR" in line:
            file.readline()
            [_, reps, rows] = list(map(int, file.readline().split()))
            for i in range(reps):
                file.readline()
                file.readline()
                dataRep = []
                for j in range(rows):
                    dataRep.append(list(map(float, file.readline().split())))
                dataReps.append(dataRep)
            break
    file.close()

    colNum = 1 if len(dataReps[0][0]) == 3 else 2
    colOneFlag = 3 if colNum == 2 else 2

    spinupBG = 9999999999
    spindownBG = 9999999999
    for i in range(reps):
        for j in range(rows):
            if dataReps[i][j][colOneFlag] < 0.5:
                diff = dataReps[i][j][1] - dataReps[i][j-1][1]	
		#print("sp up")
		#print("bands "+str(dataReps[i][j][0]) + "     " + str(dataReps[i][j-1][0]))
		#print("value " +str(dataReps[i][j][3]) + "     " + str(dataReps[i][j-1][3]))
		#print(diff)
                if diff < spinupBG:
                    spinupBG = diff
                break
        if colNum == 2:
            for j in range(rows):
                if dataReps[i][j][4] < 0.5:
                    diff = dataReps[i][j][2] - dataReps[i][j-1][2]
		    #print("sp dw")
		    #print("bands "+str(dataReps[i][j][0]) + "     " + str(dataReps[i][j-1][0]))
		    #print("value "+str(dataReps[i][j][4]) + "     " + str(dataReps[i][j-1][4]))
		    #print(diff)
                    if diff < spindownBG:
                        spindownBG = diff
                    break
    result = [spinupBG]
    if colNum == 2:
        result.append(spindownBG)
    return result
                
            
