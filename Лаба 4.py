""" С клавиатуры вводятся два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B, C, D, E заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное
заполнение, а целенаправленное.
Вид матрицы А:
D	Е
С	В
Для простоты все индексы в подматрицах относительные.
По сформированной матрице F (или ее частям) необходимо вывести не менее 3 разных графика.
Программа должна использовать функции библиотек numpy  и mathplotlib

Вариант 13:
Формируется матрица F следующим образом: скопировать в нее А и если в С количество четных чисел в нечетных столбцах
больше, чем сумма чисел в нечетных строках, то поменять местами С и Е симметрично, иначе В и Е поменять местами
несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных элементов
матрицы F, то вычисляется выражение: A * A^T – K * F^-1, иначе вычисляется выражение (A^Т + G - F^Т) * K, где G-нижняя
 треугольная матрица, полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно."""

import numpy as np
from matplotlib import pyplot as plt


try:
    n = int(input('Введите число N > 5, являющееся размерностью матрицы "A": '))
    k = int(input('Введите число K, являющееся коэффициентом умножения: '))
    while n < 6:
        n = int(input('Введите число N > 5: '))

    cnt_ch = sum_nchstr = sum_det_F = 0
    middle_n = n // 2 + n % 2  # Середина матрицы
    A = np.random.randint(-10.0, 10.0, (n, n))  # Задаём рандомно заполненную матрицу А
    AT = np.transpose(A)  # Транспонированная матрица А
    A_obr = np.linalg.inv(A)  # Обратная матрица А
    det_A = np.linalg.det(A)  # Определитель матрицы А
    F = A.copy()  # Задаём матрицу F
    G = np.tri(n) * A  # Матрица G

    print(f'\nМатрица А:\n{A}')
    print(f'\nТранспонированная А:\n{AT}')

    # Выделяем матрицы E C B
    if n % 2 == 1:
        E = [A[i][middle_n - 1:n] for i in range(middle_n)]
        C = [A[i][0:middle_n] for i in range(middle_n - 1, n)]
        B = [A[i][middle_n - 1:n] for i in range(middle_n - 1, n)]
    else:
        E = [A[i][middle_n:n] for i in range(0, middle_n)]
        C = [A[i][0:middle_n] for i in range(middle_n, n)]
        B = [A[i][middle_n:n] for i in range(middle_n, n)]

    for i in range(middle_n):  # Считаем в нечётных столбцах в матрице С кол-во чётных значений
        for j in range(0, middle_n, 2):
            if C[i][j] % 2 == 0:
                cnt_ch += 1

    for i in range(0, middle_n, 2):  # Считаем сумму чисел в нечётных строках в матрице С
        for j in range(middle_n):
            sum_nchstr += C[i][j]

    if cnt_ch > sum_nchstr:
        print(f'\nВ матрице "С" количество четных чисел в нечетных столбцах({cnt_ch})')
        print(f'больше чем сумма чисел в нечётных строках({sum_nchstr})')
        print('поэтому симметрично местами подматрицы C и E:')
        C, E = E, C
        for i in range(middle_n):
            C[i] = C[i][::-1]  # Симметрично меняем значения в C
            E[i] = E[i][::-1]  # Симметрично меняем значения в E

        if n % 2 == 1:
            for i in range(middle_n - 1, n):  # Перезаписываем С
                for j in range(middle_n):
                    F[i][j] = C[i - (middle_n - 1)][j]
            for i in range(middle_n):  # Перезаписываем Е
                for j in range(middle_n - 1, n):
                    F[i][j] = E[i][j - (middle_n - 1)]
        else:
            for i in range(middle_n, n):
                for j in range(middle_n):
                    F[i][j] = C[i - middle_n][j]
            for i in range(0, middle_n):
                for j in range(middle_n, n):
                    F[i][j] = E[i][j - middle_n]
    else:
        print(f'\nВ матрице "С" количество четных чисел в нечетных столбцах({cnt_ch})')
        print(f'меньше чем сумма чисел в нечётных строках({sum_nchstr}) или равно ей')
        print('поэтому несимметрично меняем местами области B и E:')
        B, E = E, B
        if n % 2 == 1:
            for i in range(middle_n - 1, n):  # Перезаписываем B
                for j in range(middle_n - 1, n):
                    F[i][j] = B[i - (middle_n - 1)][j - (middle_n - 1)]
            for i in range(middle_n):  # Перезаписываем Е
                for j in range(middle_n - 1, n):
                    F[i][j] = E[i][j - (middle_n - 1)]
        else:
            for i in range(middle_n, n):
                for j in range(middle_n, n):
                    F[i][j] = B[i - middle_n][j - middle_n]  # Перезаписываем B
            for i in range(0, middle_n):
                for j in range(middle_n, n):
                    F[i][j] = E[i][j - middle_n]  # Перезаписываем Е

    print(f'\nМатрица F:\n{F}')
    # Сумма диагональных элементов матрицы F
    for i in range(n):
        for j in range(n):
            if i == j:
                sum_det_F += F[i][j]
            if (i + j + 1) == n and ((i == j) != ((i + j + 1) == n)):
                sum_det_F += F[i][j]

    if det_A > sum_det_F:
        print(f'\nОпределитель матрицы А({int(det_A)})')
        print(f'больше суммы диагональных элементов матрицы F({int(sum_det_F)})')
        print('поэтому вычисляем выражение: A * A^T – K * F^-1:')

        try:
            F_obr = np.linalg.inv(F)  # Обратная матрица F
            AAT = A * AT  # A * A^T
            KF_obr = F_obr * k  # K * F^-1
            result = AAT - KF_obr  # A * A^T – K * F^-1

            print(f'\nОбратная матрица F:\n{F_obr}')
            print(f'\nРезультат A * A^T:\n{AAT}')
            print(f'\nРезультат K * F^-1:\n{KF_obr}')
            print(f'\nРезультат A * A^T – K * F^-1:\n{result}')
        except np.linalg.LinAlgError:
            print("Одна из матриц является вырожденной (определитель равен 0),"
                  " поэтому обратную матрицу найти невозможно. Перезапустите программу.")
            quit()
    else:
        print(f'\nОпределитель матрицы А({int(det_A)})')
        print(f'меньше суммы диагональных элементов матрицы F({int(sum_det_F)}) или равен ей')
        print('поэтому вычисляем выражение (A^Т + G - F^Т) * K:')

        FT = np.transpose(F)  # Транспонированная матрица F

        ATG = AT + G  # A^Т + G
        ATGFT = ATG - FT  # A^T + G - F^T
        result = ATGFT * k  # (A^Т + G - F^Т) * K

        print(f'\nТранспонированная матрица F:\n{FT}')
        print(f'\nМатрица G:\n{G}')
        print(f'\nРезультат AТ + G:\n{ATG}')
        print(f'\nРезультат AТ + G - FT:\n{ATGFT}')
        print(f'\nРезультат (AТ + G - FТ) * K:\n{result}')
    # Построение графиков
    av = [np.mean(abs(F[i, ::])) for i in range(n)]
    av = int(sum(av))  # Сумма средних значений строк (используется при создании кругового графика)
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))  # Задание поля для графиков
    x = list(range(1, n + 1))
    for j in range(n):
        y = list(F[j, ::])
        # Обычный график
        axs[0, 0].plot(x, y, label=f'{j + 1} строка.')
        axs[0, 0].set(title='График с использованием функции plot:', xlabel='Номер элемента в строке',
                      ylabel='Значение элемента')
        axs[0, 0].grid()
        # Гистограмма
        axs[1, 0].bar(x, y, 0.4, label=f'{j + 1} строка.')
        axs[1, 0].set(title='График с использованием функции bar:', xlabel='Номер элемента в строке',
                      ylabel='Значение элемента')
        if n <= 10:
            axs[1, 0].legend(loc='lower right')
            axs[0, 0].legend(loc='lower right')
    # Круговой график
    explode = [0.03]
    for i in range(n-1):
        s = explode[0] + 0.02 * i
        explode.append(s)
    sizes = [round(np.mean(abs(F[i, ::])) * 100 / av, 1) for i in range(n)]
    axs[0, 1].set_title('График с использованием функции pie:')
    axs[0, 1].pie(sizes, labels=list(range(1, n + 1)), explode=explode, autopct='%1.1f%%', shadow=True)

    plt.suptitle('Использование библиотеки matplotlib')
    plt.tight_layout()
    plt.show()

    print('\nРабота программы завершена.')
except ValueError:  # Ошибка на случай введения не числа в качестве порядка или коэффициента.
    print('\nВведенный символ не является числом. Перезапустите программу и введите число.')
