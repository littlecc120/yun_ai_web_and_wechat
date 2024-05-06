import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from openai import OpenAI
from . tests import get_llama4
# from wechatapp.views import wechat_message_received #导入信号
# from django.dispatch import receiver    #信号接收

#llama3密钥""
api_key = "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"


# @receiver(wechat_message_received)  # 接收信号
#请求llama3模型
def get_llama3(content):

        # content = kwargs["content"] #获取用户输入、信号发送过来的

        # print("询问的内容：", content)

        client = OpenAI(
          base_url = "https://integrate.api.nvidia.com/v1",
          api_key = api_key,
        )

        #初始化ai、指定角色
        history = [
            {"role": "system", "content": "使用中文简体回答输出：你是一个小新助手。你总是提供既正确又有用的经过深思熟虑的回答。"},
            {"role": "user", "content": "使用中文简体回答输出：你好，请向第一次打开这个程序的人介绍一下自己。请简洁明了。\n"},
        ]

        while True:
            data = ""
            completion = client.chat.completions.create(
              model="meta/llama3-70b-instruct",
              messages=f"用中文简体回答问题:{content}",
              temperature=0.5,
              top_p=1,
              max_tokens=1024,
              stream=True
            )

            new_message = {"role": "assistant", "content": ""}

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    #print(chunk.choices[0].delta.content, end="", flush=True)
                    #data = chunk.choices[0].delta.content
                    #print(data)
                    new_message["content"] += chunk.choices[0].delta.content

            data = new_message['content']

            # history.append(new_message)     #将历史回答内容保存在列表中、实现上下文关联
            # #print(history)
            # #userinput = input(content)
            #
            # #调取微信公众号接口：提示要输入的内容
            #
            # #调用微信公众号接口：获取用户输入的内容、如果没有就一直等待、直到有输入-赋值给content
            #
            #
            # if content.lower() in ["quit", "exit"]:
            #     print("BYE BYE!")
            #     break
            #
            # history.append({"role": "user", "content": content})
            return data


# def chat_html(request):
#     return render(request, 'chat.html')
#
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))  # 解析JSON数据
#         message = data.get('message')  # 从JSON数据中获取message
#         print(message)
#         response = get_llama4(message)
#         print(response)
#         return JsonResponse({'response': response})  # 返回JSON响应
#     else:
#         return render(request, 'chat.html')
if __name__ == '__main__':
    get_llama3("你是谁")