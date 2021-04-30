import random
import string
import json
import matplotlib.pyplot as plt
import numpy as np
import math
import os


class Files:
    endLetter = ''
    lettersArr = []
    numFiles = 0
    allFiles = []

    def __init__(self, numFiles, endLetter, rangeUpper, rangeLower, useOld=False):
        self.endLetter = endLetter
        self.lettersArr = self.createLettersArr(endLetter)
        self.numFiles = numFiles
        self.genrate_files(rangeUpper, rangeLower, useOld)
        self.TermDocFreq = self.getTermDocFreq()

    def statistical_model(self, query):
        temparr = {i: 0 for i in self.lettersArr}
        for i in query:
            temparr[i] = query[i]
        for i in self.allFiles:
            i.statistical_model_score = np.dot(np.array(list(temparr.values())),
                                               np.array(i.TermFreq))

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

    def vectorSpace_model(self, files, query):
        for f in files.allFiles:
            f.idfi = f.Contentmap
            for j, i in zip(f.TF, files.TermDocFreq):
                f.idfi[i] = files.TermDocFreq[i] * j
        """Query"""
        temparr = {i: 0 for i in files.lettersArr}
        for i in query:
            temparr[i] = query[i]

        for f in files.allFiles:
            f.vectorSpace_model_score = (
                np.dot(np.array(list(f.idfi.values())), np.array(list(temparr.values()))))

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

    def genrate_files(self, rangeUpper, rangeLower, useOld):
        self.allFiles = []
        if useOld:
            for fileID in os.listdir("DOCS"):
                filename = os.path.join("DOCS", fileID)
                f = open(filename, "r+")
                fileContent = f.read()
                fileSize = len(fileContent)//2
                f.close()
                # print(filename)
                self.allFiles.append(
                    File(fileID, fileSize, fileContent, self.lettersArr, useOld))
        else:
            for f in range(self.numFiles):
                fileID = "DOC_{}".format(f)
                fileSize = random.randint(rangeUpper, rangeLower)
                fileContent = self.genrateFilecontent(fileSize)
                self.allFiles.append(
                    File(fileID, fileSize, fileContent, self.lettersArr, useOld))


class File:
    def __init__(self, fileID, fileSize, fileContent, lettersArr, useOld):
        self.fileID = fileID
        self.fileSize = fileSize
        self.fileContent = fileContent
        self.Contentmap = {i: 0 for i in lettersArr}
        self.ContentmapGen(fileContent)
        self.TermFreq = self.getFreq()
        self.TF = self.getTF()
        if not useOld:
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

    def getTF(self):
        maximum = max(self.Contentmap.values())
        return [v / maximum for v in self.Contentmap.values()]

    def __str__(self):
        return "FileID:" + str(self.fileID) + ",\t Size:"+str(self.fileSize)+"\n \t\tTermFreq:"+str(self.TermFreq)+"\n \t\tVS_TF:"+str(self.TF)+"\n\t\tContentmap:"+str(self.Contentmap)


def prepQuery(query):
    query = query.replace("<", "", 1)
    query = query.replace(">", "", 1)
    query = query.split(";")
    query = {i.split(":")[0]: float(i.split(":")[1]) for i in query}
    return query


def Search_Statistical(query):
    query = prepQuery(query)
    files = Files(numFiles=3, endLetter='f', rangeUpper=5,
                  rangeLower=10, useOld=True)

    files.statistical_model(query)
    files.allFiles.sort(
        key=lambda files: files.statistical_model_score, reverse=True)

    out = "<h1>Statistical Model</h1><br>"
    for f in files.allFiles:
        out += "File: %s, Score: %s<br>" % (
            f.fileID, f.statistical_model_score)
    return out+"<br>"


def Search_VectorSpace(query):
    query = prepQuery(query)

    filesV = Files(numFiles=3, endLetter='f', rangeUpper=5,
                   rangeLower=10, useOld=True)
    filesV.vectorSpace_model(files=filesV, query=query)
    filesV.allFiles.sort(
        key=lambda files: files.vectorSpace_model_score, reverse=True)

    out = "<h1>Vector-Space Model</h1><br>"
    for f in filesV.allFiles:
        out += "File: %s, Score: %s<br>" % (
            f.fileID, f.vectorSpace_model_score)
    return out+"<br>"


"""--------------------------------NEXT-FOR-TESTING-FOR-WEB------------------------------------"""
# files = Files(numFiles=3, endLetter='f', rangeUpper=5,
#               rangeLower=10, useOld=True)


query = {'a': 0.2, 'b': 0.3}

# TODO: Connect with frontend
# ?-DONE-AND-TESTED
"""--Statistical-Model--"""
# files.statistical_model(query)
# files.allFiles.sort(
#     key=lambda File: File.statistical_model_score, reverse=True)
# for f in files.allFiles:
#     print(f.statistical_model_score, f.fileID)

# """--Vector-Space-Model--"""
# files = Files(numFiles=3, endLetter='f', rangeUpper=5,
#               rangeLower=10, useOld=True)
# files.vectorSpace_model(files, query)
# # print(files.TermDocFreq)
# files.allFiles.sort(
#     key=lambda File: File.vectorSpace_model_score, reverse=True)
# for f in files.allFiles:
#     print(f.vectorSpace_model_score, f.fileID)

# for f in files.allFiles:
#     print(f.idfi)
# print("->term doc fre", files.TermDocFreq)
