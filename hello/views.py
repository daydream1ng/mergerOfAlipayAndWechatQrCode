# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
import os

from PIL import Image
import qrcode
# from hello.zxing import zxing_bar
import requests
from bs4 import BeautifulSoup
import json



# Create your views here.
def index(request):
    contents = {}
    if request.method == 'POST':
        ali = request.POST.get('ali-img', None)
        wx = request.POST.get('wx-img', None)

        print(ali, wx)
        if ali == None or wx == None:
            return render(request, 'hello/wxcode.html', {'url': None,
                                                         'info': "请先上传微信和支付宝的收款二维码"})

        if ali.find('HTTPS://QR.ALIPAY.COM') != -1:
            print("是支付宝的收款码：" + ali[22:])
            contents['alipay'] = ali[22:]
        else:
            print('不是支付宝收款码')
            contents['alipay'] = None
            return render(request, 'hello/wxcode.html', {'url': None,
                                                         'info': "支付宝收款二维码错误"})

        if wx.find('wxp://') != -1:
            print("是微信的收款码：" + wx[6:])
            contents['wechat'] = wx[6:]
        else:
            print('不是微信收款码')
            contents['wechat'] = None
            return render(request, 'hello/wxcode.html', {'url': None,
                                                         'info': "微信收款二维码错误"})

    else:
        contents['alipay'] = None
        contents['wechat'] = None

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if contents['alipay'] != None and contents['wechat'] != None:
        data = 'https://heyfox.herokuapp.com/pay?ali=' + contents['alipay'] + '&wx=' + contents['wechat']
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()

        # LOGO
        logo = request.FILES.get('logo', None)
        if logo != None:
            file_path = os.path.dirname(os.path.dirname(__file__)) + '/media/' + logo.name
            destination = open(file_path, 'wb+')
            for chunk in logo.chunks():
                destination.write(chunk)
            destination.close()
            img = addLogo(img, file_path)
            os.remove(file_path)

        img.save("media/img/qrcode.png")
        file_path = '/media/img/qrcode.png'

        return render(request, 'hello/wxcode.html', {'url': file_path,
                                                     'info': "支持支付宝和微信收款"})
    else:
        return render(request, 'hello/index.html', {'url': None})

def indroduce(request):
    return render(request, 'hello/introduce.html')


def pay(request):
    agent = request.META.get('HTTP_USER_AGENT', None)
    print(agent)
    ali = request.GET.get('ali', None)
    wx = request.GET.get('wx', None)
    if ali == None or wx == None:
        return render(request, 'hello/wxcode.html', {'url': None,
                                                     'info': "未知二维码，请重新合成收款二维码"})

    ali = 'HTTPS://QR.ALIPAY.COM/' + ali
    wx = 'wxp://' + wx

    print(ali, wx)

    # MicroMessenger    Alipay
    if str(agent).find('MicroMessenger') != -1:
        print("微信浏览器", wx)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wx)
        qr.make(fit=True)
        img = qr.make_image()
        img.save("media/img/" + request.GET.get('wx', None) + ".png")
        file_path = '/media/img/' + request.GET.get('wx', None) + ".png"
        return render(request, 'hello/wxcode.html', {'url': file_path,
                                                     'info': "长按识别上面的二维码进行支付"})
    elif str(agent).find('Alipay') != -1:
        print('支付宝浏览器', ali)
        return HttpResponseRedirect(ali)
    else:
        return render(request, 'hello/wxcode.html', {'url': None,
                                                     'info': "请使用微信、支付宝进行扫码支付"})


# 添加logo
def addLogo(img, logo):
    try:
        img = img.convert("RGBA")
        icon = Image.open(logo)
        icon = icon.convert("RGBA")
        img_w, img_h = img.size
        factor = 6
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img.paste(icon, (w, h), icon)
        return img
    except:
        print('logo添加错误')
        return img


# 二维码识别
def scanQrCode(path):
    return None
    # zxing
    # codes = zxing_bar.qrCodeReader(imgPath=path)
    # if codes != None:
    #     print('二维码识别结果：' + codes)
    #     return codes
    # else:
    #     print('二维码识别失败')
    #     return None

    # zbarlight
    # with open(path, 'rb') as image_file:
    #     image = Image.open(image_file)
    #     image.load()
    # # wxp://f2f0JV5T664Amfb_JDHLXtMBTrL2_8PvU68O
    # # HTTPS://QR.ALIPAY.COM/FKX05639AEMUOSN0TE016F
    # codes = zbarlight.scan_codes('qrcode', image)
    # if codes != None:
    #     code = str(codes[0]).lstrip("b'").rstrip("'")
    #     print('二维码识别结果：' + code)
    #     return code
    # else:
    #     print('二维码识别失败')
    #     return None



# zbarlight==1.2
# zbarlight==1.2
# zbar==0.10

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
