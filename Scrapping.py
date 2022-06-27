import requests
from bs4 import BeautifulSoup
import json
import openpyxl


def Scrap(url, headers):
    # response = requests.get(url=url, headers=headers)
    # response = response.text
    # with open("index.html", "w", encoding="utf-8") as file:
    #     file.write(response)
    with open("index.html", encoding="utf-8") as file:
        source = file.read()
    soup = BeautifulSoup(source, "lxml")
    all_products = soup.find_all("div", class_="uk-flex mzr-tc-group-item")

    for product in all_products:
        info_list = []
        link = "https://health-diet.ru" + product.find(class_="mzr-tc-group-item-href").get("href")
        name = product.find(class_="mzr-tc-group-item-href").text
        folder = "data/"
        response = requests.get(link, headers=headers)
        response = response.text
        with open(f"{folder}html_files/{name}.html", 'w', encoding="utf-8") as file:
            file.write(response)
        with open(f"{folder}html_files/{name}.html", encoding="utf-8") as file:
            source = file.read()
        soup = BeautifulSoup(source, "lxml")
        alert = soup.find("div",
                          class_="uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top")
        if alert is not None:
            continue
        t_heads = soup.find("table",
                            class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find(
            "thead").find("tr").find_all("th")
        book = openpyxl.Workbook()
        sheet = book.active
        sheet["A1"] = t_heads[0].text
        sheet["B1"] = t_heads[1].text
        sheet["C1"] = t_heads[2].text
        sheet["D1"] = t_heads[3].text
        sheet["E1"] = t_heads[4].text
        row = 2
        products_info = soup.find("table",
                                  class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed").find(
            "tbody").find_all("tr")
        for i in products_info:
            info = i.find_all("td")
            sheet[row][0].value = info[0].find('a').text
            sheet[row][1].value = info[1].text
            sheet[row][2].value = info[2].text
            sheet[row][3].value = info[3].text
            sheet[row][4].value = info[4].text
            row += 1
            info_list.append({
                t_heads[0].text: info[0].find("a").text,
                t_heads[1].text: info[1].text,
                t_heads[2].text: info[2].text,
                t_heads[3].text: info[3].text,
                t_heads[4].text: info[4].text
            })
        with open(f'D:\Parsing\data\json_files/{name}.json', "w", encoding="utf-8") as file:
            json.dump(info_list, file, indent=4, ensure_ascii=False)
        book.save(f"{folder}tables/{name}.xlsx")
        book.close()
        print(f'Информация таблицы: "{name}" успешно собрана')
    print("Сбор информации завершен")


if __name__ == "__main__":
    url = "https://health-diet.ru/table_calorie/?ysclid=l4warl2j3a826575871"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
    }
    Scrap(url, headers)
