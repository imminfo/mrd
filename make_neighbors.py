import sys


def make_neighbors(line):

	def realign_v(nuc_seq, var_seq):
		res = -1
		error = -2
		for i in range(min(len(nuc_seq), len(var_seq))):
			if nuc_seq[i] != var_seq[i]:
				if error != -2:
					if error == i - 1:
						res = i - 2
					else:
						res = i - 1
					break
				else:
					error = i
			else:
				res = i

		return res + 1


	def realign_j(nuc_seq, joi_seq):
		res = -1
		error = -2
		nuc_seq = nuc_seq[::-1]
		joi_seq = joi_seq[::-1]
		for i in range(min(len(nuc_seq), len(joi_seq))):
			if nuc_seq[i] != joi_seq[i]:
				if error != -2:
					if error == i - 1:
						res = i - 2
					else:
						res = i - 1
					break
				else:
					error = i
			else:
				res = i

		# print("!!!")
		# print(nuc_seq[:res+1] + "|" + nuc_seq[res+1:])
		# print(joi_seq[:res+1] + "|" + joi_seq[res+1:])
		# print(len(nuc_seq) - res)
		return len(nuc_seq) - res

	words = line.split("\t")

	var_lib = {}
	joi_lib = {}

	with open("trbv.txt") as file:
		file.readline()
		for line in file:
			line = line.strip().split('\t')
			var_lib[line[0]] = line[11]

	with open("trbj.txt") as file:
		file.readline()
		for line in file:
			line = line.strip().split('\t')
			joi_lib[line[0]] = line[1]

	res = []
	nuc = words[0]
	var = words[2]
	joi = words[4]
	vend = int(words[5])
	jstart = int(words[8])
	meta = words[9]

	k = 1
	res.append(words)
	res[0][9] = res[0][9] + "(0)"
	for pos in range(len(nuc)):
		for letter in ['A', 'C', 'G', 'T']:
			if nuc[pos] != letter:
				new_nuc = nuc[:pos] + letter + nuc[pos+1:]
				new_vend = vend
				new_jstart = jstart
				new_vend = realign_v(new_nuc, var_lib[var])
				new_jstart = realign_j(new_nuc, joi_lib[joi])
				new_meta = meta + "(" + str(k) + ")"
				k += 1
				res.append((new_nuc, "", var, "", joi, new_vend, "", "", new_jstart, new_meta))

	return res


def process(filepath):
	with open(filepath) as infile:
		with open("mrd_neis.txt", "w") as outfile:
			outfile.write(infile.readline())
			for line in infile:
				line = line.strip()
				neis = make_neighbors(line)
				for nei in neis:
					outfile.write("\t".join(map(str, nei)) + "\n")
				# break


if __name__ == "__main__":
	process(sys.argv[1])