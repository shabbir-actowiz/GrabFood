import gzip
import json

input_file = r"C:\Intern-Practice\GrabFood\grab_food_pages\1-C2DYPGEYN8NYME.html.gz"
output_file = r"C:\Intern-Practice\GrabFood\temp\try.json"

with gzip.open(input_file, 'rt',encoding='utf-8') as f_in:
    with open(output_file, 'w', encoding='utf-8') as f_out:
        data = json.load(f_in)
        f_out.write(json.dumps(data, ensure_ascii=False, indent=4))

