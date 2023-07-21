def bandgap(filename):
    #filename was the output file from the calculation
    file = open(filename,"r")
    dataReps = []
    while True:
        #the following lines are specific to vasp. 
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

    #eigenval what column is it? 
    colNum = ...
    #occupation what column is it?
    colOneFlag = ...

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
                
            
