'''
这是一个著名的NP HARD问题，不存在多项式时间复杂度的解法

最暴力的解法
考虑city 1作为开始和结束的城市
生成所有的 (n-1)!个剩余城市的全排列。
计算全排列下每个结果的距离，找出最小的那个。
时间复杂度为 O(n!)

动态规划
let the given set of vertices be {1,2,3,4,...n}.
1 作为出发地和目的地
total cost = cost(i) + dist(i, 1)，最终我们要找到的就是让total cost最小的i
现在问题变成了如何计算cost(i)?
让我们定义 C(S,i) 为从1出发并经过S中所有点一次最后到达i的最短路径
if size of S is 2, then S must be {1, i}
    C(S,i) = dist(1,i)
else if size of S is greater than 2.
    C(S,i) = min {C(S-{i}, j) + dis(j, i)} where j belongs to S

'''

def solve_tsp_dynamic(points):
    #calc all lengths
    all_distances = [[length(x,y) for y in points] for x in points]
    #initial value - just distance from 0 to every other point + keep the track of edges
    A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(all_distances[0][1:])}
    cnt = len(points)
    for m in range(2, cnt):
        B = {}
        for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
            for j in S - {0}:
                B[(S, j)] = min( [(A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
        A = B
    res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
    return res[1]