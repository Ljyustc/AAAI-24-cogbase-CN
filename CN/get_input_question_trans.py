import json
import os


def load_jsonl(file):
    data = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            data.append(d)
    return data


# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)
# 获取脚本所在目录
script_directory = os.path.dirname(script_path)

data = load_jsonl(script_directory + r"\data\TAL-SAQ7K-CN.jsonl")

json_string = "{\"dataset_version\": \"2023-07-07\", \"queId\": \"dd7fa8e2a0884831b7f83debef223e50\", \"difficulty\": " \
              "\"2\", \"qtype\": \"short_answer\", \"problem\": \"设正整数$${{a}_{1}}$$，$${{a}_{2}}$$，$$\\\\cdots $$，$${{" \
              "a}_{n}}$$中至少有$$5$$个不同的值．若对任意的正整数$$i$$，$$j\\\\left( 1\\\\leqslant i\\\\textless{}j\\\\leqslant n " \
              "\\\\right)$$，存在正整数$$k$$，$$l$$（$$k\\\\ne l$$，且均异于$$i$$与$$j$$）使得$${{a}_{i}}+{{a}_{j}}={{a}_{k}}+{{a}_{" \
              "l}}$$，试求正整数$$n$$的最小值．\", \"knowledge_point_routes\": [\"竞赛->知识点->组合->计数问题-枚举法\", \"竞赛->知识点->组合->组合最值\"]}"

processed_data = []

for d in data:
    id = d['queId']
    problem = d['problem']

    prompt = """You are a translator. I will provide Chinese math problems in the form of a json, which includes the question ID "queId" and the problem text "problem". You need to translate the Chinese math problem in "problem" into an English question that can be understood by GPT. The output should be a json with the question ID "queId" and the problem text "problem" in input json, an additional field "trans_problem" containing the translated English problem. Please note the following:
(1) If the Chinese problem contains numbers surrounded by `$$` symbols,the translated English numbers must also be surrounded by `$$` symbols.
(2) If the Chinese problem contains mathematical expressions represented in LaTeX syntax, the translated English mathematical expressions must also be represented in the same LaTeX syntax.
(3) The "trans_problem" field should only include the translated English problem content and no other information.
Here are some examples:
Example 1:
Input:
```{"queId": "f9758f01dd2e4bdf8650b6190773fbfa", "problem": "从三位数$$100$$，$$101$$，$$102$$，\\ldots，$$699$$，$$700$$中任意取出$$n$$个不同的数，使得总能找到其中三个数，它们的数字和相同，求$$n$$的最小值． "}```
Output:
```{"queId": "f9758f01dd2e4bdf8650b6190773fbfa", "problem": "从三位数$$100$$，$$101$$，$$102$$，\\ldots，$$699$$，$$700$$中任意取出$$n$$个不同的数，使得总能找到其中三个数，它们的数字和相同，求$$n$$的最小值． ", "trans_problem": "From the set of three-digit numbers $$100$$, $$101$$, $$102$$, \\ldots, $$699$$, $$700$$, choose any $$n$$ distinct numbers such that, for any selection, there are always three numbers with the same sum. Find the minimum value of $$n$$."}```
Example 2:
Input:
```{"queId": "dd7fa8e2a0884831b7f83debef223e50", "problem": "设正整数$$\{{a}_{1}}$$，$${{a}_{2}}$$，$$\\cdots $$，$${{a}_{n}}$$中至少有$$5$$个不同的值．若对任意的正整数$$i$$，$$j\\left( 1\\leqslant i\\textless{}j\\leqslant n \\right)$$，存在正整数$$k$$，$$l$$（$$k\\ne l$$，且均异于$$i$$与$$j$$）使得$${{a}_{i}}+{{a}_{j}}={{a}_{k}}+{{a}_{l}}$$，试求正整数$$n$$的最小值．"}```
Output:
```{"queId": "dd7fa8e2a0884831b7f83debef223e50", "problem": "设正整数$${{a}_{1}}$$，$${{a}_{2}}$$，$$\\cdots $$，$${{a}_{n}}$$中至少有$$5$$个不同的值．若对任意的正整数$$i$$，$$j\\left( 1\\leqslant i\\textless{}j\\leqslant n \\right)$$，存在正整数$$k$$，$$l$$（$$k\\ne l$$，且均异于$$i$$与$$j$$）使得$${{a}_{i}}+{{a}_{j}}={{a}_{k}}+{{a}_{l}}$$，试求正整数$$n$$的最小值．"， "trans_problem": "Let positive integers $${{a}_{1}}$$, $${{a}_{2}}$$, $$\\cdots $$, $${{a}_{n}}$$ have at least $$5$$ distinct values. If for any positive integers $$i$$, $$j\\left( 1\\leqslant i\\textless{}j\\leqslant n \\right)$$, there exist positive integers $$k$$, $$l$$ ($$k\\ne l$$, and both are distinct from $$i$$ and $$j$$), such that $${{a}_{i}}+{{a}_{j}}={{a}_{k}}+{{a}_{l}}$$, find the minimum value of the positive integer $$n$$."}```
This is the math question:
Input:
"""
    prompt += problem + "\nOutput:\n```"
    new_item = {"id": d['queId'], "content": prompt}
    processed_data.append(new_item)


def write_jsonl(res, outfile):
    f = open(outfile, 'w', encoding='utf-8')
    for d in res:
        f.writelines(json.dumps(d, ensure_ascii=False))
        f.writelines('\n')
    f.close()


write_jsonl(processed_data, script_directory + r"\data\input\GPT4_CN_Trans_EN.json")
