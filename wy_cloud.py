from aiohttp import web,FormData,ClientSession
import json

# 跨域参数
corscode = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', # 需要限制请求就在这里增删
                'Access-Control-Allow-Headers': '*',
                'Server':'Welcome to api.wer.plus',
            }


# 实例化路由
routes = web.RouteTableDef()

# 封装一下web.json_resp
wj = lambda *args,**kwargs: web.json_response(*args,**kwargs)

# 处理OPTIONS和跨域的中间件
async def options_middleware(app, handler):
    async def middleware(request):
        # 处理 OPTIONS 请求，直接返回空数据和允许跨域的 header
        if request.method == 'OPTIONS':
            return wj(headers=corscode)
        
        # 继续处理其他请求,同时处理异常响应，返回正常json值或自定义页面
        try:
            response = await handler(request)
            response.headers.update(corscode)
            if response.status == 200:
                return response
        except web.HTTPException as ex:
            return wj({'code': ex.status,"msg":ex.reason},headers=corscode)
        return response
    return middleware


async def upload(content,filename='1.jpg'):
    fd = FormData()
    fd.add_field('file', content,filename=filename)
    async with ClientSession(headers=headers) as session:
        async with session.post(url, data=fd,headers=headers) as resp:
            data = await resp.text()
            try:
                data = json.loads(data)
            except:
                data = {'code':500,'error':data}
            return data


@routes.post(r'/upload')
async def geturl(request):
    try:
        data = await request.post()
        file_field = data['file']
        filename = file_field.filename
        file = file_field.file.read()
        req = await upload(file,filename)
        return wj(req)
    except Exception as e:
        return wj({'code':500,'error':str(e)})


if __name__ == '__main__':
    print('''
            Welcome to the Yiming API : https://api.wer.plus
            Github                    : https://github.com/HG-ha
            
            Upload address            : http://0.0.0.0:16182/upload
            Upload type               : form-data
            Upload parameter          : file
    ''')
    url = 'https://you.163.com/xhr/file/upload.json'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46'
    }

    app = web.Application(client_max_size=1024*1024*100)
    app.add_routes(routes)

    app.middlewares.append(options_middleware)
    web.run_app(
        app,
        host = "0.0.0.0",
        port = 16182
    )