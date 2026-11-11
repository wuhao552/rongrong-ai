from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import io
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
from dashscope import ImageSynthesis, MultiModalConversation
import json
import re
import requests
import time
from langchain_community.document_loaders import BiliBiliLoader, UnstructuredExcelLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.document_transformers import LongContextReorder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.llms import Tongyi
from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
from flask import Flask, Response, json, request, jsonify
from flask_cors import CORS
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
import asyncio
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from flask import Flask, request, jsonify
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

################################### 项目配置 ###################################
# -*- coding: utf-8 -*-

# 在 Unix 系统上，通常不需要显式设置，但如果你需要确保使用 SelectorEventLoop
# policy = asyncio.DefaultEventLoopPolicy()
# asyncio.set_event_loop_policy(policy)
#
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/api_config.json') as f:
    key = json.load(f)


def _cfg(name, default=''):
    '''
    读取运行配置：优先环境变量，其次 data/api_config.json。
    所有密钥均不入库，模板见 data/api_config.example.json
    '''
    return os.environ.get(name) or key.get(name, default)


app = Flask(__name__)
CORS(app, resources="/*")

################################### 主智能体 ###################################

# 接收全部的信息
messages = []


@app.route('/ask', methods=['POST'])
def stream_numbers_main():
    global messages
    query = request.json.get('query', '')
    network = request.json.get('network', 1)

    def chat():
        print(query)
        messages.append({'role': Role.USER, 'content': query})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus, messages=messages, result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'],
                                    enable_search=network, )

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)


# 清除历史对话
@app.route('/llm/clear')
def clear_messages():
    global messages
    messages = []

    return json.dumps({"message": "Message history cleared"})  # 返回一个JSON响应示例

################################### 文件上传接口 ###################################
# 日志配置
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 用户的配置信息（腾讯云 COS，从 api_config.json / 环境变量读取）
secret_id = _cfg('COS_SECRET_ID')  # 替换为你的 SecretId
secret_key = _cfg('COS_SECRET_KEY')  # 替换为你的 SecretKey
region = _cfg('COS_REGION', 'ap-nanjing')  # 替换为你的存储桶所在区域
token = None  # 如果使用永久密钥则无需填入token
bucket = _cfg('COS_BUCKET')  # 替换为你的存储桶名称

# 配置COS客户端
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
client = CosS3Client(config)

@app.route('/upload', methods=['POST'])
def upload_file():
    # 获取上传的文件和参数
    if 'file' not in request.files or 'object_key' not in request.form:
        return jsonify({"error": "file and object_key are required"}), 400

    file = request.files['file']
    object_key = request.form['object_key']

    try:
        # 上传文件到COS
        response = client.put_object(
            Bucket=bucket,
            Body=file,
            Key=object_key,
            EnableMD5=False
        )
        file_url = f'https://{bucket}.cos.{region}.myqcloud.com/{object_key}'
        return jsonify({"message": "Upload succeeded", "file_url": file_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
################################### 通用智能体 ###################################
messages_prompt = []
@app.route('/prompt', methods=['POST'])
def stream_numbers_prompt():
    global messages_prompt
    messages_prompt = []
    query = request.json.get('query', '')
    input_prompt = request.json.get('prompt', '')
    network = request.json.get('network', 1)
    prompt = f"""
            {input_prompt}

            Question:{query}
            """

    def chat():
        messages_prompt.append({'role': Role.USER, 'content': prompt})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus, prompt=prompt, result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'],
                                    enable_search=network)

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_prompt.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream; charset=utf-8',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)

################################### 通用智能体GET ###################################
messages_Getprompt = []
@app.route('/Getprompt', methods=['GET'])
def stream_numbers_Getprompt():
    global messages_Getprompt
    messages_Getprompt = []
    query = request.args.get('query', '')
    input_prompt = request.args.get('prompt', '')
    network = request.args.get('network', 1)
    prompt = f"""
            {input_prompt}

            Question:{query}
            """

    def chat():
        messages_Getprompt.append({'role': Role.USER, 'content': prompt})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus, prompt=prompt, result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'],
                                    enable_search=network)

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_Getprompt.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream; charset=utf-8',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)
################################### 图像理解 ###################################
messages_image_understand = []
@app.route('/image_understand', methods=['POST'])
def stream_numbers_image_understand():
    global messages_image_understand
    messages_image_understand = []
    image = request.json.get('image', 'https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg')
    query = request.json.get('query', '这是什么')

    def chat():
        print(query)
        messages_image_understand.append({'role': Role.USER, 'content': [
            {"image": image},
            {"text": query},
        ]})
        whole_message = ''
        responses = MultiModalConversation.call(model='qwen-vl-plus',
                                                messages=messages_image_understand,
                                                stream=True,
                                                incremental_output=True,
                                                api_key=key['DASHSCOPE_API_KEY'])

        for response in responses:
            part_message = response.output.choices[0].message.content[0]['text']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_image_understand.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        print('结束')

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)


