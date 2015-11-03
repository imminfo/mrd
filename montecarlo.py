from random import sample
import sys
import subprocess


def take_sample(filepath):

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

		for i in range(4, len(words)):
			if words[i].find("TRBV") != -1:
				res = list(map(lambda x: x.strip(), words[i].split(",")))
				# print("pre-res-sample", res)
				for i in range(len(res)):
					if res[i].find("*") != -1:
						res[i] = res[i][:res[i].find("*")]
				# print("res-sample", res)
				break

		return tuple(res)

	# compute number of lines
	# get random line numbers
	# extract and return desired clonotypes with V segments
	# return [(line number, CDR3, Vseg), ...]
	com = "wc -l " + filepath
	proc = subprocess.Popen(com, stdout = subprocess.PIPE, shell = True)
	n_lines = int(proc.communicate()[0].decode().split()[0])
	take = set(sample(range(1, n_lines), 63))
	patterns = []
	with open(filepath) as file:
		i = 0
		for line in file:
			if i in take:
				words = line.strip().split()
				patterns.append(tuple([i, get_sequence(words), get_v(words)]))
			i += 1
	
	return patterns


def cycle(link_path, takes, limit, output):

	def get_v(words):
		res = ''

		for i in range(4, 8):
			if words[i].find("TRBV") != -1:
				res = list(map(lambda x: x.strip(), words[i].split(",")))
				# print("pre-res", res)
				for i in range(len(res)):
					if res[i].find("*") != -1:
						res[i] = res[i][:res[i].find("*")]
				# print("res", res)
				break

		return tuple(res)


	res_stat = []

	# get dict with file paths from the file with links
	# leave only those files who has > limit clonotypes
	# { subject: [file1, file2, ...] }
	subject_files = {}
	with open(link_path) as infile:
		subject = ''
		for line in infile:
			line = line.strip()

			if line[0] == '#':
				subject = line[1:]
				if subject:
					subject_files[subject] = []

			elif line:
				com = "wc -l " + line
				proc = subprocess.Popen(com, stdout = subprocess.PIPE, shell = True)
				n_lines = int(proc.communicate()[0].decode().split()[0])
				print(n_lines, "\t", line, end = "\t")
				if n_lines >= limit:
					subject_files[subject].append(line)
					print("GOOD")
				else:
					print("BAD")

	# cycle through each people and peoples' files and get take samples
	# search sample clonotypes (CDR3 + V) in other that sampled subjects' files
	# compute statistics: how many clonotypes has been found in other subjects
	with open(output, "w") as outfile:
		cur_k = 1
		max_k = len(list(filter(lambda x: len(x) > 0, list(subject_files.values())))) * takes
		for subject in subject_files:
			files = subject_files[subject]
			if files:
				for take_i in range(takes):
					# print(take_i, "-th take from ", subject, sep = '')
					print("Iteration:", cur_k, "/", max_k, "\tFile:", files[take_i % len(files)])
					cur_k += 1
					sampled_clones = take_sample(files[take_i % len(files)])
					# print(sampled_clones)

					# patterns_to_search = set()
					patterns_to_search = set(sampled_clones)
					found_clones = {x[0]: [] for x in sampled_clones}
					with open(link_path) as infile:
						parsed_subject = ''
						for line in infile:
							line = line.strip()

							if line[0] == '#':
								parsed_subject = line[1:]
								# if subject:
								# 	subject_list.append(subject)
									# patterns_to_search = set(sampled_clones)

							elif line:
								if subject != parsed_subject:
									target_file = line
									# print("Searching in", target_file)
									for p in sampled_clones:
										if p in patterns_to_search:
											# print("\tSearching for", p[0], end = "\t")
											com = "grep -w '" + p[1] + "' " + target_file
											proc = subprocess.Popen(com, stdout = subprocess.PIPE, shell = True)
											grep_str_res = proc.communicate()[0].decode()
											if grep_str_res:
												# check V segments and update stats
												found_lines = grep_str_res.split("\n")
												for one_line in found_lines:
													if one_line.strip():
														# print("LINE:", one_line)
														words = one_line.split()
														# print("WORDS:", words)
														vs = get_v(words)
														# print("found v:", vs)
														# print("search in:", p[2])
														for v in vs:
															if v and v in p[2]:
																# print(p)
																# print(words)
																patterns_to_search.remove(p)
																found_clones[p[0]].append(subject)
																break

					found = len(list(filter(lambda x: len(x), found_clones.values())))
					print("Found subjects:\t", found)
					outfile.write(str(found) + "\t")

	# write computed statistics to the output file
	# with open("monte_carlo_result.txt", "w") as outfile:
	# 	outfile.write("\t".join(map(str, res_stat)))


if __name__ == "__main__":
	# cycle through each file with > 200K clonotypes
	# sample 63 clonotypes and search for them (CDR3 + V) at the other people files
	cycle(sys.argv[1], 4, 200000, sys.argv[2])
	# cycle(sys.argv[1], 2, 1800000)