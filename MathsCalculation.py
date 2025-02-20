import math
import sys
from decimal import Decimal


def trans_to_RPN(item:list) -> list:
    """
    将字符串转为后缀表达式
    """
    List = []
    math1 = []
    s = []
    subtract = False
    transformed_symbol = False
    item1 = [i for i in item if len(i) != 0]
    operator = False
    for i in item1:
        if i == '(':
            operator = True
            List.append(i)
            s.append(len(List))
        elif i == ')':
            operator = False
            subtract = False
            b = s[-1]
            del s[-1]
            while len(List) > 0:
                c = List[-1]
                if c in '+-*/':
                    math1.append(c)
                del List[-1]
        elif i in ['+', '-', '*', '/']:
            if i in ['+', '-']: # '-' may appear before '(', in some cases there's need to reverse the symbol from
                # '-' to '+' because the '-'(in the original formula) is OUTSIDE the parenthesis.
                if len(List) > 0:
                    if '-' in List:
                        if not operator:# means it can not take the opposite of a number
                            if not transformed_symbol: # means the symbol is original INSTEAD of changed one.
                                subtract = True
                            else: # means the symbol '-' comes from the last transformation at this place
                                # so it is NOT the one inside the formula, so no transformation needed
                                subtract = False
                                transformed_symbol = False
                        else:operator = False

                    c = List[-1]
                    if c in ['*', '/']:
                        while len(List) > 0:
                            last = List[-1]
                            if last in '+-*/':
                                math1.append(last)
                            del List[-1]
                if subtract and not operator: # isn't taking the opposite
                    if i == '+':List.append('-')
                    else:List.append('+')# 'i' is '-' and it is the one inside the formula. so reverse needed.
                    transformed_symbol = True
                else:
                    List.append(i)
            else:
                List.append(i)

            if not operator:
                operator = True
            else:
                if i == '-':
                    operator = False

        else:
            operator = False
            math1.append(i)
    while len(List) > 0:
        c = List[-1]
        math1.append(c)
        del List[-1]
    for i, j in zip(math1, range(len(math1))):
        if i == '':
            del math1[j]
    return math1


def turn_normal_expr_to_internal_expr(item: str|list|tuple):
    loc = 0
    file = item
    num_left = 0  # [ number
    num_right = 0  # ] number
    operator = False
    # '-' can only appear after an operator. such as '4 + -2', and '4 - --2' is illegal
    for i in file:
        if i in ['+', '-', '/', '*', '(', ')']:
            if i == '(' or i == ')':
                operator = True
            if num_left == num_right:
                if operator and i == '-':
                    operator = False
                else:
                    if not operator: operator = True
                    file = file[0:loc] + ' ' + i + ' ' + file[loc + 1:len(file)]
                    loc += 2
            else:
                if operator and i == '-':
                    operator = False

        elif i == '[':
            num_left += 1
            operator = True
        elif i == ']':
            num_right += 1
            operator = True
        else:
            operator = False
        loc += 1
    return file


def __calculation(inputting: str, outputting: list, index: int):
    # 计算的函数

    if inputting == '+':
        m = outputting[index - 2]
        g = outputting[index - 1]
        #print(m, g, 'calculating+')
        if str(g)[0] == '[' and str(g)[-1] == ']':
            g = Calculation(turn_normal_expr_to_internal_expr(str(g)[1:-1]))
        if str(m)[0] == '[' and str(m)[-1] == ']':
            m = Calculation(turn_normal_expr_to_internal_expr(str(m)[1:-1]))
        if m == '+':
            del outputting[index - 2]
            outputting[index-1] = Decimal(g)
        else:
            del outputting[index - 2]
            del outputting[index - 2]
            outputting[index - 2] = Decimal(m) + Decimal(g)
    elif inputting == '-':
        m = outputting[index - 2]
        g = outputting[index - 1]
        #print(m, g, 'calculating-')
        if str(g)[0] == '[' and str(g)[-1] == ']':
            g = Calculation(turn_normal_expr_to_internal_expr(str(g)[1:-1]))
        if str(m)[0] == '[' and str(m)[-1] == ']':
            m = Calculation(turn_normal_expr_to_internal_expr(str(m)[1:-1]))
        if m == '-':
            del outputting[index - 2]
            outputting[index - 1] = -Decimal(g)
        else:
            del outputting[index - 2]
            del outputting[index - 2]
            outputting[index - 2] = Decimal(m) - Decimal(g)
    elif inputting == '/':
        m = outputting[(index - 2)]
        g = outputting[(index - 1)]
        # print(m, g, 'calculating/')
        if str(g)[0] == '[' and str(g)[-1] == ']':
            g = Calculation(turn_normal_expr_to_internal_expr(str(g)[1:-1]))
        if str(m)[0] == '[' and str(m)[-1] == ']':
            m = Calculation(turn_normal_expr_to_internal_expr(str(m)[1:-1]))
        del outputting[index - 2]
        del outputting[index - 2]
        outputting[index - 2] = (Decimal(m) / Decimal(g))
    elif inputting == '*':
        m = outputting[(index - 2)]
        g = outputting[(index - 1)]
        # print(m, g, 'calculating*')
        if str(g)[0] == '[' and str(g)[-1] == ']':
            g = Calculation(turn_normal_expr_to_internal_expr(str(g)[1:-1]))
        if str(m)[0] == '[' and str(m)[-1] == ']':
            m = Calculation(turn_normal_expr_to_internal_expr(str(m)[1:-1]))
        del outputting[index - 2]
        del outputting[index - 2]
        outputting[index - 2] = (Decimal(m) * Decimal(g))
    else:
        pass


