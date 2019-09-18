SCORE_NONE = -1

import random
import math

class Life(object):
    """个体类"""
    def __init__(self, aGene = None):
        self.gene = aGene
        self.score = SCORE_NONE

class GA:
    def __init__(self, mrate, lifeCount, bestProb, geneLength, matchFun):
        self.mrate = mrate                   #突变概率
        self.lifeCount = lifeCount           #种群数量
        self.geneLength = geneLength         #基因数量
        self.matchFun = matchFun             #适配函数
        self.lives = []                      #种群
        self.bestProb = bestProb             #保存这一代中最好的个体的概率
        self.best = []                       #每一代最好的
        self.generation = 1                  #代
        self.bounds = 0.0                    #适配值之和，用于选择时计算概率

        """初始化种群"""
        self.lives = []
        for i in range(self.lifeCount):
            gene = list(range(self.geneLength))
            random.shuffle(gene)
            life = Life(gene)
            self.lives.append(life)
 
    def judge(self):
        """评估，计算每一个个体的适配值"""
        # 适配值之和，用于选择时计算概率
        self.bounds = 0.0
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
        self.lives.sort(key= lambda life : life.score, reverse=True)
        self.best = self.lives[:int(self.lifeCount * self.bestProb)]
        
    # 杂交
    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(index1, self.geneLength - 1)
        tempGene = parent2.gene[index1:index2]                      #交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)                            #插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        return newGene
        
    # 变异
    def mutation(self, gene):
        if random.random() < self.mrate:
            index1 = random.randint(0, self.geneLength - 1)
            index2 = random.randint(0, self.geneLength - 1)
            #把这两个位置的城市互换
            gene[index1], gene[index2] = gene[index2], gene[index1]
        return Life(gene)

    def getOne(self):
        # 产生0到bounds之间的任何一个实数，score越高的越容易被选中
        # 越牛逼的人越有机会生小孩
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
 
        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """生个孩子"""
        p1 = self.getOne()
        p2 = self.getOne()
        gene = self.cross(p1, p2)
        return Life(gene)

    def next(self):
        """产生下一代，记住要把最好的放入下一代"""
        self.judge()
        newLives = self.best
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        for i in range(len(newLives)):
            newLives[i] = self.mutation(newLives[i].gene)
        self.lives = newLives
        self.generation += 1
        pass

############################ TSP #########################

cities = []
with open("distance.txt", "r") as f:
    while True:
        loci = str(f.readline())
        if not loci:
            break
        loci = loci.replace("\n", "")
        loci=loci.split("\t")
        cities.append((float(loci[1]),float(loci[2]),loci[0]))

n_cities = len(cities)

distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]
for i in range(n_cities):
    for j in range(n_cities):
        distances[i][j] = math.sqrt((cities[i][0] - cities[j][0]) ** 2 
        + (cities[i][1] - cities[j][1]) ** 2)

def distanceFunc(order):
    distance = 0.0
    #i从-1到32,-1是倒数第一个
    for i in range(-1, n_cities - 1):
        index1, index2 = order[i], order[i + 1]
        city1, city2 = cities[index1], cities[index2]
        distance += distances[index1][index2]
    return distance

def matchFun():
    return lambda life: 1.0 / distanceFunc(life.gene)

MUTATE_RATE = 0.1
POPULATION_SIZE = 1000

ga = GA(MUTATE_RATE, POPULATION_SIZE, 0.25, n_cities, matchFun())

for i in range(1000):
    ga.next()
    distance = distanceFunc(ga.best[0].gene)
    if ga.generation % 10 == 0:
        print(ga.generation, " ", distance)
print ("经过{}次迭代，最优解距离为：{}".format(ga.generation, distance))
print ("遍历城市顺序为：", end=" ")
for i in ga.best[0].gene:
    print (cities[i][2], end=" ")

        
