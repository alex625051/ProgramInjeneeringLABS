import tracemalloc
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys

import sympy


def prepare_b():
    b_primes = []
    n = 1000
    for i in range(0, 50):
        b = sympy.nextprime(n)
        b_primes.append(b)
        n = b
    return b_primes

def prepare_n():
    m = 0
    n_primes = []
    while m < 800:
        n = sympy.nextprime(m)
        n_primes.append(n)
        m = n
    return n_primes



def devide(x, devider):
    o = int(x % devider)
    return int((x - o) / devider), o

def expt_bi_for(b, n):
    if b == 0: return 0
    if b == 1: return 1
    if n == 0: return 1
    if n == 1: return b
    result = b
    nns = []
    while True:
        n, o = devide(n, 2)
        if n == 0: break
        nns.append((n, o))
    for np in range(len(nns) - 1, -1, -1):
        result = ((result) ** 2) * (b) ** nns[np][1]
    return result


def expt_bi_rec(b, n):
    if b == 0: return 0
    if b == 1: return 1
    if n == 0: return 1
    if n == 1: return b
    n, o = devide(n, 2)
    if o == 0: return expt_bi_rec(b, n) ** 2
    if o == 1: return (expt_bi_rec(b, n) ** 2) * b


def expt_line_rec(b, n):
    if b == 0: return 0
    if b == 1: return 1
    if n == 0: return 1
    if n == 1: return b
    return b * expt_line_rec(b, n - 1)


def expt_line_for(b, n):
    if b == 0: return 0
    if b == 1: return 1
    if n == 0: return 1
    if n == 1: return b
    result = b
    for i in range(0, n - 1):
        result = result * b
    return result


def runAlg(alg, tracer, arges, repeats):
    tracer.clear_traces()
    t1 = time.perf_counter_ns()
    for i in range(0, repeats):
        alg(*arges)
    t2 = time.perf_counter_ns()
    size, peak = tracemalloc.get_traced_memory()
    return {"time": (t2 - t1) / repeats, "size": size, "peak": peak, }


def main():
    tracemalloc.start()
    alges = {
        "expt_bi_for": expt_bi_for,
        "expt_bi_rec": expt_bi_rec,
        "expt_line_rec": expt_line_rec,
        "expt_line_for": expt_line_for
    }
    alg_arges=['b','n']
    repeats = 1
    nlimit = 800;

    results={}
    for alg in alges.keys():
        results[alg]={'time': [], 'peak': []}
        for arg in alg_arges:
            results[alg][arg]=[]

    b_primes=prepare_b()
    n_primes=prepare_n()
    for b in list(b_primes):
        for n in n_primes:
            for alg in alges.keys():
                it=runAlg(alges[alg], tracemalloc, [b, n], repeats)
                listSize = sys.getsizeof(results)
                results[alg]['n'].append(n)
                results[alg]['b'].append(b)
                results[alg]['time'].append(it['time'])
                results[alg]['peak'].append(it['peak'] - listSize)

    dFResults={}
    for alg in alges.keys():
        dFResults[alg]=pd.DataFrame(results[alg])

    fig = plt.figure(figsize=(25, 10))
    axes=[]
    axPlace=0
    for alg in alges.keys():
        axes.append({})
        axPlace=axPlace+1
        axes[-1]=fig.add_subplot(240+axPlace, projection='3d')
        x=dFResults[alg]['b']
        y=dFResults[alg]['n']
        z=dFResults[alg]['peak']
        axes[-1].plot_trisurf(x, y, z, linewidth=0, antialiased=False)
        axes[-1].set_title(alg)
        axes.append({})
        axes[-1] = fig.add_subplot(244+axPlace, projection='3d')
        z = dFResults[alg]['time']
        axes[-1].plot_trisurf(x, y, z, linewidth=0, antialiased=False)

    fig.show()
    for alg in alges.keys():
        dFResults[alg].to_excel(alg+'.xlsx')

if __name__ == '__main__':
    main()
