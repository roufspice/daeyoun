import time
"""
변수를 직접가져다 쓰는건 좋지 않습니다. 
"""
class Citizen:
    """주민클래스"""
    drink_age = 19

    def __init__(self, name: str, age: int, resident_id):
        """이름, 나이, 주민번호"""
        self.name = name
        self.set_age(age) # setter 활용방법
        self._resident_id = resident_id

    def authenticate(self, id_field):
        """본인이 맞는지 확인하는 메소드"""
        return id_field == self._resident_id

    def can_drink(self):
        """음주가능나이인지 확인하는 메소드"""
        return self._age >= Citizen.drink_age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        print("나이를 수정합니다.")
        if value > 0:
            self._age = value
        else:
            print("올바른 입력을 해주세요")
            
            

    # def get_age(self):
    #     return self._age
    #
    # def set_age(self, value):
    #     if value > 0:
    #         self._age = value
    #     else:
    #         print("올바른 나이 값이 아닙니다. 다시입력해주세요")



