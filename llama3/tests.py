import requests
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI
#llama3密钥""
api_key = "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"

#请求llama3模型
def get_llama4():

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
            completion = client.chat.completions.create(
              model="meta/llama3-70b-instruct",
              messages=history,
              temperature=0.5,
              top_p=1,
              max_tokens=2048,
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
            print(data)
            history.append(new_message)     #将历史回答内容保存在列表中、实现上下文关联
            #print(history)
            # userinput = input("\n请输入：")
            userinput = input("\n请输入：")
            if userinput.lower() in ["quit", "exit"]:
                print("BYE BYE!")
                break

            history.append({"role": "user", "content": userinput})



if __name__ == '__main__':
    get_llama4()