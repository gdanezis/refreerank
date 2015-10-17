import csv
import matplotlib.pyplot as plt
import numpy as np
from parse_outputs import parse_outputs


def getFracFound(f):
	institution_scores = {}
	with open(f, "r") as fi:
		parser = csv.reader(fi)
		for row in parser:
			institution_scores[row[0]] = (float(row[1]), float(row[2]))
	return institution_scores

def getScores(f):
	scores = []
	with open(f) as fi:
		score_reader = csv.reader(fi)
		for score in score_reader:
			print score
			scores.append(float(score[0]))
	return scores

def plot_scores():
	score_file = "scores.csv"
	scores = getScores(score_file)
	print scores
	plt.hist(scores, bins=np.arange(0.4, 1.01, 0.01),log=True)
	plt.xlabel("Score")
	plt.ylabel("Frequency")
	plt.savefig("match_hist.pdf")
	plt.savefig("match_hist.png")
	plt.show()

def plot_outcomes():

	dblp_dict = getFracFound("fraction_found.csv")
	outcome_dict = parse_outputs("data/Outcomes.csv")

	found_people = []
	found_papers = []
	frac_4 = []
	for k, (v1, v2) in dblp_dict.iteritems():
		outcome = outcome_dict[k][0]
		print v1, v2, outcome
		found_people.append(float(v1))
		found_papers.append(float(v2))
		frac_4.append(float(outcome))
	plt.scatter(found_people, frac_4, color="b", label="people")
	plt.scatter(found_papers, frac_4, color="r", label="papers")
	plt.ylabel("Percentage 4*")
	plt.xlabel("Percentage Found")
	plt.legend()
	plt.show()

def main():
	plot_outcomes()	


if __name__ == "__main__":
	main()