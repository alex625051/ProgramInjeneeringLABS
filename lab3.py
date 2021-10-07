import random
from collections import OrderedDict


# merge_dicts
def merge_dicts(d_list):
    if len(d_list)==0:return False
    if len(d_list)==1:return d_list[0]
    for d in (range(1,len(d_list))):
        for k in d_list[d]:
            d_list[0][k]=d_list[d][k]
    return d_list[0]

# Быстрая сортировка словаря
def quickSort_rec(g_dict):
    if len(g_dict) <= 1:
        return g_dict

    keys=list(g_dict.keys())
    q = random.choice(keys)

    l_nums = OrderedDict([(k,g_dict[k]) for k in keys if g_dict[k] < g_dict[q]])
    b_nums = OrderedDict([(k,g_dict[k]) for k in keys if g_dict[k] > g_dict[q]])


    e_nums = OrderedDict([(k,g_dict[k]) for k in keys if g_dict[k] == g_dict[q]])#

    return merge_dicts([quickSort_rec(l_nums), e_nums , quickSort_rec(b_nums)])


def floydwarshall(graph, alg=False):
    # Заполняем результирующих граы
    # Добавляем бесконечный путь там, где о не обозначен
    # no edge, и еще 0 поглавной диагонали (т.к. отрабатываем без петель)
    dist = {}
    pred = {}
    count=0


    for u in graph:
        dist[u] = {}
        pred[u] = {}
        for v in graph:
            dist[u][v] = float("inf")
            pred[u][v] = -1
        dist[u][u] = 0
        for neighbor in graph[u]:
            dist[u][neighbor] = graph[u][neighbor]
            pred[u][neighbor] = u

    #Сортировка графа
    for i in dist:
        dist[i]=quickSort_rec(dist[i])


    for t in graph:

        for u in graph:
            if (alg) and (dist[u][t] == float('inf')):
                pass
                continue
            dist[u] = quickSort_rec(dist[u])

            for v in graph:
                count=count+1
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
                    pred[u][v] = pred[t][v]
                elif newdist > dist[u][v]:
                    pass


                elif newdist > dist[u][v] :
                    pass
                    # break

    print(f"счетчик проходов (с сортировкой = {alg}) {count}")
    return dist, pred

matrx= [   #матрица смежности
    [0, 3, 0, 0, 42, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [3, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 7, 0, 11, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 309, 0, 0, ],
    [0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [42, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 1, 0, 22, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 22, 0, 13, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 13, 0, 7, 0, 0, 0, 14, 0, 11, 25, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, ],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, ],
    [0, 0, 11, 0, 0, 0, 0, 0, 0, 1, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 3, 0, 0, 0, 14, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, ],
    [0, 0, 0, 7, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 5, 0, 0, ],
    [0, 0, 0, 0, 9, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 13, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 9, 25, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 5, 1, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 42, 1, 0, 0, 0, 0, 0, 0, 0, 9, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 0, 13, 0, 0, 3, 0, 0, 9, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, ],
    [0, 0, 309, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 6, 0, 13, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 0, 0, 0, 0, 0, 13, 0, ],

]

graph={}
for idx, row in enumerate(matrx):
    graph[idx]={}
    for idx2, vertex in enumerate(row):
        if vertex>0:
            graph[idx][idx2]=vertex


dist, pred = floydwarshall(graph,True)
dist2, pred2 = floydwarshall(graph)
print ( "Матрица минимальных растояний (c сортировкой):  ")
for v in dist:
    dist[v]= [(key,dist[v][key]) for key in dist[v].keys()]
    print (" %s: %s " % (v, dist[v]))


print ( "Предыдущие точки (запоминание маршрута):  ")

for v in pred:
    pred[v]= [[key,pred[v][key]] for key in pred[v].keys()]
    print (" %s: %s " % (v, pred[v]))


