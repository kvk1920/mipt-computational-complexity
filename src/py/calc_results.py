from matplotlib import pyplot as plt
import numpy as np
import sys


def read_file(file_name: str):
    result = []
    with open(file_name, 'r') as fin:
        for line in fin:
            n, score, time = line.split()
            n = int(n)
            score = float(score)
            time = float(time)
            result.append((n, score, time))
    return np.array(result)


def main(exp_in: str, pol_in: str, res_dir: str) -> None:
    exp_res, pol_res = read_file(exp_in), read_file(pol_in)
    n = len(exp_res)

    plt.figure(figsize=(16, 16))
    plt.scatter(exp_res.T[0], exp_res.T[2], color='indigo', label='$2^n$', alpha='0.3')
    plt.scatter(pol_res.T[0], pol_res.T[2],
                color='magenta', label='Гёманс-Уильямсон', alpha=0.3)
    plt.xlabel('$n$ - количество переменных в формуле')
    plt.ylabel('время работы в секундах')
    plt.title('сравнение скорости работы наивного алгоритма и алгоритма Гёманса-Уильямсона')
    plt.legend(fontsize=14)
    plt.xticks(np.arange(1, 21))
    plt.savefig(res_dir + 'time_compare.png')

    plt.figure(figsize=(16, 16))
    plt.scatter(pol_res.T[0], pol_res.T[2], alpha=0.3, color='magenta')
    plt.xlabel('$n$ - оличество переменных в формуле')
    plt.ylabel('Время работы в секундах')
    plt.title('Время работы алгоритма Гёманса-Уильямсона')
    plt.legend(fontsize=14)
    plt.xticks(np.arange(1, 21))
    plt.savefig(res_dir + 'time.png')

    plt.figure(figsize=(16, 16))
    plt.scatter(exp_res.T[0], pol_res.T[1] / exp_res.T[1], alpha=0.3)
    plt.xlabel('$n$ - количество переменных в формуле')
    plt.ylabel('Среднее отношение результата алгоритма Гёманса-Уильямсона к истинному ответу')
    plt.title('Правильность ответа алгоритма Гёманса-Уильямсона')
    plt.legend(fontsize=14)
    plt.xticks(np.arange(1, 21))
    plt.savefig(res_dir + 'Качество алгоритма Гёманса-Уильямсона')

    with open('tmp', 'w') as fout:
        for i in range(n):
            print(exp_res[i][1], pol_res[i][1], file=fout)


if '__main__' == __name__:
    main(sys.argv[1] + 'exp_res.txt', sys.argv[1] + 'pol_res.txt', sys.argv[1])