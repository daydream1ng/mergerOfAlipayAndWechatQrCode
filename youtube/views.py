from django.core.serializers import json
from django.shortcuts import render, HttpResponse

# Create your views here.

import requests
from bs4 import BeautifulSoup
import json

#  youtube
def search(request):
    video = request.POST.get('video', None)
    if video == None:
        msg = {"isSuccess": False,
               "msg": 'fail'}
        print('参数错误', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')

    searchURL = "https://www.tubeoffline.com/downloadFrom.php"
    # url = "https://youtu.be/Oqn9Z34eXZU"
    # url = "https://www.pornhub.com/view_video.php?viewkey=ph584e1456dba72"
    try:
        response = requests.get(searchURL, params={"host": 'PornHub', "video": video}, timeout=10)
    except:
        msg = {"isSuccess": False,
               "msg": 'time out'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')

    errorURL = "https://www.tubeoffline.com/error.php"
    print(response.url)
    if response.url.find(errorURL) != -1:
        print("》》》》视频地址错误 《《《《《")
        msg = {"isSuccess": False,
               "msg": 'address invalid'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        data = {'src': '', 'img': ''}
        for tag in soup.find_all("a"):
            if tag.has_attr('download') and tag.has_attr('href') and tag.has_attr('rel'):
                print('下载地址 》》》：', tag['href'])
                data['src'] = tag['href']
                break
        for tag in soup.find_all(id="videoContainer"):
            print('图片地址 》》》：', tag.img['src'])
            data['img'] = tag.img['src']
            break

        msg = {"isSuccess": True,
               'data': data,
               "msg": 'success'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')

# 内购结果验证
def verifyReceipt(request):
    # 苹果AppStore线上的购买凭证地址是： https: // buy.itunes.apple.com / verifyReceipt
    # 测试地址是：https: // sandbox.itunes.apple.com / verifyReceipt
    receipt_data = request.POST.get('receipt-data', None)
    password = request.POST.get('password', None)

    if receipt_data == None or password == None:
        msg = {"isSuccess": False,
               "msg": 'fail'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')

    buyItunesURL = "https://buy.itunes.apple.com/verifyReceipt"
    sandboxURL = "https://sandbox.itunes.apple.com/verifyReceipt"

    # receipt_data, base64编码后字符串
    param = {
        'receipt-data': receipt_data,
        'password': password
    }

    # AppStore验证
    paramJson = json.dumps(param)
    verifyRequest = requests.post(buyItunesURL, data=paramJson)
    json_data = verifyRequest.json()
    print(json_data)

    # AppStore验证
    if json_data['status'] == 0:
        msg = {"isSuccess": True,
               "msg": 'AppStore'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')

    # sandbox验证
    elif json_data['status'] == 21007:
        sandBoxRequest = requests.post(sandboxURL, data=paramJson)
        sand_data = sandBoxRequest.json()
        if sand_data['status'] == 0:
            msg = {"isSuccess": True,
                   "msg": 'sandbox'}
            print('结果', msg)
            return HttpResponse(json.dumps(msg), content_type='application/json')
        else:
            msg = {"isSuccess": False,
                   "msg": 'sandbox'}
            print('结果', msg)
            return HttpResponse(json.dumps(msg), content_type='application/json')
    else:
        msg = {"isSuccess": False,
               "msg": 'AppStore'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')





# YOUTUBE 视频下载
def video(request):
    videoURL = request.POST.get('video', None)
    print(videoURL)
    if videoURL == None:
        msg = {"isSuccess": False,
               "msg": 'fail'}
        print('参数错误', msg)
        return render(request, 'youtube/video.html', {'msg': '大丰'})

    searchURL = "https://www.tubeoffline.com/downloadFrom.php"
    # url = "https://youtu.be/Oqn9Z34eXZU"
    # url = "https://www.pornhub.com/view_video.php?viewkey=ph584e1456dba72"
    try:
        response = requests.get(searchURL, params={"host": 'PornHub', "video": video}, timeout=10)
    except:
        msg = {"isSuccess": False,
               "msg": 'time out'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')

    errorURL = "https://www.tubeoffline.com/error.php"
    print(response.url)
    if response.url.find(errorURL) != -1:
        print("》》》》视频地址错误 《《《《《")
        msg = {"isSuccess": False,
               "msg": 'address invalid'}
        print('结果', msg)
        return HttpResponse(json.dumps(msg), content_type='application/json')
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        data = {'src': '', 'img': ''}
        for tag in soup.find_all("a"):
            if tag.has_attr('download') and tag.has_attr('href') and tag.has_attr('rel'):
                print('下载地址 》》》：', tag['href'])
                data['src'] = tag['href']
                break
        for tag in soup.find_all(id="videoContainer"):
            print('图片地址 》》》：', tag.img['src'])
            data['img'] = tag.img['src']
            break

        msg = {"isSuccess": True,
               'data': data,
               "msg": 'success'}
        print('结果', data['src'])
        return HttpResponse(json.dumps(msg), content_type='application/json')

