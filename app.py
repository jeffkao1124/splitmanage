from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from sqlalchemy import desc
from flask import render_template
import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import base64
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import re


app=Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] ='postgres://brjgqjmnamwnxc:2038ec5ace178f7e6f34d1015384a39e7274126f60488b14a5403582ae5a8966@ec2-3-95-87-221.compute-1.amazonaws.com:5432/d3s7d1dsfli0sd'

app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
groupId=0
class usermessage(db.Model):
    __tablename__ ='usermessage'
    id = db.Column(db.String(50), primary_key=True)
    group_num = db.Column(db.Text)
    nickname = db.Column(db.Text)
    group_id = db.Column(db.String(50))
    type = db.Column(db.Text)
    status = db.Column(db.Text)
    account = db.Column(db.Text)
    user_id = db.Column(db.String(50))
    message = db.Column(db.Text)
    birth_date = db.Column(db.TIMESTAMP)


def get_groupPeople(groupId,mode):
    data_UserData = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.group_id==groupId).filter(usermessage.status=='set')
    GroupPeopleString=''
    for _data in data_UserData:
        GroupPeopleString += _data.nickname +' '
    new_list = GroupPeopleString.strip('  ').split(' ')
    new_list=list(set(new_list)) #刪除重複

    if mode==1:
        return len(new_list)
    elif mode==2:
        return new_list
    else:
        return 0

#從資料庫取得匯率
def get_exchangeRate(mode):
    if mode==1:
        data_UserData = usermessage.query.order_by(usermessage.birth_date.desc()).filter(usermessage.status=='USD' ).limit(1).all()
        for _data in data_UserData:
            USDrate = eval(_data.message)
        return USDrate
    if mode==2:
        data_UserData = usermessage.query.order_by(usermessage.birth_date.desc()).filter(usermessage.status=='JPY' ).limit(1).all()
        for _data in data_UserData:
            JPYrate=eval(_data.message)
        return JPYrate
    if mode==3:
        data_UserData = usermessage.query.order_by(usermessage.birth_date.desc()).filter(usermessage.status=='EUR' ).limit(1).all()
        for _data in data_UserData:
            EURrate=eval(_data.message)
        return EURrate

