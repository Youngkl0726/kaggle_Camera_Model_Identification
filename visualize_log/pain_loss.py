#coding:utf-8
import matplotlib.pyplot as plt

def loadData(flieName):
    inFile = open(flieName, 'r')#以只读方式打开某fileName文件  

    #定义两个空list，用来存放文件中的数据  
    X = []
    y = []
    index = 0
    for line in inFile:
        trainingSet = line.split() #对于每一行，按''把数据分开，这里是分成两部分 
        index = index + 1 
        if index % 2 == 0:  
            X.append(trainingSet[0]) #第一部分，即文件中的第一列数据逐一添加到list X 中  
            y.append(trainingSet[2]) #第二部分，即文件中的第二列数据逐一添加到list y 中  
    return (X, y)    # X,y组成一个元组，这样可以通过函数一次性返回  

def plotData(X, y):  
    length = len(y)  
    #pylab.figure(1)  
  
    plt.plot(X, y, label='loss',linewidth=1)  
    plt.xlabel('Iters')  
    plt.ylabel('TrainingLoss')  
    plt.title('Loss') 
    plt.legend() 
    plt.show()#让绘制的图像在屏幕上显示出来  
if __name__=="__main__":
    (X,y) = loadData('./inception_v4.log.train')
    plotData(X,y)
