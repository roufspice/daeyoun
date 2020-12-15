class Employee:
    """ 직원클래스 """
    company_name = "h_burger"
    raise_percentage = 1.03

    def __init__(self, name, wage):
        """인스턴스 변수 설정"""
        self._name = name
        self._wage = wage

    def raise_pay(self):
        """직원 시급을 인상하는 메소드"""
        self.wage == self.raise_percentage

    def __str__(self):
        return f'{Employee.company_name} 직원: {self.name}'


class Cashier(Employee):
    def __init__(self, name, wage, number_sold):
        # self.name = name
        # self.wage = wage
        """super(_)"""
        # Employee.__init__(self, name, wage)
        super().__init__(name, wage)
        self.number_sold =number_sold

    def __str__(self):
        return f'계산대 직원:{self.name} 판매액:{self.number_sold}'



c1 = Cashier("둘리", 3000000, 50)
print(Cashier.mro())