#!/usr/bin/env python3.5
"""
class for different method without simulator
"""

from math import ceil, log2, sqrt, floor, log
import sys

N = 10000000


def work_for_size(size):
    """
    get work for a size
    """
    return size*log2(size)


def run(initial_block, factor):
    """
    calcul initial block
    """
    work = 0
    merge = 0
    block_number = 0
    current_merge = 0
    remaining_size = N
#    print("#initial_block factor block_number block_size block_work block_merge block_total_work cumule_work ")
    while remaining_size > 0:
        current_task_size = min(block_size(initial_block,
                                           factor,
                                           block_number),
                                remaining_size)
        current_work = work_for_size(current_task_size)
        work += current_work
        completed_size = N - remaining_size
        if completed_size:
            current_merge = completed_size + current_task_size
        merge += current_merge
        remaining_size -= current_task_size
 #       print("{} {} {} {} {} {} {} {}".format(initial_block, factor,  block_number, current_task_size, current_work, current_merge, current_merge+current_work, work ) )
        block_number += 1
    return work, merge, work_for_size(current_task_size),block_number


def block_size(initial_block_size, factor, block_number):
    """
    return block size based on its number.
    we use "Golden ratio" to compute the size in each block
    """
    return ceil(initial_block_size * factor**block_number)
    #return initial_block_size

def main(phi):
    #phi = (1 + sqrt(5))/2
    for phi in [phi]:
        for initial_block in range(100,100000):
            work, merge, max_waiting_time, block_number = run(initial_block, phi)
            print(initial_block, phi, work, merge)

def init_blk_size(initial_block_size_threshold, task_size):
    """
    """
    block_number = floor(
        log2(task_size / initial_block_size_threshold + 1)
        - 1)
    initial_block_size = ceil(task_size / (2**(block_number + 1) - 1))
    #print(initial_block_size_threshold, block_number, initial_block_size)
    return initial_block_size


def max_block_number(phi, size, initial_block):
    """
    """
    stop_block_number = 0
    completed_size = 0
    while completed_size  < size:
        completed_size += min(initial_block * phi**stop_block_number, size-completed_size )
        stop_block_number += 1
    #print(stop_block_number - 1, "value=", log2(size/initial_block +1 )-1)
    return stop_block_number - 1

def overhead(phi, init_task_cost, size, initial_block, stop_block_number):
    """
    """

    completed_size = 0
    for i in range(stop_block_number):
        completed_size += min(initial_block*phi**i, size-completed_size)
        assert completed_size < size

    last_bock = initial_block * phi ** stop_block_number
    remaining_size = size - completed_size
    second_overhead = stop_block_number * init_task_cost + \
            (remaining_size / last_bock) * init_task_cost + last_bock

    return stop_block_number, second_overhead, stop_block_number * init_task_cost, (remaining_size / last_bock) * init_task_cost, last_bock

def f(n, b, c):
    """
    """
    x1 = (sqrt(c**2 + (4* log(2)**2*n/b + 4*log(2)**2 )*b*c) - c ) / ( 2*b*log(2) )
    x2 = (-sqrt(c**2 + (4* log(2)**2*n/b + 4*log(2)**2 )*b*c) - c ) / ( 2*b*log(2) )
    return log2(x1)

def b(n, c, k):
    """
    """

    return 2**(-2*k-1) * (sqrt( c * 2**(2*k + 2) * n - c**2 * 2**(k+2) + c**2*2**(2*k+2)) -c*2**(k+1) + c)


if __name__ == "__main__":
    print("# init_task_cost, size, initial_block_size, \
           stop_block_number, i_blk_s_t")
    i_t_c = int(sys.argv[1])
    size = int(sys.argv[2])
    i_b_s = int(sys.argv[3])
    phi = float(sys.argv[4])

    for i_b_s in range(1, i_b_s):
        cnbn, min_overhead, _, _, _ = overhead(phi, i_t_c, size, i_b_s, 0)
        x = 0, min_overhead
        for i in range(max_block_number(phi, size, i_b_s)):
            csbn, cmo, _, _, _ = overhead(phi, i_t_c, size, i_b_s, i)
            # print(cmo, min_overhead)
            if min_overhead > cmo:
                x = csbn, cmo
                min_overhead = cmo
        _, overhead_formule, term1, term2, term3 = overhead(phi, i_t_c, size, i_b_s,
                floor(f(size, i_b_s, i_t_c)+0.5))
        init_blk_size_formule = b(size, i_t_c, x[0])
        print(x[0], f(size, i_b_s, i_t_c), "ibs", i_b_s, "max_blk_nb",
              max_block_number(phi, size, i_b_s), "i_t_c", i_t_c,
              "overhead", min_overhead, "overhead_formule", overhead_formule, "t1", term1, "t2", term2, "t3", term3, "b formule", init_blk_size_formule)

