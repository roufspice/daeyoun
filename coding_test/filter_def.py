# filter 내장 함수: 여러 개의 데이터로 부터 일부의 데이터반 추려낼 때 사용합니다.
# 여러 개의 데이터를 담고 있는 list나 tuple을 대상으로 주로 사용하는 함수 입니다.

users = [
    {'mail': 'gregorythomas@gmail.com', 'name': 'Brett Holland', 'sex': 'M'},
    {'mail': 'hintoncynthia@hotmail.com', 'name': 'Madison Martinez', 'sex': 'F'},
    {'mail': 'wwagner@gmail.com', 'name': 'Michael Jenkins', 'sex': 'M'},
    {'mail': 'daniel79@gmail.com', 'name': 'Karen Rodriguez', 'sex': 'F'},
    {'mail': 'ujackson@gmail.com', 'name': 'Amber Rhodes', 'sex': 'F'}
]

def is_man(user):
    return user["sex"] == "M"

for man in filter(is_man, users):
    print(man)

# 람다함수로 필터링
for woman in filter(lambda x: x["sex"] != "M", users):
    print(woman)

# 람다함수로 여성만 가져오기
print("===============")
woman_list = list(filter(lambda x: True if x["sex"] == "F" else False, users))
print(woman_list)

#filter 함수의 결과값을 list로 변환하는 가장 쉬운 방법: list() 내장 함수를 사용!




