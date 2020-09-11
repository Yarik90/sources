import random
from math import sqrt
from matplotlib import pyplot as plt

class Point:
    def __init__(self, id, x, y, z):
        self.id = id
        self.X = x
        self.Y = y
        self.Z = z


class Cluster:
    def __init__(self, id, center):
        self.id = id
        self.center = center
        self.cluster = []
    def show(self):
        print("Центр кластера номер:", self.id, ": X = ", self.center.X, " Y = ", self.center.Y, " Z = ", self.center.Z)


def city(t):
    if t == 0:
        return "Samara"
    else:
        if t == 1:
            return "Togliatti"
        else:
            if t == 2:
                return "Chapaevsk"

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
    min_x = min_k(arr,0)
    min_y = min_k(arr,1)
    max_x = max_k(arr, 0)
    max_y = max_k(arr, 1)
    for i in arr:
        i.X = (i.X - min_x) / (max_x - min_x)
        i.Y = (i.Y - min_y) / (max_y - min_y)

def different(string1, string2):
    if string1 == string2:
        return 0
    else:
        return 1


def evklid(center, point):
    d = sqrt((center.X - point.X) ** 2 + (center.Y - point.Y) ** 2 + (different(center.Z, point.Z)) ** 2)
    return d


def manhattan(center, point):
    d = abs((center.X - point.X)) + abs((center.Y - point.Y)) + abs(different(center.Z, point.Z))
    return d

def frequency(arr):
    freq = [0, 0, 0]
    for i in arr:
        if i.Z == "Samara":
            freq[0] += 1
        elif i.Z == "Togliatti":
            freq[1] += 1
        elif i.Z == "Chapaevsk":
            freq[2] += 1
    return city(freq.index(max(freq)))


mas = []
for i in range(16):
    x = Point(i, random.uniform(0.01,0.5), random.randrange(1,300,1), city(0))
    mas.append(x)
for i in range(16,32,1):
    x = Point(i, random.uniform(0.4,1), random.randrange(1,300,1), city(1))
    mas.append(x)
for i in range(32,50,1):
    x = Point(i, random.uniform(0.7,1.0), random.randrange(1,300,1), city(2))
    mas.append(x)

normir(mas)

clusters = [Cluster(1,Point(111,0.8,0.2,"Samara")), Cluster(2,Point(112,0.1,0.5,"Togliatti")), Cluster(3,Point(111,0.5,0.9,"Chapaevsk"))]

print("Начальные точки:")
print("Центр кластера номер: 1 ", ": X = ", clusters[0].center.X, " Y = ", clusters[0].center.Y, " Z = ", clusters[0].center.Z)
print("Центр кластера номер: 2 ", ": X = ", clusters[1].center.X, " Y = ", clusters[1].center.Y, " Z = ", clusters[1].center.Z)
print("Центр кластера номер: 3 ", ": X = ", clusters[2].center.X, " Y = ", clusters[2].center.Y, " Z = ", clusters[2].center.Z)

plt.scatter(clusters[0].center.X, clusters[0].center.Y, color='red', marker = "*")
plt.scatter(clusters[1].center.X, clusters[1].center.Y, color='green', marker = "*")
plt.scatter(clusters[2].center.X, clusters[2].center.Y, color='blue', marker = "*")
X = [];
Y = [];
for i in mas:
    X.append(i.X)
    Y.append(i.Y)
plt.scatter(X, Y, color='black')
plt.show()
sum_quad_errors = 0.0
k = 0
while True:
    sum = 0

    for i in range(50):
        d1 = evklid(clusters[0].center, mas[i])
        d2 = evklid(clusters[1].center, mas[i])
        d3 = evklid(clusters[2].center, mas[i])
        if d1 < d2 and d1 < d3:
            clusters[0].cluster.append(mas[i])
            sum += d1 ** 2
        if d2 < d1 and d2 < d3:
            clusters[1].cluster.append(mas[i])
            sum += d2 ** 2
        if d3 < d1 and d3 < d2:
            clusters[2].cluster.append(mas[i])
            sum += d3 ** 2

    clusters[0].center.X = 0.0
    clusters[1].center.X = 0.0
    clusters[2].center.X = 0.0
    clusters[0].center.Y = 0.0
    clusters[1].center.Y = 0.0
    clusters[2].center.Y = 0.0

    for i in clusters[0].cluster:
        clusters[0].center.X += i.X
        clusters[0].center.Y += i.Y
    clusters[0].center.X /= len(clusters[0].cluster)
    clusters[0].center.Y /= len(clusters[0].cluster)
    clusters[0].center.Z = frequency(clusters[0].cluster)

    for i in clusters[1].cluster:
        clusters[1].center.X += i.X
        clusters[1].center.Y += i.Y
    clusters[1].center.X /= len(clusters[1].cluster)
    clusters[1].center.Y /= len(clusters[1].cluster)
    clusters[1].center.Z = frequency(clusters[1].cluster)

    for i in clusters[2].cluster:
        clusters[2].center.X += i.X
        clusters[2].center.Y += i.Y
    clusters[2].center.X /= len(clusters[2].cluster)
    clusters[2].center.Y /= len(clusters[2].cluster)
    clusters[2].center.Z = frequency(clusters[2].cluster)

    if k == 0:
        sum_quad_errors = sum+1

    k = k + 1
    print("Шаг номер: ", k)
    clusters[0].show()
    clusters[1].show()
    clusters[2].show()
    print("Сумма квадратичных ошибок: ", sum)
    Xl = []
    Yl = []
    XK = []
    YK = []
    Xm = []
    Ym = []
    for i in clusters[0].cluster:
        Xl.append(i.X)
        Yl.append(i.Y)
    for i in clusters[1].cluster:
        XK.append(i.X)
        YK.append(i.Y)
    for i in clusters[2].cluster:
        Xm.append(i.X)
        Ym.append(i.Y)
    plt.scatter(Xl, Yl, color='red')
    plt.scatter(XK, YK, color='green')
    plt.scatter(Xm, Ym, color='blue')
    plt.scatter(clusters[0].center.X, clusters[0].center.Y, color='red', marker = "*")
    plt.scatter(clusters[1].center.X, clusters[1].center.Y, color='green', marker = "*")
    plt.scatter(clusters[2].center.X, clusters[2].center.Y, color='blue', marker = "*")
    plt.show()

    if sum < sum_quad_errors:
        sum_quad_errors = sum
    else:
        break

    clusters[0].cluster = []
    clusters[1].cluster = []
    clusters[2].cluster = []


