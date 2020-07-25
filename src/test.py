game = 250
idx = game // 100

for i in range(idx + 1):
    for j in range(i * 100, i * 100 + 100):
        if j >= game:
            break
        else:
            print(j)
    print('=============================')