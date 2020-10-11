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
        GroupPeopleString += _data.nickname +'%'
    new_list = GroupPeopleString.strip('%').split('%')
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

# def strip_tag(_Data.message):
#     if '#餐飲' in _Data.message:
#         withoutcurr=_Data.message.strip("#餐飲")
#     elif "#住宿" in _Data.message:
#         withoutcurr=_Data.message.strip("#住宿")
#     elif "#交通" in _Data.message:
#         withoutcurr=_Data.message.strip("#交通")
#     elif "#行程" in _Data.message:
#         withoutcurr=_Data.message.strip("#行程")
#     else:
#         withoutcurr=_Data.message
#     return withoutcurr


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
        historySettle_dic['message'] =_data.message
        historySettle_list.append(historySettle_dic) 
        
    dataNumber=len(historySettle_list) 
    account= np.zeros((person_num,person_num)) 
    exchange_rate_USD = 0
    exchange_rate_JPY = 0
    exchange_rate_EUR = 0
    for i in range(dataNumber): 
        b=dict(historySettle_list[i]) 
        GroupPeopleString=b['GroupPeople'].split(' ')
        if 'USD' in b['message']:   #匯率轉換
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
                exchange_rate_EUR = get_exchangeRate(3)
                exchange_rate = exchange_rate_EUR
        else:
            exchange_rate = 1

        payAmount = exchange_rate * int(b['Account']) / (len(GroupPeopleString)-1)  #不包含代墊者
        a1=set(person_list)      #分帳設定有的人 
        a2=set(GroupPeopleString) 
        duplicate = list(a1.intersection(a2))         #a1和a2重複的人名 
        for j in range(len(duplicate)):      #誰付誰錢矩陣 2給1 
            place1=person_list.index(GroupPeopleString[0]) 
            place2=person_list.index(duplicate[j]) 
            account[place1][place2]+=payAmount 
    result=[]
    for j in range ( person_num ): #誰付誰錢輸出 
        for i in range ( person_num ): 
            payAmount = account[i][j] - account[j][i]
            if ( payAmount>0 ):
                result.append(person_list[j]+'付給'+person_list[i] +' NT$' +str(round(payAmount,2)))
    return result

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try:

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
                    if '#餐飲' in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#住宿" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#交通" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#行程" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    else:
                        withoutcurr=_Data.message
                    withoutcurr=withoutcurr.strip("USD/")
                    Money='$'+str(_Data.account)
                elif 'JPY/' in _Data.message:
                    if '#餐飲' in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#住宿" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#交通" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#行程" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    else:
                        withoutcurr=_Data.message
                    withoutcurr=withoutcurr.strip("JPY/")
                    Money='¥'+str(_Data.account)                
                elif 'EUR/' in _Data.message:
                    if '#餐飲' in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#住宿" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#交通" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#行程" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    else:
                        withoutcurr=_Data.message
                    withoutcurr=withoutcurr.strip("EUR/")
                    Money='€'+str(_Data.account)          
                else:
                    if '#餐飲' in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#住宿" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#交通" in _Data.message:
                        withoutcurr=_Data.message[:-3]
                    elif "#行程" in _Data.message:
                        withoutcurr=_Data.message[:-3]
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
            tagFood=0
            tagHousing=0
            tagTrans=0
            tagTravel=0
            tagOthers=0
            tagMoney=[]
            tagCategory=[]
            for i in range(count): #分帳金額
                b=dict(save_list[i])
                GroupPeopleString=b['group_num'].strip('%').split('%')
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

                tagAmount=exchange_rate*int(b['account'])
                if  '#餐飲' in b['message']:
                    tagFood+=tagAmount
                elif  '#住宿' in b['message']:
                    tagHousing+=tagAmount
                elif  '#交通' in b['message']:
                    tagTrans+=tagAmount
                elif  '#行程' in b['message']:
                    tagTravel+=tagAmount
                else:
                    tagOthers+=tagAmount


                payAmount=exchange_rate*int(b['account'])/len(GroupPeopleString)
                a1=set(person_list)
                a2=set(GroupPeopleString)
                duplicate = list(a1.intersection(a2))
                count=0
                for j in range(len(duplicate)):
                    place=person_list.index(duplicate[j])
                    account[place] -= payAmount
            
            if tagFood!=0:
                tagMoney.append(tagFood)
                tagCategory.append('餐飲')
            if tagHousing!=0:
                tagMoney.append(tagHousing)
                tagCategory.append("住宿")
            if tagTrans!=0:
                tagMoney.append(tagTrans)
                tagCategory.append("交通")
            if tagTravel!=0:
                tagMoney.append(tagTravel)
                tagCategory.append("行程")
            if tagOthers!=0:
                tagMoney.append(tagOthers)
                tagCategory.append("不分類")

            for j in range(len(save_list)):
                b=dict(save_list[j])
                GroupPeopleString=b['group_num'].strip('%').split('%')
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
            account_list=list(account)
            print(account_list)
            sys.stdout.flush()
            print(account)
            sys.stdout.flush()
            # changeArray=np.array(account.flatten())        
            changeArray=account
            print(changeArray)
            sys.stdout.flush()
            

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

            
            return render_template('index_form.html',**locals())
        except:
            
            return '1.請檢查帳目和設定分帳者的人名是否一致  2.請檢查項目和金額中間是否有多打空格'

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0

    return groupId

if __name__ =="__main__":
    app.run()

