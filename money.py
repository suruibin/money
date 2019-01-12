# -*- encoding: utf-8 -*-
import os,sys,time,datetime
import requests#,thread
from money_three import money_day_three
from rzrq import rzrq_moudle

#reload(sys)
#sys.setdefaultencoding( "utf-8" )

num_stock=0
func_ret=0

headers = {'User-Agent': 'Mozilla/6.8 (Linux; U; Android 7.2; zh-cn; EVA-AL10 Build/HUAWEIEVA) AppleWebKit/637.06 (KHTML, like Gecko)Version/6.0 Chrome/64.6.0.0 MQQBrowser/8.9 Mobile Safari/824.34',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Cookie': '_hc.v=fee4035a-52cc-5c94-565f-304a138f8ebb.1488093255; s_ViewType=10; _tr.u=tTc0c4RuJVVj5ygF; download_banner=on; cityid=2; __mta=55808532.1489472362111.1489570116986.1489580839204.7; PHOENIX_ID=4a010918-15b65a6e8fa-30a99b7; aburl=1; cy=2; cye=beijing; default_ab=shop%3AA%3A1%7Cshopreviewlist%3AA%3A1; __mta=55808532.1489472362111.1489570116986.1492060873556.7'

}

#全部资金排名
url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=4050&js=var%20ewSUDvwm={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=5'

def git_reset():
    time.sleep(1)
    os.chdir("money/")
    #os.system("git reset --hard FETCH_HEAD")
    #os.system("git add .")
    #os.system("git commit -m \"Data Share.\" -a >msg.txt")
    #os.system("git push -q")
    os.system("git push -u origin master -f")
    print('数据已同步到服务器!')
    
    os.chdir("../")
    
def update_to_git():
    time.sleep(1)
    os.chdir("money/")
    
    os.system("git add .")
    os.system("git commit -m \"Data Share.\" -a >msg.txt")
    os.system("git push -q")
    #os.system("git push -u origin master -f -q")
    print('数据已同步到服务器!')
    
    os.chdir("../")
    
def time_week_res():
    
    time_flage=int(time.strftime("%H%M", time.localtime()))
    week_flage=time.strftime("%a", time.localtime())
    
    #print  time_flage,week_flage
    
    #if(time_flage  < 915 or time_flage >1515  or(time_flage >1140 and time_flage <1250) or week_flage =='Sat' or week_flage =='Sun' ):
    if(time_flage >1515 or week_flage =='Sat' or week_flage =='Sun' or time_flage <900 ):
        return 1
    else:
        return 0

def long_sleep():
    for i in range(0,4):
        print(u'程序休眠中...')
        time.sleep(150)
        
    
def money_day():#每日实时个股资金
    global num_stock
    requests.packages.urllib3.disable_warnings()
      
    data= ''
    while data == '':
        try:
            data = requests.get(url, headers=headers)#获取数据'
        except:
            time.sleep(5)
            print(u"远端服务器无响应,正在尝试重新连接..")
            #data = requests.get(url, headers=headers)#获取数据'
            #os.system("python money.py")
            return 0
            continue
    #r = requests.get(url, headers=headers)#获取数据
    for i in eval(data.text[45:][:-1]):
        tmp = i.split(',')
        net_time=tmp[15].replace("-",'')[:8]
        #net_time = tmp[15][:4]+tmp[15][5:7]+tmp[15][8:10]
        #print(net_time)
        break 

    with open('money/money.txt','w') as ff:
        for i in eval(data.text[45:][:-1]):
            
            tmp = i.split(',')
            code=str(tmp[1])
            money=str(tmp[5])
            
            if(code[0]=='0' or code[0]=='3'):
                pre_fix = "0"
            else:
                pre_fix = "1"
            
            if len(money) <=1:
                money='0'
            
            ff.write(pre_fix+'|'+code+'|'+net_time+'|'+money+'\r\n')
            num_stock +=1
    
    return 1

#延时程序
def runTask_day(second=200):
    global num_stock,func_ret
    
    flage=1
    lhb_try=0
    rzrq_try=0
    first_in=0
    
    while True:
        func_ret=0
        num_stock=0
        error_count=0
        if(flage==1):
            #money_day()
            rec_data=0
            while rec_data == 0:
                try:
                    rec_data=money_day()
                    error_count = error_count+1
                    #print(error_count)
                    if (error_count >=2) :
                        print(u"money_day():远端服务器无响应,正在尝试重新连接..")
                        time.sleep(5)          
                except:
                    print(u"runTask_day():远端服务器无响应,正在尝试重新连接..")
                    time.sleep(5)
                    continue
                
            print(u"%d 条资金趋势数据已获取!" %(num_stock))
            money_day_three()
            print(u"%d 条资金排名数据已获取!" %(num_stock))
            update_to_git()
       
        
        #刚开始进入运行一次 龙虎榜和融资融券数据
        if(first_in==0):
            os.system('./kpl_lhb')
            rzrq_moudle()
            first_in = 1
            
        #早上运行几次融资融券程序    
        time_flage=int(time.strftime("%H%M", time.localtime()))
        if(time_flage >910 and time_flage <1000):
            if(rzrq_try <10):
                rzrq_moudle()
                rzrq_try +=1
        
        #时间和周末限制
        time_week_flage=0
        time_week_flage=time_week_res()
        update_to_git()
        if(time_week_flage ==1):
            flage=0
            print(u"沪深股市已停止交易!\n程序后台睡眠中!!!")
            time_flage=int(time.strftime("%H%M", time.localtime()))
            if(time_flage >1630 and time_flage <1830):
                if(lhb_try <10):
                    os.system('./kpl_lhb')
                    update_to_git()
                lhb_try +=1
                long_sleep()
            if(time_flage >1830 and time_flage < 2230):
                long_sleep()
                lhb_try=0
            if(time_flage >2230 and time_flage <2340):
                rzrq_moudle()
                update_to_git()
                long_sleep()
                rzrq_try=0
        else:
            flage=1
        
        #程序正常延时
        time.sleep(second)
        func_ret=1


#runTask_day(150)

def main_op():
    git_reset()
    print (u"主程序已启动!\n")
    while True:
        error=0
        func_ret=0
        
        while func_ret == 0:
            try:
                func_ret=runTask_day()
                error = error+1
                print("error:%d\n"%(error))
                if (error >=2) :
                    print(u"func():error..")
                    time.sleep(5)          
            except:
                print(u"func_ret():error except..")
                time.sleep(5)
                func_ret=0
                continue
        print(u"主程序没运行!\n")
        time.sleep(5)
        

def weak_main():
    print(u"唤醒程序启动!\n")
    while True:
        time_flage=int(time.strftime("%H%M", time.localtime()))
        time_week_flage=0
        time_week_flage=time_week_res()
        #if 1:
        if(((time_flage >930 and time_flage <1135) or (time_flage >1300 and time_flage <1520)) and time_week_flage ==0):
            
            file="./money/money.txt"
            ModifiedTime=time.localtime(os.stat(file).st_mtime)
            y=int(time.strftime('%Y', ModifiedTime))
            m=int(time.strftime('%m', ModifiedTime))
            d=int(time.strftime('%d', ModifiedTime))
            H=int(time.strftime('%H', ModifiedTime))
            M=int(time.strftime('%M', ModifiedTime))
            starttime=datetime.datetime(y,m,d,H,M)
            #starttime = datetime.datetime.now()  
            #long running  
            #time.sleep(5)
            endtime = datetime.datetime.now()
            time_to_now=int((endtime - starttime).seconds)
            if(time_to_now >600):
                rec_data=0
                while rec_data == 0:
                    try:
                        rec_data=money_day()
                        update_to_git()
                        print(u"weak_main() exec money_day()")
                        time.sleep(5)   
                    except:
                        print(u"weak_main():")
                        time.sleep(5)
                        continue
        time.sleep(5)
        
try:
   #thread.start_new_thread(main_op, ())
   #thread.start_new_thread(weak_main, ())
   main_op()
except:
   print("Error: unable to start thread!")
 
while 1:
   pass
