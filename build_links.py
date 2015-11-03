import os
import sys


def search_files(folder_path, index_list):
	res = []
	if folder_path:
		print("Folder:\t", folder_path, "with", len(os.listdir(folder_path)), "files")
		for filename in os.listdir(folder_path):
			print(filename)
			file_index = filename[filename.find('_') + 1 : filename.find('_', filename.find('_') + 1)]
			for index in index_list:
				if index == file_index:
					print("\tmatches '", file_index, "'", sep = '')
					res.append(filename)
					break
			else:
				print("\tdon't match anything")

	return res


def build_links(index_path):
	with open(index_path) as index_file:
		with open(index_path.replace(".txt", ".links.txt"), 'w') as out_file:
			header = False
			folder_path = ''
			indices = []
			last_man = ''
			for line in index_file:
				line = line.strip()
				if line:
					if line[0] == "}":
						header = False

						res = search_files(folder_path, indices)
						out_file.write("#" + last_man + "\n")
						for x in res:
							out_file.write(folder_path + x + "\n")

					elif line[0] == '#':
						res = search_files(folder_path, indices)
						out_file.write("#" + last_man + "\n")
						for x in res:
							out_file.write(folder_path + x + "\n")
						
						last_man = line[1:]
						indices = []

					elif not header:
						header = True

						folder_path = line + "/"
						indices = []
						last_man = ''

					else:
						indices.append(line)
				else:
					res = search_files(folder_path, indices)
					out_file.write("#" + last_man + "\n")
					for x in res:
						out_file.write(folder_path + x + "\n")


if __name__ == '__main__':
	build_links(sys.argv[1])