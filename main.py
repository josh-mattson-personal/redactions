import os
import re

def parse_files_from_directory(directory):
    with open("redaction_strings.txt", "r", encoding="utf-8") as f:
        string_list = [line.strip() for line in f if line.strip()]

    with open("test_strings.txt", "r", encoding="utf-8") as f:
        test_string_list = [line.strip() for line in f if line.strip()]

    # Walk through all the files in directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            files_to_delete = [
                '.wav',                     # .wav files contain audio recordings of every Alexa transaction, these are large, and unable to be cross referenced with other text files
                '.eml',                     # Emails are harder to parse for PII to redact, and I don't think any unique information would be contained in them
                'Retail.Addresses.json',    # Too hard to parse, and contains PII
                'node_metadata_na_1.csv',   # Contains file metadata for amazon drive
                '.jpeg',                    # Delivery Photos
                '.jpg',                     # Other Uploaded Photos
            ]

            for string in files_to_delete:
                if file.endswith(string):
                    print(f'Deleting {file_path}')
                    os.remove(file_path)

            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    for s in string_list:
                        if s.upper() in content.upper():
                            content = content.replace(s, "[REDACTED]")
                            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                                f.write(content)
                            print(f"Matched string: {s} in {file_path}")

                    for s in test_string_list:
                        if s.upper() in content.upper():
                            print(f"Test Matched string: {s} in {file_path}")

                    # Redact the delivery photo location metadata
                    matches = re.findall(r'"photographCoordinates":\s*"([-+]?\d{2}\.\d{6},\s*[-+]?\d{2,3}\.\d{6})"', content)
                    for match in matches:
                        print(f"Found photographCoordinates: {match} in {file_path}")
                        content = content.replace(match, "[REDACTED]")
                        with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                            f.write(content)

                    matches = re.findall(r'deliveryAddress":\s*"([^"]+)"', content)
                    for match in matches:
                        if match == '[REDACTED]':
                            continue
                        print(f'Found deliveryAddress: {match} in {file_path}')
                        content = content.replace(match, "[REDACTED]")
                        with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                            f.write(content)

                    # Redact any latitude or longitude entries
                    lat_long_patterns = [
                        r'\,([-+]?\d{1,2}\.\d{6})\,',  #  37.123456,
                        r'\,([-+]?\d{1,3}\.\d{6})\,',  # -122.123456,
                        r'([-+]?\d{1,2}\.\d{6})[, ]\s*([-+]?\d{1,3}\.\d{6})' # 37.123456, -122.123456
                    ]
                    for pattern in lat_long_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            if isinstance(match, tuple):
                                for m in match:
                                    print(f"Found latitude/longitude: {m} in {file_path}")
                                    content = content.replace(m, "[REDACTED]")
                            else:
                                print(f"Found latitude/longitude: {match} in {file_path}")
                                content = content.replace(match, "[REDACTED]")
                        if matches:
                            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                                f.write(content)

if __name__ == "__main__":
    directory = "All Data Categories"
    parse_files_from_directory(directory)