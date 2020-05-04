import matplotlib.pyplot as plt
# import urllib
import sys
import os
import time  # 引入time模块
import numpy as np
from sklearn.cluster import KMeans



ticks = time.time()
SPEED = 100
TEST = 1

def keyTime(filename):
    timeArray = []
    f = open(filename,'r')
    contents =f.read()

    content = contents.split('$')
    times = content[0]
    speed = content[1]
    codelen = int(content[2])
    code = content[3]
    # sentence = sentences.split(',')
    timeArray = times.split(',')
    for i in range(len(timeArray)):
        timeArray[i] = int(timeArray[i])
    codeArray = code.split(',')
    for i in range(len(codeArray)):
        codeArray[i] = int(codeArray[i])
    f.close()
    return timeArray, speed, codelen, codeArray

def TimeFPS(filename, startTime, stopTime):
    time = []
    FPS = []
    ### get Time-FPS file
    f = open(filename,'r')
    content =f.read()
    contents = content.split(',')
    for index in range(int(len(contents)/2)):
        tmp = contents[index*2]
        tmpTime = int(tmp)
        if(tmpTime in range(startTime, stopTime)):
            time.append(tmpTime)
            tmp = contents[index*2+1]
            i = float(tmp)
            FPS.append(i)
    f.close() 
    return time, FPS


def draw(predict):
    fig= plt.figure(figsize=(40,6))

    axes= fig.add_axes([0.1,0.1,0.8,0.8], ylabel='m sec', xlabel='time')
    axes.grid(True)
    # plt.ylim(0,60)
    
    timeArray, speed, codelen, codeArray = keyTime(sys.argv[2])
    axes.set_title('refresh speed:'+ speed + ' ms per time')
    for i in range(0,len(timeArray)):
        axes.axvline(timeArray[i], c = 'red')
        # axes.hlines(y=predict[i], xmin=timeArray[i], xmax=timeArray[i]+SPEED, color = 'red')
        axes.text(timeArray[i], 30, codeArray[i])

    time, FPS = TimeFPS(sys.argv[1], timeArray[0]-500, timeArray[-1]+500)
    axes.plot(time, FPS, color='blue', linestyle='solid')
    
    saveName = os.path.join('images', speed+'_'+ str(ticks)+'.png')
    plt.savefig(saveName)

    plt.show()

def Loss(predict, codelen, codeArray):
    codeArray = codeArray[0:codelen]
    d = np.argwhere(codeArray!=predict)
    # print('d',d)
    loss = len(d)
    lossrate = loss/codelen
    return loss, lossrate

def KmeansPred(sampleFPS, codelen):
    sampleFPS = sampleFPS[0:codelen]
    a = np.average(sampleFPS)
    b = np.min(sampleFPS)
    c = np.max(sampleFPS)
    d = np.median(sampleFPS)
    print(a,b,c, d)


    ksampleFPS = np.zeros([codelen,2])
    for i in range(0, codelen):
        ksampleFPS[i][0] = 0
        ksampleFPS[i][1] = sampleFPS[i] 
    clf=KMeans(n_clusters=2)
    clfa=clf.fit(ksampleFPS)
    predict = clfa.labels_
    return predict

def biPred(sampleFPS, codelen, threshold):
    sampleFPS = sampleFPS[0:codelen]
    predict = np.zeros(codelen)
    for i in range(0, codelen):
        if sampleFPS[i]>threshold:
            predict[i] = 1
        else:
            predict[i] = 0
    return predict

def sampleAverage(timeArray, time, FPS, codelen):
    averageFPS = np.zeros(codelen)
    j = 0
    for i in range(0, codelen-1):
        FPSsum = 0
        count = 0
        while  time[j] in range(timeArray[i], timeArray[i+1]):
            FPSsum += FPS[j]
            j+=1
            count+=1
        if count==0:
            averageFPS[i] = 0
        else:
            averageFPS[i] = (FPSsum/count)
    FPSsum = 0
    count = 0
    while  j<len(time) and time[j] in range(timeArray[codelen-1], timeArray[codelen-1]+SPEED):
        FPSsum += FPS[j]
        j+=1
        count+=1
        if count==0:
            averageFPS[codelen-1] = 0
        else:
            averageFPS[codelen-1] = (FPSsum/count)
    return averageFPS

