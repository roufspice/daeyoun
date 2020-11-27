from animals import dog # animals 패키지에서 dog 모듈을 가져와줘
from animals import cat
# from animals import *  : 지양하는 코드임 !!

d = dog.Dog()
d.do_dog()


c = cat.Cat()
c.do_cat()
