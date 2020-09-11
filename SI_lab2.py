import random
from math import sqrt
from matplotlib import pyplot as plt
from operator import itemgetter, attrgetter, methodcaller

class Point:
    def __init__(self, id, x, y, d, c):
        self.id = id
        self.X = x
        self.Y = y
        self.d = d
        self.c = c


class Class:
    def __init__(self, id):
        self.id = id
        self.mas = []



def min_k(mas,ch):
    x = []
    if ch == 0:
        for i in mas:
            x.append(i.X)
    elif ch == 1:
        for i in mas:
            x.append(i.Y)
    return min(x)

def max_k(mas,ch):
    x = []
    if ch == 0:
        for i in mas:
            x.append(i.X)
    elif ch == 1:
        for i in mas:
            x.append(i.Y)
    return max(x)


def normir(arr):
    for i in arr:
        i.X = (i.X - 0.01) / (1 - 0.01)
        i.Y = (i.Y - 1) / (300 - 1)



def evklid(center, point):
    d = sqrt((center.X - point.X) ** 2 + (center.Y - point.Y) ** 2)
    return d


def manhattan(center, point):
    d = abs((center.X - point.X)) + abs((center.Y - point.Y))
    return d

def printPoints(class1, class2, class3):
    Xl = []
    Yl = []
    XK = []
    YK = []
    Xm = []
    Ym = []
    for i in class1:
        Xl.append(i.X)
        Yl.append(i.Y)
    for i in class2:
        XK.append(i.X)
        YK.append(i.Y)
    for i in class3:
        Xm.append(i.X)
        Ym.append(i.Y)
    plt.scatter(Xl, Yl, color='red')
    plt.scatter(XK, YK, color='green')
    plt.scatter(Xm, Ym, color='blue')
    plt.show()

n = 10
classes = [Class(1), Class(2), Class(3)]
mas = [];
k = 0
for i in range(n):
    x = Point(k, random.uniform(0.01,0.4), random.randrange(1,100,1), 0, 1)
    k = k + 1
    classes[0].mas.append(x)
    mas.append(x)
for i in range(n):
    x = Point(k, random.uniform(0.4,0.8), random.randrange(100,210,1), 0, 2)
    k = k + 1
    classes[1].mas.append(x)
    mas.append(x)
for i in range(n):
    x = Point(k, random.uniform(0.7,1.0), random.randrange(210,301,1), 0, 3)
    k = k + 1
    classes[2].mas.append(x)
    mas.append(x)

normir(classes[0].mas)
normir(classes[1].mas)
normir(classes[2].mas)

printPoints(classes[0].mas, classes[1].mas, classes[2].mas)
newPoint = Point(31, random.uniform(0, 1.0), random.uniform(0, 1.0), 0, 0)
plt.scatter(newPoint.X, newPoint.Y, color='black')
printPoints(classes[0].mas, classes[1].mas, classes[2].mas)

for i in mas:
    i.d = manhattan(newPoint, i)

N = len(mas)

for i in range(N-1):
    for j in range(N-i-1):
        if mas[j].d > mas[j+1].d:
            mas[j], mas[j+1] = mas[j+1], mas[j]


for i in range(N):
    print(mas[i].id, " d = ", mas[i].d, " Класс: ", mas[i].c)

result = [0,0,0]
t = 30
for i in range(t):
    if mas[i].c == 1:
        result[0] += 1/(mas[i].d ** 2)
    if mas[i].c == 2:
        result[1] += 1/(mas[i].d ** 2)
    if mas[i].c == 3:
        result[2] += 1/(mas[i].d ** 2)

res = result.index(max(result))
print("Итоговые оценки: Класс 1:", result[0], " Класс 2:", result[1], "Класс 3:",result[2])
print("Точка относиться к классу номер: ", res+1)
newPoint.c = res + 1
classes[res].mas.append(newPoint)
printPoints(classes[0].mas, classes[1].mas, classes[2].mas)










