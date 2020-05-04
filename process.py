import sys
from graph import keyTime
from graph import TimeFPS

def train():
    timeArray, speed, codelen, codeArray = keyTime(sys.argv[2])
    time, FPS = TimeFPS(sys.argv[1], timeArray[0], timeArray[-1] + 200)
    sampleFPS = []
    j = 0
    for i in range(0, codelen-1):
        FPSsum = 0
        while  time[j] in range(timeArray[i], timeArray[i+1]):
            FPSsum += FPS[j]
            j+=1
        sampleFPS.append(FPSsum)
    FPSsum = 0
    while j<len(time) and time[j] in range(timeArray[codelen-1], timeArray[codelen-1]+200):
        FPSsum += FPS[j]
        j+=1
    sampleFPS.append(FPSsum)
    for i in range(0, codelen):
        print(codeArray[i])
        print(sampleFPS[i])
    return sampleFPS
        

if __name__ == '__main__':
    train()