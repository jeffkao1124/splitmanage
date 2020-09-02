from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from sqlalchemy import desc
from flask import render_template
import numpy as np
import sys

app=Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] ='postgres://szcllceapwexar:6de14fbb3a64a6ac2c1f81d1a6f6e528ee13cdbf7e2abf80ee0f57396180b228@ec2-54-236-146-234.compute-1.amazonaws.com:5432/deu86ol7k69o7t'

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
    SetMsgNumber = usermessage.query.filter(usermessage.group_id==groupId).filter(usermessage.status=='set').count()
    data_UserData = usermessage.query.filter(usermessage.group_id==groupId).filter(usermessage.status=='set')
    history_dic = {}
    history_list = []
    for _data in data_UserData:
        history_dic['nickname'] = _data.nickname
        history_list.append(history_dic)
        history_dic = {}
    final_list=[]
    for i in range(SetMsgNumber):
        final_list.append(str(history_list[i]['nickname']))
    new_list=[]
    for i in final_list:
        if not i in new_list:
            new_list.append(i)
    if mode==1:
        return len(new_list)
    elif mode==2:
        return new_list
    else:
        return 0


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        groupId = request.values['groupId']
        SaveMsgNumber = usermessage.query.filter(usermessage.group_id==groupId).filter(usermessage.status=='save').count()
        data_SaveData = usermessage.query.filter(usermessage.group_id==groupId).filter(usermessage.status=='save')
        save_dic = {}
        save_list = []
        count=0
        for _Data in data_SaveData:
            save_dic['group_num'] = _Data.group_num
            save_dic['account'] = _Data.account
            save_dic['message'] = _Data.message
            save_list.append(save_dic)
            save_dic = {}
            count+=1
        # savefinal_list=[]
        # count=0
        # for i in range(SaveMsgNumber):
        #     count+=1
        #     savefinal_list.append(str(save_list[i]['message'])+' '+str(save_list[i]['account'])+' '+str(save_list[i]['group_num']))
        # perfect_list=''
        # for j in range(SetMsgNumber):
        #     perfect_list=perfect_list+str(j+1)+'.'+str(savefinal_list[j])+'\n'

        person_list  = get_groupPeople(groupId,2)
        dataNumber=count
        Zero= np.zeros((dataNumber,get_groupPeople(groupId,1)))
        for i in range(dataNumber):
            b=dict(save_list[i])
            GroupPeopleString=b['group_num'].split(' ')
            payAmount=int(b['account'])/len(GroupPeopleString)
            a1=set(get_groupPeople(groupId,2))
            a2=set(GroupPeopleString)
            duplicate = list(a1.intersection(a2))
            count=0
            for j in range(len(duplicate)):
                place=get_groupPeople(groupId,2).index(duplicate[count])
                Zero[i][place]=payAmount
                count+=1

        replaceZero=Zero
        totalPayment=replaceZero.sum(axis=0)

        paid= np.zeros((1,len(get_groupPeople(groupId,2))))
        for i in range(len(get_groupPeople(groupId,2))):
            for j in range(len(save_list)):
                b=dict(save_list[j])
                GroupPeopleString=b['group_num'].split(' ')
                if GroupPeopleString[0] == get_groupPeople(groupId,2)[i]:
                    paidAmount=int(b['account'])
                    paid[0][i]=paid[0][i]+paidAmount
                else:
                    continue

        account=paid-totalPayment

        #將人和錢結合成tuple，存到一個空串列
        person_account=[]
        for i in range(len(person_list)):
            zip_tuple=(person_list[i],account[0][i])
            person_account.append(zip_tuple)
        print(person_account)
        sys.stdout.flush()

        #重複執行交換動作
        result=""
        for i in range(len(person_list)-1):
            #排序
            person_account=sorted(person_account, key = lambda s:s[1])

            #找到最大、最小值
            min_tuple=person_account[0]
            max_tuple=person_account[-1]
            min=float(min_tuple[1])
            max=float(max_tuple[1])

            #交換，印出該付的錢
            if min==0 or max==0:
                pass
            elif (min+max)>0:
                result=result+str(min_tuple[0])+'付給'+str(max_tuple[0])+str(abs(round(min,2)))+'元'+'\n'
                max_tuple=(max_tuple[0],min+max)
                min_tuple=(min_tuple[0],0)
            elif (min+max)<0:
                result=result+str(min_tuple[0])+'付給'+str(max_tuple[0])+str(abs(round(max,2)))+'元'+'\n'
                min_tuple=(min_tuple[0],min+max)
                max_tuple=(max_tuple[0],0)
            else:
                result=result+str(min_tuple[0])+'付給'+str(max_tuple[0])+str(abs(round(max,2)))+'元'+'\n'
                min_tuple=(min_tuple[0],0)
                max_tuple=(max_tuple[0],0)
            person_account[0]=min_tuple
            person_account[-1]=max_tuple

        settle = result.split()

        
        return render_template('index_form.html',**locals())

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0

    return groupId

if __name__ =="__main__":
    app.run()
