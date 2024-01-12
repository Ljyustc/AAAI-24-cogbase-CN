import json
import os

import func_timeout


def execute_code(code_string: str, keys=None, timeout_duration=5, value=None):
    def execute(x):
        try:
            local_namespace = {**locals(), **globals()}
            exec(x, local_namespace, local_namespace)
            if keys is None:
                return local_namespace.get('result', None)
            else:
                return [local_namespace.get(k, None) for k in keys]
        except Exception as e:
            return None

    try:
        # 找到最后一个'\n'
        index = code_string.rfind('\n')
        # 删除index之后的内容
        code_string = code_string[:index]
        # 添加result = Verify(value)
        code_string = code_string + f"result = Verify({value})"
        result = func_timeout.func_timeout(timeout_duration, execute, args=(code_string,))
    except func_timeout.FunctionTimedOut:
        result = None
    except Exception as e:
        result = None

    return result


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


with open(os.path.join(output_dir, 'GPT4_CN_Verify.json'), 'r', encoding='utf-8') as json_file:
    verify_codes = json.load(json_file)

# Load initial results with safe conversion
result1 = {}
result2 = {}
result3 = {}
result_gpt4_official = {}
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
with open(os.path.join(result_dir, 'GPT-4-Official-CN-all.json'), 'r', encoding='utf-8') as file:
    temp = json.load(file)
    for key, value in temp.items():
        result_gpt4_official[key] = safe_float(value)
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
for i in range(0, 19):
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
if os.path.exists(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify.json')):
    try:
        with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify.json'), 'r',
                  encoding='utf-8') as json_file:
            result = json.load(json_file)
    except json.JSONDecodeError:
        print(
            f"Error reading from {os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify.json')}. File might be empty or corrupted.")
else:
    print(
        f"{os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify.json')} does not exist. Starting with an empty list.")
may_be_wrong = []
if os.path.exists(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify_may_be_wrong.json')):
    try:
        with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify_may_be_wrong.json'), 'r',
                  encoding='utf-8') as json_file:
            may_be_wrong = json.load(json_file)
    except json.JSONDecodeError:
        print(
            f"Error reading from {os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify_may_be_wrong.json')}. File might be empty or corrupted.")
else:
    print(
        f"{os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify_may_be_wrong.json')} does not exist. Starting with an empty list.")

for key in result1.keys():  # Iterate over keys from the first result 
    if key in result:
        continue
    print(len(result), key)
    values = []
    verify_code = verify_codes[key][0]
    # Add results from the first file
    value = result1.get(key, "-5201314")
    if value != "-5201314":
        if execute_code(verify_code, value=value) == True:
            values.extend([value] * 2)
        else:
            values.extend([value])

    # Add results from the second file
    value = result2.get(key, "-5201314")
    if value != "-5201314":
        if execute_code(verify_code, value=value) == True:
            values.extend([value] * 2)
        else:
            values.extend([value])
    # Add results from the third file
    value = result3.get(key, "-5201314")
    if value != "-5201314":
        if execute_code(verify_code, value=value) == True:
            values.extend([value] * 2)
        else:
            values.extend([value])

    # Add results from pal 3
    for result_file in results_pal_3:
        if result_file.get(key, "-5201314") != "-5201314":
            value = result_file[key]
            if execute_code(verify_code, value=value) == True:
                values.extend([value] * 4)
            else:
                values.extend([value] * 2)

    # Add results from pal 4
    for result_file in results_pal_4:
        if result_file.get(key, "-5201314") != "-5201314":
            value = result_file[key]
            if execute_code(verify_code, value=value) == True:
                values.extend([value] * 4)
            else:
                values.extend([value] * 3)

    # Consider the official results
    if result_gpt4_official.get(key, "-5201314") != "-5201314":
        value = result_gpt4_official[key]
        if execute_code(verify_code, value=value) == True:
            values.extend([value] * 40)
        else:
            values.extend([value] * 30)

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
    with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify.json'), 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False)
    print("may_be_wrong: ", len(may_be_wrong))
    with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify_may_be_wrong.json'), 'w',
              encoding='utf-8') as file:
        json.dump(may_be_wrong, file, ensure_ascii=False)

# 输出结果
print(len(result))
# Output final result
with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify.json'), 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False)
print("may_be_wrong: ", len(may_be_wrong))
with open(os.path.join(file_to_be_submitted_dir, 'GPT4_CN_vote_all_verify_may_be_wrong.json'), 'w',
          encoding='utf-8') as file:
    json.dump(may_be_wrong, file, ensure_ascii=False)
