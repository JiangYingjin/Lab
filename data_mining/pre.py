"""
确定使用算法

N：最近邻分类器    
R：随机森林
T：分类与回归树
"""

# import string

# alphabet = string.ascii_uppercase
# Alphabet = {}
# for i in range(26):
#     Alphabet[alphabet[i]] = i + 1

# tasks_str = "ABCGMNRT"
# tasks = [tasks_str[i : i + 3] for i in range(0, len(tasks_str) - 2)]
# name = "JYZ"


# def clac_error(task, name):
#     error = 0
#     for i in range(3):
#         error += abs(Alphabet[name[i]] - Alphabet[task[i]]) ** 2
#     return error


# tasks_error = {task: clac_error(task, name) for task in tasks}

# print(tasks_error)
