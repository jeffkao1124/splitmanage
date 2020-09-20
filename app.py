<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1" />
    <title>查帳小幫手</title>
    <script src="https://d.line-scdn.net/liff/1.0/sdk.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0/jquery.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script>
        function print_value() {

            document.getElementById("result") = document.getElementById("number").value
        }
</script>
<script>
	function initializeApp(data) {  //初始化LIFF
        var userid = data.context.userId;
        var groupid = data.context.groupId; //取得ID
        document.getElementById('post_groupID').value = groupid;

	}
	function closewin() {

        liff.closeWindow();


	}
    function pushMsg() {
        var msg = '刪除';
        liff.sendMessages([  //推播訊息
			{ type: 'text',
			  text: msg
			},
		])
			.then(() => {
			alert('已刪除所有資料');
            window.location.reload();
			});


    }

	$(document).ready(function () {
    
		liff.init(function (data) {  //初始化LIFF
            initializeApp(data);
		});
		
        $('#sure').click(function (e) {  //按下確定鈕
            
			closewin(); 
		});
        $('#delete').click(function (e) {  //按下確定鈕
            
			pushMsg(); 
		});
	});
</script>
<style>
body{
  background-color: #FFEEDD;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;

}

li {
  float: left;
  justify-content:center;
}
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  text-align: center;
  padding: 8px;
}

