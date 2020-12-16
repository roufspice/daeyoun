def main():
    n, m, k = map(int, input().split())
    data = list(map(int, input().split()))
    #배열의 크기 n, 숫자가더해지는 횟수 m, 최대 반복 횟수 k
    # data의 최대값 두개만 가져오기
    data = sorted(data, reverse=True)
    max = data[0]
    while True:
        i = data.pop(0)
        if i != max:
            second = i
            break
    return (k * (m//k) * max + (m - (m//k)) * second)



if __name__ == '__main__':
    data = list(map(int, input().split()))
    a= data.sort()
    print(a)
