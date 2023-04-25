# Тестовая часть

# 1. Создать программу, которая будет находить медиану списка из чисел, длинной до 20 чисел. Числа должны быть сгенерированы случайным образом.
# Если количество элементов в списке четное, медианой считается среднее значение двух центральных элементов, если нечетное - центральный элемент.

from random import randint


list = sorted(randint(1, 21) for i in range(randint(1, 20)))
print(list)
print(f"Длина списка: {len(list)}")
if len(list) % 2 == 0:
    print('чётное')
    mediana_chet = len(list) / 2
    print(f"Медиана: {(list[int(mediana_chet)-1] + list[int(mediana_chet)]) / 2}")
else:
    print("не чётное")
    mediana_ne_chet = (len(list) + 1) / 2
    print(f"Медиана: {list[int(mediana_ne_chet) - 1]}")




# 2. Написать функцию, которая принимает на вход список строк и возвращает новый список, состоящий из строк, содержащих только уникальные символы.
# Например, если на вход подается список ["hello", "world", "python"], то функция должна вернуть список ["heo", "wrd", "pytn"].

# lorem ipsum dolor sit amet amet amet
# ["hello", "world", "python"]

def unique_symbols():
    str1 = input("Ввод: ")
    str2 = ''
    for i in str1:
        if i == ' ' or i == '"' or i == ',' or i == "'":
            str2 += i
        elif i not in str2:
            str2 +=i
    print(f"Вывод: {str2}")
unique_symbols()



# 3. Напишите программу на Python, которая принимает на вход строку и выводит все ее подстроки, отсортированные в лексикографическом порядке.
# Например, для строки "abc" результатом работы программы должны быть строки "a", "ab", "abc", "b", "bc", "c".


# zxca
str1 = input("Ввод: ")
print(f"Оригинальная строка: {str1}")

test_str = ''
for i in sorted(str1):
    test_str += i
print(f"Сортированная строка: {test_str}")

res = [test_str[i: j] for i in range(len(test_str))
       for j in range(i + 1, len(test_str) + 1)]

print(f"Подстроки: {res}")






# 4. Напишите программу для поиска наибольшего общего делителя (НОД) двух чисел с помощью алгоритма Евклида. Программа должна принимать два целых числа и возвращать их НОД.


n1 = int(input("Введите 1-ое число: "))
n2 = int(input("Введите 2-ое число: "))
def nod(n1, n2):
    while n1 != 0 and n2 != 0:
        if n1 >= n2:
            n1 -= n2
        else:
            n2 -= n1
    if n1 != 0:
        print(f"НОД = {n1}")
    else:
        print(f"НОД = {n2}")
nod(n1, n2)

