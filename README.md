# AliDDNS

**Python 3+**

## 快速开始
1. 克隆该仓库  
2. cd进仓库目录 安装库  
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
3. 配置config 文件名可以自定义  
```
{
    "accessKeyId": "",      // 填入你的accessKey
    "accessSecret": "",     // 填入你的accessSecret
    "aliddns": {
        "domainname": "",   // 填入域名(例如 example.com)
        "rrkeyworld": "",   // 填入前缀(例如 www)
        "_type": "A"        // 类型为A 不可更改
    }
}
```
4. 启动  
```
python3 main.py config.json    // config.json为配置文件 可以更改
(python main.py config.json)
```

## 运行示例
```
请求数据成功
找到主机记录
	域名	: www.example.com
	类型	: A
	记录值	: x.x.x.x
	TTL	: 600
	Status	: ENABLE
获取当前本机IP中...
获取成功, 当前本机IP为: x.x.x.x

域名解析记录值与当前本机IP一致, 无需更改
```
```
请求数据成功
找到主机记录
	域名	: www.example.com
	类型	: A
	记录值	: x.x.x.x
	TTL	: 600
	Status	: ENABLE
获取当前本机IP中...
获取成功, 当前本机IP为: x.x.x.x

域名解析记录值与当前本机IP不一致, 正在更改
更新成功
```