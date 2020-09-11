import random
import math
import copy


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
    def __init__(self, id, records, atr, rule):
        self.id = id
        self.childs = []
        self.records = records
        self.atr = atr
        self.rule = rule
        self.notsplit = []

    def showt(self, tab):
        for i in self.records:
            i.show(tab)

    def splitin(self, childs, atr, rule):
        self.childs = childs
        self.atr = atr
        self.rule = rule


def shootergen(k):
    if k == 1:
        return "Shooter1"
    elif k == 2:
        return "Shooter2"
    elif k == 3:
        return "Shooter3"
    elif k == 4:
        return "Shooter4"
    elif k == 5:
        return "Shooter5"


def barrelgen(k):
    if k == 1:
        return "rifled"
    elif k == 2:
        return "smooth"


def freq(records, c):
    count = 0
    for i in records:
        if i.c == c:
            count = count + 1
    return count


def info(records):
    s = len(records)
    info_t = 0
    for i in range(4):
        k = freq(records, i + 1) / s
        if k != 0:
            info_t = info_t + (k * math.log(k, 4))
        else:
            continue
    info_t = -info_t
    return info_t


def splitinfo(split, n):
    splitinf = 0
    for i in split:
        k = len(i) / n
        splitinf = splitinf + (k * math.log(k, 2))
    splitinf = -splitinf
    if splitinf == 0:
        return 2
    return splitinf


def infos(records, atr):
    infot = info(records)
    if atr == 1:
        uniq = []
        s1, s2, s3, s4, s5 = [], [], [], [], []
        splits = [s1, s2, s3, s4, s5]
        for i in records:
            uniq.append(i.shooter)
        nset = set(uniq)
        uniq = list(nset)
        num = len(uniq)
        uniq.sort()
        for i in records:
            if i.shooter == uniq[0]:
                splits[0].append(i)
            elif i.shooter == uniq[1]:
                splits[1].append(i)
            elif i.shooter == uniq[2]:
                splits[2].append(i)
            elif i.shooter == uniq[3]:
                splits[3].append(i)
            elif i.shooter == uniq[4]:
                splits[4].append(i)
        infos_t = 0
        s = len(records)
        for i in range(num):
            k = len(splits[i]) / s
            infos_t = infos_t + k * info(splits[i])
        gain = infot - infos_t
        return gain, splits
    elif atr == 2:
        uniq = []
        s1, s2 = [], []
        splits = [s1, s2]
        for i in records:
            uniq.append(i.barrel)
        nset = set(uniq)
        uniq = list(nset)
        num = len(uniq)
        uniq.sort()
        for i in records:
            if i.barrel == uniq[0]:
                splits[0].append(i)
            elif i.barrel == uniq[1]:
                splits[1].append(i)
        infos_t = 0
        s = len(records)
        for i in range(num):
            k = len(splits[i]) / s
            infos_t = infos_t + k * info(splits[i])
        gain = infot - infos_t
        return gain, splits
    elif atr == 3:
        split_min = []
        info_min = 1
        atrs = 0
        uniq = []
        for i in records:
            uniq.append(i.lenbar)
        nset = set(uniq)
        uniq = list(nset)
        uniq.sort()
        uniq.remove(max(uniq))
        for k in uniq:
            s1, s2 = [], []
            splits = [s1, s2]
            for i in records:
                if i.lenbar <= k:
                    splits[0].append(i)
                elif i.lenbar > k:
                    splits[1].append(i)
            infos_tt = 0
            s = len(records)
            for i in range(2):
                ck = len(splits[i]) / s
                infos_tt = infos_tt + ck * info(splits[i])
            if infos_tt < info_min:
                info_min = infos_tt
                split_min = splits
                atrs = k
        gain = infot - info_min
        return gain, split_min, atrs
    elif atr == 4:
        uniq = []
        s1, s2, s3 = [], [], []
        splits = [s1, s2, s3]
        for i in records:
            uniq.append(i.stand)
        nset = set(uniq)
        uniq = list(nset)
        num = len(uniq)
        uniq.sort()
        for i in records:
            if i.stand == uniq[0]:
                splits[0].append(i)
            elif i.stand == uniq[1]:
                splits[1].append(i)
            elif i.stand == uniq[2]:
                splits[2].append(i)
        infos_t = 0
        s = len(records)
        for i in range(num):
            k = len(splits[i]) / s
            infos_t = infos_t + k * info(splits[i])
        gain = infot - infos_t
        return gain, splits
    elif atr == 5:
        uniq = []
        s1, s2, s3, s4 = [], [], [], []
        splits = [s1, s2, s3, s4]
        for i in records:
            uniq.append(i.distance)
        nset = set(uniq)
        uniq = list(nset)
        num = len(uniq)
        uniq.sort()
        for i in records:
            if i.distance == uniq[0]:
                splits[0].append(i)
            elif i.distance == uniq[1]:
                splits[1].append(i)
            elif i.distance == uniq[2]:
                splits[2].append(i)
            elif i.distance == uniq[3]:
                splits[3].append(i)
        infos_t = 0
        s = len(records)
        for i in range(num):
            k = len(splits[i]) / s
            infos_t = infos_t + k * info(splits[i])
        gain = infot - infos_t
        return gain, splits