################################### 图像生成 ###################################
@app.route('/image', methods=['POST'])
def simple_call():
    image_url = []
    prompt = request.json.get('prompt', '老鼠骑大象')
    rsp = ImageSynthesis.call(model=ImageSynthesis.Models.wanx_v1,
                              prompt=prompt,
                              n=4,
                              size='1024*1024',
                              api_key=key['DASHSCOPE_API_KEY'],
                              negative_prompt="""
                              低分辨率、错误、最差质量、低质量、jpeg 伪影、丑陋、重复、病态、残缺、超出框架、多余的手指、变异的手、
                              画得不好的手、画得不好的脸、突变、变形、模糊、脱水、不良的解剖结构、 
                              比例不良、多余肢体、克隆脸、毁容、总体比例、畸形肢体、缺臂、缺腿、多余手臂、多余腿、融合手指、手指过多、
                              长脖子、用户名、水印、签名
                              """)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            url = result.url
            image_url.append({
                'filename': file_name,
                'url': url
            })
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    print(image_url)
    return image_url


################################### 视频理解 ###################################
# DashScope embeddings
embedding = DashScopeEmbeddings(model='text-embedding-v2', dashscope_api_key=key['DASHSCOPE_API_KEY'])

# 初始化 Tongyi LLM
llm = Tongyi(temperature=1, dashscope_api_key=key['DASHSCOPE_API_KEY'])


def load_document(bilibili_url):
    print("连接测试")
    print(bilibili_url)
    loader = BiliBiliLoader(
        video_urls=[bilibili_url],
        sessdata=key['SESSDATA'],
        bili_jct=key['BILI_JCT'],
        buvid3=key['BUVID3']
    )
    documents = loader.load()
    if documents:
        documents[0].page_content = re.sub(r'\n{2,}', '\n', documents[0].page_content)
        documents[0].page_content = re.sub(r'\t', '', documents[0].page_content)
    return documents


def format_docs(docs):
    reordering = LongContextReorder()
    reordered_docs = reordering.transform_documents(docs)
    return "\n\n".join([doc.page_content for doc in reordered_docs])


