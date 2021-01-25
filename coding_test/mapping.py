users = [
    {'mail': 'gregorythomas@gmail.com', 'name': 'Brett Holland', 'sex': 'M'},
    {'mail': 'hintoncynthia@hotmail.com', 'name': 'Madison Martinez', 'sex': 'F'},
    {'mail': 'wwagner@gmail.com', 'name': 'Michael Jenkins', 'sex': 'M'},
    {'mail': 'daniel79@gmail.com', 'name': 'Karen Rodriguez', 'sex': 'F'},
    {'mail': 'ujackson@gmail.com', 'name': 'Amber Rhodes', 'sex': 'F'}
]

def conver_to_name(user):
    first, last = user["name"].split()
    return {"first": first, "last": last}


def run(users):

    # for name in map(conver_to_name, users):
    #     print(name)
    # 람다함수로 필터링
    result = list(map(lambda x: "남" if x["sex"] == "M" else "여", users))
    # map filter 보다는 list comprehension
    result = [user["name"] for user in users]


    return result


if __name__ == '__main__':
    print(run(users))
