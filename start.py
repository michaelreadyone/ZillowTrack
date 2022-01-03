import requests
from bs4 import BeautifulSoup
import re
from house_detail import get_metrics


zipcode = 15206



url_zillow_zipcode = f'https://www.zillow.com/pittsburgh-pa-{zipcode}/house,multifamily,townhouse_type/1.5-_baths/'
headers = {
    "cookie": 'JSESSIONID=F116D48265286F345BFD53280A243396; zguid=23|$40e68918-84fe-47a6-8069-cc2487af6845; zgsession=1|73b37f1d-84be-4a04-af1b-c282e24d19e8; _pxvid=fcdc730f-6b83-11ec-9222-647046664c6a; _pxff_rf=1; _pxff_fp=1; _pxff_bsco=1; _px3=d83da6be3935561a93174fe815211cae40cb16920c77b3fc9eca9606f41fd21b:AaMm2rblA6GBUGGRzOax4S7NsaLrH+sKCd7CaEEIsXRdF3M/LiykAB+autsUBr1HUG1DwvhUq0epucAuzlvZyw==:1000:xSzCdBw0xjDADwCFA2uzU3Z0uMrSYuBGQbtp7VsH4l7fC4ZI7HfV9sd/u3DbZXE+XUfni0hqvaiS1tHjP9KmNnKmHOdSn/9zQmF94GawOY0FkbSgSvKRtMMvJRYq6aslh0vIA2Q/K3iIJkAn5ZQBov6ujfp9IWi2bTQBlsP6lODpd0Yn8fPM9BzeDdiXL1wyd+c0jXhMLiJkpNGIFXUGbw==; _ga=GA1.2.2098024061.1641097532; _gid=GA1.2.2077016672.1641097532; zjs_user_id=null; zjs_anonymous_id="40e68918-84fe-47a6-8069-cc2487af6845"; _gat=1; __gads=ID=12ab913c518b639b:T=1641097534:S=ALNI_MavSTEHaLeJaTqM0krQHJFfLgc14Q; _gcl_au=1.1.1097772823.1641097535; KruxPixel=true; DoubleClickSession=true; __pdst=86d6f642a5d846c4a268946daecef1e6; _uetsid=081e16606b8411eca44b6dd21a145327; _uetvid=081e66c06b8411ecb2615300fe473263; _fbp=fb.1.1641097535968.904432185; _pin_unauth=dWlkPU0yUTVZbU5rTlRFdE1XVXhZaTAwWkRCakxXRXpNR1F0T1RJMk5tRXdZamM1TkRNeQ; AWSALB=agk9lKKq5vam5Ioe3FczabBG7CZhlwCQmorFTGk8YIcG675/tIMBNmPYQIvbrfJW0Z5Kn5nRbx9nRaQcFakS45lCCcXS+SgyVy6eOk+LP7jV1lUlAaYGgzqskRxu; AWSALBCORS=agk9lKKq5vam5Ioe3FczabBG7CZhlwCQmorFTGk8YIcG675/tIMBNmPYQIvbrfJW0Z5Kn5nRbx9nRaQcFakS45lCCcXS+SgyVy6eOk+LP7jV1lUlAaYGgzqskRxu; search=6|1643689539701|rect=40.48238649533691%2C-79.91380465098031%2C40.46508419146056%2C-79.98590834901974&rid=63932&disp=map&mdm=auto&p=1&sort=days&z=1&fs=1&fr=0&mmm=0&rs=0&ah=0&singlestory=0&housing-connector=0&abo=0&garage=0&pool=0&ac=0&waterfront=0&finished=0&unfinished=0&cityview=0&mountainview=0&parkview=0&waterview=0&hoadata=1&zillow-owned=0&3dhome=0&featuredMultiFamilyBuilding=0		63932						; utag_main=v_id:017e190920f4001541d2cbd75b5f05069002606100d05$_sn:1$_se:1$_ss:1$_st:1641099335735$ses_id:1641097535735;exp-session$_pn:1;exp-session$dcsyncran:1;exp-session$tdsyncran:1;exp-session$dc_visit:1$dc_event:1;exp-session$dc_region:us-east-1;exp-session$ttd_uuid:5110c0f3-ba6c-413e-8152-f1abbeeeccc6;exp-session; KruxAddition=true',
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
res = requests.get(url=url_zillow_zipcode, headers=headers)
# soup = BeautifulSoup(page.content, "html.parser")


house_urls = re.findall('www.zillow.com/homedetails/(.*?)"', res.text)
house_urls = set(house_urls)
print(house_urls)

# 为什么同样的url，从浏览器里和从script里返回的结果不一样？
# 好吧，又是我煞笔了，我在script里面的url，没有加筛选器阿。那应该怎么加呢？

# succefully get the list of house, what next? house detail info
data = []

for url in house_urls:
    house_url = 'https://www.zillow.com/homedetails/' + url
    data.append(get_metrics(house_url))

# 先试试dataframe，再试试mongodb
