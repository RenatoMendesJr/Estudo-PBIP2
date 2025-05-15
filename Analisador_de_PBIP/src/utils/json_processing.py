def load_json(file_path):
    import json
    import os

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def validate_json_structure(data):
    required_keys = ["sections", "config"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key} in JSON data.")
    
    return True

def load_and_validate_json(file_path):
    data = load_json(file_path)
    validate_json_structure(data)
    return data

def flatten_json(y, parent_key='', sep='.'):
    """
    Função para achatar um JSON aninhado em um dicionário plano.
    """
    items = []
    if isinstance(y, list):
        for i, item in enumerate(y):
            items.extend(flatten_json(item, f"{parent_key}[{i}]", sep=sep).items())
    elif isinstance(y, dict):
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, y))
    return dict(items)