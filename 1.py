import math

def calculate_level(score):
    level = math.floor(math.sqrt(score))
    return level

# 示例使用
user_score = 400
user_level = calculate_level(user_score)
print(f"The user's level is: {user_level}")