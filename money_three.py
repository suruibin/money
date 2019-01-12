# -*- encoding: utf-8 -*-
import sys
import os,time
import requests


zjyd_num=1    #资金异动股票统计
ltp_control=0 #流通盘数据标准，用于只运行一次 节约时间
LTP_AMOUNT=0  #流通盘大小
LTP_code_name=''#流通盘股票名
zf=0            #涨幅
num=0
num_stock=0
only_money_data=0

headers = {'User-Agent': 'Mozilla/6.8 (Linux; U; Android 7.2; zh-cn; EVA-AL10 Build/HUAWEIEVA) AppleWebKit/637.06 (KHTML, like Gecko)Version/6.0 Chrome/64.6.0.0 MQQBrowser/8.9 Mobile Safari/824.34',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Cookie': '_hc.v=fee4035a-52cc-5c94-565f-304a138f8ebb.1488093255; s_ViewType=10; _tr.u=tTc0c4RuJVVj5ygF; download_banner=on; cityid=2; __mta=55808532.1489472362111.1489570116986.1489580839204.7; PHOENIX_ID=4a010918-15b65a6e8fa-30a99b7; aburl=1; cy=2; cye=beijing; default_ab=shop%3AA%3A1%7Cshopreviewlist%3AA%3A1; __mta=55808532.1489472362111.1489570116986.1492060873556.7'

}
#全部资金排名
#三日资金排名
url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(BalFlowMainNet3)&sr=-1&p=1&ps=4050&js=var%20ZYROyBQj={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA3&rt=50737950'
#url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=4050&js=var%20ewSUDvwm={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=5'
url_begin = 'http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id='
url_end1 = '2&type=hff&rtntype=2&js=result25951001([(x)])&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&callback=result25951001&_=1509687474214' #300  000
url_end2 = '1&type=hff&rtntype=2&js=result25951001([(x)])&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&callback=result25951001&_=1509687474214' #600

#主板资金排名
#url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=4050&js=var%20FMBoJLAT={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C.2&sty=DCFFITA&rt=50322875'
#创业板资金排名
#url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=4050&js=var%20vXjpKMsO={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C.80&sty=DCFFITA&rt=50322858'
#中小板资金排名
#url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=4050&js=var%20TXcJEooc={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C.13&sty=DCFFITA&rt=50322869'
#三日资金排名
#url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMainNet3)&sr=-1&p=1&ps=4050&js=var%20hZehvJNX={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA5&rt=50322837'
#五日资金排名
#url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMainNet5)&sr=-1&p=1&ps=4050&js=var%20hZehvJNX={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA5&rt=50322837'
#个股实时查询:(一条数据)
#uri = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=3006182&sty=DCFFMBFMS&st=&sr=&p=&ps=&cb=&js=result65402263((x))&token=0b9469e9fdfd123fcec4532ae1c20f4f&callback=result65402263&_=1509687474171'
#个股实时查询:(4个月内)
#url = 'http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id=3006182&type=hff&rtntype=2&js=result25951001([(x)])&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&callback=result25951001&_=1509687474214'


def mkdir(path):
    path=path.strip()
    path=path.rstrip("/")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        #print path+' 创建成功'
        return True

def Create_Yjc(code,blk): #创建预警池
    blk_name="money/tdx_blk/"+blk
    
    with open(blk_name,"r+") as frw:
        frw.seek(0,os.SEEK_END)
        if code[0] == '0' or code[0] =='3' :
            code_data = "0"+code+"\r\n"
        else:
            code_data = "1"+code+"\r\n"
        frw.write(code_data)
   
def DC_LTP(code=''):
    global LTP_AMOUNT,LTP_code_name,zf
    i=0
    url_begin='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd='
    url_end='&sty=ESBFD&st=z&sr=&p=&ps=&cb=&js=jcbr1515301221931148((x))&token=01c2801b9710ae7a0cbf712bd30c5715&callback=jcbr1515301221931148&_=1515301220876'
    
    if code[0]=='6':
        url=url_begin+code+'1'+url_end
    else:
        url=url_begin+code+'2'+url_end
    
    r = ''
    while r == '':
        try:
            r = requests.get(url, headers=headers)#获取数据'
        except:
            time.sleep(5)
            print("远端服务器无响应,正在尝试重新连接..")
            continue
    #r = requests.get(url, headers=headers)#获取数据
    
    data_all=r.text
    #print data_all
    rows=data_all.split(",")
    for row in rows:
        i +=1
        #print i,row
        if i ==3:
            LTP_code_name=row
            strlen=len(LTP_code_name)
            
            if ord(LTP_code_name[strlen-1]) in (97,122) or ord(LTP_code_name[strlen-1]) in (65,90):
                if strlen == 4:
                    LTP_code_name = LTP_code_name + " "
                if strlen == 3:
                    LTP_code_name = LTP_code_name + "   "
                    
            strlen=len(LTP_code_name)
            if strlen ==3:
                LTP_code_name = LTP_code_name + "  "
                
        if i ==7:
            if(row =='-'):    
                #print row
                row='0'
            
            zf=float(row)
        if i ==17:
            if(row =='-'):    
                #print row
                row='0'
            LTP_AMOUNT=int(row)/100000000
    #print LTP_code_name,zf,LTP_AMOUNT

def money_day_three():#三日资金排名
    global num,num_stock,Desktop_File
    num=0
    Top_num=1 #用来记录前50名资金排名 并选出流通盘小于300亿的票


    ff=open("money/tdx_blk/ZJPM.blk",'wb+')
    ff.close()
    mkpath="money/tdx_blk/"
    mkdir(mkpath)
    #os.chdir("~/")
    
    r = ''
    while r == '':
        try:
            r = requests.get(url, headers=headers)#获取数据'
        except:
            time.sleep(5)
            print("远端服务器无响应,正在尝试重新连接..")
            continue
    #r = requests.get(url, headers=headers)#获取数据
    
    for i in eval(r.text[45:][:-1]):
        data=i.split(',')
        if len(data[5]) <=1:
            money=0
        else:
            money=float(data[5])

        #创建每日最强资金流通达信板块
        if(Top_num <=15) and money >5000:
            code=str(data[1])
            DC_LTP(code)
            if LTP_AMOUNT <100:
                Top_num +=1
                #print code
                Create_Yjc(code,"ZJPM.blk")


#money_day_three()