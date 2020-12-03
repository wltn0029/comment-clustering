import numpy as np

korean_scores = [[-1, 1, 1, -1, -1, 1, -1, 1, -1, 1], [1, 1, 1, 1, -1, -1, 1, 1, 1]]
scores = [[-1, 1], [1]]



korean_scores = np.array(korean_scores).flatten()
scores = np.array(scores).flatten()
print(korean_scores)
print(scores)