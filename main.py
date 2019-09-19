import random
import math

class GA:
    def __init__(self, mrate, lifeCount, bestProb, geneLength, matchFun):
        self.mrate = mrate                   #突变概率
        self.lifeCount = lifeCount           #种群数量
        self.geneLength = geneLength         #基因数量
        self.matchFun = matchFun             #适配函数
        self.lives = []                      #种群
        self.bestCount = int(lifeCount * bestProb) #保存这一代中最好的个体数
        self.best = []                       #每一代最好的
        self.generation = 0                  #代

        """初始化种群"""
        for i in range(self.lifeCount):
            gene = list(range(self.geneLength))
            random.shuffle(gene)
            self.lives.append(gene)
 
    # 变异
    def mutation(self):
        for i in range(self.lifeCount):
            if random.random() < self.mrate:
                gene = self.lives[i]
                index1 = random.randint(0, self.geneLength - 1)
                index2 = random.randint(0, self.geneLength - 1)
                #把这两个位置的城市互换
                gene[index1], gene[index2] = gene[index2], gene[index1]

    def newChild(self):
        g1 = self.lives[random.randint(0, self.lifeCount-1)]
        g2 = self.lives[random.randint(0, self.lifeCount-1)]
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(index1, self.geneLength - 1)
        cp1, cp2 = [], []
        for i in range(index1, index2):
            cp1.append(g1[i])
        cp2 = [item for item in g2 if item not in cp1]
        return cp1 + cp2
    
    def findBest(self):
        self.lives.sort(key= lambda life : self.matchFun(life), reverse=True)
        self.best = self.lives[:self.bestCount]

    def newGeneration(self):
        newge = self.best
        newge.extend([self.newChild() for _ in range(self.lifeCount-self.bestCount)])
        self.lives = newge
        self.generation += 1

    def next(self):
        self.findBest()
        best = self.best[0]
        self.newGeneration()
        self.mutation()
        self.lives[0] = best

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

# 计算距离矩阵(邻接矩阵存储图)
distances = [[math.sqrt((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2)
             for i in range(n_cities)] for j in range(n_cities)]

def calc_distance(gene):
    distance = 0.0
    for i in range(-1, n_cities - 1):
        index1, index2 = gene[i], gene[i + 1]
        city1, city2 = cities[index1], cities[index2]
        distance += distances[index1][index2]
    return distance

MUTATE_RATE = 0.01
POPULATION_SIZE = 1000

ga = GA(MUTATE_RATE, POPULATION_SIZE, 0.25, n_cities, lambda gene: 1.0 / calc_distance(gene))

for i in range(1000):
    ga.next()
    if ga.generation % 10 == 0:
        print(ga.generation, " ", calc_distance(ga.best[0]))
print ("经过{}次迭代，最优解距离为：{}".format(ga.generation, calc_distance(ga.best[0])))
print ("遍历城市顺序为：", end=" ")
for i in ga.best[0]:
    print (cities[i][2], end=" ")  
