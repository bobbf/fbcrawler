'''
usage 
crawler.py {short_live_access_token}
'''
import sys
import json
import urllib.request
from datetime import datetime
import datetime as DT
import socket


def getJsonFromUrl(urlString):
    #print(urlString)
    response = urllib.request.urlopen(urlString).read().decode('utf-8')
    responseJson = json.loads(response)
    return responseJson
'''test
url = "https://graph.facebook.com/v3.2/me?fields=posts&"+tokenParam
url = "https://graph.facebook.com/v3.2/me?"+tokenParam
testJson = getJsonFromUrl(url)
print(testJson)
'''

access_token= sys.argv[1]
client_id= 345750606037202
client_secret = "7445ab4757f1ebc1633c1f2107066052"
shortLiveToken = access_token
getLongLiveTokenUrl = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id="+str(client_id)+"&client_secret="+client_secret+"&fb_exchange_token="+access_token
#print(getLongLiveTokenUrl)
longLiveToken = getJsonFromUrl(getLongLiveTokenUrl)["access_token"]
print(longLiveToken)
access_token = longLiveToken
tokenParam = "access_token="+access_token


def get_posts():
    url = "https://graph.facebook.com/v3.2/me?fields=posts&"+tokenParam
    postsJson = getJsonFromUrl(url)
    for post in postsJson["posts"]["data"]:
        print("---------------------------post")
        print("id :" + post["id"])
        print("message : " + post["message"])
        print("---------------------------")


def get_comments(post_id):
    url = "https://graph.facebook.com/v3.2/"+post_id+"/comments?limit=10000000&"+tokenParam
    commentJson = getJsonFromUrl(url)
    result = []
    for comment in commentJson["data"]:
        #print(comment)
        #print("--------------------------comment")
        #print("created_time: "+comment["created_time"])
        #print("message: " +comment["message"])
        '''get Likes
        '''
        likeUrl="https://graph.facebook.com/v3.2/"+comment["id"]+"/reactions?"+tokenParam
        #likeJson = getJsonFromUrl(likeUrl)
        #print(likeJson["data"])
        #print("like count :",len(likeJson["data"]))
        #print("--------------------------")        
        resultComment = comment
        #resultComment["writer"] = comment["from"]["name"]
        #resultComment["like_count"] = len(likeJson["data"])
        resultComment["like_count"]=0
        #print(get_comments(comment["id"]))
        #result += get_comments(comment["id"])
        if "from" in resultComment:
            resultComment["writer"] = comment["from"]["name"]
            del resultComment["from"]
        del resultComment["id"]
        result.append(resultComment)
    print(commentJson["paging"])
    return result






#get_posts()
post_num = "264581367591821_264581670925124"
#post_num = "264581367591821_264973414219283"
while True:
    start_time = datetime.now(DT.timezone.utc)
    try:
        all_comments = get_comments(post_num)
        filtered_comments=[]
        this_time = datetime.now(DT.timezone.utc)
        for comment in all_comments:
            that_time = datetime.strptime(comment["created_time"], "%Y-%m-%dT%H:%M:%S%z")
            print("--------------------")
            print("this time : ", this_time)
            print("that time : ", that_time)
            print("time delta : ", this_time-that_time)
            print("--------------------")
            print(comment["message"])
            if(len(comment["message"]) > 20):
                print("Fail - long commnet")
                continue
            if(this_time-that_time <  DT.timedelta(seconds=60*10)):
            #if(True):
                print(comment)
                filtered_comments.append(comment)
            else:
                print("Fail - old comment")
        print("================================================")
        print(json.dumps(filtered_comments,indent=2, sort_keys=True))
        print("-----------------------------------------------")
        #print(json.dumps(all_comments,indent=2, sort_keys=True))
        print("===============================================")
        filteredJson={}
        filteredJson["data"] = filtered_comments
        sendData= json.dumps(filteredJson)
        print(sendData)
        byteData = sendData.encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(byteData,("127.0.0.1",1234))
    except:
        
        print("*********************Error***************************")
    while True:
        end_time = datetime.now(DT.timezone.utc)
        if( end_time-start_time > DT.timedelta(seconds=1)):
            break
