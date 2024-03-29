# Одноразовый код для формирования датасетов для обучения/проверки(меняется folder_path)
import json
import os

import pandas as pd

folder_path = "data/test"

all_train_data = pd.DataFrame(columns=["Wrong", "Correct"])
print(0)
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if file.endswith(".json"):
        with open(file_path, 'r', encoding="utf8") as f:
            lines = f.readlines()
        for line in lines:
            item = json.loads(line)
            tmp = pd.DataFrame({"Wrong": [item["source"].lower()], "Correct": [item["correction"].lower()]})
            all_train_data = pd.concat([all_train_data, tmp], ignore_index=True)
csv_file = "data/all_test_data.csv"

all_train_data.to_csv(csv_file, index=False)
print(500)