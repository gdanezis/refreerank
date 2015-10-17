import csv
import matplotlib.pyplot as plt
import numpy as np

def getScores(f):
	scores = []
	with open(f) as fi:
		score_reader = csv.reader(fi)
		for score in score_reader:
			print score
			scores.append(float(score[0]))
	return scores


def main():
	score_file = "scores.csv"
	scores = getScores(score_file)
	print scores
	plt.hist(scores, bins=np.arange(0.4, 1.01, 0.01),log=True)
	plt.xlabel("Score")
	plt.ylabel("Frequency")
	plt.savefig("match_hist.pdf")
	plt.savefig("match_hist.png")
	plt.show()
	


if __name__ == "__main__":
	main()