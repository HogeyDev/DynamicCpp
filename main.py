import os
import json

srcDirectory = './src'
outDirectory = './build'
fileEnding = '.cpp'
headerFileEnding = '.hpp'
mtimesPath = 'mtimes.json'

srcFiles = []
headerFiles = []

recursiveFileList = []
for root, _, files in os.walk(srcDirectory):
	for file in files:
		fullPath = os.path.join(root, file)
		if file.endswith(fileEnding):
			srcFiles.append(fullPath)
			recursiveFileList.append(fullPath)
		elif file.endswith(headerFileEnding):
			headerFiles.append(fullPath)
			recursiveFileList.append(fullPath)

oldmtimes = {}
with open(mtimesPath, "r") as mtimesfile:
	oldmtimes = json.load(mtimesfile)

newmtimes = {}
for index, value in enumerate(recursiveFileList):
    newmtimes[value] = os.path.getmtime(value)

newSourceFiles = []
for index, value in enumerate(srcFiles):
	fileChanged = True
	if value in oldmtimes and newmtimes[value] == oldmtimes[value]:
			fileChanged = False

	if fileChanged:
		newSourceFiles.append(value)

newHeaderFiles = []
for index, file in enumerate(headerFiles):
	fileChanged = True
	if file in oldmtimes and newmtimes[file] == oldmtimes[file]:
		fileChanged = False

	if fileChanged:
		newHeaderFiles.append(file)

with open(mtimesPath, "w") as mtimesfile:
	mtimesfile.write(json.dumps(newmtimes, indent=4))

CXX = 'g++'
CXXARGS = '-I ./src/include -Werror -Wpedantic -Wall'

os.system(f'mkdir -p {outDirectory}/objects')

for index, value in enumerate(srcFiles):
	includesEditedHeader = False
	for file in newHeaderFiles:
		if f'#include <{file}>' in value or f'#include "{file}"' in value or f'#include<{file}>' in value or f'#include"{file}"' in value:
			newSourceFiles.append(file)
	outputPath = os.path.basename(value).split('/')[-1][:-len(fileEnding)] + '.o'
	command = f'{CXX} -c {CXXARGS} {value} -o {outDirectory}/objects/{outputPath}'
	os.system(command)

print(f'Built files: {newSourceFiles}')

os.system(f'{CXX} {outDirectory}/objects/*.o -o {outDirectory}/main')