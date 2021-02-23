import re
from datetime import timedelta, date

class User:
    EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+[^@]+")

    def __init__(self, user_name):
        self.user_name = user_name
        self._email = None

    @property
    def email(self):
        return self._email


    @email.setter
    def email(self, new_email):
        if not self._is_valid_email(new_email):
            print("유효한 이메일 아닙니다.")
            return

        self._email = new_email


    def _is_valid_email(self, email):
        return re.match(self.EMAIL_FORMAT, email) is not None




class DateRangeInterable:

    def __init__(self, start_date, end_date):
        print("__init__")
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        print("__iter__")
        return self

    def __next__(self):
        print("__next__")
        if self._present_day >= self.end_date:
            raise StopIteration

        today = self._present_day
        self._present_day += timedelta(days=1)
        return today


if __name__ == '__main__':
    for day in DateRangeInterable(date(2021,1,1), date(2021, 2, 28)):
        print(day)

