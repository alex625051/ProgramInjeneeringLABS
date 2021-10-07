import tracemalloc
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import random


import sympy


def prepare_n(nLimit,nstart):
    return [n for n in range(nstart,nLimit,50000) ]
    m = nstart
    n_primes = []
    i=0
    while i < nLimit:
        n = sympy.nextprime(m)
        n_primes.append(n)
        m = n
        i=i+1
    return n_primes


#Функция разделения для нужд "быстрой сортировки"
def partition(arr, low, high):
    i = (low - 1)  # индекс меньшего элемента
    pivot = arr[high]
    for j in range(low, high):
        # Если текущий элемент меньше
        # чем или равно Pivot
        if arr[j] <= pivot:
            # индекс приращения
            # меньший элемент
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)


# Основная функция, реализующая QuickSort
# Классический рекурсивный вариант
def quickSort_rec(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n < q]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n > q]
    return quickSort_rec(l_nums) + e_nums + quickSort_rec(b_nums)


# Рекурсивный алгоритм для сортировки слиянием
def merge_rec(left, right):
    if not len(left) or not len(right):
        return left or right

    result = []
    i, j = 0, 0

    while (len(result) < len(left) + len(right)):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

        if i == len(left) or j == len(right):
            result.extend(left[i:] or right[j:])
            break
    return result


def quickSort_iter(arr, l=False, h=False):
    if h==False:
        l=0;h=len(arr)-1
    # Создать вспомогательный стек
    size = h - l + 1
    stack = [0] * (size)
    # инициализировать вершину стека
    top = -1
    # поместь начальные значения l и h в стек
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h
    # Продолжать забирать из стека, пока не пусто
    while top >= 0:
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
        # отсортированный массив
        p = partition(arr, l, h)
        # Если есть элементы на левой стороне оси
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
        # Если есть элементы на правой стороне оси
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h



def mergesort_rec(list):
    if len(list) < 2:
        return list
    middle = math.ceil(len(list) / 2)
    left = mergesort_rec(list[:middle])
    right = mergesort_rec(list[middle:])
    return merge_rec(left, right)



# Итеративная функция сортировки слиянием
from collections import deque

def atomize(l):
    return deque(
        map(
            lambda x: deque([x]),
            l if l is not None else []
        )
    )

def merge_iter(l, r):
    res = deque()
    while (len(l) + len(r)) > 0:
        if len(l) < 1:
            res += r
            r = deque()
        elif len(r) < 1:
            res += l
            l = deque()
        else:
            if l[0] <= r[0]:
                res.append(l.popleft())
            else:
                res.append(r.popleft())
    return res

def mergesort_iter(l):
    atoms = atomize(l) # O(n)
    while len(atoms) > 1: # O(n - 1)
        atoms.append(merge_iter(atoms.popleft(), atoms.popleft()))
    return list(atoms[0])




def runAlg(alg, tracer, arges, repeats):
    n=arges[0]
    array = np.random.randint(200000, size=(n)).tolist()
    tracer.clear_traces()
    t1 = time.perf_counter_ns()
    for i in range(0, repeats):
        alg(array)
    t2 = time.perf_counter_ns()
    size, peak = tracemalloc.get_traced_memory()
    return {"time": (t2 - t1) / repeats, "size": size, "peak": peak, }


def main():
    tracemalloc.start()
    alges = {
        # "mergesort_iter": mergesort_iter,
        # "mergesort_rec": mergesort_rec,
        # "quickSort_iter": quickSort_iter,
        # "quickSort_rec": quickSort_rec,
        "sorted": sorted,

    }
    alg_arges = ['n']
    repeats = 1
    nlimit = 1000000;
    nstart = 10000;

    results = {}
    for alg in alges.keys():
        results[alg] = {'time': [], 'peak': []}
        for arg in alg_arges:
            results[alg][arg] = []

    n_primes = prepare_n(nlimit,nstart)
    for n in n_primes:
        for alg in alges.keys():
            it = runAlg(alges[alg], tracemalloc, [n], repeats)
            # print(alg)
            # print(f"n={n}")
            # print(array)
            # print(it)
            # print("----------------------------------")
            listSize = sys.getsizeof(results)
            results[alg]['n'].append(n)
            results[alg]['time'].append(it['time'])
            results[alg]['peak'].append(it['peak'] - listSize)

    dFResults = {}
    for alg in alges.keys():
        dFResults[alg] = pd.DataFrame(results[alg])

    fig = plt.figure(figsize=(25, 10))
    axes = []
    axPlace = 0
    for alg in alges.keys():
        axes.append({})
        axPlace = axPlace + 1
        axes[-1] = fig.add_subplot(240 + axPlace)
        x = dFResults[alg]['n']
        y = dFResults[alg]['peak']
        axes[-1].plot(x, y, ':o')
        axes[-1].set_title(alg)
        axes.append({})
        axes[-1] = fig.add_subplot(244 + axPlace)
        y = dFResults[alg]['time']
        axes[-1].plot(x, y , ':o')

    fig.show()
    for alg in alges.keys():
        dFResults[alg].to_excel(alg + '.xlsx')


if __name__ == '__main__':
    main()
