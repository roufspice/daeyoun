users = [
    {'mail': 'gregorythomas@gmail.com', 'name': 'Brett Holland', 'sex': 'M'},
    {'mail': 'hintoncynthia@hotmail.com', 'name': 'Madison Martinez', 'sex': 'F'},
    {'mail': 'wwagner@gmail.com', 'name': 'Michael Jenkins', 'sex': 'M'},
    {'mail': 'daniel79@gmail.com', 'name': 'Karen Rodriguez', 'sex': 'F'},
    {'mail': 'ujackson@gmail.com', 'name': 'Amber Rhodes', 'sex': 'F'}
]


# List Comprehension
print([user for user in users if user["sex"] == "M"])

# List Comprehension
def list_comprehension_temp(users):
    dataset = [user for user in users if user["sex"] == "F"]
    return dataset

print(list_comprehension_temp(users))
