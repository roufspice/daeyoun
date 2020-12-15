
"""함수의 다형성 """
def sum_numbers(*numbers, message):
    """*args: *하나가 붙으면 갯수가 정해지지 않는 파라미터"""
    print(message)

    return sum(numbers)

print(sum_numbers(1,2,3,4,5, message="hello world"))


