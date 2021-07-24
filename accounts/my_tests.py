dic = {}

nums = [1, 2, 2, 3, 4, 5, 9]

for num in nums:
    if not dic.get(str(num)):
        dic[str(num)] = [num]
    else:
        dic[str(num)].append(num)


if '9' in dic.keys():
    print(True)
else:
    print(False)
