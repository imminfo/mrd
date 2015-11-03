import subprocess
import sys


def parse_links_and_search(link_path, cl_file, num_err, postfix = ""):
	patterns = []

	with open(cl_file) as pattern_file:
		# name - sequence - prob - vseg
		patterns = [tuple(x.strip().split()) for x in pattern_file]


	grep_res = {p: [] for p in patterns}
	sample_list = []
	with open(link_path) as infile:
		sample = ''
		for line in infile:
			line = line.strip()

			if line[0] == '#':
				sample = line[1:]
				if sample:
					sample_list.append(sample)
					patterns_to_search = set(patterns)

			elif line:
				target_file = line
				print("Searching in", target_file)
				for p in patterns:
					if p in patterns_to_search:
						print("\tSearching for", p[0], end = "\t")
						com = "agrep -" + str(num_err) + " " + p[1] + " " + target_file
						proc = subprocess.Popen(com, stdout = subprocess.PIPE, shell = True)
						grep_str_res = proc.communicate()[0].decode()
						if grep_str_res:
							counts = -2
							words = grep_str_res.split("\n")[0].split()
							for i in range(len(words)):
								if words[i] != "NA":
									try:
										counts = int(words[i])
									except Exception:
										counts = "undef"
									break
							grep_res[p].append(tuple([sample, target_file, str(counts), grep_str_res]))
							patterns_to_search.remove(p)
							print("MATCH")
						else:
							print("NOT FOUND")

	with open("clonal.counts." + postfix + ".txt", "w") as outfile:
		for p in grep_res:
			outfile.write(p[0] + "\t" + p[1] + "\t" + str(len(grep_res[p])) + '\n')

	with open("clonal.files." + postfix + ".txt", "w") as outfile:
		for p in grep_res:
			outfile.write(p[0] + "\t" + p[1] + "\t" + str(len(grep_res[p])) + '\n')
			for x in sorted(grep_res[p]):
				outfile.write("|".join(x[:-1]) + '\n')

	with open("clonal.tables." + postfix + ".txt", "w") as outfile:
		outfile.write("Pattern\tProbability\tSequence\t#People\t" + "\t".join(sample_list) + "\n")
		for p in grep_res:
			outfile.write(p[0] + "\t" + p[2] + "\t" + p[1]+  "\t" + str(len(grep_res[p])) + '\t')
			in_samples = {x[0]: x[2] for x in grep_res[p]}
			for sample in sample_list:
				if sample in in_samples:
					outfile.write(str(in_samples[sample]) + '\t')
				else:
					outfile.write("0" + '\t')
			outfile.write('\n')

	with open("clonal.lines." + postfix + ".txt", "w") as outfile:
		for p in grep_res:
			outfile.write(p[0] + "\t" + p[1] + "\t" + p[3] + str(len(grep_res[p])) + '\n')
			for x in sorted(grep_res[p]):
				outfile.write(x[0] + ":" + x[1] + "\n" + x[-1] + '\n')


if __name__ == '__main__':
	parse_links_and_search(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) == 5 else "")