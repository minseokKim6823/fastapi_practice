import json

def parse_threshold_data(raw_json: str, default_threshold=0.7) -> tuple[dict, list[str]]:
    try:
        incoming_data = json.loads(raw_json)
        threshold_map = {}
        group_names = []

        for item in incoming_data:
            name = item.get("template_group_name")
            value = item.get("threshold")
            group_names.append(name)
            if isinstance(value, (float, int)) and 0 <= value <= 1:
                threshold_map[name] = float(value)
            else:
                threshold_map[name] = default_threshold
                print(f"[!] 무시된 threshold: {name} = {value}")

        return threshold_map, group_names

    except Exception as e:
        raise ValueError(f"threshold JSON 파싱 오류: {e}")
