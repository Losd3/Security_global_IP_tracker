from pymongo import MongoClient
import requests
import json
import re
import time

def log():
    user_dic = {
        'david':'admin',
        'profe':'admin',
        'user':'user'

        }
    while True:
        user = input("Enter your user name: \n")
        password = input("Password: \n")

        if user in user_dic and password == user_dic[user]:
            print('Access approved! Welcome:',user)
            main()
            break
        else:
            print('Access denied')
def main():
    open_file = open('sec.txt','r')
    lines = open_file.readlines()
    
    ip_list = []
    duplictaes_remover = []
    for l in lines:
        
        string = l
        pattern = 'invalid\suser\s\D+\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

        result = re.findall(pattern, string) 
       
        ip_address = (result)
        res = [ele for ele in ip_list if ele != []]
        ip_list.append(ip_address)
        

    if "" in ip_list:
        ip_list.remove("")
    
    for i in res:
        if i not in duplictaes_remover:
            duplictaes_remover.append(i)
    
    app_request(duplictaes_remover)

def app_request(file):
    for x in file:
        string = str(x)
        pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

        result = re.findall(pattern, string) 

        ip_address = (result[0])
        print(ip_address)


        request_url = 'https://geolocation-db.com/jsonp/' + ip_address

        response = requests.get(request_url)
        result = response.content.decode()
        
        result = result.split("(")[1].strip(")")
        
        result  = json.loads(result)
        

        client = MongoClient(
            host='mongodb+srv://admin:splunk123@cluster0.ovqmh.mongodb.net/myFirstDatabase?authSource=admin&connectTimeoutMS=60000'
            )
        db = client.get_database('security_access')
        records = db.ip_add

        records.insert_one(result)
        print("Success! ")
    print('Proccess Completed! ')
 



log()
