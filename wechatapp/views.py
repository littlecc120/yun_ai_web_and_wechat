import hashlib
import time
from django.http import JsonResponse, HttpResponse
from wechatpy import parse_message, create_reply    #微信信息处理模块
from llama3.views import get_llama3     #llama3 接口


# 绑定服务器获取微信服务器发来的消息
def handle(request):
    # 验证微信服务器、绑定个人服务器
    #global reply
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        token = '123456'   # 设置的Token、自定义的Token
        list = [timestamp, nonce, token]    # 排序要正确
        list.sort()
        list = ''.join(list)
        if hashlib.sha1(list.encode('utf-8')).hexdigest() == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')

        response = HttpResponse(echo_str, content_type="text/plain")
        return response


    #接收公众号发来的消息
    elif request.method == 'POST':

        #开始时间
        start_time = time.time()

        #获取粉丝发送的消息
        #parse_message(request.body) ：解析微信发来的消息、将html格式转为字典
        recv_msg_dict = parse_message(request.body)
        #print('recv_msg:', recv_msg_dict)
        # recv_msg_tousername = recv_msg_dict.ToUserName  # 获取公众号
        # recv_msg_fromusername = recv_msg_dict.FromUserName  # 获取粉丝的微信号
        # recv_msg_type = recv_msg_dict.type      # 获取粉丝发送的消息类型 text为文本类型
        # recv_msg_content = recv_msg_dict.content    # 获取粉丝发送的消息内容
        # print(recv_msg_content)
        #print("输出：", recv_msg_dict.content)

        # 判断消息类型-文本消息
        if recv_msg_dict.type == 'text':
            #recv_msg: TextMessage({'ToUserName': 'gh_2e54a3fad033', 'FromUserName': 'oz9286DtNsAX6Em5iXIKJfECnOt4', 'CreateTime': '1714551362', 'MsgType': 'text', 'Content': '111', 'MsgId': '24546475055041726'})
            # reply = create_reply('http://www.google.com', recv_msg_dict)
            #create_reply('回复的字符串', 回复模板需要的字段recv_msg_dict-自动结合里面的字段组合回复模板)

            content = recv_msg_dict.content
            init_msg = f"你好！我是小新助手，一个智能的语言模型\n你的问题: {content} 回答如下：\n"

            # 调用llama3接口
            answer = get_llama3(content)
            # #接口调用结束时间
            # end_time = time.time()
            # excution_time = end_time - start_time   # 计算执行时间
            # print("开始时间：", start_time)
            # print("结束时间：", end_time)
            # print("执行时间：", excution_time)



            try:
                reply = create_reply(init_msg + answer, recv_msg_dict)
                print("reply:", reply)
            except Exception as e:
                print(e)
                reply = create_reply('抱歉，我暂时无法回答你的问题', recv_msg_dict)
                # response = HttpResponse(reply.render(), content_type="application/xml")  # 返回微信服务器状态
                # return response

        response = HttpResponse(reply.render(), content_type="application/xml")  # 返回微信服务器状态、消息才能发送
        return response
