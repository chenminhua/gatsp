"""
啥是基因 gene
啥是遗传交叉
啥是基因突变
啥是优胜劣汰，啥是适应度函数
"""

SCORE_NONE = -1

import random

class Life(object):
    """个体类"""
    def __init__(self, aGene = None):
        self.gene = aGene
        self.score = SCORE_NONE

class GA:
    def __init__(self, crate, mrate, lifeCount, bestProb, geneLength, matchFun):
        self.crate = crate                   #交叉概率
        self.mrate = mrate                   #突变概率
        self.lifeCount = lifeCount           #种群数量，就是每次我们在多少个城市序列里筛选，这里初始化为100
        self.geneLength = geneLength         #其实就是城市数量
        self.matchFun = matchFun             #适配函数
        self.lives = []                      #种群
        self.bestProb = bestProb             #保存这一代中最好的个体的概率
        self.best = []                       #每一代最好的
        self.generation = 1                  #代
        self.crossCount = 0                  #一开始还没交叉过，所以交叉次数是0
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
        print(len(self.lives))
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
        self.crossCount += 1
        return newGene
        
    # 变异
    def mutation(self, gene):
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(0, self.geneLength - 1)
        #把这两个位置的城市互换
        gene[index1], gene[index2] = gene[index2], gene[index1]
        #突变次数加1
        return gene

    def getOne(self):
        """随机选两个生小孩用的函数"""
        #产生0到（适配值之和）之间的任何一个实数，score越高的越容易被选中
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
 
        raise Exception("选择错误", self.bounds)

    def newChild(self):
        """生个孩子"""
        p1 = self.getOne()
        gene = p1.gene
        if random.random() < self.crate:
            p2 = self.getOne()
            gene = self.cross(p1, p2)

        if random.random() < self.mrate:
            gene = self.mutation(gene)
        return Life(gene)

    def next(self):
        """产生下一代，记住要把最好的放入下一代"""
        self.judge()
        newLives = self.best
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1
        pass

import math

class TSP:
    def __init__(self, aLifeCount = 200):
        self.initCitys()
        self.lifeCount = aLifeCount
        self.ga = GA(0.7, 0.02, self.lifeCount, 0.2,
                    len(self.citys), self.matchFun())

    def initCitys(self):
        self.citys = []
        f=open("distance.txt","r")
        while True:
            loci = str(f.readline())
            if loci:
                pass
            else:
                break
            loci = loci.replace("\n", "")
            loci=loci.split("\t")
            self.citys.append((float(loci[1]),float(loci[2]),loci[0]))

    #order是遍历所有城市的一组序列，如[1,2,3,7,6,5,4,8……]
    #distance就是计算这样走要走多长的路
    def distance(self, order):
        distance = 0.0
        #i从-1到32,-1是倒数第一个
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

        return distance
 
      #适应度函数，因为我们要从种群中挑选距离最短的，作为最优解，所以（1/距离）最长的就是我们要求的
    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, n = 0):
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best[0].gene)
            print (("%d : %f") % (self.ga.generation, distance))
            print (self.ga.best[0].gene)
            n -= 1
        print ("经过{}次迭代，最优解距离为：{}".format(self.ga.generation, distance))
        print ("遍历城市顺序为：")
        for i in self.ga.best[0].gene:
                print (self.citys[i][2])

tsp = TSP(300)
tsp.run(2000)