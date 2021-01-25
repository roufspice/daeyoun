users = [
    {'mail': 'gregorythomas@gmail.com', 'name': 'Brett Holland', 'sex': 'M', 'age': 73},
    {'mail': 'hintoncynthia@hotmail.com', 'name': 'Madison Martinez', 'sex': 'F', 'age': 29},
    {'mail': 'wwagner@gmail.com', 'name': 'Michael Jenkins', 'sex': 'M', 'age': 51},
    {'mail': 'daniel79@gmail.com', 'name': 'Karen Rodriguez', 'sex': 'F', 'age': 32},
    {'mail': 'ujackson@gmail.com', 'name': 'Amber Rhodes', 'sex': 'F', 'age': 18}
]

# 여러 개의 데이터를 대상으로 주로 누적 집계를 내기 위해
# reduce(집계함수, 순회가능한 데이터[, 초기값])

from functools import reduce

print(reduce(lambda acc, cur: acc + cur["age"], users, 0))

# 유저의 이메일 목록도 reduce()함수를 이용하면 어렵지 않게 만들어 낼 수 있습니다.

print(reduce(lambda acc, cur: acc + [cur["mail"]], users, []))

# 초기값의 중요성 "
print(reduce(lambda acc, cur: acc + cur["age"], users))

