import requests
from lxml import etree

#锦江区https://cd.fangjia.zhuge.com/jinjiang/
r = requests.get('https://cd.fangjia.zhuge.com/')

datas = r.text

html = etree.HTML(datas)

#数据时间
update_time = html.xpath('/html/body/div[5]/div[7]/div[2]/div[2]/div[3]/text()')[0]
if update_time is None or update_time == '':
    update_time = '截止到目前'
update_time = update_time.split('，')[-1]

#新上房源数
today_new_hosuse_num = html.xpath('.//div[@class="room-today-new"]/text()')
#新上房源与昨日相比
room_price_up_or_down = html.xpath('(.//div[@class="room-price-up"]/span)[2]/text()')
room_price_percent = html.xpath('(.//div[@class="room-price-up"]/span)[3]/text()')
if len(room_price_up_or_down) == 0:
    room_price_up_or_down = html.xpath('(.//div[@class="room-price-low"]/span)[2]/text()')
    room_price_percent = html.xpath('(.//div[@class="room-price-low"]/span)[3]/text()')

#今日降价房源
today_hosuse_low = html.xpath('.//div[@class="room-today-low"]/text()')

#均价
average_price = html.xpath('(.//div[@class="average-price"]/p)[1]/text()')
#环比
price_up_or_low = html.xpath('(.//div[@class="average-price-up"]/span)[1]/text()')
if len(price_up_or_low) > 0:
    relative = html.xpath('(.//div[@class="average-price-up"]/span)[2]/text()')
else:
    price_up_or_low = html.xpath('(.//div[@class="average-price-low"]/span)[1]/text()')
    relative = html.xpath('(.//div[@class="average-price-low"]/span)[2]/text()')

#7天信息成交套数
seven_day_nums = html.xpath('/html/body/div[5]/div[7]/div[2]/div[2]/div[1]/div[2]/div[1]/text()')
transfer_lastday = html.xpath('(.//div[@class="transfer-lastweek"]/span)[2]/text()')

content = '''
成都每日楼市数据播报：{}，成都二手房均价为{}元/平方米，环比上月{}，
{}，与昨日相比{}，
成都二手房{}，相比昨日{}。
'''.format(update_time, average_price[0], price_up_or_low[0] + relative[0], 
        today_new_hosuse_num[0], room_price_up_or_down[0] + room_price_percent[0],
        seven_day_nums[0],transfer_lastday[0])

print(content)