def samplesAverage(timeArray, time, FPS, codelen):
    averageFPS = np.zeros(codelen)
    j = 0
    for i in range(0, codelen):
        FPSsum = 0
        count = 0
        while  time[j] in range(timeArray[i]-50, timeArray[i]+50):
            FPSsum += FPS[j]
            j+=1
            count+=1
        if count==0:
            averageFPS[i] = 0
        else:
            averageFPS[i] = (FPSsum/count)
    return averageFPS

def samplePeak(timeArray, time, FPS, codelen):
    peakFPS = np.zeros(codelen)
    j = 0
    for i in range(0, codelen-1):
        FPSsum = 0
        count = 0
        while  time[j] in range(timeArray[i], timeArray[i+1]):
            FPSsum += FPS[j]
            if (FPS[j]>peakFPS[i]):
                peakFPS[i] = FPS[j]
            j+=1
            count+=1
    while  j<len(time) and time[j] in range(timeArray[codelen-1], timeArray[codelen-1]+SPEED):
        if (FPS[j]>peakFPS[codelen-1]):
            peakFPS[codelen-1] = FPS[j]
        j=+1
    return peakFPS

def getrealcode(codeArray, codelen):
    realcodeArray = []
    realcodeArray.append(codeArray[0])
    for i in range(1, codelen):
        realcodeArray.append(abs(codeArray[i] - codeArray[i-1]))
    return realcodeArray

def thres(codelen, sampleFPS, realcodeArray):
    threshold = 0
    minloss = 1000
    bestpredict = np.zeros(codelen)
    bestthreshold = 0
    MAXLOSS = 1000
    sortaverageFPS = np.sort(sampleFPS)
    for i in range(0, codelen):
        predict = biPred(sampleFPS, codelen, threshold)
        loss, lossrate = Loss(predict, codelen, realcodeArray)
        if loss<minloss:
            minloss = loss
            bestpredict = predict
            bestthreshold= threshold
        threshold = sortaverageFPS[i]
    lossrate = minloss/codelen
    return bestthreshold, minloss, lossrate


def train():
    timeArray, speed, codelen, codeArray = keyTime(sys.argv[2])
    time, FPS = TimeFPS(sys.argv[1], timeArray[0], timeArray[-1] + SPEED)

    realcodeArray = getrealcode(codeArray, codelen)

    averageFPS = sampleAverage(timeArray, time, FPS, codelen)
    predict = KmeansPred(averageFPS, codelen)
    loss, lossrate = Loss(predict, codelen, realcodeArray)
    print('loss1:', loss)
    print('lossrate', lossrate)

    bestthreshold, minloss, lossrate = thres(codelen, averageFPS, realcodeArray)
    print('bestthreshold:', bestthreshold)
    print('threshold loss:', minloss)
    print('lossrate', lossrate)

    peakFPS = samplePeak(timeArray, time, FPS, codelen)
    predict2 = KmeansPred(peakFPS, codelen)
    loss2, lossrate = Loss(predict2, codelen, realcodeArray)
    print('loss2:',loss2)
    print('lossrate', lossrate)

    bestthreshold, minloss, lossrate = thres(codelen, peakFPS, realcodeArray)
    print('bestthreshold:', bestthreshold)
    print('threshold loss:', minloss)
    print('lossrate', lossrate)

    predict3 = biPred(peakFPS, codelen, np.median(peakFPS))
    loss3, lossrate = Loss(predict3, codelen, realcodeArray)
    print('loss2:',loss3)
    print('lossrate', lossrate)


    # plt.plot(timeArray, averageFPS)
    # plt.plot(timeArray, peakFPS)
    # plt.show()
    return predict2

if __name__ == '__main__':
    predict = train()
    # draw(predict)






