# arr1 = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0}
# arr2 = {'a': 0.2, 'b': 0.3}

# for char in arr2:
#     arr1[char]=arr2[char]

# print(arr1)

import os
for filename in os.listdir("DOCS"):
    if filename.endswith(".txt"):
        fileID = os.path.join("DOCS", filename)
        f = open(fileID, "r+")
        fileContent = f.read()
        fileSize = len(fileContent)//2
        f.close()
        # print(fileID,fileContent,fileSize)
        print(filename)
