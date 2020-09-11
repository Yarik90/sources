import random
import math
import copy
import itertools
import numpy


class Record:
    def __init__(self, p1, p2, y):
        self.p1 = p1
        self.p2 = p2
        self.y = y


    def show(self,tab):
        print(tab, "p1 = ", self.p1, " p2 = ", self.p2, " y = ", self.y)


class Tree:
    def __init__(self, records, atrl, atrr, atr, atr_name):
        self.left = None
        self.right = None
        self.records = records
        self.atr_name = atr_name
        self.atr = atr
        self.atrl = atrl
        self.atrr = atrr
        #self.rule = rule
        self.notsplit = []

    def showt(self, tab):
        for i in self.records:
            i.show(tab)




def f_error(t1, t2):
    if len(t1) == 0 or len(t2) == 0:
        return 1000
    sumt1 = 0
    for i in t1:
        sumt1 += i.y
    f1 = (1/len(t1))*sumt1
    sumt2 = 0
    for i in t2:
        sumt2 += i.y
    f2 = 1 / len(t2) * sumt2
    sum_er1 = 0
    for i in t1:
        sum_er1 += (i.y - f1)**2
    sum_er2 = 0
    for i in t2:
        sum_er2 += (i.y - f2) ** 2
    er = sum_er1 + sum_er2
    return er


def leaf(records):
    if len(records) == 1:
        return 1
    else:
        return 0


def tabulator(level):
    tab = ""
    for i in range(level):
        tab += "\t\t"
    return tab


def cart_reg(unit,level):
    uniqp1 = []
    uniqp2 = []
    left = []
    right = []
    atrleft = ""
    atrright = ""
    atr = 0
    atr_name = ""
    for i in unit.records:
        uniqp1.append(i.p1)
        uniqp2.append(i.p2)
    nset1 = set(uniqp1)
    nset2 = set(uniqp2)
    uniqp1 = list(nset1)
    uniqp2 = list(nset2)
    uniqp1.sort()
    uniqp2.sort()
    uniqp1.remove(max(uniqp1))
    uniqp2.remove(max(uniqp2))
    error = 1000
    for k in uniqp1:
        if ("p1 <= " + str(k)) in unit.notsplit:
            continue
        n_left = [x for x in unit.records if x.p1 <= k]
        n_right = [x for x in unit.records if x.p1 > k]
        n_error = f_error(n_left, n_right)
        if n_error < error:
            error = n_error
            left = n_left
            right = n_right
            atr = k
            atr_name = "p1"
            atrleft = "p1 <= " + str(k)
            atrright = "p1 > " + str(k)
    for k in uniqp2:
        if ("p2 <= " + str(k)) in unit.notsplit:
            continue
        n_left = [x for x in unit.records if x.p2 <= k]
        n_right = [x for x in unit.records if x.p2 > k]
        n_error = f_error(n_left, n_right)
        if n_error < error:
            error = n_error
            left = n_left
            right = n_right
            atr = k
            atr_name = "p2"
            atrleft = "p2 <= " + str(k)
            atrright = "p2 > " + str(k)
    unit.left = Tree(left, 0, 0, 0, "")
    unit.right = Tree(right, 0, 0, 0, "")
    unit.atrl = atrleft
    unit.atrr = atrright
    unit.atr = atr
    unit.atr_name = atr_name
    unit.notsplit.append(atrleft)
    unit.left.notsplit = copy.copy(unit.notsplit)
    unit.right.notsplit = copy.copy(unit.notsplit)
    tab = tabulator(level + 1)
    if leaf(unit.left.records) == 1:
        print(tab,unit.atrl)
        print(tab, "Лист:")
        unit.left.showt(tab)
    else:
        print(tab, unit.atrl)
        unit.left.showt(tab)
        cart_reg(unit.left, level + 1)

    if leaf(unit.right.records) == 1:
        print(tab,unit.atrr)
        print(tab, "Лист:")
        unit.right.showt(tab)
    else:
        print(tab, unit.atrr)
        unit.right.showt(tab)
        cart_reg(unit.right, level + 1)

    return 0

res = 0
def model(treet, record):
    if treet.atr_name == "p1":
        if record.p1 <= treet.atr:
            model(treet.left, record)
        else:
            model(treet.right, record)
    elif treet.atr_name == "p2":
        if record.p2 <= treet.atr:
            model(treet.left, record)
        else:
            model(treet.right, record)
    else:
        global res
        res = treet.records[0].y
        return res
    return  res

def func(p1, p2):
    return (p1/1.3 + 1)**2 + p2**2


def sett(records):
    for i in range(-2,3):
        for j in range(-1,-6,-1):
            records.append(Record(i, j, func(i,j)))


def sett_test(records):
    ii = 0
    j = -3
    while j > -5.5:
        records.append(Record(ii, j, func(ii,j)))
        j -= 0.5
    ii = 0.5
    j = -3
    while j > -3.8:
        records.append(Record(ii, j, func(ii,j)))
        j -= 0.4
    ii = 2
    j = -3
    while j > -5:
        records.append(Record(ii, j, func(ii, j)))
        j -= 0.3


def mse(a, p):
    sum = 0
    for i in range(len(a)):
        sum += (p[i] - a[i])**2
    sum = sum/len(a)
    return sum


def rmse(a, p):
   return math.sqrt(mse(a,p))


def mae(a, p):
    sum = 0
    for i in range(len(a)):
        sum += abs(p[i] - a[i])
    sum = sum/len(a)
    return sum


def rse(a, p):
    sum1 = 0
    for i in range(len(a)):
        sum1 += (p[i] - a[i])**2
    sr = numpy.mean(a)
    sum2 = 0
    for j in range(len(a)):
        sum2 += (sr - a[j])**2
    sum = sum1/sum2
    return sum


def rrse(a, p):
   return math.sqrt(rse(a,p))


def rae(a, p):
    sum1 = 0
    for i in range(len(a)):
        sum1 += abs(p[i] - a[i])
    sr = numpy.mean(a)
    sum2 = 0
    for j in range(len(a)):
        sum2 += abs(sr - a[j])
    sum = sum1/sum2
    return sum


def cof_det(a, p):
    sum1 = 0
    sp = numpy.mean(p)
    for i in range(len(a)):
        sum1 += (sp - p[i])**2
    sr = numpy.mean(a)
    sum2 = 0
    for j in range(len(a)):
        sum2 += (sr - a[j])**2
    sum = sum1/sum2
    return sum


records = []
sett(records)
tree = Tree(records, 0, 0, 0, "")
test_records = []
sett_test(test_records)
cart_reg(tree,0)
a = []
p = []
for i in test_records:
    a.append(func(i.p1, i.p2))
    p.append(model(tree,i))
print("a = ",a)
print("p = ",p)
print("MSE = ", mse(a, p))
print("RMSE = ", rmse(a, p))
print("MAE = ", mae(a, p))
print("RSE = ", rse(a, p))
print("RRSE = ", rrse(a, p))
print("RAE = ", rae(a, p))
print("R^2 = ", cof_det(a, p))






#q,l,r,al,ar = splitter(tree.records,5)
#print(r)

