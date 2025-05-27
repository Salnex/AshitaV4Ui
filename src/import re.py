import re
from ini_data import tooltips

def extract_valid_values(tooltips):
    result = {}
    for section, keys in tooltips.items():
        for key, tip in keys.items():
            # Match "Valid values:", "Valid values are:", or "Value values:"
            match = re.search(r"(Valid values?(?: are)?|Value values?):\s*(.+)", tip, re.IGNORECASE)
            if match:
                values_str = match.group(2)
                value_map = {}
                # Split on commas, but also handle ... for ranges
                for part in values_str.split(','):
                    part = part.strip()
                    if '=' in part:
                        val, desc = part.split('=', 1)
                        # Try to guess which side is the label and which is the value
                        val, desc = val.strip(), desc.strip()
                        # If value is numeric and desc is not, swap
                        if val.isdigit() and not desc.isdigit():
                            value_map[desc] = val
                        else:
                            value_map[val] = desc
                    elif '...' in part:
                        # Handle ranges like "12 = Lowest ... 20 = Highest"
                        range_match = re.match(r"(\d+)\s*=\s*([^\.\,]+)\s*\.\.\.\s*(\d+)\s*=\s*([^\.\,]+)", part)
                        if range_match:
                            start_val, start_desc, end_val, end_desc = range_match.groups()
                            value_map[start_desc.strip()] = start_val.strip()
                            value_map[end_desc.strip()] = end_val.strip()
                if value_map:
                    if section not in result:
                        result[section] = {}
                    result[section][key] = value_map
    return result

def print_ui_metadata_valid_values(tooltips):
    valid_values = extract_valid_values(tooltips)
    for section, keys in valid_values.items():
        print(f'"{section}": {{')
        for key, value_map in keys.items():
            print(f'    "{key}": {{"valid_values": {value_map}}},')
        print('},')

if __name__ == "__main__":
    print_ui_metadata_valid_values(tooltips)