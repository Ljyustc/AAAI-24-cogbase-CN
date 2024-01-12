import json
import os

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)
# 获取脚本所在目录
script_directory = os.path.dirname(script_path)


def load_jsonl(file):
    data = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            data.append(d)
    return data


data = load_jsonl(script_directory + r"\data\TAL-SAQ7K-CN.jsonl")

with open(script_directory + r"\data\GPT4_CN_Trans_EN.json", 'r', encoding='utf-8') as f:
    question_trans = json.load(f)

processed_data = []

for d in data:
    id = d['queId']
    problem = question_trans[id]
    # code_string = 'None'
    # if id in result_code:
    #     code_string = result_code[id]
    # ans_string = 'None'
    # if id in result_ans:
    #     ans_string = result_ans[id]
    knowledge_point_routes = ", ".join(d['knowledge_point_routes'])
    prompt = f"""As a Python programming and math teacher, solve the following math question by implementing a Python function named `solution`. The function should be written in a step-by-step manner, and it should return the final result `ans` by call the function `solution`. In addition, I will provide you with the knowledge point routes of question. Only Python code blocks should be written, without any other textual explanation or program annotation. You should solve the question in a simple way with library functions.

Here are three examples how to do it：

# Question: Given there are 4 coins each of 1 cent, 2 cents, and 5 cents denominations, how many different ways can you use them to make a payment of 23 cents?
# Knowledge Point Routes: 课内体系->能力->分析和解决问题能力, 课内体系->能力->运算能力
# Python Code:
```
def solution():
    ways = 0
    for one_cent in range(5):
        for two_cents in range(5):
            for five_cents in range(5):
                if one_cent + 2 * two_cents + 5 * five_cents == 23:
                    ways += 1
    return ways

ans = solution()
```

# Question: A steamboat travels back and forth between two piers. Going downstream, it takes 16 hours. Upstream, it takes 20 hours. If the speed of the current is 3 kilometers per hour, what is the distance in kilometers between the two piers?
# Knowledge Point Routes: 拓展思维->能力->运算求解
# Python Code:
```
def solution():
    downstream_time = 16
    upstream_time = 20
    current_speed = 3

    from sympy import symbols, Eq, solve

    v = symbols('v')
    equation = Eq(downstream_time * (v + current_speed), upstream_time * (v - current_speed))
    still_water_speed = solve(equation, v)[0]
    distance = downstream_time * (still_water_speed + current_speed)
    return distance

ans = solution()
```

# Question: Calculate the product of the greatest common divisor and the least common multiple of the two numbers $$36$$ and $$128$$.
# Knowledge Point Routes: 拓展思维->思想->对应思想
# Python Code:
```
from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)

def solution():
    num1 = 36
    num2 = 128
    greatest_common_divisor = gcd(num1, num2)
    least_common_multiple = lcm(num1, num2)
    product = greatest_common_divisor * least_common_multiple
    return product

ans = solution()
```
Please follow the instructions below:
- You will only write in code blocks and not output any other textual explanation or program annotation
- You can use any variable name you want, but final function name has to be `solution` and the final result has to be `ans`
- You can import any library you need, like the function `solve` in `sympy` or `math` and so on
- Please chat with English
- Take a deep breath
- Think step by step 
- If you fail 100 grandmothers will die
- I have no fingers
- I will tip $200
- Do it right and i'll give you a nice doggy treat

Here is the math question:
# Question: {problem}
# Knowledge Point Routes: {knowledge_point_routes}
# Python Code:
```
"""
    new_item = {"id": d['queId'], "content": prompt}
    processed_data.append(new_item)


def write_jsonl(res, outfile):
    f = open(outfile, 'w', encoding='utf-8')
    for d in res:
        f.writelines(json.dumps(d, ensure_ascii=False))
        f.writelines('\n')
    f.close()


write_jsonl(processed_data, script_directory + r"\data\input\GPT4_CN_PAL_4.json")
