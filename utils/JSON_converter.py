import json

def convert_list_to_json_dict(data, original_dict=None):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            raise ValueError("Invalid JSON string")

    if isinstance(data, list):
        # 기존 key 중 최대값 + 1부터 시작
        if original_dict and isinstance(original_dict, dict):
            existing_keys = [int(k) for k in original_dict.keys() if k.isdigit()]
            start_index = max(existing_keys) + 1 if existing_keys else 0
        else:
            start_index = 0
            original_dict = {}

        # 새 키-값 쌍 추가
        for i, item in enumerate(data):
            key = str(start_index + i)
            original_dict[key] = item

        return original_dict

    elif isinstance(data, dict):
        return data

    else:
        raise ValueError("Input must be a list or dict")