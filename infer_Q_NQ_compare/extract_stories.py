import csv
import re


# Clean <0x0A> and split properly
def clean_text(text):
    return text.replace('<0x0A>', '\n').strip()


def export_to_csv(input_file_name='test_res.txt', temp_file_name='stories.csv'):
    # Read from a file
    input_filename = input_file_name
    with open(input_filename, 'r', encoding='utf-8') as file:
        text = file.read()
    # Pattern to match each test
    pattern = re.compile(
        r'TEST(\d+),\s+Number of TOKEN: (\d+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)\n(.*?)Total tokens: ([\d.]+) ; Achieved tok/s: ([\d.]+)',
        re.DOTALL)
    # Collect rows
    rows = []
    for match in pattern.finditer(text):
        label = f"TEST{match.group(1)}"
        token_num = match.group(2)
        first_features_and_text = match.group(3).strip()
        first_tokens = match.group(4)
        first_tokps = match.group(5)
        second_features_and_text = match.group(6).strip()
        second_tokens = match.group(7)
        second_tokps = match.group(8)
        third_features_and_text = match.group(9).strip()
        third_tokens = match.group(10)
        third_tokps = match.group(11)
        fourth_features_and_text = match.group(12).strip()
        fourth_tokens = match.group(13)
        fourth_tokps = match.group(14)
        fifth_features_and_text = match.group(15).strip()
        fifth_tokens = match.group(16)
        fifth_tokps = match.group(17)
        sixth_features_and_text = match.group(18).strip()
        sixth_tokens = match.group(19)
        sixth_tokps = match.group(20)
        seventh_features_and_text = match.group(21).strip()
        seventh_tokens = match.group(22)
        seventh_tokps = match.group(23)
        eighth_features_and_text = match.group(24).strip()
        eighth_tokens = match.group(25)
        eighth_tokps = match.group(26)

        # Further split features and main text for both architectures
        def split_features_text(block):
            lines = block.split('\n')
            features = lines[0].strip()
            story_lines = lines[1:]  
            story = clean_text(' '.join(story_lines))
            return features, story

        first_features, first_text = split_features_text(first_features_and_text)
        second_features, second_text = split_features_text(second_features_and_text)
        third_features, third_text = split_features_text(third_features_and_text)
        fourth_features, fourth_text = split_features_text(fourth_features_and_text)
        fifth_features, fifth_text = split_features_text(fifth_features_and_text)
        sixth_features, sixth_text = split_features_text(sixth_features_and_text)
        seventh_features, seventh_text = split_features_text(seventh_features_and_text)
        eighth_features, eighth_text = split_features_text(eighth_features_and_text)

        rows.append({
            'label': label,
            'token_num': token_num,
            'features': first_features,
            'main_text': first_text,
            'tokens': first_tokens,
            'tok_per_sec': first_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': second_features,
            'main_text': second_text,
            'tokens': second_tokens,
            'tok_per_sec': second_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': third_features,
            'main_text': third_text,
            'tokens': third_tokens,
            'tok_per_sec': third_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': fourth_features,
            'main_text': fourth_text,
            'tokens': fourth_tokens,
            'tok_per_sec': fourth_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': fifth_features,
            'main_text': fifth_text,
            'tokens': fifth_tokens,
            'tok_per_sec': fifth_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': sixth_features,
            'main_text': sixth_text,
            'tokens': sixth_tokens,
            'tok_per_sec': sixth_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': seventh_features,
            'main_text': seventh_text,
            'tokens': seventh_tokens,
            'tok_per_sec': seventh_tokps
        })
        rows.append({
            'label': label,
            'token_num': token_num,
            'features': eighth_features,
            'main_text': eighth_text,
            'tokens': eighth_tokens,
            'tok_per_sec': eighth_tokps
        })
    # Write to CSV
    csv_filename = temp_file_name
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['label', 'token_num', 'features', 'main_text','tokens', 'tok_per_sec']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        row_count = 0
        for row in rows:
            writer.writerow(row)
            row_count += 1

    print(f"CSV 文件 '{csv_filename}' 创建成功！共写入 {row_count} 行数据。")
