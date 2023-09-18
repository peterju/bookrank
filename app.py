import requests
import re
import bs4

url = "https://www.books.com.tw/web/sys_newtopb/books/"  # 博客來新書網址
html = requests.get(url)  # 利用 requests 套件取回網頁原始碼
if html.status_code != 200:  # 判斷回傳值決定是否正確擷取
    print("網址無效:", html.url)
    quit()

# print(dir(html))
# print(html.headers)
# print(html.encoding)

# 二種抓出網頁標題
# 1. 以 BeautifulSoup 對網頁進行剖析，透過物件抓出網頁標題
soup = bs4.BeautifulSoup(html.text, "lxml")
print(soup.title.text)  # 抓取頁面標題，也可用 soup.title.string 抓出來

# 2. 以 Regular Expression 正規表示式來抓出網頁標題
# 設定比對的樣板, 若附加 re.DOTALL 參數可讓任意字元.可比對換行字元
# patten = re.compile("<title>(.*)</title>")
# result = re.search(patten, html.text)
# print(result.group(1))

# 二種抓出新書榜片段原始碼的方法
# 1. list
brank = soup.select("ul.clearfix")
# print(brank[2].prettify)  # <class 'bs4.element.Tag'>

# 2. <class 'bs4.element.ResultSet'>
brank2 = soup.find_all("ul", {"class": "clearfix"})
# print(brank2[1])  # <class 'bs4.element.Tag'>

# 片段原始碼：第一名
# <li class="item">
#   <div class="stitle">
#     <p class="no_list"><span class="symbol icon_01">TOP</span><strong class="no">1</strong></p>
#   </div>
#   <a href="https://www.books.com.tw/products/0010840659?loc=P_0003_001"><img class="cover" src="//im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/084/06/0010840659.jpg&v=5de5e1fa&w=150&h=150" alt="勇敢層級：用你喜歡的方式，活出你自己"></a>
#   <div class="type02_bd-a">
#     <h4><a href="https://www.books.com.tw/products/0010840659?loc=P_0003_001">勇敢層級：用你喜歡的方式，活出你自己</a></h4>
#     <ul class="msg">
#       <li>作者：<a href='//search.books.com.tw/search/query/key/%E7%B4%AB%E5%9A%B4%E5%B0%8E%E5%B8%AB/adv_author/1/'>紫嚴導師</a></li>
#       <li class="price_a">優惠價：
#         <strong><b>79</b></strong>折
#         <strong><b>269</b></strong>元
#       </li>
#     </ul>
#   </div>
# </li>
#
# 列出排行書籍前100名的 名次、書名、作者、價格
books = []
book = {}
for item in brank[2].select(".item"):
    book["rank"] = item.select_one(".stitle .no").text
    book["title"] = item.select_one(".type02_bd-a").h4.a.text
    # book["author"]=item.select_one(".type02_bd-a .msg").li.a.text                # 因為部分沒有作者的書籍會造成錯誤，因此不能使用此判斷，改用先判斷是否存在作者
    author = item.select_one(".type02_bd-a .msg").li.a
    book["author"] = author.get_text() if author is not None else "不明"
    # print(item.select_one(".type02_bd-a .msg .price_a").contents[3].b.text)      # 因為部分沒有折數的書籍會造成錯誤，因此不能使用此判斷，改用正規表示式

    # 優惠價：79折269元
    price = item.select_one(".type02_bd-a .msg .price_a").text
    patten = re.compile(r"(\d*)元")  # 設定比對的樣板
    result = re.search(patten, price)
    book["price"] = result.group(1)

    # price = item.select_one(".type02_bd-a .msg .price_a")
    # book["price"]=price.get_text() if price is not None else item.select_one(".type02_bd-a .msg .price_a > div:nth-of-type(2)").text

    books.append(book)
    book = {}

# print(books[0].keys())
for book in books:
    print("TOP{} {} 作者：{} 價格：{}".format(book["rank"], book["title"], book["author"], book["price"]))
