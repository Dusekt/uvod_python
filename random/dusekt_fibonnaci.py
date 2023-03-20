#iterace
n = 0
#hodnota funkce
y = 0

even_sum = 0
while y <= 5000000:

    #pro n = 0 je hodnota fce 0
    if n == 0:
        y1 = 0
        y = 0
    #pro n = 1 je hodnota fce 0
    elif n == 1:
        y2 = 1
        y = 1
    #pro n > 0 je hodnota funkce soucet predchozich 2 clenu
    elif n > 1:
        y = y1 + y2
        y1 = y2
        y2 = y
    #pokud je hodnota y suda, pricte ji k promenne even_sum
    if y%2 == 0:
        even_sum += y

    n += 1

print(even_sum)