clusters = [Cluster(1,Point(111,0.8,0.2,"Samara")), Cluster(2,Point(112,0.1,0.5,"Togliatti")), Cluster(3,Point(111,0.5,0.9,"Chapaevsk"))]

print("Начальные точки:")
print("Центр кластера номер: 1 ", ": X = ", clusters[0].center.X, " Y = ", clusters[0].center.Y, " Z = ", clusters[0].center.Z)
print("Центр кластера номер: 2 ", ": X = ", clusters[1].center.X, " Y = ", clusters[1].center.Y, " Z = ", clusters[1].center.Z)
print("Центр кластера номер: 3 ", ": X = ", clusters[2].center.X, " Y = ", clusters[2].center.Y, " Z = ", clusters[2].center.Z)

plt.scatter(clusters[0].center.X, clusters[0].center.Y, color='red', marker = "*")
plt.scatter(clusters[1].center.X, clusters[1].center.Y, color='green', marker = "*")
plt.scatter(clusters[2].center.X, clusters[2].center.Y, color='blue', marker = "*")
X = [];
Y = [];
for i in mas:
    X.append(i.X)
    Y.append(i.Y)
plt.scatter(X, Y, color='black')
plt.show()
sum_quad_errors = 0.0
k = 0
while True:
    sum = 0

    for i in range(50):
        d1 = manhattan(clusters[0].center, mas[i])
        d2 = manhattan(clusters[1].center, mas[i])
        d3 = manhattan(clusters[2].center, mas[i])
        if d1 < d2 and d1 < d3:
            clusters[0].cluster.append(mas[i])
            sum += d1 ** 2
        if d2 < d1 and d2 < d3:
            clusters[1].cluster.append(mas[i])
            sum += d2 ** 2
        if d3 < d1 and d3 < d2:
            clusters[2].cluster.append(mas[i])
            sum += d3 ** 2

    clusters[0].center.X = 0.0
    clusters[1].center.X = 0.0
    clusters[2].center.X = 0.0
    clusters[0].center.Y = 0.0
    clusters[1].center.Y = 0.0
    clusters[2].center.Y = 0.0

    for i in clusters[0].cluster:
        clusters[0].center.X += i.X
        clusters[0].center.Y += i.Y
    clusters[0].center.X /= len(clusters[0].cluster)
    clusters[0].center.Y /= len(clusters[0].cluster)
    clusters[0].center.Z = frequency(clusters[0].cluster)

    for i in clusters[1].cluster:
        clusters[1].center.X += i.X
        clusters[1].center.Y += i.Y
    clusters[1].center.X /= len(clusters[1].cluster)
    clusters[1].center.Y /= len(clusters[1].cluster)
    clusters[1].center.Z = frequency(clusters[1].cluster)

    for i in clusters[2].cluster:
        clusters[2].center.X += i.X
        clusters[2].center.Y += i.Y
    clusters[2].center.X /= len(clusters[2].cluster)
    clusters[2].center.Y /= len(clusters[2].cluster)
    clusters[2].center.Z = frequency(clusters[2].cluster)

    if k == 0:
        sum_quad_errors = sum+1

    k = k + 1
    print("Шаг номер: ", k)
    clusters[0].show()
    clusters[1].show()
    clusters[2].show()
    print("Сумма квадратичных ошибок: ", sum)
    Xl = []
    Yl = []
    XK = []
    YK = []
    Xm = []
    Ym = []
    for i in clusters[0].cluster:
        Xl.append(i.X)
        Yl.append(i.Y)
    for i in clusters[1].cluster:
        XK.append(i.X)
        YK.append(i.Y)
    for i in clusters[2].cluster:
        Xm.append(i.X)
        Ym.append(i.Y)
    plt.scatter(Xl, Yl, color='red')
    plt.scatter(XK, YK, color='green')
    plt.scatter(Xm, Ym, color='blue')
    plt.scatter(clusters[0].center.X, clusters[0].center.Y, color='red', marker = "*")
    plt.scatter(clusters[1].center.X, clusters[1].center.Y, color='green', marker = "*")
    plt.scatter(clusters[2].center.X, clusters[2].center.Y, color='blue', marker = "*")
    plt.show()

    if sum < sum_quad_errors:
        sum_quad_errors = sum
    else:
        break

    clusters[0].cluster = []
    clusters[1].cluster = []
    clusters[2].cluster = []




