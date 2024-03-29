import random
import requests

from bs4 import BeautifulSoup

import pandas as pd
import warnings
warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.")


df = pd.DataFrame(columns=["Word", "Mistake", "Weight"])
df2 = pd.DataFrame(columns=["Word", "Mistake"])
print("Start")
for index in range(1, 318980):
    print(f"Page - {index}")
    # Расим сайт с опечатки: получаем правильное слово и его опечатки
    url = f'https://slovonline.ru/slovar_el_opechatka/b-0/id-{index}/abazhur.html'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    title = soup.select("#cnt > div.cnt-1-con > div.se-cnt > div.word-article > div.header-article > h3")
    title = title[0].text

    element = soup.find_all(attrs={"id": "cnt"})[0].find_all("div")[0].find_all("div")[12].find_all("div")[4].text
    list_elements = [i.lower().rstrip() for i in element.split("\n")[5].replace(f'Возможные опечатки в слове {title}', '').split(', ')]

    info = []
    info_wo_weight = []

    # Генерация весов
    # Если в правильном слове и ошибке одинаковая длина и ошибка в одной-две букве, то вес больше
    # Если слово не дописали, то вес больше чем если слово напечатали с лишней буквой
    for i in range(len(list_elements)):
        tmp2 = pd.DataFrame({"Word": [title.lower()], "Mistake": [list_elements[i]]})
        df2 = pd.concat([df2, tmp2], ignore_index=True)
        if len(list_elements[i]) == len(title.lower()) and sum(1 for a, b in zip(title.lower(), list_elements[i]) if a != b) <= 2:
            tmp = pd.DataFrame({"Word": [title.lower()], "Mistake": [list_elements[i]], "Weight": [random.uniform(0.36, 0.5 + 0.000000001)]})
            df = pd.concat([df, tmp], ignore_index=True)
        elif len(title.lower()) - len(list_elements[i]) == 1:
            tmp = pd.DataFrame({"Word": [title.lower()], "Mistake": [list_elements[i]], "Weight": [random.uniform(0.3, 0.35)]})
            df = pd.concat([df, tmp], ignore_index=True)
        elif len(title.lower()) - len(list_elements[i]) == -1:
            tmp = pd.DataFrame({"Word": [title.lower()], "Mistake": [list_elements[i]], "Weight": [random.uniform(0.25, 0.35)]})
            df = pd.concat([df, tmp], ignore_index=True)
        elif not all(c.isalpha() and 1040 <= ord(c) <= 1103 for c in list_elements[i]):
            tmp = pd.DataFrame({"Word": [title.lower()], "Mistake": [list_elements[i]], "Weight": [random.uniform(0, 0.2 + 0.00000001)]})
            df = pd.concat([df, tmp], ignore_index=True)
        else:
            tmp = pd.DataFrame({"Word": [title.lower()], "Mistake": [list_elements[i]], "Weight": [0.0]})
            df = pd.concat([df, tmp], ignore_index=True)
            
csv_file, csv_file2 = "info_with_weights_my.csv", "info_without_weights_my.csv"
with open(csv_file, 'a', newline='', encoding='utf-8') as file:
    df.to_csv(file, index=False, header=file.tell() == 0)

with open(csv_file2, 'a', newline='', encoding='utf-8') as file2:
    df2.to_csv(file2, index=False, header=file2.tell() == 0)
print("End")