def get_notsimplify():
    groupId = request.values['groupId']
    dataSettle_UserData = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.group_id==groupId).filter(usermessage.status=='save')
    historySettle_list = [] 
    person_list  = get_groupPeople(groupId,2)  #分帳設定人名
    person_num = get_groupPeople(groupId,1)  #分帳設定人數
    for _data in dataSettle_UserData: 
        historySettle_dic = {} 
        historySettle_dic['Account'] = _data.account 
        historySettle_dic['GroupPeople'] =_data.group_num 
        historySettle_list.append(historySettle_dic) 
        
    dataNumber=len(historySettle_list) 
    account= np.zeros((person_num,person_num)) 
    for i in range(dataNumber): 
        b=dict(historySettle_list[i]) 
        GroupPeopleString=b['GroupPeople'].split(' ')
        payAmount = round( int(b['Account']) / (len(GroupPeopleString)-1),2)  #不包含代墊者
        a1=set(person_list)      #分帳設定有的人 
        a2=set(GroupPeopleString) 
        duplicate = list(a1.intersection(a2))         #a1和a2重複的人名 
        for j in range(len(duplicate)):      #誰付誰錢矩陣 2給1 
            place1=person_list.index(GroupPeopleString[0]) 
            place2=person_list.index(duplicate[j]) 
            account[place1][place2]+=payAmount 
    result=[]
    for i in range ( person_num ): #誰付誰錢輸出 
        for j in range ( person_num ): 
            payAmount = account[i][j] - account[j][i]
            if ( payAmount<0 ):
                result.append(person_list[i]+'付給'+person_list[j] +'NT$' +str(account[i][j]))
    return result

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':

        groupId = request.values['groupId']
        data_SaveData = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.group_id==groupId).filter(usermessage.status=='save')
        save_list = []
        count=0
        for _Data in data_SaveData:
            count+=1
            save_dic = {}
            save_dic['number'] = count
            firstSpace=_Data.group_num.split(' ', 1 ) #代墊者/分帳者
            withoutSpace= firstSpace[0]+ ' / ' + firstSpace[1]
            save_dic['group_num'] = _Data.group_num
            save_dic['payPeople'] = withoutSpace
            save_dic['account'] = _Data.account
            save_dic['message'] = _Data.message
            if 'USD/' in _Data.message:
                withoutcurr=_Data.message.strip("USD/")
                Money='$'+str(_Data.account)
            elif 'JPY/' in _Data.message:
                withoutcurr=_Data.message.strip("JPY/")
                Money='¥'+str(_Data.account)                
            elif 'EUR/' in _Data.message:
                withoutcurr=_Data.message.strip("EUR/") 
                Money='€'+str(_Data.account)          
            else:
                withoutcurr=_Data.message
                Money='NT$'+str(_Data.account)
            save_dic['clearMessage'] = withoutcurr
            save_dic['withcurr'] = Money
            save_list.append(save_dic)
            
        person_list  = get_groupPeople(groupId,2)
        person_num = get_groupPeople(groupId,1)
        numberlist=[]
        peopleResult=''
        for i in range(get_groupPeople(groupId,1)):
            peopleResult+=str(i+1)+'.'+str(person_list[i])+' '
            numberlist.append(i+1)

        account = np.zeros(person_num)
        exchange_rate_USD = 0
        exchange_rate_JPY = 0
        exchange_rate_EUR = 0
        for i in range(count): #分帳金額
            b=dict(save_list[i])
            GroupPeopleString=b['group_num'].strip(' ').split(' ')
            del GroupPeopleString[0]

            if  'USD' in b['message']:
                if exchange_rate_USD:
                    exchange_rate = exchange_rate_USD
                else:
                    exchange_rate_USD = get_exchangeRate(1)
                    exchange_rate = exchange_rate_USD
            elif 'JPY' in b['message']:
                if exchange_rate_JPY:
                    exchange_rate = exchange_rate_JPY
                else:
                    exchange_rate_JPY = get_exchangeRate(2)
                    exchange_rate = exchange_rate_JPY
            elif 'EUR' in b['message']:
                if exchange_rate_EUR:
                    exchange_rate = exchange_rate_EUR
                else:
                    exchange_rate_EUR = get_exchangeRate(1)
                    exchange_rate = exchange_rate_EUR
            else:
                exchange_rate = 1

            payAmount=exchange_rate*int(b['account'])/len(GroupPeopleString)
            a1=set(person_list)
            a2=set(GroupPeopleString)
            duplicate = list(a1.intersection(a2))
            count=0
            for j in range(len(duplicate)):
                place=person_list.index(duplicate[j])
                account[place] -= payAmount
        
        for j in range(len(save_list)):
            b=dict(save_list[j])
            GroupPeopleString=b['group_num'].strip(' ').split(' ')
            if 'USD' in b['message']:
                if exchange_rate_USD:
                    exchange_rate = exchange_rate_USD
                else:
                    exchange_rate_USD = get_exchangeRate(1)
                    exchange_rate = exchange_rate_USD
            elif 'JPY' in b['message']:
                if exchange_rate_JPY:
                    exchange_rate = exchange_rate_JPY
                else:
                    exchange_rate_JPY = get_exchangeRate(2)
                    exchange_rate = exchange_rate_JPY
            elif 'EUR' in b['message']:
                if exchange_rate_EUR:
                    exchange_rate = exchange_rate_EUR
                else:
                    exchange_rate_EUR = get_exchangeRate(1)
                    exchange_rate = exchange_rate_EUR
            else:
                exchange_rate = 1

            for i in range(person_num):  
                if GroupPeopleString[0] ==  person_list[i]:
                    account[i] += exchange_rate * int(b['account'])

        changeArray=np.array(account.flatten())

        #將人和錢結合成tuple，存到一個空串列
        person_account=[]
        for i in range(person_num):
            zip_tuple=(person_list[i],account[i])
            person_account.append(zip_tuple)

        #重複執行交換動作
        result=""
        for i in range(person_num-1):  #排序
            person_account=sorted(person_account, key = lambda s:s[1])

            #找到最大、最小值
            min_tuple=person_account[0]
            max_tuple=person_account[-1]
            #找到目前代墊最多的人
            if i==0:
                maxPerson=max_tuple[0]
                minPerson=min_tuple[0]

            min=float(min_tuple[1])
            max=float(max_tuple[1])

            #交換，印出該付的錢
            if min==0 or max==0:
                pass
            elif (min+max)>0:
                result=result+str(min_tuple[0])+'付給'+str(max_tuple[0])+'NT$'+str(abs(round(min,2)))+'\n'
                max_tuple=(max_tuple[0],min+max)
                min_tuple=(min_tuple[0],0)
            elif (min+max)<0:
                result=result+str(min_tuple[0])+'付給'+str(max_tuple[0])+'NT$'+str(abs(round(max,2)))+'\n'
                min_tuple=(min_tuple[0],min+max)
                max_tuple=(max_tuple[0],0)
            else:
                result=result+str(min_tuple[0])+'付給'+str(max_tuple[0])+'NT$'+str(abs(round(max,2)))+'\n'
                min_tuple=(min_tuple[0],0)
                max_tuple=(max_tuple[0],0)
            person_account[0]=min_tuple
            person_account[-1]=max_tuple
        if count>=1:
            warning=str(maxPerson)+'目前代墊最多!'
        else:
            warning=''

        settle = result.split()
        notsimplify=get_notsimplify()

        plt.rcParams['figure.dpi'] = 200  # 分辨率
        plt.figure(facecolor='#FFEEDD',edgecolor='black',figsize=(2.5,1.875))
        plt.rcParams['savefig.dpi'] = 150  # 圖片像素
        #plt.rcParams["font.sans-serif"]= "Microsoft JhengHei"
        # plt.rcParams['figure.figsize'] = (1.5, 1.0)  # 设置figure_size尺寸800x400
        # plt.grid(True,color = "#ededed") 
        axes = plt.gca()
        axes.yaxis.grid(color = "#ededed")
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=4)
        my_x_ticks = np.arange(0, get_groupPeople(groupId,1)+1, 1)
        plt.xticks(my_x_ticks)
        plt.rcParams["font.family"]="SimHei"
        # plt.xlabel('Person List',fontsize=10)
        # plt.ylabel('Amount',fontsize=10)
        colors=[]
        for _data in changeArray:
            if _data>0:
                colors.append('#FFA042')
            else:
                colors.append("#FF5151")
        plt.bar(numberlist,changeArray,width=0.5,color=colors)

        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        # 將matplotlib圖片轉換為HTML
        imb = base64.b64encode(plot_data)  # 對plot_data進行編碼
        ims = imb.decode()
        imd = "data:image/png;base64," + ims
        img = imd
        
        return render_template('index_form.html',**locals())

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0

    return groupId

if __name__ =="__main__":
    app.run()

