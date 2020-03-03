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

img_extension_list = ['jpg', 'gif', 'jpeg']

from cloth.models import Cloth, Cloth_Detail_Musinsa
cloth_fields = Cloth._meta.local_fields[1:-2]   # id, created, modified 제외
cloth_fields_names = tuple(field.name for field in cloth_fields)
cloth_Detail_Musinsa_fields = Cloth_Detail_Musinsa._meta.local_fields[1:] # cloth 제외
cloth_Detail_Musinsa_fields_names = tuple(field.name for field in cloth_Detail_Musinsa_fields)

def musinsa_crawling():
    musinsa_category_codes_dict = {
        'top': '001',
        # 'outer': '002',
    }
    musinsa_store_url = 'https://store.musinsa.com/'
    musinsa_store_detail_url = 'https://store.musinsa.com/app/product/detail/'
    musinsa_items_lists_code = 'app/items/lists/'

    urls = tuple(musinsa_store_url + musinsa_items_lists_code +
            musinsa_category_codes_dict[category] for category in musinsa_category_codes_dict)

    for categ, url in zip(musinsa_category_codes_dict.keys(), urls):
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')

        items_li = soup.select('#searchList > li.li_box')
        for item in items_li:
            itemDict = {}
            itemDetailDict = {}

            try:
                tmp_a = item.select_one('div.li_inner > div.list_img > a')
                productNo = tmp_a.get('href').split('/')[-2]
                clothImgSuffix = tmp_a.find('img').get('data-original').split('goods_img/')[1]
                brand = item.select_one('div.li_inner > div.article_info > p.item_title > a').get_text()
                title = item.select_one('div.li_inner > div.article_info > p.list_info > a').get('title').replace('  ', ' ')

                # 원래 가격, 할인된 가격
                try:
                    prices = item.select_one('div.li_inner > div.article_info > p.price').get_text().split()
                    original_price, discounted_price = prices
                except:
                    original_price, discounted_price = prices[0], None
                price = {"original_price":original_price, "discounted_price":discounted_price}

                gender = item.select_one('div.icon_group > ul > li').get_text()
                category = categ
            except:
                print(title, 'error')

            for field_name in cloth_fields_names:
                itemDict.update({field_name: locals()[field_name]})

            ########################
            # 각 아이템 상세페이지 #
            ########################
            item_detail_url = musinsa_store_detail_url + productNo

            req = requests.get(item_detail_url)
            html = req.text
            soup = BeautifulSoup(html, 'lxml')

            # 제품 설명
            tmp_opinion = soup.select_one('#opinion_con')
            if tmp_opinion: description = tmp_opinion.get_text()
            else: description = None

            # 시즌, 성별, 인기도(1개월)
            tmp_article = soup.select_one('#product_order_info > div.explan_product.product_info_section > ul')
            tmp_p = tmp_article.select_one('li:nth-child(2) > p.product_article_contents')
            season = ' '.join(tmp_p.find('strong').get_text().split())
            gender = tmp_p.select_one('span.txt_gender > span').get_text()
            monthlyPopularity = tmp_article.select_one('li:nth-child(3) > p.product_article_contents'
                                                       ' > strong').get_text()

            # 상세 이미지

            try:
                tmp_imgs = soup.select('#detail_view img')
                detailImageUrlList = [u.get('src') for u in tmp_imgs
                                      if os.path.splitext(u.get('src'))[1]]
            except:
                print(item_detail_url, 'img url 가져오기 오류!')

            # 추가정보
            tmp_tbody = soup.select_one('#page_product_detail > div.right_area.page_detail_product'
                                        ' > div.right_contents.product_info_contents > div.product_info_table'
                                        ' > table > tbody')

            color = tmp_tbody.select_one('tr:nth-child(1) > td:nth-child(2)').get_text()
            sizeNweight = tmp_tbody.select_one('tr:nth-child(1) > td:nth-child(4)').get_text()
            importation = tmp_tbody.select_one('tr:nth-child(2) > td:nth-child(2)').get_text()
            manufacturer = tmp_tbody.select_one('tr:nth-child(2) > td:nth-child(4)').get_text()
            manufacturingYM = tmp_tbody.select_one('tr:nth-child(3) > td:nth-child(2)').get_text()
            manufactured = tmp_tbody.select_one('tr:nth-child(3) > td:nth-child(4)').get_text()
            material = tmp_tbody.select_one('tr:nth-child(4) > td:nth-child(2)').get_text()
            asdirector = tmp_tbody.select_one('tr:nth-child(4) > td:nth-child(4)').get_text()
            precautions = tmp_tbody.select_one('tr:nth-child(5) > td:nth-child(2)').get_text()
            warrantyBasis = tmp_tbody.select_one('tr:nth-child(6) > td:nth-child(2)').get_text()

            for field_name in cloth_Detail_Musinsa_fields_names:
                itemDetailDict.update({field_name: locals()[field_name]})

            ###########
            # DB 저장 #
            ###########

            # --- Cloth ---
            c = Cloth.objects.filter(productNo=productNo)
            # productNo 가 존재하면 update
            if c:
                c.update(**itemDict)
                itemDetailDict.update({'cloth': c[0]})
            else:
                c = Cloth.objects.create(**itemDict)
                itemDetailDict.update({'cloth':c})

            # --- Cloth_Detail_Musinsa ---
            c_detail = Cloth_Detail_Musinsa.objects.filter(cloth__productNo=productNo)
            # cloth__productNo 가 존재하면 update
            if c_detail: c_detail.update(**itemDetailDict)
            else:
                c_detail = Cloth_Detail_Musinsa(**itemDetailDict)
                c_detail.save()

            pprint.pprint(itemDict)
            pprint.pprint(itemDetailDict)



if __name__ == "__main__":
    musinsa_crawling()