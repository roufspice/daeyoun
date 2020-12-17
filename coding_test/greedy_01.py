def main():
    n, m, k = map(int, input().split())
    data = list(map(int, input().split()))
    data.sort()
    max = data[n-1]
    second_max = data[n-2]
    total_sum = 0

    while True:
        if m == 0:
            break
        for i in range(k):
            if m == 0:
                break
            total_sum += max
            m -= 1
        total_sum += second_max
        m -= 1



    print(total_sum)



if __name__ == '__main__':
    print(f'실행중...')

