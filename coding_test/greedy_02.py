"""숫자 카드 게임"""
# 각 행을 돌면서 가장 낮은 숫자가 적힌 카드를 뽑는다.
# 그중 가장 큰 수를 찾으면 된다.
# min(), max() 함수를 어떻게 활용하는가에 대한 질문이다.

# 한줄 씩 입력받아 확인
def test():
    answer = 0
    n, m = map(int, input().split())
    # 한줄 씩 2차원 배열로 입력받는 법
    for i in range(n):
        # row가 n인 데이터 입력받기
        data = list(map(int, input().split()))
        min_value = min(data)
        answer = max(answer, min_value)

    return answer


def test_01():
    n, m = map(int, input().split())
    answer = 0
    for i in range(n):
        data = list(map(int, input().split()))
        min_value= 10001
        for j in data:
            min_value = min(min_value, j)
        answer = max(answer, min_value)

    return answer


if __name__ == '__main__':
    result = test()
    print(result)