def Calculation(item1: str, mode: str = 'RAD'):
    if item1 == '':
        return ''
    try:
        if Decimal(item1):
            return item1
    except:
        pass
    M = 0
    for i in item1:
        if i == '+' or i == '-' or i == '/' or i == '*':
            M += 1
    """
    -----------------------------
    - version: 7.0  -------------
    - develop time: 2025-1-16  --
    -----------------------------
    """

    if item1 == '':
        return ''

    d = item1.count('(')
    f = item1.count(')')
    if d != f:
        if d > f:
            return 'ERROR,"("is not close'
        else:
            return 'ERROR,unmatched ")"'
    try:
        return Decimal(item1)
    except Exception as e:
        pass
    item2 = item1
    item1 = str(item2).split(' ')
    item = trans_to_RPN(item1)
    #print('after trans:', item)
    for i in item:
        r = 0
        for a in i:
            if a in ['+', '-', '*', '/', '^']:
                r += 1
        if i.count('.') > r + 1:
            return 'ERROR! Unmatched "." !'
    for i in item:
        if '^' in i:
            if not any(
                    [k in i for k in ["sin", "cos", "tan", 'arcsin', "arccos", "arctan", "log", "ln", "root", 'min']]):
                if '[' not in i and ']' not in i:
                    item[item.index(i)] = Decimal(i.split('^')[0]) ** Decimal(i.split('^')[1])
                else:
                    a = str(i.split('^')[0])
                    b = str(i.split('^')[1])
                    if '[' in a and ']' in a:
                        a = Calculation(turn_normal_expr_to_internal_expr(a), mode)
                    if '[' in b and ']' in b:
                        b = Calculation(turn_normal_expr_to_internal_expr(b), mode)
                    item[item.index(i)] = Decimal(a) ** Decimal(b)
            else:
                k = i
                while '[' in k and ']' in k:
                    k = k.split('[')[1][0:-1]
                a = str(k.split('^')[0])
                b = str(k.split('^')[1])
                if '[' in a and ']' in a:
                    a = Calculation(turn_normal_expr_to_internal_expr(a), mode)
                if '[' in b and ']' in b:
                    b = Calculation(turn_normal_expr_to_internal_expr(b), mode)
                item[item.index(i)] = item[item.index(i)].replace(k, str(Decimal(a) ** Decimal(b)))

    # 函数检测
    loc = 0
    for j in item:
        if 'sin' in str(j):
            if mode == 'RAD':
                if 'arc' in j:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.asin(Decimal(j.split(';')[1]))
                    else:
                        item[loc] = math.asin(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'RAD'))

                else:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.sin(Decimal(j.split(';')[1]))
                    else:
                        item[loc] = math.sin(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'RAD'))
            else:
                if 'arc' in j:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.asin(math.radians(Decimal(j.split(';')[1])))
                    else:
                        item[loc] = math.asin(math.radians(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'DEG')))
                else:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.sin(math.radians(Decimal(j.split(';')[1])))
                    else:
                        item[loc] = math.sin(math.radians(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'DEG')))
        elif 'cos' in str(j):
            if mode == 'RAD':
                if 'arc' in j:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.acos(Decimal(j.split(';')[1]))
                    else:
                        item[loc] = math.acos(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'DEG'))
                else:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.cos(Decimal(j.split(';')[1]))
                    else:
                        item[loc] = math.cos(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'DEG'))
            else:
                if 'arc' in j:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.acos(math.radians(Decimal(j.split(';')[1])))
                    else:
                        item[loc] = math.acos(math.radians(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'RAD')))
                else:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.cos(math.radians(Decimal(j.split(';')[1])))
                    else:
                        item[loc] = math.cos(math.radians(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'RAD')))
        elif 'tan' in str(j):
            if mode == 'RAD':
                if 'arc' in j:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.atan(Decimal(j.split(';')[1]))
                    else:
                        item[loc] = math.atan(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'RAD'))
                else:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.tan(Decimal(j.split(';')[1]))
                    else:
                        item[loc] = math.tan(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'RAD'))
            else:
                if 'arc' in j:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.atan(math.radians(Decimal(j.split(';')[1])))
                    else:
                        item[loc] = math.atan(math.radians(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'DEG')))
                else:
                    if not (('[' in j) and (']' in j)):
                        item[loc] = math.tan(math.radians(Decimal(j.split(';')[1])))
                    else:
                        item[loc] = math.tan(math.radians(Calculation(turn_normal_expr_to_internal_expr(j[j.index('[') + 1:-1]), 'DEG')))
        else:
            if '!' in str(j):
                if not (('[' in j) and (']' in j)):
                    try:
                        item[loc] = (math.factorial(int(j.split('!')[0])))
                    except TypeError:
                        return 'ERROR'
                else:
                    try:
                        item[loc] = (math.factorial(int(Calculation(turn_normal_expr_to_internal_expr(j.split('!')[0][j.index('[') + 1:-1])))))
                    except TypeError:
                        return 'ERROR'
            else:
                if ';' in str(j):
                    return 'ERROR'
                else:
                    if 'root' in str(j):
                        if not (('[' in j) and (']' in j)):
                            try:
                                a = j.split('root')[0]
                                b = j.split('root')[1]
                                try:
                                    item[loc] = int(b) ** (1 / int(a))
                                except ValueError:
                                    item[loc] = Decimal(b) ** (1 / Decimal(a))
                            except ValueError:
                                return 'TYPE ERROR,must be int or float'
                        else:
                            a = j.split('root')[0]
                            b = j.split('root')[1]
                            try:

                                b = b[1:-1]
                                b = Decimal(b)
                            except:
                                if ('[' in a) and (']' in a):
                                    a = Calculation(turn_normal_expr_to_internal_expr(a[j.index('[') + 1:-1]))
                                else:
                                    b = Calculation(turn_normal_expr_to_internal_expr(b))
                            try:
                                item[loc] = int(b) ** (1 / int(a))
                            except ValueError:
                                item[loc] = Decimal(b) ** (1 / Decimal(a))
                    elif 'log' in str(j):
                        a = j.split('log')[0]
                        b = j.split('log')[1]
                        if not (('[' in j) and (']' in j)):
                            a = j.split('log')[0]
                            b = j.split('log')[1]
                            try:
                                item[loc] = math.log(int(b), int(a))
                            except ValueError:
                                item[loc] = math.log(Decimal(b), Decimal(a))
                        else:
                            if ('[' in a) and (']' in a):
                                a = Calculation(turn_normal_expr_to_internal_expr(j.split('log')[0][j.index('[') + 1:-1]))
                            else:
                                a = Decimal(j.split('log')[0])
                            b = Calculation(turn_normal_expr_to_internal_expr(j.split('log')[1][j.index('[') + 1:-1]))
                            try:
                                item[loc] = math.log(int(b), int(a))
                            except ValueError:
                                item[loc] = math.log(Decimal(b), Decimal(a))
                    elif 'ln' in str(j):
                        if not (('[' in j) and (']' in j)):
                            b = j.split('ln')[1]
                            if type(b) == int:
                                item[loc] = math.log(int(b), math.e)
                            else:
                                item[loc] = math.log(Decimal(b), math.e)
                        else:
                            b = Calculation(turn_normal_expr_to_internal_expr(j.split('ln')[1][j.index('[') + 1:-1]))
                            if type(b) == int:
                                item[loc] = math.log(int(b), math.e)
                            else:
                                item[loc] = math.log(Decimal(b), math.e)
                    elif 'mis' in str(j):
                        if not (('[' in j) and (']' in j)):
                            item[loc] = -Decimal(j[3:])
                        else:
                            item[loc] = -Decimal(Calculation(turn_normal_expr_to_internal_expr(j.split('mis')[1][j.index('[') + 1:-1])))
                    elif '%' in str(j):
                        if not (('[' in j) and (']' in j)):
                            item[loc] = Decimal(j[0:-1]) / 100
                        else:
                            item[loc] = Decimal(Calculation(turn_normal_expr_to_internal_expr(j.split('%')[1][j.index('[') + 1:-1]))) / 100
                    elif ';' in str(j):
                        item[loc] = Calculation(turn_normal_expr_to_internal_expr(j[1:]))
        loc += 1
    # 计算
    index = 0
    while len(item) != 1:
        p = item[index]
        __calculation(p, item, index)
        if p == '+' or p == '-' or p == '*' or p == '/':
            index = 0
            continue
        index += 1
        if index > len(item):
            index = 0
    try:
        n = Decimal(item[0])
    except TypeError or ValueError as e:
        #print(str(e))
        return str(e)
    return n


#
# 计算试例  ∮∭∬∑±∫∰∯
if __name__ == '__main__':
    #print(trans_to_RPN('9 - ( 1 * 10 + ( 3 + 1 ) ) '.split(' ')))
    #print(trans_to_RPN('- + 3'.split(' ')))
    #print(Calculation(turn_normal_expr_to_internal_expr('1--4+-(101-2)')))
    print(turn_normal_expr_to_internal_expr('1--4-(101-2)'), 'exp')
    #print(trans_to_RPN('1 - -4 - ( 101 - 2 ) '.split(' ')), 'exp2')
    #1 - -4 - ( 101 - 2 )
    #print(trans_to_RPN('9 + ( -7 + -2 )'.split(' ')))
    #print(turn_normal_expr_to_internal_expr('(1--2)+3-4-12-(-(3-5))'))
    # ( 1 - -2 ) + 3 - 4 - 12 - ( - ( 3 - 5 ) )
    #print(turn_normal_expr_to_internal_expr('1 - ( 2 - 4 + 5 ) '))
