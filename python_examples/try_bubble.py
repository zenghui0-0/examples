import os
import sys


def main(*args):
    L = list(args)
    print("Befor sorted:{}".format(L))
    num = len(L)
    for i in range(0, num):
        for j in range(i, num):
            if L[i] < L[j]:
                L[i], L[j] = L[j], L[i]
    print("After sort: {}".format(L))


if __name__ == "__main__":
    main(1, 4, 3, 5, 1)

