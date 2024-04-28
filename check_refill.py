

# 1.+ Создаем отдельный файл, который работает в отдельном потоке
# 2 + В нем долджен быть цикл While с задержкой во времени работы 5 секунд
# 3.+ На каждой итерации цикла мы запрашиваем чеки со статусом - созданный из нашей базы данных
# 4.+ Внутри цикла создает цикл for 
# 4.+ Он будет перебирать чеки которые были получены из базы данных
# 5.+ Отправляет запрос на получение статуса чека
# 6.+ В Цикле for проверяет статус чеков через if
# 7.+ Если чек оплачен то пополяется баланс клиент и меняет статус в базе данных на оплоченный
# 8.+ Если чек отменен или прошло время действия чека, то меняет статус чека в базе данных

"""
    Создать коннект к sqlite
    Писать SQL запросы 
"""


import sqlite3, requests
import time



connect = sqlite3.connect('D:/Python/Online Store Project/backend/instance/store_database.db')
cursor = connect.cursor()

while True:
    query = 'SELECT * FROM Refill WHERE status_refill==0'

    cursor.execute(query)
    connect.commit()

    refills = cursor.fetchall()
    
    for refill in refills:

        refill = {'id':refill[0],'money':refill[1],'invoice_id':refill[3],'account_id':refill[4]}

        resp = requests.post('https://testnet-pay.crypt.bot/api/getInvoices', json={"invoice_ids":f"{refill['invoice_id']},"}, 
                              headers={'Content-Type':'application/json', 'Crypto-Pay-API-Token':'11072:AANJ95ROJJ40qmu42JuEMQEbZgl4cWjWOZk'})
        data = resp.json()

        print(data['result']['items'][0]['status'])
        if data['result']['items'][0]['status'] == "paid":

            query = f"SELECT balance FROM Accounts WHERE id = {refill['account_id']}"

            cursor.execute(query)
            account_balance = cursor.fetchone()[0]

            curs = float(data['result']['items'][0]['paid_usd_rate'])
            total_sum = (refill['money'] * curs) + account_balance
      
            query = f"UPDATE Accounts SET balance = {total_sum} WHERE id = {refill['account_id']}"
            
            cursor.execute(query)
            connect.commit()

            query = f"UPDATE Refill SET status_refill=1 WHERE id = {refill['id']}"

            cursor.execute(query)
            connect.commit()

        elif data['result']['items'][0]['status'] != "paid" and data['result']['items'][0]['status'] != 'active':

            query = f"UPDATE Refill SET status_refill=2 WHERE id = {refill['id']}"

            cursor.execute(query)
            connect.commit()
    time.sleep(3)


# https://api.coinlore.net/api/ticker/?id=90  BTC
# https://api.coinlore.net/api/ticker/?id=518 USDT
# https://api.coinlore.net/api/ticker/?id=54683 TON
