from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import json, sys, requests
import chardet

config_file = ''

try:
    config_file = sys.argv[1]
except Exception:
    print('没有传入配置文件')
    sys.exit()

def read_config():
    try:
        with open(config_file, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']
        config = json.load(open(config_file, encoding=encoding))
        return config
    except Exception:
        print("找不到配置文件")
        sys.exit()

def check_config(config_data):
    if config_data['aliddns']['domainname'] == '':
        print('未配置域名')
        sys.exit()
    elif config_data['aliddns']['rrkeyworld'] == '':
        print('没有配置域名前缀')
        sys.exit()
    elif config_data['aliddns']['_type'] != 'A':
        print('目前仅支持A记录')
        sys.exit()

def get_now_ip():
    print('获取当前本机IP中...')
    try:
        r = requests.get('http://members.3322.org/dyndns/getip')
        print('获取成功, 当前本机IP为: ' + r.text.strip())
        return r.text.strip()
    except Exception:
        print('无法获取本机IP')
        sys.exit()

def get_domain_ip(domainname, rrkeyworld, _type):
    try:
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_TypeKeyWord(_type)
        request.set_DomainName(domainname)
        request.set_RRKeyWord(rrkeyworld)

        response = client.do_action_with_exception(request)
        try:
            source_data = str(response, encoding='utf-8')
            print('请求数据成功')
        except Exception as e:
            print('请求数据失败')
            print(e)
            sys.exit()
        try:
            datas = json.loads(source_data)['DomainRecords']['Record'][0]
            print('找到主机记录')
        except Exception:
            print('没有找到主机记录')
            sys.exit()

        if datas:
            print('\t域名\t: ' + str(datas['RR'] + '.' + datas['DomainName']))
            print('\t类型\t: ' + str(datas['Type']))
            print('\t记录值\t: ' + str(datas['Value']))
            print('\tTTL\t: ' + str(datas['TTL']))
            print('\tStatus\t: ' + str(datas['Status']))
            return str(datas['Value']), str(datas['RR']), str(datas['RecordId']), str(datas['Type'])
        else:
            print('请求数据失败')
            print(source_data)
    except Exception as e:
        print('请求数据失败')
        print(e)

def update_ip(rr, record_id, _type, value):
    try:
        from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RR(rr)
        request.set_RecordId(record_id)
        request.set_Type(_type)
        request.set_Value(value)
        response = client.do_action_with_exception(request)
        try:
            source_data = str(response, encoding='utf-8')
            datas = json.loads(source_data)['RecordId']
            print('更新成功')
        except Exception as e:
            print('更新失败')
            print(e)
            sys.exit()
    except Exception as e:
        print('更新失败')
        print(e)

if __name__ == '__main__':
    config = read_config()
    check_config(config)
    client = AcsClient(config['accessKeyId'], config['accessSecret'], 'cn-hangzhou')
    domain_ip, rr, record_id, _type = get_domain_ip(config['aliddns']['domainname'], config['aliddns']['rrkeyworld'], config['aliddns']['_type'])
    now_ip = get_now_ip()
    if now_ip == domain_ip:
        print('\n域名解析记录值与当前本机IP一致, 无需更改')
    else:
        print('\n域名解析记录值与当前本机IP不一致, 正在更改')
        update_ip(rr, record_id, _type, now_ip)