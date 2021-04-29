import random
import string
import json
import matplotlib.pyplot as plt
import numpy as np
import math


class Files:
    endLetter = ''
    lettersArr = []
    numFiles = 0
    allFiles = []

    def __init__(self, numFiles, endLetter, rangeUpper, rangeLower):
        self.endLetter = endLetter
        self.lettersArr = self.createLettersArr(endLetter)
        self.numFiles = numFiles
        self.genrate_files(rangeUpper, rangeLower)
        self.TermDocFreq = self.getTermDocFreq()

    def statistical_model(self, query):
        temparr = {i: 0 for i in self.lettersArr}
        for i in query:
            temparr[i] = query[i]
        for i in self.allFiles:
            i.statistical_model_score = np.dot(np.array(list(temparr.values())),
                                               np.array(i.TermFreq))
            # print(np.dot(np.array(list(temparr.values())),
            #          np.array(i.TermFreq)))

    def getTermDocFreq(self):
        """getTermDocFreq"""
        df = {}
        for f in self.allFiles:
            for term in f.Contentmap:
                if(f.Contentmap[term] > 0):
                    if(term not in df):
                        df[term] = 1
                    else:
                        df[term] += 1
        return {key: math.log((self.numFiles/value), 2)
                for (key, value) in sorted(df.items())}

    def vectorSpace_model(self, query):
        for f in files.allFiles:
            f.idfi = f.Contentmap
            for j in f.TermFreq:
                for i in self.TermDocFreq:
                    f.idfi[i] = self.TermDocFreq[i] * j
        """Query"""
        temparr = {i: 0 for i in self.lettersArr}
        for i in query:
            temparr[i] = query[i]

        for f in files.allFiles:
            f.vectorSpace_model_score = (
                np.dot(np.array(list(f.idfi.values())), np.array(list(temparr.values()))))
            # print(np.array(list(f.idfi.values())))
            # print(np.array(list(temparr.values())))
            # print(np.array(list(self.TermDocFreq.values())))
            # print(np.array(f.TermFreq))

        # print("->", self.TermDocFreq)
        # for i in files.allFiles:
        #     print("-->>", i.TermFreq)

    def createLettersArr(self, letter):
        if(isinstance(letter, int)):
            letter += (ord('a')-1)
            letter = str(chr(letter))
        return [_letter for _letter in string.ascii_lowercase if(
            _letter <= letter)]

    def genrateFilecontent(self, fileSize):
        strcontent = " "
        for _ in range(fileSize):
            strcontent += random.choice(self.lettersArr) + " "
        return strcontent

    def genrate_files(self, rangeUpper, rangeLower):
        for f in range(self.numFiles):
            fileID = "DOC_{}".format(f)
            fileSize = random.randint(rangeUpper, rangeLower)
            fileContent = self.genrateFilecontent(fileSize)
            self.allFiles.append(
                File(fileID, fileSize, fileContent, self.lettersArr))


class File:
    def __init__(self, fileID, fileSize, fileContent, lettersArr):
        self.fileID = fileID
        self.fileSize = fileSize
        self.fileContent = fileContent
        self.Contentmap = {i: 0 for i in lettersArr}
        self.ContentmapGen(fileContent)
        self.TermFreq = self.getFreq()
        self.createFile()

    def createFile(self):
        f = open("DOCS/{}.txt".format(self.fileID), "w")
        f.write(self.fileContent)
        f.close()

    def ContentmapGen(self, fileContent):
        for word in fileContent:
            if(word not in self.Contentmap):
                self.Contentmap[word] = 1
            else:
                self.Contentmap[word] += 1
        self.Contentmap.pop(' ', None)

    def getFreq(self):
        return [v / self.fileSize for v in self.Contentmap.values()]

    def __str__(self):
        return "FileID:" + str(self.fileID) + ",\t Size:"+str(self.fileSize)+"\n \t\tTermFreq:"+str(self.TermFreq)+"\n\t\tContentmap:"+str(self.Contentmap)


"""--------------------------------NEXT-FOR-TESTING-FOR-WEB------------------------------------"""
files = Files(numFiles=3, endLetter='f', rangeUpper=5, rangeLower=10)


query = {'a': 0.2, 'b': 0.3}
"""--------SEMI-DONE-AND-TESTED--------"""
"""--Statistical-Model--"""
# files.statistical_model(query)
# files.allFiles.sort(
#     key=lambda File: File.statistical_model_score, reverse=True)
# for f in files.allFiles:
#     print(f.statistical_model_score, f.fileID)
"""--Vector-Space-Model--"""
# files.vectorSpace_model(query)
# files.allFiles.sort(
#     key=lambda File: File.vectorSpace_model_score, reverse=True)
# for f in files.allFiles:
#     print(f.vectorSpace_model_score, f.fileID)
