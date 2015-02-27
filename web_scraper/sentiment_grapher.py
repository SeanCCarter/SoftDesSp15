import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pickle import dump, load

sentiments = open("Sentiments.txt", 'r')
data = load(sentiments)

#Creates lists with the correct sentiment data
positive_sentiments = []
negative_sentiments = []
x = np.linspace(0, 31, len(data))
for sentiment in data:
	positive_sentiments.append(sentiment[0])
	negative_sentiments.append(sentiment[1])


fig, ax = plt.subplots()
ax.plot(x, positive_sentiments, 'o')
ax.plot(x, negative_sentiments, 'ro')
ax.set_title('Sentiment')
plt.xlabel('Book Arc')
plt.ylabel('Sentiment (polarity)')
plt.xlim([0, 31])
plt.legend(['Most Positive Sentiment (per chapter)', 'Most Negative Sentiment (per chapter)'])
plt.show()