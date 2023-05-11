from bs4 import BeautifulSoup as bs
import requests
import json


def save_appendix(n, sf=False):
    data = requests.get('https://www.gesetze-im-internet.de/bsi-kritisv/anhang_{}.html'.format(n), )
    data.encoding = 'utf-8'

    soup = bs(data.content, 'html.parser')
    table = soup.find_all('table', {'style': lambda s: 'border-collapse: collapse;' in s})[0]

    jsonr = []
    descf = ['nr', 'category', 'criteria', 'treshold']

    for row in table.tbody.find_all('tr'):
        if len(row) == 4:
            jsonc = {}

            for i, column in enumerate(row.find_all('td')):
                jsonc[descf[i]] = column.get_text(separator=' ').strip().replace(u'\xa0', '.')

            if jsonc['category'] != '' and jsonc['criteria'] != '':
                jsonr.append(jsonc) 

    filepath = 'results/a{}.json'.format(n)

    if sf:
        with open(filepath, 'w') as out:
            out.write(json.dumps(jsonr, indent=4, ensure_ascii=False))

    return jsonr


if __name__ == '__main__':
    sectors = ['energy', 'water', 'food', 'it', 'health', 'finance', 'transport']
    data = {}

    for i in range(1, 8):
        data[sectors[i-1]] = save_appendix(i)

    with open('results/results.json', 'w') as out:
        out.write(json.dumps(data, indent=4, ensure_ascii=False))