@app.route('/get_video_info', methods=['GET'])
def get_video_info():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': '缺少url参数'})

        documents = load_document(url)
        if not documents:
            return jsonify({'error': '未能获取视频信息'})

        doc = documents[0]
        metadata = doc.metadata
        return jsonify({
            'cover': metadata['pic'],
            'title': metadata['title'],
            'desc': metadata['desc'],
            'bvid': metadata['bvid'],
            'cid': metadata['cid']
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_video_play_url', methods=['GET'])
def get_video_play_url():
    try:
        bvid = request.args.get('bvid')
        cid = request.args.get('cid')
        if not bvid or not cid:
            return jsonify({'error': '缺少bvid或cid参数'})

        headers = {
            'Referer': 'https://www.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'cookie': key['SESSDATA']
        }

        api_url = f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnver=0&fnval=0&qn=112&fourk=1'
        print(f"请求的URL: {api_url}")

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'durl' in data['data'] and len(data['data']['durl']) > 0:
                play_url = data['data']['durl'][0]['backup_url']
                return jsonify({'play_url': play_url})
            else:
                return jsonify({'error': '未能获取视频播放地址'})
        else:
            return jsonify({'error': f'请求视频播放地址失败，状态码：{response.status_code}'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/proxy', methods=['GET'])
def proxy():
    video_url = request.args.get('video_url')
    print(video_url)
    headers = {
        'Referer': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(video_url, headers=headers, stream=True)
    return response.raw.read(), response.status_code, response.headers.items()


async def generate_chunks(bilibili_url):
    documents = load_document(bilibili_url)
    chunks = chunk_data(documents)
    vector_store = create_embeddings(chunks, embedding)

    template = """
        这是一段Bilibili视频的文字记录{text}
        请使用中文回答
        Question:{question}
        """

    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 5})
    chain = {"text": retriever | format_docs, "question": RunnablePassthrough()} \
            | prompt \
            | llm \
            | output_parser

    async for chunk in chain.astream("请总结视频内容"):
        yield f"{chunk}"


def to_sync_iter(async_gen):
    async def async_gen_wrapper():
        async for item in async_gen:
            yield item

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    queue = asyncio.Queue()

    async def producer():
        async for item in async_gen_wrapper():
            await queue.put(item)
        await queue.put(None)

    def consumer():
        asyncio.ensure_future(producer(), loop=loop)
        while True:
            item = loop.run_until_complete(queue.get())
            if item is None:
                break
            yield item

    return consumer()

messages_bilibili_video = []
@app.route('/bilibili_video', methods=['GET'])
def summarize_video():
    global messages_bilibili_video
    messages_bilibili_video = []
    try:
        bilibili_url = request.args.get('url')
        documents = load_document(bilibili_url)
        #  分割数据
        chunks = chunk_data(documents)
        # 创建知识库的嵌入向量
        vector_store = create_embeddings(chunks, embedding)

        retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 5})

        question = "请总结这段视频的内容"

        text = format_docs(retriever.get_relevant_documents(question))

        prompt = f"""
               这是一段Bilibili视频的文字记录{text}
               请使用中文回答
               Question:{question}
               """

        def chat():
            print(bilibili_url)
            messages_bilibili_video.append({'role': Role.USER, 'content': prompt})
            whole_message = ''
            responses = Generation.call(Generation.Models.qwen_plus,
                                        prompt=prompt,
                                        result_format='message',
                                        stream=True,
                                        incremental_output=True,
                                        api_key=key['DASHSCOPE_API_KEY'])

            for response in responses:
                part_message = response.output.choices[0]['message']['content']
                whole_message += part_message
                print(part_message, end='')
                json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
                yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

            messages_bilibili_video.append({'role': 'assistant', 'content': whole_message})
            json_data = json.dumps({"message": 'done'})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        headers = {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }

        return Response(chat(), content_type='text/event-stream', headers=headers)
    except Exception as e:
        return jsonify({'error': str(e)})


################################### 数据库访问 ###################################
@app.route('/llm/sql')
def result():
    query = request.args.get('query', default='video表中有多少条数据')

    db_user = key["db_user"]
    db_password = key["db_password"]
    db_host = key["db_host"]
    db_name = key["db_name"]

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    llm = Tongyi(temperature=1, dashscope_api_key=key['DASHSCOPE_API_KEY'])

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    reply = agent_executor.invoke(query)['output']
    return reply


################################### 语音模块 ###################################

# 全局变量，存储消息
messages_voice = []


class SpeechLongSynthesizerRestfulDemo:
    def __init__(self, appkey, token):
        self.accessToken = token
        self.appkey = appkey

    def processPOSTRequest(self, text, format, sampleRate, voice):
        url = "https://nls-gateway-cn-shanghai.aliyuncs.com/rest/v1/tts/async"

        context = {
            "device_id": "my_device_id"
        }

        header = {
            "appkey": self.appkey,
            "token": self.accessToken
        }

        tts = {
            "text": text,
            "voice": voice,
            "format": format,
            "sample_rate": sampleRate,
            "enable_subtitle": True
        }

        payload = {
            "enable_notify": False,
            "tts_request": tts
        }

        bodyContent = json.dumps({
            "context": context,
            "header": header,
            "payload": payload
        })

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.40.0",
            "Connection": "keep-alive"
        }

        try:
            response = requests.post(url, headers=headers, data=bodyContent)
            result = response.json()

            if 'error_code' in result and result['error_code'] == 20000000:
                task_id = result['data']['task_id']
                request_id = result['request_id']
                return task_id, request_id
            else:
                return None, None

        except Exception as e:
            print("Exception occurred:", str(e))
            return None, None

    def waitLoop4Complete(self, task_id, request_id):
        url = "https://nls-gateway-cn-shanghai.aliyuncs.com/rest/v1/tts/async"
        fullUrl = f"{url}?appkey={self.appkey}&task_id={task_id}&token={self.accessToken}&request_id={request_id}"

        while True:
            try:
                response = requests.get(fullUrl)
                result = response.json()

                if 'error_code' in result and result['error_code'] == 20000000:
                    audio_address = result['data'].get('audio_address')
                    print(audio_address)
                    if audio_address:
                        return audio_address
                    else:
                        print("Tts Queuing...")
                else:
                    print("Tts Queuing...")

                time.sleep(1)

            except Exception as e:
                print("Exception occurred:", str(e))
                return None