def rem(splits):
    splits = [x for x in splits if x != []]
    return splits


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


def id3(unit,level):
    gain = 0
    splitg = []
    atrg = 0
    atr = 0
    for i in range(1, 6):
        if i in unit.notsplit:
            if i == 3:
                if unit.rule in unit.notsplit:
                    continue
            else:
                continue
        if i != 3:
            gains, split = infos(unit.records, i)
            split = rem(split)
            gains = gains / splitinfo(split,len(unit.records))
            if gains > gain:
                gain = gains
                splitg = split
                atr = i
        else:
            gains, split, atrs = infos(unit.records, i)
            split = rem(split)
            gains = gains / splitinfo(split, len(unit.records))
            if gains > gain:
                gain = gains
                splitg = split
                atrg = atrs
                atr = i
    desc = []
    unit.notsplit.append(atr)
    for i in splitg:
        global idtree
        t = Tree(idtree, i, 0, 0)
        idtree += 1
        t.notsplit = copy.copy(unit.notsplit)
        desc.append(t)
    if atr == 3:
        rul = atrg
        if rul not in unit.notsplit:
            unit.notsplit.append(rul)
    else:
        rul = 0
    unit.splitin(desc, atr, rul)
    for t in unit.childs:
        tab = tabulator(level + 1)
        if leaf(t.records) == 1:
            if unit.atr == 3:
                print(tab, "Разбиение по атрибуту: ", unit.atr, " : ", unit.rule)
            else:
                print(tab, "Разбиение по атрибуту: ", unit.atr)
            print(tab, "Лист:")
            t.showt(tab)
            continue
        else:
            if unit.atr == 3:
                print(tab, "Разбиение по атрибуту: ", unit.atr, " : ", unit.rule)
            else:
                print(tab, "Разбиение по атрибуту: ", unit.atr)
            t.showt(tab)
            id3(t,level+1)
    return 0


def sett(records):
    f = open('set.txt', 'r')
    for line in f:
        lst = line.split()
        r = Record(int(lst[0]), lst[1], lst[2], int(lst[3]), int(lst[4]), int(lst[5]), int(lst[6]))
        records.append(r)
    f.close()


Records = []
'''for i in range(40):
    r = Record(i, shootergen(random.randrange(1,6,1)), barrelgen(random.randrange(1,3,1)), random.randrange(50,100,5), random.randrange(100,250,50), random.randrange(500,900,100), random.randrange(1,5,1))
    Records.append(r)'''
sett(Records)
tree = Tree(idtree, Records, 0, 0)
idtree += 1
print("Записи корневого узла:")
tree.showt("")
id3(tree,0)
