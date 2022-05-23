import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

url = 'https://www.perekrestok.ru/cat/d'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

all_products_page = []

async def get_page_data(session, cat_url):
    async with session.get(url=cat_url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        all_products_card = soup.find_all(class_='sc-dlfnbm ldVxnE')

        for card in all_products_card:
            title = card.find(class_='product-card__title').text
            price_new = card.find(class_='price-new').text
            discont = card.find(class_='product-card__badge').span.text
            link = 'https://www.perekrestok.ru' + card.find(class_='product-card__link').get('href')
            all_products_page.append(
                {
                    "Title": title,
                    "Price_new": price_new,
                    "Discont": discont,
                    "Link": link
                }
            )



async def gather_data():
    url = 'https://www.perekrestok.ru/cat/d'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        category_list = soup.find('div', class_='cat-list-aside__scrollbar').find_all('li', class_='cat-list-aside__item')
        category_hrefs = []
        for cat in category_list:
            cat_href = cat.find('a').get('href')
            cat_href = 'https://www.perekrestok.ru' + cat_href
            category_hrefs.append(cat_href)
        tasks = []

        for cat_url in category_hrefs[:2]:
            task = asyncio.create_task(get_page_data(session, cat_url))
            tasks.append(task)

        await asyncio.gather(*tasks)



def main():
    asyncio.run(gather_data())
    with open('data.json', 'w') as file:
        json.dump(all_products_page, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()