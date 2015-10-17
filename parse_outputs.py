import csv

def parse_outputs(f):
	intitution_outputs = {}
	with open(f, "r") as fr:
		parser = csv.reader(fr)
		for row in parser:
			if row[3] == "Outputs":
				intitution_outputs[row[0]] = (float(row[4]), float(row[5]), float(row[6]), float(row[7]))
				#print row[0], row[4], row[5], row[6], row[7]
	return intitution_outputs

def main():
	outputs = parse_outputs("data/Outcomes.csv")
	for k, v in outputs.iteritems():
		print k, v


if __name__ == "__main__":
	main()