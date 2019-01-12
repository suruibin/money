# -*- encoding: utf-8 -*-
import time,sys
import requests,re

#reload(sys)
#sys.setdefaultencoding( "utf-8" )

headers = {'User-Agent': 'Mozilla/6.0 (Linux; U; Android 7.0; zh-cn; EVA-AL10 Build/HUAWEIEVA-AL12) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/40.0.0.0 MQQBrowser/7.5 Mobile Safari/537.36',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Cookie': '_hc.v=fee4035a-52cc-5c94-565f-304a138f8ebb.1488093255; s_ViewType=10; _tr.u=tTc0c4RuJVVj5ygF; download_banner=on; cityid=2; __mta=55808532.1489472362111.1489570116986.1489580839204.7; PHOENIX_ID=0a010918-15b65a6e8fd-30a99b7; aburl=1; cy=2; cye=beijing; default_ab=shop%3AA%3A1%7Cshopreviewlist%3AA%3A1; __mta=55808532.1489472362111.1489570116986.1492060873556.7'

}
zjyd_num=1 #异动股票统计
ltp_control=0 #流通盘数据标准，用于只运行一次 节约时间
LTP_AMOUNT=0 #流通盘大小
LTP_code_name=''#流通盘股票名
zf=0            #涨幅
rzrq_count=0
#融资融券
#需要自己填写时间
url_ok='http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(tdate=%272017-11-23T00:00:00%27)&st=rzjmre&sr=-1&p=1&ps=4050&js=var%20LLyjEfZz={pages:(tp),data:(x)}&type=RZRQ_DETAIL_NJ&time=1&rt=50380005'
#网页提取时间
url0='http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(tdate=%27'
url1='T00:00:00%27)&st=rzjmre&sr=-1&p=1&ps=4050&js=var%20LLyjEfZz={pages:(tp),data:(x)}&type=RZRQ_DETAIL_NJ&time=1&rt=50380005'

#全部融资融券
url_begin='http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(scode=%27'
url_end='%27)&st={sortType}&sr={sortRule}&p={page}&ps={pageSize}&js=var%20{jsname}={pages:(tp),data:(x)}{param}'

Rzrq_Desktop_File="money/rzrq.txt"


#数据获取
num=0
ttime=0
jrj_time=0

def get_rzrq_day():#融资融券 当日全部
    global num,ttime

    #############获取时间######################
    time_url='http://data.eastmoney.com/rzrq/detail/all.html'

    r = ''
    while r == '':
        try:
            r = requests.get(time_url, headers=headers)#获取数据'
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            print("now let me continue...")
            continue
    #r = requests.get(time_url, headers=headers)#获取数据'
    i=0
    dd=str(r.text[5000:])
    p=re.compile(r'"tdate":"\d{4}-\d{2}-\d{2}')
    for m in p.finditer(dd):
        i +=1
        if i ==2:
            cc=m.group()
            break
    #print cc
    dd=cc.split("\"")
    ttime=dd[3]
    #print ttime
    url=url0+ttime+url1
    #print url
    ##########################################
    rr = ''
    while rr == '':
        try:
            rr = requests.get(url, headers=headers)#获取数据'
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            print("now let me continue...")
            continue
    #rr = requests.get(url, headers=headers)#获取数据'
    #print r.text
    data_all=str(rr.text[28:][:-1])
    rows=data_all.split("},")
    #print "done"
    outputFile = open(Rzrq_Desktop_File, "w") #Linux
    for row in rows:
        #print row[10:16],row[458:498]
        dd=row.split(",")
        name=dd[0][10:16]
        date=dd[3][9:13]+dd[3][14:16]+dd[3][17:19]
        #data=dd[21][9:]  #净买
        #data=dd[40][11:] #融资融券余额差值
        data=dd[39][9:]   #融资融券余额
        #print name,date,data

        if int(str((name[0])[0])) >3:
            prefix='1|'
        else:
            prefix='0|'

        mm=data.split(".")

        #print stock_file_name,net_time,money
        outputFile.write(prefix+name+"|"+date+"|"+mm[0]+"\r\n")
        
        num +=1

    outputFile.close()


#默认更新当日数据
def rzrq_moudle():
    global num
    num=0
    get_rzrq_day()#更新每日的融资融券数据
    print(ttime,u"%d条融资融券数据已获取!"%(num))
    return num

#rzrq_moudle()
