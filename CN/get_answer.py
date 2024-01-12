import json
import os


def auto_round(num_str):
    import re
    match = re.search(r'(\.(\d*?)(9{3,}|0{3,}|1{3,}|2{3,}|3{3,}|4{3,}|5{3,}|6{3,}|7{3,}|8{3,})\d*)', num_str)
    if match:
        precision = len(match.group(2))
        num = str(round(float(num_str), precision))
    else:
        num = num_str
    return num


# Paths
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
base_dir = script_directory + r'\data'
result_dir = os.path.join(base_dir, 'result')
output_dir = os.path.join(base_dir, 'output')
file_to_be_submitted_dir = os.path.join(base_dir, 'file_to_be_submitted')


def safe_float(value, default="-5201314"):
    try:
        return str(float(value))  # Convert to float and then back to string for uniformity
    except Exception as e:
        return default


# Load initial results with safe conversion
result1 = {}
result2 = {}
result3 = {}
with open(os.path.join(result_dir, 'prompt1-2-trans-vote_CN.json'), 'r', encoding='utf-8') as file:
    temp = json.load(file)
    for key, value in temp.items():
        result1[key] = safe_float(value)
with open(os.path.join(result_dir, 'GPT4_CN_PAL_1.json'), 'r', encoding='utf-8') as file:
    temp = json.load(file)
    for key, value in temp.items():
        result2[key] = safe_float(value)
with open(os.path.join(result_dir, 'GPT4_CN_PAL_2.json'), 'r', encoding='utf-8') as file:
    temp = json.load(file)
    for key, value in temp.items():
        result3[key] = safe_float(value)

results_pal_3 = []
for i in range(0, 3):
    index = f"{i:02}"
    try:
        with open(os.path.join(result_dir, f'GPT4_CN_PAL_3_{index}.json'), 'r', encoding='utf-8') as file:
            temp = json.load(file)
            safe_results = {key: safe_float(value) for key, value in temp.items()}
            results_pal_3.append(safe_results)
    except FileNotFoundError:
        print(f"File GPT4_EN_PAL_3_{index}.json not found.")
        results_pal_3.append({})

results_pal_4 = []
for i in range(0, 18):
    index = f"{i:02}"
    try:
        with open(os.path.join(result_dir, f'GPT4_CN_PAL_4_{index}.json'), 'r', encoding='utf-8') as file:
            temp = json.load(file)
            safe_results = {key: safe_float(value) for key, value in temp.items()}
            results_pal_4.append(safe_results)
    except FileNotFoundError:
        print(f"File GPT4_EN_PAL_4_{index}.json not found.")
        results_pal_4.append({})

result = {}

may_be_wrong = []

for key in result1.keys():  # Iterate over keys from the first result 
    print(key)
    values = []
    # Add results from the first file
    value = result1.get(key, "-5201314")
    if value != "-5201314":
        values.extend([value])

    # Add results from the second file
    value = result2.get(key, "-5201314")
    if value != "-5201314":
        values.extend([value])

    # Add results from the third file
    value = result3.get(key, "-5201314")
    if value != "-5201314":
        values.extend([value])

    # Add results from pal 3
    for result_file in results_pal_3:
        if result_file.get(key, "-5201314") != "-5201314":
            value = result_file[key]
            values.extend([value] * 2)

    # Add results from pal 4
    for result_file in results_pal_4:
        if result_file.get(key, "-5201314") != "-5201314":
            value = result_file[key]
            values.extend([value] * 3)

    # Vote counting
    vote_count = {}
    max_vote = 0
    max_value = "-5201314"
    for value in values:
        vote_count[value] = vote_count.get(value, 0) + 1
        if vote_count[value] > max_vote:
            max_vote = vote_count[value]
            max_value = value

    max_value = auto_round(max_value)  # Round the value
    # Verification logic here (if needed)

    result[key] = max_value
    print(max_value, ": ", max_vote)
    may_be_wrong.append({"key": key, "value": max_value, "vote": max_vote})

# 输出结果
print(len(result))
# Output final result
with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all.json'), 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False)
print("may_be_wrong: ", len(may_be_wrong))
with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_may_be_wrong.json'), 'w', encoding='utf-8') as file:
    json.dump(may_be_wrong, file, ensure_ascii=False)
