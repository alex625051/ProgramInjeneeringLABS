import tracemalloc
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys

import sympy

b_primes = []
n_primes = []
tracemalloc.start()
n = 1000
for i in range(0, 50):
    b = sympy.nextprime(n)
    b_primes.append(b)
    n = b
m = 0
while m<800:
    n = sympy.nextprime(m)
    n_primes.append(n)
    m = n

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


def runAlg(alg, tracer, b, n, repeats):
    tracer.clear_traces()
    t1 = time.perf_counter_ns()
    for i in range(0, repeats):
        alg(b, n)
    t2 = time.perf_counter_ns()
    size, peak = tracemalloc.get_traced_memory()
    return {"time": (t2 - t1) / repeats, "size": size, "peak": peak, }


def main():
    results = {'expt_bi_for': {'n': [], 'b': [], 'time': [], 'peak': []},
               'expt_bi_rec': {'n': [], 'b': [], 'time': [], 'peak': []},
               'expt_line_rec': {'n': [], 'b': [], 'time': [], 'peak': []},
               'expt_line_for': {'n': [], 'b': [], 'time': [], 'peak': []}}
    repeats = 100
    nlimit = 800;
    nstep = int(round(nlimit / 50));
    for b in list(b_primes):
        for n in n_primes:
            listSize = sys.getsizeof(results)
            a = runAlg(expt_bi_for, tracemalloc, b, n, repeats)
            results['expt_bi_for']['n'].append(n)
            results['expt_bi_for']['b'].append(b)
            results['expt_bi_for']['time'].append(a['time'])
            results['expt_bi_for']['peak'].append(a['peak']-listSize)
            a = runAlg(expt_bi_rec, tracemalloc, b, n, repeats)
            results['expt_bi_rec']['n'].append(n)
            results['expt_bi_rec']['b'].append(b)
            results['expt_bi_rec']['time'].append(a['time'])
            results['expt_bi_rec']['peak'].append(a['peak']-listSize)
            a = runAlg(expt_line_rec, tracemalloc, b, n, repeats)
            results['expt_line_rec']['n'].append(n)
            results['expt_line_rec']['b'].append(b)
            results['expt_line_rec']['time'].append(a['time'])
            results['expt_line_rec']['peak'].append(a['peak']-listSize)
            a = runAlg(expt_line_for, tracemalloc, b, n, repeats)
            results['expt_line_for']['n'].append(n)
            results['expt_line_for']['b'].append(b)
            results['expt_line_for']['time'].append(a['time'])
            results['expt_line_for']['peak'].append(a['peak']-listSize)
    expt_bi_for_g = pd.DataFrame(results['expt_bi_for'])
    expt_bi_rec_g = pd.DataFrame(results['expt_bi_rec'])
    expt_line_rec_g = pd.DataFrame(results['expt_line_rec'])
    expt_line_for_g = pd.DataFrame(results['expt_line_for'])
    fig = plt.figure(figsize=(25, 10))
    ax1 = fig.add_subplot(241, projection='3d')
    ax1.plot_trisurf(expt_bi_for_g['b'], expt_bi_for_g['n'], expt_bi_for_g['peak'], linewidth=0, antialiased=False)

    ax2 = fig.add_subplot(242, projection='3d')
    ax2.plot_trisurf(expt_bi_rec_g['b'], expt_bi_rec_g['n'], expt_bi_rec_g['peak'], linewidth=0, antialiased=False)

    ax3 = fig.add_subplot(243, projection='3d')
    ax3.plot_trisurf(expt_line_rec_g['b'], expt_line_rec_g['n'], expt_line_rec_g['peak'], linewidth=0,
                     antialiased=False)

    ax4 = fig.add_subplot(244, projection='3d')
    ax4.plot_trisurf(expt_line_for_g['b'], expt_line_for_g['n'], expt_line_for_g['peak'], linewidth=0,
                     antialiased=False)

    ax1.set_title('expt_bi_for')
    ax2.set_title('expt_bi_rec')
    ax3.set_title('expt_line_rec')
    ax4.set_title('expt_line_for')

    ax5 = fig.add_subplot(245, projection='3d')
    ax5.plot_trisurf(expt_bi_for_g['b'], expt_bi_for_g['n'], expt_bi_for_g['time'], linewidth=0, antialiased=False)

    ax6 = fig.add_subplot(246, projection='3d')
    ax6.plot_trisurf(expt_bi_rec_g['b'], expt_bi_rec_g['n'], expt_bi_rec_g['time'], linewidth=0, antialiased=False)

    ax7 = fig.add_subplot(247, projection='3d')
    ax7.plot_trisurf(expt_line_rec_g['b'], expt_line_rec_g['n'], expt_line_rec_g['time'], linewidth=0,
                     antialiased=False)

    ax8 = fig.add_subplot(248, projection='3d')
    ax8.plot_trisurf(expt_line_for_g['b'], expt_line_for_g['n'], expt_line_for_g['time'], linewidth=0,
                     antialiased=False)


    fig.show()
    df=pd.DataFrame(results)
    print(df)
    df.to_html('out.html')
    df.to_excel('out.xlsx')
    expt_bi_for_g.to_excel('expt_bi_for_g.xlsx')
    expt_bi_rec_g.to_excel('expt_bi_rec_g.xlsx')
    expt_line_rec_g.to_excel('expt_line_rec_g.xlsx')
    expt_line_for_g.to_excel('expt_line_for_g.xlsx')
    print(expt_line_for_g)

if __name__ == '__main__':
    main()
