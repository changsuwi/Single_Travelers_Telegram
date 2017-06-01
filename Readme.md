# Readme

## BOT介紹

名稱：**SingleTravelers** (@GoGoTest_bot)

簡介：是一個旅遊景點推播bot，可以搜尋所在位置附近景點或是搜尋指定位置的景點，並可用inline mode 在群組或是朋友中分享景點 :smile:

伺服器平台： Heroku

Database： mlab(MongoDB)

## 如何實作出這個bot 

### pyTelegramBotAPI

採用pyTelegramBotAPI這個api來開發telegram bot

### 旅遊景點data來源：

政府opendata http://data.gov.tw/node/7777

### google map api & imgur api


因為opendata很多景點並沒有圖片連結，且為了實作旅遊景點導航，因此採用google map api，依照

關鍵字抓取旅遊景點圖片與該景點的google map id & url，並用imgur api 自動上傳圖片，有了圖

片網址與google map 網址，就可以讓bot傳送附圖的景點資訊與導航連結

### database

用mongodb資料庫來存景點資料，並依使用者需求輸出景點資料

## 如何與bot交流

點選start即可開始與bot對話，因放置於heroku的免費方案server，第一次呼叫時會有比較長的等待時間

![](https://i.imgur.com/cQk9jTs.jpg)


bot會回應使用方法，輸入 /search 即可開始找尋景點

![](https://i.imgur.com/GSlIT4m.jpg)

此時可選擇傳送地點或是手動輸入想查詢的地點

![](https://i.imgur.com/Sa8QOXO.jpg)

試著傳送gps座標給bot，bot會回傳一定距離內的4個旅遊景點的圖片與介紹

![](https://i.imgur.com/MyUl1Zy.jpg)

若想看更多的旅遊景點，點擊想看更多按鈕

![](https://i.imgur.com/vMSocfV.jpg)

若想前往該景點，可以點選導航帶我去，會連結到google地圖該景點的位置，例如點選新化高爾夫球場

![](https://i.imgur.com/APBDzyB.jpg)

若想搜尋特定位置的景點，也可直接輸入，舉例:輸入台南

BOT會回傳地址位於台南的景點

![](https://i.imgur.com/gyvtOvk.jpg)

若想再次使用可輸入 /search 即可

### inline mode
輸入 @GoGotest 可以在任何聊天介面呼叫BOT，預設在不輸入任何文字時，會搜尋附近景點

![](https://i.imgur.com/ls7Ahhz.jpg)

若輸入文字，則會判斷地點並輸出符合的景點

![](https://i.imgur.com/8AOg68t.jpg)

點選景點即可分享給好友

![](https://i.imgur.com/OIofDnk.jpg)



## code 說明

### bot.py

主程式，收到從telegram的各種指令執行相對應的動作

### db.py

跟database有關的code放在這邊，當使用者搜尋景點時，會依據使用者的資訊去database抓取相對應的資料

### select_loc.py

用來判斷使用者輸入文字並對應到適當的tag，以利之後查詢景點方便


### single_travelers_construct_db.py

當初用來建database時的程式，會去呼叫google map api來抓取該景點的圖片，並且用imgur api將

圖片上傳至imgur，再將imgur圖片的網址寫入database裡，因imgur api 每小時有流量限制，故設

定為每小時上傳40筆data以免超量，用apscheduler這個套件來達到定時執行

### debug_db.py

開發中途發現眾多database問題，故寫個程式修改database :triumph:
1. 因google map api不一定每個地點都有圖片，故將沒有圖片的地點設定預設圖片
2. 有些opendata地點在google map 上找不到，因此也無法導航，為了避免程式出錯故將這些資料刪除
3. 有些opendata地點沒有地址，用google map api抓取該地點地址

### imgur.py

上傳圖片至imgur的模組

### fsm.py

輸出fsm

## 使用或處理的 telegram function and type

1. send_message 包含傳送含html的訊息
2. reply_to 
3. InlineKeyboardMarkup
4. InlineKeyboardButton
5. 處理 content type = location
6. inline mode
7. InlineQueryResultVenue
8. 處理 callback


