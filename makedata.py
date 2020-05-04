import os
from graph import TimeFPS, keyTime
import numpy as np

def labelDic():
    labeldic = {}
    labeldic['00'] = 0 
    labeldic['01'] = 1 
    labeldic['02'] = 2 
    labeldic['03'] = 3 
    labeldic['10'] = 4 
    labeldic['11'] = 5 
    labeldic['12'] = 6 
    labeldic['13'] = 7 
    labeldic['20'] = 8 
    labeldic['21'] = 9 
    labeldic['22'] = 10 
    labeldic['23'] = 11
    labeldic['30'] = 12
    labeldic['31'] = 13 
    labeldic['32'] = 14
    labeldic['33'] = 15


def makedata(folder):
    files = os.listdir(folder)

    for file in files:
        if file.endswith('_.txt'):
            TimeFPSFile = os.path.join(folder, file)
        else:
            keyTimeFile = os.path.join(folder, file)

    timeArray, speed, codelen, codeArray = keyTime(keyTimeFile)
    time, FPS = TimeFPS(TimeFPSFile, timeArray[0]-500, timeArray[-1]+500)
    a = np.array(FPS)
    b = np.average(a)
    print(b)
    c = np.min(a)
    print(c)

    for i in range(0,len(timeArray)-1):
        sample = []
        for time in range(timeArray[i], timeArray[i+1], 2):
            
            sample.append(FPS[i])
    

    label = []



if __name__ == '__main__':
    makedata('1000data')
