print('123')
a, b = map(int, input().split())
for i in range(a):
    print(b * b % 39)