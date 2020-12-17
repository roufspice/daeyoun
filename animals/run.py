# 조합형 iterator
import itertools
from collections import Counter
data = ['A', 'B']

#permutations 순열 -> index중심
data_01 = list(itertools.permutations(data, r=2))
# print(data_01)
# print(len(data_01))
#
# #combinations: 조합 -> value중심
# data_02 = list(itertools.combinations(data, r=2))
# print(data_02)
# print(len(data_02))
#
# # product: 순열, 독립시행
# data_03 = list(itertools.product(data, repeat=2))
# print(data_03)
# print(len(data_03))
#
# # combinations_with_replacement()
# data_04 = list(itertools.combinations_with_replacement(data, r=2))
# print(data_04)
# print(len(data_04))




