from pathlib import Path
import json
import os
import tablib


class IpaclabBug:
    """ipactory 크롤링 버그체크 클래스"""
    def __init__(self, base_path):
        """json 파일 기본경로 설정"""
        self._base_path = LoadJson(base_path)
        self._json_data = {}


class LoadJson:
    """json파일 관리하는 클래스"""
    def __init__(self, base_path):
        self._base_path = base_path
        self._json_data = {}


    def load_json(self):
        """json 파일 불러오는 메소드"""
        directory = os.path.join(self._base_path)
        p = Path(directory)

        if p.exists():
            with open(p, 'r', encoding='UTF8') as f_json:
                json_data = json.load(f_json)
            if type(json_data) == list:
                json_data = json_data[0]
            self._json_data = json_data
            return self._json_data

        else:
            print("올바른 경로를 확인해주세요")

    def __str__(self):
        return f'{self._base_path} 경로의 파일을 불러왔습니다.'


class BugCheck:
    """버그가 있는 번역문을 확인하는 클래스"""
    def __init__(self, base_path):
        """json_data 업로드"""
        self._json_data = LoadJson(base_path).load_json()
        self.is_bug_exists = []


    def get_bugs(self):
        """버그가 존재하는 tranNum keys를  리스트로 리턴함
            총 갯수의 일치여부로 버그를 판단"""
        json_data = self._json_data

        for key, value in json_data.items():
            bug_counts = 0
            is_bug_exists = False
            tran_num = key

            desc_origin_counts = len(json_data[tran_num]['desc']['origin'])
            desc_trans_counts = len(json_data[tran_num]['desc']['trans'])
            claims_origin_counts = len(json_data[tran_num]['claims']['origin'])
            claims_trans_counts = len(json_data[tran_num]['claims']['trans'])

            is_bug_exists = True if desc_origin_counts != desc_trans_counts or claims_origin_counts != claims_trans_counts else False

            if is_bug_exists:
                self.is_bug_exists.append(tran_num)

        return self.is_bug_exists


class BugInform:
    """버그가 있는 번역문들의 갯수를 알려주는 클래스"""
    def __init__(self, base_path, status=2):
        self.status = str(status)
        self._json_data = LoadJson(base_path).load_json()
        self.total_is_status = [] # 작업상태 총 갯수 파악
        self.is_bug_exists = BugCheck(base_path).get_bugs()
        self.is_bug_inform = {} # 작업상태 중 버그의 총 갯수 파악



    def get_bug_inform(self):
        """작업상태에 따른 버그번역문 정보 리턴 메서드"""
        json_data = self._json_data
        for key, value in json_data.items():
            if value['is_transcripted'] == self.status:
                self.total_is_status.append(key)
                if key in self.is_bug_exists:
                    desc_origins = len(value['desc']['origin'].values())
                    desc_trans = len(value['desc']['trans'].values())
                    claims_origins = len(value['claims']['origin'].values())
                    claims_trans = len(value['claims']['trans'].values())
                    desc_result = abs(desc_origins - desc_trans) if desc_origins != desc_trans else 0
                    claims_result = abs(claims_origins - claims_trans) if claims_origins != claims_trans else 0

                    self.is_bug_inform[key] = {
                        'desc': desc_result,
                        'claims': claims_result
                    }
        return self.is_bug_inform, self.total_is_status

    def get_static(self):
        headers = ['순번', '원문번호1', '원문번호2', 'desc차이', 'claims차이', '작업자ID', 'is_transcripted']
        dataset = tablib.Dataset(headers=headers)
        idx = 0

        for key,value in self._json_data.items():
            if value['is_transcripted'] == self.status:
                if key in self.is_bug_exists:
                    desc_origins = len(value['desc']['origin'].values())
                    desc_trans = len(value['desc']['trans'].values())
                    claims_origins = len(value['claims']['origin'].values())
                    claims_trans = len(value['claims']['trans'].values())
                    # desc차이
                    desc_subs = abs(desc_origins - desc_trans) if desc_origins != desc_trans else 0
                    # claim차이
                    claims_subs = abs(claims_origins - claims_trans) if claims_origins != claims_trans else 0
                    # 순번
                    idx += 1
                    # 원문번호1
                    tran_num = key
                    # 원문번호2
                    original_num = value['originalNum']
                    # 작업자 ID
                    voucher = value['is_assgined']

                    dataset.append([
                        idx,
                        tran_num,
                        original_num,
                        desc_subs,
                        claims_subs,
                        voucher,
                        value['is_transcripted']
                    ])

        return dataset


base_path = os.path.join(os.getcwd(), 'json', 'ipaclab_crawler/ipaclab_trans_1471_tot.json')
export_path = os.path.join(os.getcwd(), 'statistic/ipaclab_statistics_1211.xlsx')
print(base_path)
bug_check_01 = BugCheck(base_path)
bug_inform_01 = BugInform(base_path, status=2)
dataset = bug_inform_01.get_static()
print(dataset)

with open(export_path, 'wb') as f_output:
    f_output.write(dataset.export('xlsx'))





# json_02_path = os.path.join(os.getcwd(),'json/ipaclab_crawler/ipaclab_trans_1471_02.json')
# json_03_path = os.path.join(os.getcwd(), 'json/ipaclab_crawler/ipaclab_trans_1474_03.json')
# json_04_path = os.path.join(os.getcwd(), 'json/ipaclab_crawler/ipaclab_trans_1479_04.json')
#
#
#
# #json 불러오기
# with open(json_02_path, encoding='UTF8') as f_1:
#     data_01 = json.load(f_1)
#     print("loading__")
#
# with open(json_03_path, encoding='UTF8') as f_2:
#     data_02 = json.load(f_2)
#     print("loading__")
#
# with open(json_04_path, encoding='UTF8') as f_3:
#     data_03 = json.load(f_3)
#     print("loading__")
#
# # json합치기
# with open(os.path.join(os.getcwd(),'json/ipaclab_crawler/ipaclab_trans_1471_tot.json'), 'w', encoding='UTF8') as new_json:
#     json.dump(data_01+data_02+data_03, new_json, indent=4, ensure_ascii=False)
#     print("new file is created")

















