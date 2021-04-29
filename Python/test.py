arr1 = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0}
arr2 = {'a': 0.2, 'b': 0.3}

for char in arr2:
    arr1[char]=arr2[char]

print(arr1)
