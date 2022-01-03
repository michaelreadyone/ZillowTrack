import requests
from bs4 import BeautifulSoup
import re


def get_metrics(house_url):
    # house_url = 'https://www.zillow.com/homedetails/1160-Beechwood-Blvd-Pittsburgh-PA-15206/11629224_zpid/'

    headers = {
        "cookie": 'zguid=23|$40e68918-84fe-47a6-8069-cc2487af6845; _pxvid=fcdc730f-6b83-11ec-9222-647046664c6a; _ga=GA1.2.2098024061.1641097532; _gid=GA1.2.2077016672.1641097532; zjs_user_id=null; zjs_anonymous_id="40e68918-84fe-47a6-8069-cc2487af6845"; __gads=ID=12ab913c518b639b:T=1641097534:S=ALNI_MavSTEHaLeJaTqM0krQHJFfLgc14Q; _gcl_au=1.1.1097772823.1641097535; KruxPixel=true; __pdst=86d6f642a5d846c4a268946daecef1e6; _fbp=fb.1.1641097535968.904432185; utag_main=v_id:017e190920f4001541d2cbd75b5f05069002606100d05$_sn:1$_se:1$_ss:1$_st:1641099335735$ses_id:1641097535735;exp-session$_pn:1;exp-session$dcsyncran:1;exp-session$tdsyncran:1;exp-session$dc_visit:1$dc_event:1;exp-session$dc_region:us-east-1;exp-session$ttd_uuid:5110c0f3-ba6c-413e-8152-f1abbeeeccc6;exp-session; KruxAddition=true; _pin_unauth=dWlkPVpUTTJZalF6T1RVdE56ZzFPUzAwTWpOaUxUbGtZalF0TVdVMU5qa3dabVprWXpoaw; JSESSIONID=44C71B4607B07D90F7A7F75403C97919; zgsession=1|4ae67d67-496d-4079-9351-02eefe236666; _pxff_bsco=1; _gat=1; _px3=467ef1c9970c94e6658777df988341093fff2e35d72b0cbca53c252fd37d8109:nTSfQyl0QPowQ/Dr0Rh9m1DSGm2o03dPeZ2m9Myexc5lbQaM1xCd/zBxy6FcF6BZPWzghLHFDqrBahSK1SrXxg==:1000:dL+TexCPdwtpzWy+pe9AjhK/RlTpeeE0KU7angvKy8xbmQBHv/bL2M8tuTXtN1UfVD5ps52KIwiE4EJ8iAE30c1H7RVLY/91bLkI599Jh5rT3SKcuH63wT1BJFhC7ZWkVU4x5ELMRkV3p2iql4TIpiymtQIvvfK3u9LG3REjFiutB5ASwLHs2wl2hokqmRAqHKId6wrw5nQmPT1ZixeTZQ==; search=6|1643703599470|rect=40.47871663455279%2C-79.8601770401001%2C40.42130495166255%2C-79.97767925262451&disp=map&mdm=auto&p=1&sort=days&z=1&fs=1&fr=0&mmm=0&rs=0&ah=0&singlestory=0&housing-connector=0&abo=0&garage=0&pool=0&ac=0&waterfront=0&finished=0&unfinished=0&cityview=0&mountainview=0&parkview=0&waterview=0&hoadata=1&zillow-owned=0&3dhome=0&featuredMultiFamilyBuilding=0		63937						; DoubleClickSession=true; _uetsid=081e16606b8411eca44b6dd21a145327; _uetvid=081e66c06b8411ecb2615300fe473263; AWSALB=ZofqZZI5mXl4gj5gNVV8gGT0RDxiwjUDRCfcTo/4pVyfVPFjWfEEmhifXYYETNkvFQDAyTap6+M9L4MuiJN4c307KAgmt2w3r6P76MAZjxCMIyrAGVLizKMo7hrg; AWSALBCORS=ZofqZZI5mXl4gj5gNVV8gGT0RDxiwjUDRCfcTo/4pVyfVPFjWfEEmhifXYYETNkvFQDAyTap6+M9L4MuiJN4c307KAgmt2w3r6P76MAZjxCMIyrAGVLizKMo7hrg',
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    res = requests.get(url=house_url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    sc = soup.find('div', class_='summary-container')
    summary = sc.get_text(separator='spsp').split('spsp')
    print(summary)
    price, bd_num, ba_num, sqft = summary[0], summary[1], summary[4], summary[7]
    jump = 3 if 'Price cut' in summary[10] else 0

    address, zestimate = summary[10 + jump] + \
        summary[12 + jump], summary[17 + jump]
    sc_dict = {
        'price': price,
        'bd_num': bd_num,
        'ba_num': ba_num,
        'sqft': sqft,
        'address': address,
        'zestimate': zestimate
    }

    Building, Calendar, Heating, Snowflake, Parking, Lot, PriceSquareFeet = '', '', '', '', '', '', ''

    ff = soup.find('ul', class_='dpf__sc-xzpkxd-0 jHoFQf')
    summary_ff = ff.get_text(separator='spsp').split('spsp')
    ff_dict = {}
    for i in range(0, len(summary_ff), 2):
        if summary_ff[i] == 'Building':
            Building = summary_ff[i + 1]
        if summary_ff[i] == 'Calendar':
            Calendar = summary_ff[i + 1]
        if summary_ff[i] == 'Heating':
            Heating = summary_ff[i + 1]
        if summary_ff[i] == 'Snowflake':
            Snowflake = summary_ff[i + 1]
        if summary_ff[i] == 'Parking':
            Parking = summary_ff[i + 1]
        if summary_ff[i] == 'Lot':
            Lot = summary_ff[i + 1]
        if summary_ff[i] == 'Price Square Feet':
            PriceSquareFeet = summary_ff[i + 1]

    return_list = [price, bd_num, ba_num, sqft, address, zestimate, Building,
                   Calendar, Heating, Snowflake, Parking, Lot, PriceSquareFeet, house_url]

    return return_list
