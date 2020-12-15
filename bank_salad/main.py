import json
import os

# json 불러오기
card_name_list = []
checking_list_equal = []
checking_list = []

base = os.getcwd()
input_file_name = 'task1_input.json'
card_file_name = 'card.json'

input_path = os.path.join(base, input_file_name)
card_path = os.path.join(base,card_file_name)


with open(input_path, 'r', encoding='UTF8') as file_json:
    input_data = json.load(file_json)

with open(card_path, 'r', encoding='UTF8') as f:
    card_data = json.load(f)

# card_json 확인

for card in card_data:
    # print(card['name'])
    # name 조회
    if not card['name'] in card_name_list:
        card_name_list.append(card['name'])

# print(card_name_list)


for input in input_data:
    for card in card_data:
        if input['company_name'] == card['company_name'] and input['name'] == card['name']:
            # print(card['card_id'], "모두일치 카드이름 확인")
            checking_list.append(card['card_id'])

# print(len(checking_list))

