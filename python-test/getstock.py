import requests as res
import json
import time

def get_stock(keyWord):
    url = "http://www.cninfo.com.cn/new/information/topSearch/query"
    requestbody = {
        'keyWord': 'keyWord',
        'maxSecNum': 10,
        'maxListNum': 5,
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}  # 加请求头

    data = json.loads(res.post(url, data=requestbody, headers=headers).content)
    index = 0  # 初始值
    data = [i for i in data['keyBoardList'] if i['category'] == 'A股']  # 剔除A股外的股票
    if len(data) == 0:
        raise Exception('关键字错误！请重新输入！')
    # print(data)
    if len(data) > 1:
        print()
        print('出现多只股票!请选择一只股票！比如说输入0 选择'+str(data[0]['zwjc']))
        for i in range(len(data)) :
            print(str(i)+':'+data[i]['zwjc'], end='  ')
        print()
        index = int(input('请输入你要选择的股票：'))

    print()
    name = data[index]['zwjc']  # 股票名
    orgId = data[index]['orgId']  # 股票ID
    plate = data[0]['plate']  # 股票平台
    code = data[index]['code']  # 股票代码
    print('股票基本信息如下：')
    print('股票名字:', name, '\n股票代码:', code)
    print()
    return orgId, plate, code



def get_stock_introduction(plate, code):
    url2 = 'http://www.cninfo.com.cn/data20/companyOverview/getHeadStripData?scode=' + code
    data2 = json.loads(res.get(url2).text)['data']['records'][0]
    # print(data2)
    # print(data2)
    code_info = {}
    # print(basicInformation)
    code_info['ROE'] = str(data2['F081N']) + '%'
    code_info['主营收入'] = data2['F089N']
    code_info['净利润'] = data2['F102N']
    code_info['货币资金'] = data2['F109N']
    code_info['负债率'] = str(data2['F041N']) + '%'
    code_info['商誉'] = data2['F115N']
    code_info['应收款'] = data2['F111N']
    code_info['总股本'] = str(data2['F020N']) + '股'
    code_info['流通股本'] = str(data2['F021N']) + '股'
    code_info['质押率'] = str(data2['F005N']) + '%'
    # print(time.time())
    print(plate)
    if plate == 'szse' or plate == 'sse':
        plate = 'sh'
    else:
        plate = 'sz'
    url3 = 'http://api.cninfo.com.cn/v5/hq/dataItem?jsonpCallback=jQuery00627445787571963_' + str(
        round(time.time() * 1000)) + '&codelist=' + plate + code + '&_=' + str(round(time.time() * 1000))
    print(url3)
    data3 = json.loads(res.get(url3).text.split('(')[1][:-1])[0]
    # print(data3)
    # print(data2)
    code_info['市盈率'] = data3['91']
    code_info['换手率'] = str(data3['1968584']) + '%'
    code_info['成交额'] = data3['19']
    code_info['成交量'] = str(data3['13']) + '股'
    code_info['市净率'] = data3['1149395']
    print(code+'股票的基本信息如下:', )
    for k, v in code_info.items():
        print(k, ':', v)
    print('*'*120, '\n\n\n')
    return 'success'

def brush_report(report_type, start_date, end_date, orgId, plate, code):
    url1 = 'http://www.cninfo.com.cn/data20/companyOverview/getCompanyIntroduction?scode=' + code
    market = json.loads(res.get(url1).text)
    print('股票所在交易所为:', market['data']['records'][0]['basicInformation'][0]['MARKET'])

    url2 = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    category_dict = {
        '年报': 'category_ndbg_szsh;', '半年报': 'category_bndbg_szsh;', '一季度报': 'category_yjdbg_szsh;',
        '三季度报': 'category_sjdbg_szsh;', '业绩报告': 'category_yjygjxz_szsh;', '权益分派': 'category_qyfpxzcs_szsh;',
        '董事会': 'category_dshgg_szsh;', '监事会': 'category_jshgg_szsh;', '股东大会': 'category_gddh_szsh;',
        '日常经营': 'category_rcjy_szsh;', '公司治理': 'category_gszl_szsh;', '中介报告': 'category_zj_szsh;',
        '首发': 'category_sf_szsh;', '增发': 'category_zf_szsh;', '股权激励': 'category_gqjl_szsh;',
        '配股': 'category_pg_szsh;', '解禁': 'category_jj_szsh;', '公司债': 'category_gszq_szsh;',
        '可转让债': 'category_kzzq_szsh;', '其他融资': 'category_qtrz_szsh;', '股权变动': 'category_gqbd_szsh;',
        '补充更正': 'category_bcgz_szsh;', '澄清致歉': 'category_cqdq_szsh;', '风险提示': 'category_fxts_szsh;',
        '特别处理和退市': 'category_tbclts_szsh;', '退市整理期': 'category_tszlq_szsh;'
    }
    category = str()  # 公告类型分类
    for k in category_dict:
        if k in report_type:
            category += category_dict[k]
    # print(category)  # 公告参数

    requestbody = {
        'stock': '{},{}'.format(code, orgId),
        'tabName': 'fulltext',
        'pageSize': 30,
        'pageNum': 1,
        'column': plate,
        'category': category,  # 公告分类
        'plate': '',
        'seDate': start_date + '~' + end_date,
        'searchkey': '',
        'secid': '',
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true',
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}  # 加请求头
    data = json.loads(res.post(url2, headers=headers, data=requestbody).content)
    # print(data)
    reports_list = data['announcements']  # 提取announcements内容
    
    for report in reports_list:
        file_name = report['announcementTitle']
        pdf_url = "http://static.cninfo.com.cn/" + report['adjunctUrl']
        print('文件名为:', file_name, '  pdf文件url为:', pdf_url)
    print('*' * 120)
    return reports_list



