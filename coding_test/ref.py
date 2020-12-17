#permutations 순열 -> index중심
import itertools
from collections import Counter
data = list(map(int, input().split(',')))

#permutation 순열 :index 중심
# n개의 원소를 사용해서 순서를 정하여 r개의 배열로 나타내는 것을 말한다 순서0 nPr = n!/(n-r)!
data_01 = list(itertools.permutations(data, r=2))
print(data_01)
print(len(data_01))

#combinations: 조합 -> value중심
# n개의 원소를 사용해서 순서의 관계없이 r개의 배열로 나타내는 것 순서 X nCr = nPr/r!
data_02 = list(itertools.combinations(data, r=2))
print(data_02)
print(len(data_02))

# product: 순열, 독립시행
data_03 = list(itertools.product(data, repeat=2))
print(data_03)
print(len(data_03))

# combinations_with_replacement()
data_04 = list(itertools.combinations_with_replacement(data, r=2))
print(data_04)
print(len(data_04))
