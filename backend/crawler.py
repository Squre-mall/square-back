import requests
from bs4 import BeautifulSoup
import sys, os
import pprint

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
django.setup()

from cloth.models import Cloth
cloth_fields = Cloth._meta.local_fields[1:-2]   # id, created, modified 제외
cloth_fields_names = tuple(field.name for field in cloth_fields)

def musinsa_crawling():
    musinsa_category_codes_dict = {
        'outer': '002'
    }
    musinsa_store_url = 'https://store.musinsa.com'
    musinsa_items_lists_code = '/app/items/lists/'

    urls = tuple(musinsa_store_url + musinsa_items_lists_code +
            musinsa_category_codes_dict[category] for category in musinsa_category_codes_dict)

    for categ, url in zip(musinsa_category_codes_dict.keys(), urls):
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')

        # 각 아이템 상세페이지
        # items_a = soup.select('#searchList > li > div.li_inner > div.list_img > a')
        # items_a_href = [a['href'] for a in items_a]
        # for item_url_tail in items_a_href:

        items_li = soup.select('#searchList > li.li_box')

        itemsList = []

        for item in items_li:
            itemDict = {}

            try:
                tmp_a = item.select_one('div.li_inner > div.list_img > a')

                productNo = tmp_a.get('href').split('/')[-2]
                brand = item.select_one('div.li_inner > div.article_info > p.item_title > a').get_text()
                title = item.select_one('div.li_inner > div.article_info > p.list_info > a').get('title').replace('  ', ' ')
                description = '1'
                clothImgUrl = tmp_a.find('img').get('data-original')
                price = item.select_one('div.li_inner > div.article_info > p.price').get_text().split()[-1]
                # TODO
                TODO = """
                price가 두개인경우 존재(세일상품)
                1. 세일여부 컬럼을 추가하여 관리
                2. 그냥 세일 가격만 저장
                3. 세일 전/후 가격 둘다 저장(리스트형식)
                """
                gender = item.select_one('div.icon_group > ul > li').get_text()
                category = categ
            except:
                print(title, 'error')

            for a in cloth_fields_names:
                itemDict.update({a: locals()[a]})
            itemsList.append(itemDict)

            ################################################
            # 각 아이템 상세페이지

            # item_url = musinsa_store_url + item_url_tail
            #
            # req2 = requests.get(item_url)
            # html2 = req2.text
            # soup2 = BeautifulSoup(html2, 'html.parser')
            #
            # items_a = soup2.select('#product_order_info > div.explan_product.product_info_section'
            #                        ' > ul > li:nth-child(1) > p.product_article_contents > strong > a')
            ################################################

            # productNo 가 존재하면 update
            c = Cloth.objects.filter(productNo=productNo)
            if c: c.update(**itemDict)
            else: Cloth(**itemDict).save()

            pprint.pprint(c)


        # pprint.pprint(itemsList)





if __name__ == "__main__":
    musinsa_crawling()