def update_token_in_json(token):
    # 读取现有的JSON文件
    with open('data/api_config.json', 'r') as file:
        data = json.load(file)

    # 更新token值
    data['token'] = token

    # 写回修改后的数据
    with open('data/api_config.json', 'w') as file:
        json.dump(data, file, indent=4)  # indent参数用于美化输出


@app.route('/synthesize', methods=['POST'])
def synthesize():
    # 设置访问密钥（阿里云语音服务，从 api_config.json / 环境变量读取）
    ACCESS_KEY_ID = _cfg('ALIYUN_ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = _cfg('ALIYUN_ACCESS_KEY_SECRET')

    # 创建AcsClient实例
    client = AcsClient(
        ACCESS_KEY_ID,
        ACCESS_KEY_SECRET,
        "cn-shanghai"
    )

    # 创建request_token，并设置参数
    request_token = CommonRequest()
    request_token.set_method('POST')
    request_token.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request_token.set_version('2019-02-28')
    request_token.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request_token)
        print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            expireTime = jss['Token']['ExpireTime']
            print("token = " + token)
            print("expireTime = " + str(expireTime))
            update_token_in_json(token)

    except Exception as e:
        print(e)

    content = request.json
    text = content.get('text')

    if not text:
        return jsonify({"error": "Text parameter is required"}), 400

    with open('data/api_config.json') as f:
        key = json.load(f)

    appkey = key["appkey"]
    accessToken = key["token"]
    demo = SpeechLongSynthesizerRestfulDemo(appkey, accessToken)

    task_id, request_id = demo.processPOSTRequest(text, "mp3", 16000, "zhimiao_emo")

    if task_id and request_id:
        audio_address = demo.waitLoop4Complete(task_id, request_id)
        if audio_address:
            return jsonify({"audio_address": audio_address}), 200
        else:
            return jsonify({"error": "Failed to retrieve audio address"}), 500
    else:
        return jsonify({"error": "Failed to start synthesis task"}), 500


@app.route('/studio_ask', methods=['POST'])
def handle_ask():
    global messages_voice
    # 设置访问密钥（阿里云语音服务，从 api_config.json / 环境变量读取）
    ACCESS_KEY_ID = _cfg('ALIYUN_ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = _cfg('ALIYUN_ACCESS_KEY_SECRET')

    # 创建AcsClient实例
    client = AcsClient(
        ACCESS_KEY_ID,
        ACCESS_KEY_SECRET,
        "cn-shanghai"
    )

    # 创建request_token，并设置参数
    request_token = CommonRequest()
    request_token.set_method('POST')
    request_token.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request_token.set_version('2019-02-28')
    request_token.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request_token)
        print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            expireTime = jss['Token']['ExpireTime']
            print("token = " + token)
            print("expireTime = " + str(expireTime))
            update_token_in_json(token)

    except Exception as e:
        print(e)

    # 从请求中获取音频地址参数
    audio_address = request.json.get('audio_address', '')

    if not audio_address:
        return jsonify({'error': 'Missing audio_address parameter'}), 400

    # 语音识别部分
    url = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/FlashRecognizer"

    with open('data/api_config.json') as f:
        key = json.load(f)
    
    params = {
        "appkey": key["appkey"],  # 替换为你的阿里云AppKey
        "token": key["token"],  # 替换为你的阿里云Token
        "format": "mp3",  # 确认音频格式是否正确，如果是mp3，请改为'mp3'
        "sample_rate": "16000",
        "audio_address": audio_address  # 使用上传到云存储后的文件URL
    }
    headers = {
        "Content-type": "application/text"
    }

    # 发送POST请求到阿里云语音识别接口
    response = requests.post(url, params=params, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to call speech recognition API'}), 500

    # 获取语音识别结果
    recognition_result = response.json()

    # 提取语音识别结果中的文本
    if 'flash_result' in recognition_result and 'sentences' in recognition_result['flash_result']:
        sentences = recognition_result['flash_result']['sentences']
        user_message = ''.join([sentence['text'] for sentence in sentences])
        messages_voice.append({'role': Role.USER, 'content': user_message})

    # 调用 Dashscope 生成回复
    def generate_responses():
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus, messages=messages_voice, result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'],
                                    enable_search=1)

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        print(part_message, end='')
        messages_voice.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(generate_responses(), content_type='text/event-stream', headers=headers)


