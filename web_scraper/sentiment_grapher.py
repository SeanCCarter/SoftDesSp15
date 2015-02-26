import numpy as np
import matplotlib.pyplot as plt
from pickle import dump, load

sentiments = open("Sentiments_2.txt", 'r')
data = load(sentiments)

positive_sentiments = []
negative_sentiments = []
x = np.linspace(0, 31, len(data))
for sentiment in data:
	positive_sentiments.append(sentiment[1])
	negative_sentiments.append(sentiment[0])

print positive_sentiments
print negative_sentiments

# plt.plot(x, positive_sentiments)
# plt.show()

# matplotlib.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots()
ax.plot(x, positive_sentiments, 'o')
ax.plot(x, negative_sentiments, 'ro')
ax.set_title('Sentiment')
ax.legend()
plt.show()