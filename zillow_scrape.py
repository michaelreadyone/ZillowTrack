# import modules
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime


# function to return data as list for one house detail information
def get_metrics(house_url, headers, zipcode):
    '''return key house information in a list format giving house url and headers
    '''

    # prepare for soup
    res = requests.get(url=house_url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    # summary info in title
    sc = soup.find('div', class_='summary-container')
    summary = sc.get_text(separator='spsp').split('spsp')

    # hard coded, content may vary in the future, two data format, vars and dict
    # vars for list output, dict for potential json output
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

    # info in Facts and features
    Building, Calendar, Heating, Snowflake, Parking, Lot, PriceSquareFeet = '', '', '', '', '', '', ''
    ff = soup.find('ul', class_='dpf__sc-xzpkxd-0 bqENCM')
    summary_ff = ff.get_text(separator='spsp').split('spsp')

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

    ff_dict = {}
    # for i in range(0, len(summary_ff), 2):
    #     ff_dict[summary_ff[i]] = ff_dict[summary_ff[i+1]]

    # generate return result
    return_list = [price, bd_num, ba_num, sqft, address, zestimate, Building,
                   Calendar, Heating, Snowflake, Parking, Lot, PriceSquareFeet, house_url, zipcode]

    return return_list


# function to return dataframe given the zipcode of searching area
def search_zipcode(zipcode, headers):
    ''' search all house given the zipcode, return a list of list, not dataframe
    '''

    # url from zipcode, also specify house type and number of bathroom conditions
    url_zillow_zipcode = f'https://www.zillow.com/pittsburgh-pa-{zipcode}/house,multifamily,townhouse_type/'
    # url_zillow_zipcode = f'https://www.zillow.com/pittsburgh-pa-{zipcode}/house,multifamily,townhouse_type/1.5-_baths/'
    # url for all types of house
    # url_zillow_zipcode = f'https://www.zillow.com/homes/{zipcode}_rb/'

    # get response from zillow
    res = requests.get(url=url_zillow_zipcode, headers=headers)

    # process urls
    house_urls = re.findall('www.zillow.com/homedetails/(.*?)"', res.text)
    house_urls = set(house_urls)
    print(house_urls)

    # prepare data for dataframe
    data = []
    for url in house_urls:
        house_url = 'https://www.zillow.com/homedetails/' + url
        try:
            data.append(get_metrics(house_url, headers, zipcode))
        except:
            print(f'error in url: {house_url}')

    return data


def get_zipcodes():
    '''return zipcodes inteseted
    '''
    pitts_zipcodes = []
    raw_zips = '15106, 15120, 15201, 15203, 15204, 15205, 15206, 15207, 15208, 15210, 15211, 15212, 15213, 15214, 15215, 15216, 15217, 15218, 15219, 15220, 15221, 15222, 15224, 15226, 15227, 15232, 15233, 15234, 15235, 15236, 15238, 15260, 15290'
    for zipcode in raw_zips.split(', '):
        # print(zipcode)
        pitts_zipcodes.append(zipcode)

    list_a = ['15206']
    list_b = ['15215', '15201', '15224', '15232', '15206', '15208', '15213', '15217', '15207']
    return pitts_zipcodes


def generate_headers():
    '''return headers for srape'''
    return {
        "cookie": 'zguid=23|$f30e8c58-cbe3-4e84-86f5-21fe338b9f7c; _ga=GA1.2.861927222.1634657795; zjs_user_id=null; zjs_anonymous_id="f30e8c58-cbe3-4e84-86f5-21fe338b9f7c"; _gcl_au=1.1.1476391709.1634657796; _pxvid=57d8e154-30f2-11ec-9973-455146757552; __pdst=39863dceec6442a18a9a094cb9764f19; _pin_unauth=dWlkPU9XWmpaR1F4Wm1NdE1UTTNZUzAwTTJZMkxUaGxNMll0Wm1JMk16WXdOek13TnpCag; zgsession=1|0d271aa8-31a5-46ca-ae04-ce6668f6165a; _gid=GA1.2.1337674931.1641414024; KruxPixel=true; DoubleClickSession=true; utag_main=v_id:017c99327f2700af651b1bdd5aa005078001707000ac2$_sn:3$_se:1$_ss:1$_st:1641415824738$dc_visit:3$ses_id:1641414024738;exp-session$_pn:1;exp-session$dcsyncran:1;exp-session$tdsyncran:1;exp-session$dc_event:1;exp-session$dc_region:us-east-1;exp-session; JSESSIONID=7D7641E3C097327805B9CD912889D1CB; KruxAddition=true; g_state={"i_p":1642020713793,"i_l":3}; _gat=1; _pxff_bsco=1; _px3=bd4de2c7100cafa5fb13a762bc9972fd8844e0180b34f87c88adeba824379aa3:dioCp4uf8d+auq1SQJEygsNeVZOalQ9ZO3H1b5HNWtw+VSiTmEty040kzYfqVRa5DIlTXLlCfQ8JGhxCwB/aIQ==:1000:TWCeLfVJk34cJyh0t3H5T0NVQRflwxs4tQt7m1Q57+bBcne7hHlRbShVGHTz5AXHAETWB3z7VphMLa09iOihAwdJreUo/lQS+RpktUv9+HV32kweszAqxIBvfiM2Z6yzryOL7EPoT8zlDJD11I0gukncA8cSzuvNnBuGic+i9WhoggdqlaM2vBzbC6DOAB/QHlEN6blNZiBOhlDUgjUW0w==; _uetsid=ea3867306e6411ec8095cdc9a3e32301; _uetvid=5802f71030f211ecb102e739443dc102; AWSALB=4C3OouS0LXesagt8Xs5cx4fOrBSa2fx5d74LkKtk7HmdC6zS+xP9D+j4zkYfqLOmRsG9YWDd+2LtxiS56o2WSX7huRQM/y+hRyWvyCcWczSod0HPdEQg1kVDFSLd; AWSALBCORS=4C3OouS0LXesagt8Xs5cx4fOrBSa2fx5d74LkKtk7HmdC6zS+xP9D+j4zkYfqLOmRsG9YWDd+2LtxiS56o2WSX7huRQM/y+hRyWvyCcWczSod0HPdEQg1kVDFSLd; search=6|1644008558257|rect=40.486061712683%2C-79.78374481201172%2C40.39277753915928%2C-80.08655548095703&disp=map&mdm=auto&p=1&z=1&beds=2-&days=90&type=house%2Cmultifamily%2Ctownhouse&price=0-500000&mp=0-1701&fs=1&fr=0&mmm=0&rs=0&ah=0&singlestory=0&housing-connector=0&abo=0&garage=0&pool=0&ac=0&waterfront=0&finished=0&unfinished=0&cityview=0&mountainview=0&parkview=0&waterview=0&hoadata=1&zillow-owned=0&3dhome=0&featuredMultiFamilyBuilding=0		43						',
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }


if __name__ == "__main__":
    # write into database or write into a csv. first convert into csv, if no error, write into database

    headers = generate_headers()
    zipcodes = get_zipcodes()

    info = []
    for zipcode in zipcodes:
        datas = search_zipcode(zipcode, headers)
        info += datas

    df = pd.DataFrame(info, columns=['price', 'bd_num', 'ba_num', 'sqft', 'address', 'zestimate', 'Building',
                      'Calendar', 'Heating', 'Snowflake', 'Parking', 'Lot', 'PriceSquareFeet', 'url', 'zipcode'])

    df.to_csv(str(datetime.datetime.now())+'.csv')
