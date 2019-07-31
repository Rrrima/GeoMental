import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def draw_train_size():
	sns.set(style="white")
	data = pd.read_excel('analysis/tr2_train_size.xlsx')
	#print(data)
	sns.lineplot(x="train_size", y="accuracy",
	             hue="alg", style='alg',data=data)
	plt.show()

def draw_alg_acc():
	sns.set(style="whitegrid")
	data = pd.read_excel('analysis/tr2_alg_acc.xlsx')
	#print(data)
	sns.stripplot(x="accuracy", y="alg", hue="dataset",
              data=data, dodge=True, jitter=True,
              alpha=.65, zorder=1)
	sns.pointplot(x="accuracy", y="alg", hue="dataset",
              data=data, dodge=.532, join=False, palette="dark",
              markers="d", scale=.75, ci=None)
	sns.boxplot(x="accuracy", y="alg", hue="dataset",
              data=data,orient="h")
	plt.show()

def draw_alg_region():
	sns.set(style="whitegrid")
	data = pd.read_excel('analysis/alg_region.xlsx')
	sns.boxplot(x="alg", y="accuracy",
              data=data,palette='Blues')
	plt.show()

def draw_heatmap():
	sns.set(style="ticks")
	data = pd.read_excel('analysis/plsr_heatmap.xlsx')
	print(data)
	sns.heatmap(data.T, annot=False,cmap="YlGnBu")
	plt.show()


def draw_stackbar():
	data = pd.read_excel('analysis/stackbar.xlsx')
	plt.show()
	sns.barplot(x="TestSize", y="AF", data=data, capsize=.2,palette='Blues')
	#sns.barplot(x="TestSize", y="FN", data=data, capsize=.2,color="salmon")
	plt.ylim(0.1,0.4)
	plt.show()

draw_alg_acc()