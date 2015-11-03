import sys


def hamming_dist(alpha, beta):
	if len(alpha) != len(beta):
		return -1

	dist = 0
	for i in range(len(alpha)):
		dist += 1 if alpha[i] != beta[i] else 0
	return dist


def parse_lines_file(filename):

	def get_sequence(words):
		tmp = 0
		res = ''

		try:
			tmp = float(words[2])
			res = words[3]
		except Exception:
			res = words[2]

		if not res: print("Empty string in NUC!!!")
		return res


	def get_v(words):
		res = ''

		for i in range(4, 8):
			if words[i].find("TRBV") != -1:
				res = list(map(lambda x: x.strip(), words[i].split(",")))
				for i in range(len(res)):
					if res[i].find("*") != -1:
						res[i] = res[i][:res[i].find("*")]
					break

		if not res: print("Empty string in V!!!")
		return res


	# { hamm dist: {pattern: [pattern_seq, vseg, { subj1: [(count1, seq1, vseg1), (count2, seq2, vseg2) ... ] } }
	db = {}

	with open(filename) as infile:
		pattern_body = False
		match_body = False

		name = ''
		seq = ''
		ith_match = 0
		max_matches = 0
		subject = ''
		vseg = ''

		for line in infile:
			line = line.strip()
			if line:
				if len(line.split()) == 3:
					# name, seq, vseg, max_matches = line.split()
					name, seq, max_matches = line.split()
					if max_matches == 0:
						pattern_body = False
				elif ":" in line and "/" in line:
					subject, _ = line.split(":")
					match_body = True
					ith_match += 1
				else:
					words = line.split()
					count = int(words[0])
					subj_seq = get_sequence(words)
					subj_v = get_v(words)

					hd = hamming_dist(seq, subj_seq)
					if hd != -1:
						if hd not in db:
							db[hd] = {}
						if name not in db[hd]:
							db[hd][name] = [seq, vseg, {}]
						if subject not in db[hd][name][2]:
							db[hd][name][2][subject] = []
						db[hd][name][2][subject].append((count, subj_seq, subj_v))

	return db


def write_subset(db, name):

	def aggregate_v(tuples):
		res = {}
		for _, _, vseg in tuples:
			for v in vseg:
				res[v] = res.get(v, 0) + 1
		return res

	with open("output.hamm" + str(name) + ".txt", "w") as outfile:
		for pattern, val in db.items():
			pseq, vseg, subjects = val
			outfile.write(pattern + "\t" + pseq + "\t" + str(len(subjects)) + "\n")
			summary = {}
			for subj in subjects:
				vs = aggregate_v(subjects[subj])
				outfile.write(subj)
				for v, cnt in vs.items():
					outfile.write("\t" + v + "(" + str(cnt) + ")")
				outfile.write("\n")
				if v not in summary:
					summary[v] = set()
				summary[v].add(subj)

			outfile.write("Summary:\t")
			for v, subjs in summary.items():
				outfile.write(v + "(" + str(len(subjs)) + ")" + "\t")
			outfile.write("\n\n")


if __name__ == "__main__":
	db = parse_lines_file(sys.argv[1])
	for key, val in db.items():
		write_subset(val, key)