# 清除历史对话
@app.route('/studio_ask/clear')
def clear_studio_ask():
    global messages_voice
    messages_voice = []

    return json.dumps({"message": "语音历史记录已清空"})  # 返回一个JSON响应示例


################################### 文档阅读模型 ###################################

vector_store = ""


def load_document_file(file):
    '''
    导入文档，支持 PDF, DOCX and TXT 文件
    :param file: 文件路径
    :return: 文本数据
    '''
    name, extension = os.path.splitext(file)
    if extension == '.pdf':
        loader = PyPDFLoader(file)
        documents = loader.load()
    elif extension == '.docx':
        loader = Docx2txtLoader(file)
        documents = loader.load()
    elif extension == '.txt':
        try:
            loader = TextLoader(file, encoding='utf8')
            documents = loader.load()
        except:
            loader = TextLoader(file, encoding='gbk')
            documents = loader.load()
    else:
        print('不支持的文件格式，仅支持PDF、DOCX、TXT文件')
        documents = ''
    # 文档预处理
    documents[0].page_content = re.sub(r'\n{2,}', '\n', documents[0].page_content)
    documents[0].page_content = re.sub(r'\t', '', documents[0].page_content)
    return documents


def create_embeddings(documents, embedding):
    '''
    文档向量化和存储
    :param documents: 切分好的文档
    :param embedding: 向量化模型
    :return: 向量化存储的对象
    '''
    vectorstore = Qdrant.from_documents(
        documents=documents,
        embedding=embedding,
        location=':memory:',
        collection_name='my_documents')
    return vectorstore


def format_docs(docs):
    '''
    将返回的文档page_content的内容拼接为字符串，减少其他信息干扰
    :param docs: 文档对象
    :return: 拼接后的字符串
    '''
    reordering = LongContextReorder()  # 实例化对象
    reordered_docs = reordering.transform_documents(docs)  # 文档重排
    # 文档重排后，将内容拼接为字符串输出
    return "\n\n".join([doc.page_content for doc in reordered_docs])


def chunk_data(data, chunk_size=1024, chunk_overlap=128):
    '''
    文档切分
    :param data: 待切分的文档
    :param chunk_size: 切块大小
    :param chunk_overlap: 切块重叠大小
    :return: 切分后的文档对象
    '''
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


# 加载文件
@app.route('/llm/document')
def document_vectors():
    global vector_store
    document = request.args.get('document', default='')
    print(document)
    documents = load_document_file(document)

    #  分割数据
    chunks = chunk_data(documents)

    # 创建知识库的嵌入向量
    vector_store = create_embeddings(chunks, embedding)

    print("向量知识库加载成功")
    return "向量知识库加载成功"


@app.route('/llm/del_document')
def del_document():
    global vector_store
    vector_store = ""
    print("向量知识库已清空")
    return "向量知识库已清空"

messages_ask_document = []
@app.route('/llm/ask_document')
def stream_numbers():
    global messages_ask_document
    messages_ask_document = []

    question = request.args.get('question', default='')
    if vector_store != "":
        retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})

        text = format_docs(retriever.get_relevant_documents(question))

        prompt = f"""
            Answer the question based only on the following context:{text}
            Please answer the question only by chinese.
            If you can't answer the question, please say "对不起，我没有找到相关的知识".
            Question:{question}
            """
    else:
        prompt = f'''Answer the question by chinese.
                Question:{question}
                '''

    def chat():
        messages_ask_document.append({'role': Role.USER, 'content': prompt})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus,
                                    prompt=prompt,
                                    result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'])

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_ask_document.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)

################################### 主页语音 ###################################