tr:nth-child(odd) {background-color: #ffe7ca;}

th{
    background-color: #ffdcb1;
}
.custom-select {
  position: relative;
  font-family: Arial;
}

.custom-select select {
  display: none; /*hide original SELECT element:*/
}

.select-selected {
  background-color: #ffe7ca;
}

/*style the arrow inside the select element:*/
.select-selected:after {
  position: absolute;
  content: "";
  top: 14px;
  right: 10px;
  width: 0;
  height: 0;
  border: 6px solid transparent;
  border-color: #ffe7ca transparent transparent transparent;
}

/*point the arrow upwards when the select box is open (active):*/
.select-selected.select-arrow-active:after {
  border-color: transparent transparent #b37224 transparent;
  top: 7px;
}

/*style the items (options), including the selected item:*/
.select-items div,.select-selected {
  color: #000000;
  padding: 8px 16px;
  border: 1px solid transparent;
  border-color: transparent transparent rgba(0, 0, 0, 0.1) transparent;
  cursor: pointer;
  user-select: none;
}

/*style items (options):*/
.select-items {
  position: absolute;
  background-color: #ffdcb1;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 99;
}

/*hide the items when the select box is closed:*/
.select-hide {
  display: none;
}
.button2 {
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    padding: 0px 17px;
    border: 1px solid #a88d8d;
    border-radius: 7px;
    background: #b2eaff;
    background: -webkit-gradient(linear, left top, left bottom, from(#b2eaff), to(#94afff));
    background: -moz-linear-gradient(top, #b2eaff, #94afff);
    background: linear-gradient(to bottom, #b2eaff, #94afff);
    -webkit-box-shadow: #fff1f1 0px 0px 46px 0px;
    -moz-box-shadow: #fff1f1 0px 0px 46px 0px;
    box-shadow: #fff1f1 0px 0px 46px 0px;
    text-shadow: #ffffff 1px 1px 1px;
    font: normal normal bold 20px arial;
    color: #001891;
    text-decoration: none;
}
.button2:hover,
.button2:focus {
    border: 1px solid #f0c9c9;
    background: #d6ffff;
    background: -webkit-gradient(linear, left top, left bottom, from(#d6ffff), to(#b2d2ff));
    background: -moz-linear-gradient(top, #d6ffff, #b2d2ff);
    background: linear-gradient(to bottom, #d6ffff, #b2d2ff);
    color: #001891;
    text-decoration: none;
}
.button2:active {
    background: #6b8c99;
    background: -webkit-gradient(linear, left top, left bottom, from(#6b8c99), to(#94afff));
    background: -moz-linear-gradient(top, #6b8c99, #94afff);
    background: linear-gradient(to bottom, #6b8c99, #94afff);
}
.button2:before{
    content:  "\0000a0";
    display: inline-block;
    height: 20px;
    width: 20px;
    line-height: 20px;
    margin: 0 4px -6px -4px;
    position: relative;
    top: 0px;
    left: 0px;
    background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUAgMAAADw5/WeAAAADFBMVEVUpN47cpuIv+j////WN4xEAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMklEQVQImWN4tWrVqtUMDQwMDIzEkfb//wBJ09BYIGnCwAsW+QskWUNDiTPhamhoaDgATK0VHVjI0UwAAAAASUVORK5CYII=") no-repeat left center transparent;
    background-size: 100% 100%;
}
.button3 {
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    padding: 0px 17px;
    border: 1px solid #a88d8d;
    border-radius: 7px;
    background: #ffb2b2;
    background: -webkit-gradient(linear, left top, left bottom, from(#ffb2b2), to(#ff9494));
    background: -moz-linear-gradient(top, #ffb2b2, #ff9494);
    background: linear-gradient(to bottom, #ffb2b2, #ff9494);
    -webkit-box-shadow: #fff1f1 0px 0px 46px 0px;
    -moz-box-shadow: #fff1f1 0px 0px 46px 0px;
    box-shadow: #fff1f1 0px 0px 46px 0px;
    text-shadow: #ffffff 1px 1px 1px;
    font: normal normal bold 20px arial;
    color: #910000;
    text-decoration: none;
}
.button3:hover,
.button3:focus {
    border: 1px solid #f0c9c9;
    background: #ffd6d6;
    background: -webkit-gradient(linear, left top, left bottom, from(#ffd6d6), to(#ffb2b2));
    background: -moz-linear-gradient(top, #ffd6d6, #ffb2b2);
    background: linear-gradient(to bottom, #ffd6d6, #ffb2b2);
    color: #001891;
    text-decoration: none;
}
.button3:active {
    background: #996b6b;
    background: -webkit-gradient(linear, left top, left bottom, from(#996b6b), to(#ff9494));
    background: -moz-linear-gradient(top, #996b6b, #ff9494);
    background: linear-gradient(to bottom, #996b6b, #ff9494);
}
.button3:before{
    content:  "\0000a0";
    display: inline-block;
    height: 20px;
    width: 20px;
    line-height: 20px;
    margin: 0 4px -6px -4px;
    position: relative;
    top: 0px;
    left: 0px;
    background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUAgMAAADw5/WeAAAADFBMVEVUpN47cpuIv+j////WN4xEAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMklEQVQImWN4tWrVqtUMDQwMDIzEkfb//wBJ09BYIGnCwAsW+QskWUNDiTPhamhoaDgATK0VHVjI0UwAAAAASUVORK5CYII=") no-repeat left center transparent;
    background-size: 100% 100%;
}
</style>
</head>
<body>


<script type="text/javascript">
function divShow(){
document.getElementById("btnshow").style.display="block";
document.getElementById("btnhref").innerHTML ="隱藏清單";
document.getElementById("btnhref").href ="javascript:divhidden()";
}
function divhidden(){
document.getElementById("btnshow").style.display="none";
document.getElementById("btnhref").innerHTML ="展開清單";
document.getElementById("btnhref").href ="javascript:divShow()"; 
}
</script>

<script type="text/javascript">
function div_show(){
document.getElementById("simpleshow").style.display="block";
document.getElementById("notsimpleshow").style.display="none";
document.getElementById("simplehref").innerHTML ="不簡化結算";
document.getElementById("simplehref").href ="javascript:div_hidden()";
}
function div_hidden(){
document.getElementById("simpleshow").style.display="none";
document.getElementById("notsimpleshow").style.display="block";
document.getElementById("simplehref").innerHTML ="簡化結算";
document.getElementById("simplehref").href ="javascript:div_show()"; 
}
</script>

<div align="center">
<ul>
  <li><img src="https://imgur.com/JV8bflw.png" width=100px height=auto align=center></img></li>
  <li><h1 style="line-height:100px;"><strong>查帳結算</strong></h1></li>
</ul>
    <p align="left" style="background-color:#fff9c4;font-size:20px;text-align: left;">
    <strong> &nbsp目前帳目</strong>
    <a href="javascript:divShow();" id="btnhref" class="btn-slide">展開清單</a>
    </p>
    <div  style="display: none;" id="btnshow">
    <table>
        <thead align="center">
            <th>編號</th>
            <th>項目</th>
            <th>金額</th>
            <th>代墊/分帳者</th>
        </thead>
        <tbody>
            {% for _data in save_list %}
                <tr>
                    <td align="center">{{ _data.number }}</td>
                    <td>{{ _data.clearMessage }}</td>
                    <td>{{ _data.withcurr }}</td>
                    <td>{{ _data.payPeople }}</td>
                </tr>
            {% endfor%}
        </tbody>
    </table><br/>
     <p class="text-background" align="left" style="font-size:18px;"><strong>&nbsp編輯：</strong></p>
    <script>
        function deleteOption(list){
            var index=list.selectedIndex;
            var msg = 'delete';
            msg=msg+index;
        if(index>0){        
            liff.sendMessages([  
			{ type: 'text',
			  text: msg
			},
		])
        .then(() => {
			alert('已刪除該筆資料');
            window.location.reload();
			});
        }

            if (index>0)
                list.options[index]=null;

            else
                alert("無資料可以刪除！");
        }
        
        </script>
        
        <form>
        <select id=theList size=5>
            <option value='請選擇'>請選擇</option>
            {% for _data in save_list %}
            <option id="{{ _data.number }}" value="{{ _data.number }}">{{ _data.number }} {{ _data.message }} {{ _data.account }}</option>
            {% endfor %}

        </select>
        <br/><br/>
        <input type="button" value="刪除此筆資料" onclick="deleteOption(theList)" class="button2"><br>
        </form>
        <br/>
        <input type="button" name="ok" id="delete" value="刪除所有資料" class=button3><br>
        <br/>
    </div>
    
    <p align="left" style="background-color:#fff9c4;font-size:20px;text-align: left;"><strong> &nbsp代墊與欠款統計</strong></p>
    <!-- <p>說明：以現在匯率換算</p><br/> -->
    <p align="left">&nbsp群組分帳人：</p>
    <p>{{ peopleResult }}</p><br/>
    <p align="left">&nbsp金額(NTD)
        <img src="{{ img }}" align="right" >
    </p>
    <p>分帳者</p>
    <p style="font-color: red"><strong>{{warning}}</strong></p>
    <br/>
    <p align="left" style="background-color:#fff9c4;font-size:20px;text-align: left;">
    <strong>&nbsp結算</strong>
    <a href="javascript:div_show();" id="simplehref">簡化結算</a>
    </p>

    <div id="notsimpleshow" style="display: block;">
    {% for list in notsimplify %}
    <p>{{list}}</p>
     {% endfor %}
    </div><br/>
    <div id="simpleshow" style="display: none;">
    {% for list in settle %}
    <p>{{ list }}</p>
    {% endfor %}
    </div><br/>
    <p style="text-align:left;"><strong>Q : 什麼是簡化分帳?</strong></p>
    <p style="text-align:left;"><strong>A : 簡化分帳能夠自動將群組中的債務結合起來。</strong></p>
    <p style="text-align:left;">如下圖所示 : </p>
    <p style="text-align:left;">假設鳥A原本必須先將1000元交給鳥B，鳥B再將1000元交給C；若使用簡化分帳，則會顯示鳥A直接將1000元交給C</p>
<img src="https://imgur.com/TNJOwwD.png" style="width:240px;height:auto;"></img>

</div>
<br/>
</body>
</html>

