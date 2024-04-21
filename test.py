n = int(input("Istalgan sonni kiriting: "))
yigindi = 0
while n > 0:
    yigindi += n % 10
    n //= 10
print(f"Kiritilgan sonning raqamlar yig'indisi: {yigindi}")
