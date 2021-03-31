import requests
from bs4 import BeautifulSoup
import pandas as pd




def get_hrefs(url):
    hrefs = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html5lib")
    elements = soup.find_all('div', {'class': 'views-row'})
    for i in range(len(elements)):
        name = soup.select('span.field-content a')[i].get("href")
        hrefs.append("https://data.gov.ru" + name)
    return hrefs

def get_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html5lib")
    try:
        name = soup.select('tbody td[property="dc:title"]')[0].text
        hyper = soup.select('a.available')[1].get("href")
        format = soup.select('tbody td[property="dc:format"]')[0].text
        f_date = soup.select('tbody td[property="dc:created"]')[0].text
        l_date = soup.select('tbody td[property="dc:modified"]')[0].text
        kwords = soup.select('tbody td[property="dc:subject"]')[0].text
        type = soup.select("div.panel-pane.pane-custom.pane-3.pane-node-field-rubric a")[0].text
        views = int(soup.select("div.pane-node-total-count")[0].text)
        downloads = int(soup.select("div.od-common-pubdlcnt-count-wrapper span")[0].text)
    except:
        return ["", "", "", "", "", "", "", "", ""]
    else:
        return [name, hyper, format, f_date, l_date, kwords, type, views, downloads]

def get_data(url):
    columns = ["Наименование", "Ссылка", "Формат", "Дата первой публикации", "Дата последней публикации", "Ключевые слова", "Тип", "Просмотры", "Загрузки"]
    data = []

    # Главная страница
    main_page_urls = get_hrefs(url)
    for u in main_page_urls:
        data.append(get_info(u))
    print("Страница 1. Выполнено")

    # Остальные страницы
    for i in range(1, 15):
        page_url = f"{url}?page={i}"
        page_urls = get_hrefs(page_url)

        for u in page_urls:
            data.append(get_info(u))
        print(f"Страница {i+1}. Выполнено")
    
    data = pd.DataFrame(data, columns = columns)

    return data


if __name__ == "__main__":
    url = 'https://data.gov.ru/organizations/7710349494'
    data = get_data(url)
    print(data)
    data.to_excel("output.xlsx")
