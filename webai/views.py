import json

from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from openai import OpenAI

api_key = "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"
def chat_view(request):
    if request.method == 'POST':
        # message = request.POST.get('message')
        # print("message:", message)
        # print(f"Request content: {request.body.decode('utf-8')}")
        # 解析JSON数据、因为message是从js前端推过来的json数据、不能直接使用get
        try:
            #request.body.decode('utf-8'): 获取请求体中的JSON数据
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message')
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        print(f"Received message: {message!r}")

        # history = [
        #     {"role": "system", "content": "使用中文简体回答输出：你是一个小新助手。你总是提供既正确又有用的经过深思熟虑的回答。"},
        #     {"role": "user", "content": "使用中文简体回答输出：你好，请向第一次打开这个程序的人介绍一下自己。请简洁明了。\n"},
        # ]

        # 从session中获取历史记录，如果不存在则初始化
        # 这里提问的顺序是：定义系统角色（可无）、用户提问、助手回答、反复这样、确保会话启动时系统能展示其身份和功能
        history = request.session.get('history', [
            {"role": "system",
             "content": "使用中文简体回答输出：你是一个小新助手。你总是提供既正确又有用的经过深思熟虑的回答。"},
            {"role": "user",
             "content": "使用中文简体回答输出：你好，请向第一次打开这个程序的人介绍一下自己。请简洁明了。"},
            {"role": "assistant",
             "content": "使用中文简体回答问题：你好，我是一个小新助手。我是一个智能助手，我帮助用户解决各种问题。\n"},
        ])

        # 添加用户提问的最新消息到历史记录的最后、这样就实现了用户提问、系统助手回答的一个模式
        history.append({"role": "user", "content": "使用中文简体回答问题："+message})

        print("history:", history)

        # 创建当前对话的列表、取history最后一条记录、也就是用户user提问的最新一条信息
        #这里只会保存用户user提问的最新一条信息、每次循环都是覆盖之前的消息
        # current_chat = [{"role": "user", "content": history[-1]["content"]}]
        # print("current_chat:", current_chat)
        # 如果历史记录中的倒数第二个元素{字典}存在 assistant 消息（这是assistant 角色-后面都是这个角色给用户回答）
        # 则将其插入到 current_chat 中、只支持前后一条信息的联动
        # if len(history) > 1 and history[-2]["role"] == "assistant":
        #     # 将history中的assistant消息插入到current_chat的开头-下标是0、所以这里的current_chat里面就是两个元素(助手回答的和用户的提问)
        #     current_chat.insert(0, {"role": "assistant", "content": history[-2]["content"]})
        #
        #     print("current_chat2:", current_chat)

        # session = request.session['history'] = history

        # 创建OpenAI客户端
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

        # 创建聊天 completions
        completion = client.chat.completions.create(
            model="meta/llama3-70b-instruct",   # 模型名称
            messages=history,                   # 聊天记录、将所有的历史问答放进去
            temperature=0.5,                    # 随机性\值越高，输出文本的确定性就越低
            top_p=1,                            #  nucleus采样
            max_tokens=1024,                    # 最大生成长度
            stream=True                         # 是否流式返回、一段一段的返回
        )

        # 遍历 completions 的每个chunk，将每个chunk的content添加到新的消息中
        new_message = {"role": "assistant", "content": ""}  #初始化new_message()
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message['content'] += chunk.choices[0].delta.content

        # # 确保历史记录的最后一个消息是来自用户的，然后再添加assistant消息
        # if history[-1]["role"] == "user":
        #     history.append({"role": "assistant", "content": response_content})
        # else:
        #     # 如果不是，则可能出现了逻辑错误，这里可以选择抛出异常或采取其他恢复措施
        #     raise ValueError("历史记录的最后一个消息不是来自用户，不能添加assistant消息")

        data = new_message['content']
        # print(data)
        history.append(new_message)  # 将历史回答内容保存在列表中、实现上文是用户的提问、下文是ai的回答

        print("ai的回答：", data)
        print("历史记录：", history)

        if message in ["quit", "exit", "clear"]:
            #清掉session缓存
            request.session.flush()
            print("BYE BYE!")
            return JsonResponse({'response': "BYE BYE!"})

        # history.append({"role": "user", "content": message})

        # 更新session
        request.session['history'] = history
        request.session.modified = True # 更新session

        return JsonResponse({'response': data}) # 返回响应
    else:
        return render(request, 'chat.html') #如果是get请求就将页面展示