@app.route('/studio_exchange', methods=['POST'])
def handle_studio_exchange():
    global messages

    # 设置访问密钥（阿里云语音服务，从 api_config.json / 环境变量读取）
    ACCESS_KEY_ID = _cfg('ALIYUN_ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = _cfg('ALIYUN_ACCESS_KEY_SECRET')

    # 创建AcsClient实例
    client = AcsClient(
        ACCESS_KEY_ID,
        ACCESS_KEY_SECRET,
        "cn-shanghai"
    )

    # 创建request_token，并设置参数
    request_token = CommonRequest()
    request_token.set_method('POST')
    request_token.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request_token.set_version('2019-02-28')
    request_token.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request_token)
        print(response)

        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            token = jss['Token']['Id']
            expireTime = jss['Token']['ExpireTime']
            print("token = " + token)
            print("expireTime = " + str(expireTime))
            update_token_in_json(token)

    except Exception as e:
        print(e)

    # 从请求中获取音频地址参数
    audio_address = request.json.get('audio_address', '')

    if not audio_address:
        return jsonify({'error': 'Missing audio_address parameter'}), 400

    # 语音识别部分
    url = "https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/FlashRecognizer"

    with open('data/api_config.json') as f:
        key = json.load(f)
    
    params = {
        "appkey": key.get("appkey", ""),  # 从 api_config.json 读取阿里云AppKey
        "token": key["token"],  # 替换为你的阿里云Token
        "format": "mp3",  # 确认音频格式是否正确，如果是mp3，请改为'mp3'
        "sample_rate": "16000",
        "audio_address": audio_address  # 使用上传到云存储后的文件URL
    }
    headers = {
        "Content-type": "application/text"
    }

    # 发送POST请求到阿里云语音识别接口
    response = requests.post(url, params=params, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to call speech recognition API'}), 500

    # 获取语音识别结果
    recognition_result = response.json()

    # 提取语音识别结果中的文本
    if 'flash_result' in recognition_result and 'sentences' in recognition_result['flash_result']:
        sentences = recognition_result['flash_result']['sentences']
        user_message = ''.join([sentence['text'] for sentence in sentences])
    return jsonify({"user_message": user_message}), 200

################################### 简历求职 ###################################
vector_resume = ""


def load_document_zhilian():
    '''
    :return: 文本数据
    '''

    loader = UnstructuredExcelLoader("./data/zhilian.xlsx", mode="elements")
    documents = loader.load()

    # 文档预处理
    documents[0].page_content = re.sub(r'\n{2,}', '\n', documents[0].page_content)
    documents[0].page_content = re.sub(r'\t', '', documents[0].page_content)
    return documents


# 加载文件
@app.route('/llm/resume')
def resume_vectors():
    global vector_resume

    documents = load_document_zhilian()

    #  分割数据
    chunks = chunk_data(documents)

    # 创建知识库的嵌入向量
    vector_resume = create_embeddings(chunks, embedding)

    print("向量知识库加载成功")
    return "向量知识库加载成功"


@app.route('/llm/del_resume')
def del_resume():
    global vector_resume
    vector_resume = ""
    print("向量知识库已清空")
    return "向量知识库已清空"


@app.route('/llm/ask_resume')
def stream_resume():
    llm = Tongyi(temperature=1, dashscope_api_key=key['DASHSCOPE_API_KEY'])

    resume_url = request.args.get('resume', default='')

    loader = PyPDFLoader(resume_url)
    documents = loader.load()

    retriever = vector_resume.as_retriever(search_type='similarity', search_kwargs={'k': 3})

    template = """
            Answer the question based only on the following context:{context}
            Please answer the question only by chinese.
            请使用json格式输出，格式如下：
            公司名称：xxx，职位：xxx，学历：xxx，工作经验：xxx，薪资：xxx，待遇：xxx，工作地点：xxx，工作内容：xxx
            不要输出无关内容
            请根据我的简历信息匹配三个合适工作:{question}
            """

    output_parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_template(template)

    chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} \
            | prompt \
            | llm \
            | output_parser
    output = chain.invoke(documents[0].page_content)

    return output


################################### 面试助手 ###################################

vector_interview = ""


