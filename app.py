from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from sqlalchemy import desc
from flask import render_template

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

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        groupId = request.values['groupId']
        SaveMsgNumber = usermessage.query.filter(usermessage.group_id==groupId).filter(usermessage.status=='save').count()
        data_SaveData = usermessage.query.filter(usermessage.group_id==groupId).filter(usermessage.status=='save')
        save_dic = {}
        save_list = []
        for _Data in data_SaveData:
            save_dic['group_num'] = _Data.group_num
            save_dic['account'] = _Data.account
            save_dic['message'] = _Data.message
            save_list.append(save_dic)
            save_dic = {}
        # savefinal_list=[]
        # count=0
        # for i in range(SaveMsgNumber):
        #     count+=1
        #     savefinal_list.append(str(save_list[i]['message'])+' '+str(save_list[i]['account'])+' '+str(save_list[i]['group_num']))
        # perfect_list=''
        # for j in range(SetMsgNumber):
        #     perfect_list=perfect_list+str(j+1)+'.'+str(savefinal_list[j])+'\n'















        
        return render_template('index_form.html',**locals())

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0



    return groupId

if __name__ =="__main__":
    app.run()
