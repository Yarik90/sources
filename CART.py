import random
import math
import copy
import itertools


class Record:
    def __init__(self, id, shooter, barrel, lenbar, stand, distance, c):
        self.id = id
        self.shooter = shooter
        self.barrel = barrel
        self.lenbar = lenbar
        self.stand = stand
        self.distance = distance
        self.c = c

    def show(self, tab):
        print(tab, self.id, self.shooter, self.barrel, self.lenbar, self.stand, self.distance, self.c)


class Tree:
    def __init__(self, records, atrl, atrr):
        self.left = None
        self.right = None
        self.records = records
        self.atrl = atrl
        self.atrr = atrr

    def showt(self, tab):
        for i in self.records:
            i.show(tab)

    def splitin(self, childs, atr, rule):
        self.childs = childs
        self.atr = atr
        self.rule = rule


def p_param(split, clas):
    count = 0
    for i in split:
        if i.c == clas:
            count = count + 1
    pj = count/len(split)
    return pj


def q_param(left, right, n):
    if len(left) == 0 or len(right) == 0:
        return 0
    pl = len(left)/n
    pr = len(right)/n
    sumt = 0
    for i in range(1,5):
        sumt = sumt + abs(p_param(left,i) - p_param(right,i))
    q = 2*pl*pr*sumt
    return q


def splitter(records, atr):
    if atr == 1:
        uniq = []
        left = []
        right = []
        split_l = []
        split_r = []
        for i in records:
            uniq.append(i.shooter)
        nset = set(uniq)
        uniq = list(nset)
        uniq.sort()
        q = 0
        for k in range(1,3):
            for i in itertools.combinations(uniq, k):
                n_left = [x for x in records if x.shooter in i]
                s1 = [s for s in uniq if s in i]
                n_right = [x for x in records if x.shooter not in i]
                s2 = [s for s in uniq if s not in i]
                qn = q_param(n_left,n_right,len(records))
                if qn > q:
                    q = qn
                    left = n_left
                    right = n_right
                    split_l = s1
                    split_r = s2
        splitl = "Атрибут: Shooter, Левый узел: " + ','.join(split_l)
        splitr = "Атрибут: Shooter, Правый узел: " + ','.join(split_r)
        return q, left, right, splitl, splitr
    elif atr == 2:
        uniq = []
        for i in records:
            uniq.append(i.barrel)
        nset = set(uniq)
        uniq = list(nset)
        uniq.sort()
        i = itertools.combinations(uniq, 1)
        left = [x for x in records if x.barrel == "rifled"]
        right = [x for x in records if x.barrel == "smooth"]
        split_l = ["rifled"]
        split_r = {"smooth"}
        q = q_param(left, right, len(records))
        splitl = "Атрибут: Barrel, Левый узел: " + ','.join(split_l)
        splitr = "Атрибут: Barrel, Правый узел: " + ','.join(split_r)
        return q, left, right, splitl, splitr
    elif atr == 3:
        uniq = []
        left = []
        right = []
        for i in records:
            uniq.append(i.lenbar)
        nset = set(uniq)
        uniq = list(nset)
        uniq.sort()
        uniq.remove(max(uniq))
        q = 0
        number = 0
        for i in itertools.combinations(uniq, 1):
            n_left = [x for x in records if x.lenbar <= i[0]]
            n_right = [x for x in records if x.lenbar > i[0]]
            qn = q_param(n_left, n_right, len(records))
            if qn > q:
                q = qn
                left = n_left
                right = n_right
                number = i[0]
        split_l = ["x <= " + str(number)]
        split_r = ["x > " + str(number)]
        splitl = "Атрибут: Lenbar, Левый узел: " + ','.join(split_l)
        splitr = "Атрибут: Lenbar, Правый узел: " + ','.join(split_r)
        return q, left, right, splitl, splitr
    elif atr == 4:
        uniq = []
        left = []
        right = []
        split_l = []
        split_r = []
        for i in records:
            uniq.append(i.stand)
        nset = set(uniq)
        uniq = list(nset)
        uniq.sort()
        q = 0
        for i in itertools.combinations(uniq, 1):
            n_left = [x for x in records if x.stand in i]
            s1 = [s for s in uniq if s in i]
            n_right = [x for x in records if x.stand not in i]
            s2 = [s for s in uniq if s not in i]
            for t in s2:
                str(t)
            qn = q_param(n_left, n_right, len(records))
            if qn > q:
                q = qn
                left = n_left
                right = n_right
                split_l = s1
                split_r = s2
        split_l = [str(s) for s in split_l]
        split_r = [str(s) for s in split_r]
        splitl = "Атрибут: Stand, Левый узел: " + ','.join(split_l)
        splitr = "Атрибут: Stand, Правый узел: " + ','.join(split_r)
        return q, left, right, splitl, splitr
    elif atr == 5:
        uniq = []
        left = []
        right = []
        split_l = []
        split_r = []
        for i in records:
            uniq.append(i.distance)
        nset = set(uniq)
        uniq = list(nset)
        uniq.sort()
        q = 0
        k_c = 0
        for k in range(1, 3):
            for i in itertools.combinations(uniq, k):
                if k_c == 3:
                    continue
                if k == 2:
                    k_c += 1
                n_left = [x for x in records if x.distance in i]
                s1 = [s for s in uniq if s in i]
                n_right = [x for x in records if x.distance not in i]
                s2 = [s for s in uniq if s not in i]
                qn = q_param(n_left, n_right, len(records))
                if qn > q:
                    q = qn
                    left = n_left
                    right = n_right
                    split_l = s1
                    split_r = s2
        split_l = [str(s) for s in split_l]
        split_r = [str(s) for s in split_r]
        splitl = "Атрибут: Distance, Левый узел: " + ','.join(split_l)
        splitr = "Атрибут: Distance, Правый узел: " + ','.join(split_r)
        return q, left, right, splitl, splitr


def leaf(records):
    if len(records) == 1:
        return 1
    l = records[0].c
    for i in range(1, len(records)):
        if records[i].c != l:
            return 0
    return 1


idtree = 0

def tabulator(level):
    tab = ""
    for i in range(level):
        tab += "\t\t"
    return tab


def cart(unit,level):
    q = 0
    left = []
    right = []
    atrleft = ""
    atrright = ""
    for i in range(1, 6):
        qn, leftn, rightn, atrl, atrr = splitter(unit.records, i)
        if qn > q:
            q = qn
            left = leftn
            right = rightn
            atrleft = atrl
            atrright = atrr
    unit.left = Tree(left,0,0)
    unit.right = Tree(right,0,0)
    unit.atrl = atrleft
    unit.atrr = atrright
    tab = tabulator(level + 1)
    if leaf(unit.left.records) == 1:
        print(tab,unit.atrl)
        print(tab, "Лист:")
        unit.left.showt(tab)
    else:
        print(tab, unit.atrl)
        unit.left.showt(tab)
        cart(unit.left, level + 1)

    if leaf(unit.right.records) == 1:
        print(tab,unit.atrr)
        print(tab, "Лист:")
        unit.right.showt(tab)
    else:
        print(tab, unit.atrr)
        unit.right.showt(tab)
        cart(unit.right, level + 1)

    return 0


def sett(records):
    f = open('set.txt', 'r')
    for line in f:
        lst = line.split()
        r = Record(int(lst[0]), lst[1], lst[2], int(lst[3]), int(lst[4]), int(lst[5]), int(lst[6]))
        records.append(r)
    f.close()


records = []
sett(records)
tree = Tree(records, 0, 0)
cart(tree,0)