def download_PDF(reports_list):  # 下载pdf
    for report in reports_list:
        file_name = report['announcementTitle']
        pdf_url = "http://static.cninfo.com.cn/" + report['adjunctUrl']
        # print('文件名为:', file_name, '  pdf文件url为:', pdf_url)
        print('正在下载:' + pdf_url, '存放在当前目录:' +file_name)
        time.sleep(2)  # 阻塞2秒
        r = res.get(pdf_url)
        f = open(file_name + ".pdf", "wb")
        f.write(r.content)
    return 'success'


def excute():
    while True:
        orgId = None
        plate = None
        code = None
        print('*' * 120)
        print('功能一：搜索股票')
        while True:
            response = ''
            keyword = input('查询股票请输入关键词，退出系统请输入0：')
            if keyword == '0':
                exit()
            try:
                orgId, plate, code = code_info = get_stock(keyword)
                if orgId is not None:
                    while True:
                        try:
                            response = get_stock_introduction(plate, code)  # 无异常打印股票基本信息
                            if response == 'success':
                                break
                        except:
                            print('出现错误，重试中...')
            except:
                print('关键字错误,请重新输入')  # 有异常
            if response == 'success':
                break

        repost_dict = {'1': '年报', '2': '半年报', '3': '一季度报', '4': '三季度报', '5': '业绩报告', '6': '权益分派',
                       '7': '董事会', '8': '监事会', '9': '股东大会', '10': '日常经营', '11': '公司治理', '12': '中介报告',
                       '13': '首发', '14': '增发', '15': '股权激励', '16': '配股', '17': '解禁', '18': '公司债',
                       '19': '可转让债', '20': '其他融资', '21': '股权变动', '22': '补充更正', '23': '澄清致歉', '24': '风险提示',
                       '25': '特别处理和退市', '26': '退市整理期'
                       }
        count = 0
        print('*' * 120)
        while True:
            sleep = input(f'筛选股票{code}报告请输入任意键回车，退出系统请输入0：')
            if sleep == '0':
                exit()
            else:
                print('功能二：筛选报告')
                for k, v in repost_dict.items():
                    print(str(k) + ':', v, end='    ')
                    count += 1
                    if count % 5 == 0 and count != 26:
                        print()
                print('\n')
                report = input('请输入要获取的公告，比如输入1 获取年报，获取多个公告请以英文逗号,隔开，比如输入 1,2 获取年报和半年报:')
                # print(report)
                report_list = report.split(',')
                report = ''
                for i in report_list:
                    if i in repost_dict:
                        report += repost_dict[i]

                start_date = ''
                end_date = ''
                while True:
                    start_date = input('请输入开始时间,格式为2019-01-01:')
                    end_date = input('请输入结束时间,格式为2022-01-01:')
                    try:
                        start_date = time.strftime("%Y-%m-%d", time.strptime(start_date, "%Y-%m-%d"))
                        end_date = time.strftime("%Y-%m-%d", time.strptime(end_date, "%Y-%m-%d"))
                        break
                    except:
                        print('日期格式错误，请重新输入')

                while True:
                    try:
                        report_name_url = brush_report(report, start_date, end_date, orgId, plate, code)
                        if report_name_url != None:
                            print('\n')
                            print('\n\n' + '*' * 120)
                            kw = input('下载报告请输入任意键回车，退出系统请输入0：')
                            if kw != '0':
                                print('功能三：下载报告')
                                reponse = download_PDF(report_name_url)
                                if reponse == 'success':
                                    break  # break while
                            else:
                                exit()
                    except:
                        print('出现错误，重试中...')


if __name__ == '__main__':  # 程序入口
    excute()