def load_interview():
    loader = Docx2txtLoader('./data/人事面试常见问题.docx')  # 定义读取方法和文档
    loader = PyPDFLoader('./data/人事面试常见问题.pdf')  # 定义读取方法和文档
    documents = loader.load()  # 进行读取文档
    # 文档预处理
    documents[0].page_content = re.sub(r'\n{2,}', '\n', documents[0].page_content)
    documents[0].page_content = re.sub(r'\t', '', documents[0].page_content)
    return documents

def chunk_data_interview(data, chunk_size=512, chunk_overlap=128):
    '''
    文档切分
    :param data: 待切分的文档
    :param chunk_size: 切块大小
    :param chunk_overlap: 切块重叠大小
    :return: 切分后的文档对象
    '''
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


# 加载文件
@app.route('/llm/interview')
def interview_vectors():
    global vector_interview
    documents = load_interview()

    #  分割数据
    chunks = chunk_data_interview(documents)

    # 创建知识库的嵌入向量
    vector_interview = create_embeddings(chunks, embedding)

    print("向量知识库加载成功")
    return "向量知识库加载成功"


@app.route('/llm/del_interview')
def del_interview():
    global vector_interview
    vector_interview = ""
    print("向量知识库已清空")
    return "向量知识库已清空"


messages_ask_interview = []


@app.route('/llm/ask_interview')
def stream_interview():
    global messages_ask_interview
    messages_ask_interview = []

    question = request.args.get('question', default='')
    if vector_interview != "":
        retriever = vector_interview.as_retriever(search_type='similarity', search_kwargs={'k': 3})

        text = format_docs(retriever.get_relevant_documents(question))

        prompt = f"""
            基于<start> 和 <end>之间的内容回答问题即可，回答用中文。
            <start> {text} <end>
            问题是：{question}
            """
    else:
        prompt = f'''Answer the question by chinese.
                Question:{question}
                '''

    def chat():
        messages_ask_interview.append({'role': Role.USER, 'content': prompt})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus,
                                    prompt=prompt,
                                    result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'])

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_ask_interview.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)

################################### 金融行业问答 ###################################

vector_finance = ""


def load_finance():
    documents = []
    # 遍历目录及子目录
    for root, dirs, files in os.walk('./data/金融行业知识库'):
        for file in files:
            # 只处理PDF文件
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())  # 合并所有文档
    # 文档预处理
    documents[0].page_content = re.sub(r'\n{2,}', '\n', documents[0].page_content)
    documents[0].page_content = re.sub(r'\t', '', documents[0].page_content)
    return documents

def chunk_data_finance(data, chunk_size=1024, chunk_overlap=128):
    '''
    文档切分
    :param data: 待切分的文档
    :param chunk_size: 切块大小
    :param chunk_overlap: 切块重叠大小
    :return: 切分后的文档对象
    '''
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


# 加载文件
@app.route('/llm/finance')
def finance_vectors():
    global vector_finance
    documents = load_finance()

    #  分割数据
    chunks = chunk_data_finance(documents)

    # 创建知识库的嵌入向量
    vector_finance = create_embeddings(chunks, embedding)

    print("向量知识库加载成功")
    return "向量知识库加载成功"


@app.route('/llm/del_finance')
def del_finance():
    global vector_finance
    vector_finance = ""
    print("向量知识库已清空")
    return "向量知识库已清空"


messages_ask_finance = []


@app.route('/llm/ask_finance')
def stream_finance():
    global messages_ask_finance
    messages_ask_finance = []

    question = request.args.get('question', default='')

    if vector_finance != "":
        retriever = vector_finance.as_retriever(search_type='similarity', search_kwargs={'k': 3})

        text = format_docs(retriever.get_relevant_documents(question))

        prompt = f"""
            你是智能投资助手融融AI，擅长处理财经资讯的需求。你的能力有：分析财经要闻，提炼关键信息，辅助投资决策。
            基于<start> 和 <end>之间的内容回答问题即可，回答用中文。
            <start> {text} <end>
            问题是：{question}
            """
    else:
        prompt = f'''Answer the question by chinese.
                Question:{question}
                '''

    def chat():
        messages_ask_finance.append({'role': Role.USER, 'content': prompt})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_plus,
                                    prompt=prompt,
                                    result_format='message',
                                    stream=True,
                                    incremental_output=True,
                                    api_key=key['DASHSCOPE_API_KEY'])

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_ask_finance.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
