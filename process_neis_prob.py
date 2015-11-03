import sys
import math


def process(filepath):
	with open(sys.argv[1]) as prob_file:
		with open("mrd_neis.txt") as orig_file:
			with open("mrd_neis_prob_summary.txt", "w") as outfile:
				orig_file.readline()
				pattern = ''
				prob = 0
				orig_prob = 0
				for line in prob_file:
					new_prob = float(line.strip())
					new_pattern = orig_file.readline().strip().split("\t")[9]
					new_pattern = new_pattern[:new_pattern.find("(")]
					if new_pattern == pattern:
						prob += new_prob
					else:
						if orig_prob != 0:
							outfile.write(pattern + "\t" + str(orig_prob) + "\t" + str(prob) + "\t" + str(math.log(prob / orig_prob, 10)) + "\n")
						else:
							outfile.write("zero\n")
						pattern = new_pattern
						prob = new_prob
						orig_prob = new_prob


if __name__ == "__main__":
	process(sys.argv[1])