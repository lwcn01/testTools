# -*- coding: utf-8 -*-
import re,time,datetime,base64
import json,random,uuid,operator
import xml.dom.minidom
from collections import OrderedDict
from utils import IdentityCard
from mylog import MyLogger as myLog

@myLog()
def getName(sex=0):
    last_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', 
                  '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', 
                  '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', 
                  '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康', 
                  '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', 
                  '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', 
                  '席', '季', '麻', '强', '贾', '路', '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '钟', '徐', '邱', '骆', '高', '夏', 
                  '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万', '支', '柯', '咎', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', 
                  '宣', '丁', '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆', 
                  '荣', '翁', '荀', '羊', '於', '惠', '甄', '魏', '加', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫', 
                  '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫', '宁', '仇', 
                  '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '姜', '詹', '束', '龙', '叶', '幸', '司', '韶', '郜', '黎', '蓟', '薄', 
                  '印', '宿', '白', '怀', '蒲', '台', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阴', '郁', '胥', '能', 
                  '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '却', '璩', '桑', '桂', 
                  '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', 
                  '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎', '戈', '廖', '庚', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', 
                  '匡', '国', '文', '寇', '广', '禄', '阙', '东', '殴', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', 
                  '敖', '融', '冷', '訾', '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', 
                  '查', '后', '江', '红', '游', '竺', '权', '逯', '盖', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', 
                  '赫连', '皇甫', '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '仲孙', '太叔', '申屠', '公孙', '乐正', '轩辕', '令狐', '钟离', 
                  '闾丘', '长孙', '慕容', '鲜于', '宇文', '司徒', '司空', '亓官', '司寇', '仉督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', 
                  '壤驷', '公良', '拓拔', '夹谷', '宰父', '谷粱', '晋楚', '阎法', '汝鄢', '涂钦', '段干', '百里', '东郭', '南门', '呼延', '归海', '羊舌', 
                  '微生', '岳帅', '缑亢', '况后', '有琴', '梁丘', '左丘', '东门', '西门', '商牟', '佘佴', '伯赏', '南宫', '墨哈', '谯笪', '年爱', '阳佟', 
                  '第五', '言福'] 
    first_names_girl = ['秀娟', '英华', '慧巧', '美娜', '静淑', '惠珠', '翠雅', '芝玉', '萍红', '娥玲', '芬芳', '燕彩', '春菊', '兰凤', '洁梅', '琳素', 
                        '云莲', '真环', '雪荣', '爱妹', '霞香', '月莺', '媛艳', '瑞凡', '佳嘉', '琼勤', '珍贞', '莉桂', '娣叶', '璧璐', '娅琦', '晶妍', 
                        '茜秋', '珊莎', '锦黛', '青倩', '婷姣', '婉娴', '瑾颖', '露瑶', '怡婵', '雁蓓', '纨仪', '荷丹', '蓉眉', '君琴', '蕊薇', '菁梦', 
                        '岚苑', '婕馨', '瑗琰', '韵融', '园艺', '咏卿', '聪澜', '纯毓', '悦昭', '冰爽', '琬茗', '羽希', '宁欣', '飘育', '滢馥', '筠柔', 
                        '竹霭', '凝晓', '欢霄', '枫芸', '菲寒', '伊亚', '宜可', '姬舒', '影荔', '枝思', '丽']
    first_names_boy = ['伟刚', '勇毅', '俊峰', '强军', '平保', '东文', '辉力', '明永', '健世', '广志', '义兴', '良海', '山仁', '波宁', '贵福', '生龙',
                       '元全', '国胜', '学祥', '才发', '武新', '利清', '飞彬', '富顺', '信子', '杰涛', '昌成', '康星', '光天', '达安', '岩中', '茂进',
                       '林有', '坚和', '彪博', '诚先', '敬震', '振壮', '会思', '群豪', '心邦', '承乐', '绍功', '松善', '厚庆', '磊民', '友裕', '河哲',
                       '江超', '浩亮', '政谦', '亨奇', '固之', '轮翰', '朗伯', '宏言', '若鸣', '朋斌', '梁栋', '维启', '克伦', '翔旭', '鹏泽', '晨辰',
                       '士以', '建家', '致树', '炎德', '行时', '泰盛', '雄琛', '钧冠', '策腾', '楠榕', '风航', '弘']                       
    if sex == 0:
        name_all = random.choice(last_names) + random.choice(first_names_girl) # 随机取姓+名
    else:
        name_all = random.choice(last_names) + random.choice(first_names_boy)    
    return name_all

@myLog()
def getPhoneNumber():
    pre_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150",
                "151", "152","153", "155", "156", "157", "158", "159", "186", "187", "188"]
    #timeString = int(time.time()) # float into int
    num = getRandom(8)
    phoneNumber = random.choice(pre_list) + num
    return phoneNumber

@myLog()
def checkPhone(phone_num='23312341111'):
    # 11位，其中前3位是网络识别号，4-7位是地区编码，8-11位是用户号码
    phone_info = {}
    #assert 7 <= len(phone_num) <= 11
    if len(phone_num) <7 or len(phone_num) >11:
        return phone_info
    channel = {1: '移动', 2: '电信', 3: '联通',4:'中国广电',5:'卫星通信',
               6:'移动虚拟运营商',7:'电信虚拟运营商',8:'联通虚拟运营商',9:'物联网'}
    prefix_phone = {1:['1340','1341','1342','1343','1344','1345','1346','1347','1348','135','136','137','138','139','1440','147',
                       '148','150','151','152','157','158','159','172','178','182','183','184','187','188','195','197','198'],
                    2:['133','149','153','173','177','180','181','189','190','191','193','199'],
                    3:['130','131','132','145','155','156','166','167','171','175','176','185','186','196'],
                    4:['192'],
                    5:['1349','174'],
                    6:['1703','1705','1706','165'],
                    7:['1700','1701','1702','162'],
                    8:['1704','1707','1708','1709','167','171'],
                    9:['140','141','144','146','148']}       
    net_3 = str(phone_num)[0:3]
    net_4 = str(phone_num)[0:4]
    district_code = str(phone_num)[3:7]
    for k, v in prefix_phone.items():
    	if net_3 in v or net_4 in v:
    		phone_type = channel[k]
    		break
    else:
    	phone_type=''
    phone_info['phone'] = str(phone_num)[0:7]
    phone_info['province'] = district_code
    # phone_info['city']
    # phone_info['zip_code']
    # phone_info['area_code']
    phone_info['phone_type'] = phone_type
    return phone_info

@myLog()
def getBankCard(bankID='102',cardType=1):
    # * 1借记卡，2贷记卡
    binCode102_10 = ['620086', '621226', '900000', '622200', '621670', '621372', '621375', '621723', '620058', '620086', '620058', '621558',
                     '623062', '623272', '623260', '621476', '621414', '621721', '621227', '621475', '621558', '622208', '622200', '623271',
                     '623229', '621559', '621288', '621218', '621281', '620516', '622203', '900010', '621618', '621722', '623272', '623272',
                     '623272', '623272', '623272', '623272', '623272']  # 卡bin校验
    binCode102_20 = ['628288', '628286', '625941', '625930', '625929', '625928', '625926', '625925', '625924', '625921', '625920', '625916',
                     '625915', '625914', '625900', '625865', '625860', '625859', '625858', '625801', '625709']
    if cardType == 1:
        if bankID == '102': 
            AccountNumber = random.choice(binCode102_10) + getRandom(10) + "10"
        elif bankID == '103':
            AccountNumber = "620059" + getRandom(13) 
        elif bankID == '104':
            AccountNumber = "621668" + getRandom(13)
        elif bankID == '105':
            AccountNumber = "621466" + getRandom(10) 
        else:
            AccountNumber = str(random.randint(0000000000000, 9999999999999))
    elif cardType == 2:
        if bankID == '102': 
            AccountNumber = "438125" + getRandom(10)
        elif bankID == '103':
            AccountNumber = "404120" + getRandom(10) 
        elif bankID == '104':
            AccountNumber = "409670" + getRandom(10)
        elif bankID == '105':
            AccountNumber = "489592" + getRandom(10) 
        else:
            AccountNumber = str(random.randint(0000000000000, 9999999999999))
    else:
        AccountNumber = str(random.randint(0000000000000, 9999999999999))                                       
    return AccountNumber

@myLog()
def getEmail():
    base_name = "abcdefghijklmnopqrstuvwxyz0123456789"
    email_suffix = ['@gmail.com', '@yahoo.com', '@msn.com', '@hotmail.com', '@aol.com', '@ask.com', '@live.com', '@qq.com', '@0355.net', '@163.com', 
                    '@163.net', '@263.net', '@3721.net', '@yeah.net', '@googlemail.com', '@126.com', '@sina.com', '@sohu.com', '@yahoo.com.cn']
    email_name = ''.join(random.sample(base_name, len(random.choice(email_suffix))))
    email_address =  email_name + random.choice(email_suffix)
    return email_address

@myLog()
def getAddress():
    road = ['重庆大厦', '黑龙江路', '十梅庵街', '遵义路', '湘潭街', '瑞金广场', '仙山街', '仙山东路', '仙山西大厦', '白沙河路', '赵红广场', '机场路', '民航街', '长城南路', '流亭立交桥', 
            '虹桥广场', '长城大厦', '礼阳路', '风岗街', '中川路', '白塔广场', '兴阳路', '文阳街', '绣城路', '河城大厦', '锦城广场', '崇阳街', '华城路', '康城街', '正阳路', '和阳广场', 
            '中城路', '江城大厦', '顺城路', '安城街', '山城广场', '春城街', '国城路', '泰城街', '德阳路', '明阳大厦', '春阳路', '艳阳街', '秋阳路', '硕阳街', '青威高速', '瑞阳街', '丰海路', 
            '双元大厦', '惜福镇街道', '夏庄街道', '古庙工业园', '中山街', '太平路', '广西街', '潍县广场', '博山大厦', '湖南路', '济宁街', '芝罘路', '易州广场', '荷泽四路', '荷泽二街', 
            '荷泽一路', '荷泽三大厦', '观海二广场', '广西支街', '观海一路', '济宁支街', '莒县路', '平度广场', '明水路', '蒙阴大厦', '青岛路', '湖北街', '江宁广场', '郯城街', '天津路', 
            '保定街', '安徽路', '河北大厦', '黄岛路', '北京街', '莘县路', '济南街', '宁阳广场', '日照街', '德县路', '新泰大厦', '荷泽路', '山西广场', '沂水路', '肥城街', '兰山路', 
            '四方街', '平原广场', '泗水大厦', '浙江路', '曲阜街', '寿康路', '河南广场', '泰安路', '大沽街', '红山峡支路', '西陵峡一大厦', '台西纬一广场', '台西纬四街', '台西纬二路', 
            '西陵峡二街', '西陵峡三路', '台西纬三广场', '台西纬五路', '明月峡大厦', '青铜峡路', '台西二街', '观音峡广场', '瞿塘峡街', '团岛二路', '团岛一街', '台西三路', '台西一大厦', 
            '郓城南路', '团岛三街', '刘家峡路', '西藏二街', '西藏一广场', '台西四街', '三门峡路', '城武支大厦', '红山峡路', '郓城北广场', '龙羊峡路', '西陵峡街', '台西五路', '团岛四街', 
            '石村广场', '巫峡大厦', '四川路', '寿张街', '嘉祥路', '南村广场', '范县路', '西康街', '云南路', '巨野大厦', '西江广场', '鱼台街', '单县路', '定陶街', '滕县路', '钜野广场', 
            '观城路', '汶上大厦', '朝城路', '滋阳街', '邹县广场', '濮县街', '磁山路', '汶水街', '西藏路', '城武大厦', '团岛路', '南阳街', '广州路', '东平街', '枣庄广场', '贵州街', '费县路', 
            '南海大厦', '登州路', '文登广场', '信号山支路', '延安一街', '信号山路', '兴安支街', '福山支广场', '红岛支大厦', '莱芜二路', '吴县一街', '金口三路', '金口一广场', '伏龙山路', 
            '鱼山支街', '观象二路', '吴县二大厦', '莱芜一广场', '金口二街', '海阳路', '龙口街', '恒山路', '鱼山广场', '掖县路', '福山大厦', '红岛路', '常州街', '大学广场', '龙华街', '齐河路', 
            '莱阳街', '黄县路', '张店大厦', '祚山路', '苏州街', '华山路', '伏龙街', '江苏广场', '龙江街', '王村路', '琴屿大厦', '齐东路', '京山广场', '龙山路', '牟平街', '延安三路', '延吉街', 
            '南京广场', '东海东大厦', '银川西路', '海口街', '山东路', '绍兴广场', '芝泉路', '东海中街', '宁夏路', '香港西大厦', '隆德广场', '扬州街', '郧阳路', '太平角一街', '宁国二支路', 
            '太平角二广场', '天台东一路', '太平角三大厦', '漳州路一路', '漳州街二街', '宁国一支广场', '太平角六街', '太平角四路', '天台东二街', '太平角五路', '宁国三大厦', '澳门三路', 
            '江西支街', '澳门二路', '宁国四街', '大尧一广场', '咸阳支街', '洪泽湖路', '吴兴二大厦', '澄海三路', '天台一广场', '新湛二路', '三明北街', '新湛支路', '湛山五街', '泰州三广场', 
            '湛山四大厦', '闽江三路', '澳门四街', '南海支路', '吴兴三广场', '三明南路', '湛山二街', '二轻新村镇', '江南大厦', '吴兴一广场', '珠海二街', '嘉峪关路', '高邮湖街', '湛山三路', 
            '澳门六广场', '泰州二路', '东海一大厦', '天台二路', '微山湖街', '洞庭湖广场', '珠海支街', '福州南路', '澄海二街', '泰州四路', '香港中大厦', '澳门五路', '新湛三街', '澳门一路', 
            '正阳关街', '宁武关广场', '闽江四街', '新湛一路', '宁国一大厦', '王家麦岛', '澳门七广场', '泰州一路', '泰州六街', '大尧二路', '青大一街', '闽江二广场', '闽江一大厦', '屏东支路', 
            '湛山一街', '东海西路', '徐家麦岛函谷关广场', '大尧三路', '晓望支街', '秀湛二路', '逍遥三大厦', '澳门九广场', '泰州五街', '澄海一路', '澳门八街', '福州北路', '珠海一广场', '宁国二路', 
            '临淮关大厦', '燕儿岛路', '紫荆关街', '武胜关广场', '逍遥一街', '秀湛四路', '居庸关街', '山海关路', '鄱阳湖大厦', '新湛路', '漳州街', '仙游路', '花莲街', '乐清广场', '巢湖街', 
            '台南路', '吴兴大厦', '新田路', '福清广场', '澄海路', '莆田街', '海游路', '镇江街', '石岛广场', '宜兴大厦', '三明路', '仰口街', '沛县路', '漳浦广场', '大麦岛', '台湾街', '天台路', 
            '金湖大厦', '高雄广场', '海江街', '岳阳路', '善化街', '荣成路', '澳门广场', '武昌路', '闽江大厦', '台北路', '龙岩街', '咸阳广场', '宁德街', '龙泉路', '丽水街', '海川路', '彰化大厦', 
            '金田路', '泰州街', '太湖路', '江西街', '泰兴广场', '青大街', '金门路', '南通大厦', '旌德路', '汇泉广场', '宁国路', '泉州街', '如东路', '奉化街', '鹊山广场', '莲岛大厦', '华严路', 
            '嘉义街', '古田路', '南平广场', '秀湛路', '长汀街', '湛山路', '徐州大厦', '丰县广场', '汕头街', '新竹路', '黄海街', '安庆路', '基隆广场', '韶关路', '云霄大厦', '新安路', '仙居街', 
            '屏东广场', '晓望街', '海门路', '珠海街', '上杭路', '永嘉大厦', '漳平路', '盐城街', '新浦路', '新昌街', '高田广场', '市场三街', '金乡东路', '市场二大厦', '上海支路', '李村支广场', 
            '惠民南路', '市场纬街', '长安南路', '陵县支街', '冠县支广场', '小港一大厦', '市场一路', '小港二街', '清平路', '广东广场', '新疆路', '博平街', '港通路', '小港沿', '福建广场', '高唐街', 
            '茌平路', '港青街', '高密路', '阳谷广场', '平阴路', '夏津大厦', '邱县路', '渤海街', '恩县广场', '旅顺街', '堂邑路', '李村街', '即墨路', '港华大厦', '港环路', '馆陶街', '普集路', 
            '朝阳街', '甘肃广场', '港夏街', '港联路', '陵县大厦', '上海路', '宝山广场', '武定路', '长清街', '长安路', '惠民街', '武城广场', '聊城大厦', '海泊路', '沧口街', '宁波路', '胶州广场', 
            '莱州路', '招远街', '冠县路', '六码头', '金乡广场', '禹城街', '临清路', '东阿街', '吴淞路', '大港沿', '辽宁路', '棣纬二大厦', '大港纬一路', '贮水山支街', '无棣纬一广场', '大港纬三街', 
            '大港纬五路', '大港纬四街', '大港纬二路', '无棣二大厦', '吉林支路', '大港四街', '普集支路', '无棣三街', '黄台支广场', '大港三街', '无棣一路', '贮水山大厦', '泰山支路', '大港一广场', 
            '无棣四路', '大连支街', '大港二路', '锦州支街', '德平广场', '高苑大厦', '长山路', '乐陵街', '临邑路', '嫩江广场', '合江路', '大连街', '博兴路', '蒲台大厦', '黄台广场', '城阳街', 
            '临淄路', '安邱街', '临朐路', '青城广场', '商河路', '热河大厦', '济阳路', '承德街', '淄川广场', '辽北街', '阳信路', '益都街', '松江路', '流亭大厦', '吉林路', '恒台街', '包头路', 
            '无棣街', '铁山广场', '锦州街', '桓台路', '兴安大厦', '邹平路', '胶东广场', '章丘路', '丹东街', '华阳路', '青海街', '泰山广场', '周村大厦', '四平路', '台东西七街', '台东东二路', 
            '台东东七广场', '台东西二路', '东五街', '云门二路', '芙蓉山村', '延安二广场', '云门一街', '台东四路', '台东一街', '台东二路', '杭州支广场', '内蒙古路', '台东七大厦', '台东六路', 
            '广饶支街', '台东八广场', '台东三街', '四平支路', '郭口东街', '青海支路', '沈阳支大厦', '菜市二路', '菜市一街', '北仲三路', '瑞云街', '滨县广场', '庆祥街', '万寿路', '大成大厦', 
            '芙蓉路', '历城广场', '大名路', '昌平街', '平定路', '长兴街', '浦口广场', '诸城大厦', '和兴路', '德盛街', '宁海路', '威海广场', '东山路', '清和街', '姜沟路', '雒口大厦', '松山广场', 
            '长春街', '昆明路', '顺兴街', '利津路', '阳明广场', '人和路', '郭口大厦', '营口路', '昌邑街', '孟庄广场', '丰盛街', '埕口路', '丹阳街', '汉口路', '洮南大厦', '桑梓路', '沾化街', 
            '山口路', '沈阳街', '南口广场', '振兴街', '通化路', '福寺大厦', '峄县路', '寿光广场', '曹县路', '昌乐街', '道口路', '南九水街', '台湛广场', '东光大厦', '驼峰路', '太平山', '标山路', 
            '云溪广场', '太清路']
    first = random.choice(road)
    second = str(random.randint(11, 150)) + "号"
    third = "-" + str(random.randint(1, 20)) + "-" + str(random.randint(1, 10))
    return first + second + third

#@myLog()
def getID(citycode='',birthday='',sex=0,num=100):
    if str(citycode) and str(citycode) and str(sex):
        ID = IdentityCard.getIdentifyCard(str(citycode)+str(birthday),sex,num)
    else:
        ID = IdentityCard.getIdentify()    
    return ID

@myLog()
def getDays(month,year=1999):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        monthday = 31
    elif month in [4, 6, 9, 11]:
        monthday = 30
    else:
        if year%4 == 0:
            monthday = 29
        else:
            monthday = 28
    return monthday
        
@myLog()    
def getRandom(length, string=""):
    #str_length = len(string) if string else 9
    valus = ""
    for _ in range(length):
        if string:
            valus += ''.join(random.sample(string,1))
        else:  
            valus += str(random.randint(0,9))
    return valus

@myLog()
def getTxSN(length=27):
    txsn_prefix = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    if len(txsn_prefix) < length:
        txsn = txsn_prefix + getRandom(length-len(txsn_prefix))
    else:    
        txsn = txsn_prefix[:length]
    return txsn    

@myLog()
def getOrganizingCode():
    # 获取组织机构代码 9位数
    codes = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    weightFactor = [ 3, 7, 9, 10, 5, 8, 4, 2 ]
    
    sum = 0
    code1_8 = getRandom(8, "123456789")
    for i in range(len(code1_8)):
        sum += weightFactor[i] * codes.index(code1_8[i:i + 1])
    mod = sum % 11
    checkCode = list(codes)[11 - mod]
    return code1_8 + checkCode

@myLog()    
def getUscc():
    # * 获取统一社会信用代码
    # * 第1位：登记管理部门代码 123456789ANY 第2位：机构类别代码 123459 第3位～第8位：登记管理机关行政区划码
    # * 第9位～第17位：主体标识码（组织机构代码） 第18位：校验码 例子： 91110105306652183Y
    code1 = getRandom(1, "123456789ANY")
    code2 = getRandom(1, "123459")
    code3 = [k for k in IdentityCard.identityCard.keys()]
    code3_7 = str(random.choice(code3))
    code8_17 = getOrganizingCode()
    code1_17 = code1 + code2 + code3_7 + code8_17
    #// 代码字符集，不含 I O S V Z，共30位
    codes = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    # #// 各位置序号上的加权因子
    weightFactor = [ 1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28 ]
    # #// 级数之和
    sum = 0
    for i in range(len(code1_17)):
        sum += weightFactor[i] * codes.index(code1_17[i:i + 1])
    # #// 求级数之和模31的余数
    mod = sum % 31
    if(mod==0):
        return code1_17 + str(mod)
    else:
        checkCode = list(codes)[31 - mod]
    return code1_17 + checkCode

@myLog()
def checkUscc(uscc):
    # 是否为真实的统一社会信用代码
    # 代码字符集，不含 I O S V Z，共30位
    codes = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    # 各位置序号上的加权因子
    weightFactor = [ 1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28 ]
    # 级数之和
    sum = 0
    # 前17位
    for i in range(0, len(uscc) - 1):
        sum += weightFactor[i] * codes.index(uscc[i: i + 1])
    # 求级数之和模31的余数
    mod = sum % 31
    if(mod==0):
        return operator.eq(uscc[len(uscc) - 1],str(mod))
    else:
        # 求理论上计算出来的校验码字符值
        calculatedCheckCode = list(codes)[31 - mod]
        return operator.eq(uscc[len(uscc) - 1],calculatedCheckCode)  
        
#@myLog()
def getIdentify():
    prov_city = {}
    city_county = {}
    idcards = IdentityCard.identityCard
    for i in idcards.keys():
        j = str(i)
        prov = j[:2] + '0000'
        city = j[:4] + '00'
        # {'110000':['110100','110200']}
        if  prov in prov_city:
            if j == city:
                prov_city[prov].append(j)
        else:
            prov_city[prov] = []
        # {'110100':['110101','110102']}
        if j != prov:
            if  city in city_county:
                city_county[city].append(j)
            else:
                city_county[city] = []    
    return prov_city,city_county,idcards

@myLog()
def getUnixTime(str_time, mod):
    if mod == 'data2time':
        #将日期转换为时间戳,单位秒
        try:
            if "年" in str_time:
                str_time = str_time.replace(r'年','-').replace(r'月','-').replace(r'日','')
                str_time = str_time.replace(r'时',':').replace(r'分',':').replace(r'秒','')
            if '-' in str_time and ':' in str_time:
                format_string = '%Y-%m-%d %H:%M:%S'
            elif '-' in str_time and ':' not in str_time:
                format_string = '%Y-%m-%d'
            else:
                format_string = "%a %b %d %H:%M:%S %Y"
            result = time.mktime(time.strptime(str_time, format_string))
        except Exception as e:
            result = None#"Error: %s"%e
    else:
        #将时间戳转换为日期
        try:
            if len(str_time) > 10:
                int_time = float(str_time)/1000
            else:
                int_time = float(str_time)
            result = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int_time))
        except Exception as e:
            result = None#"Error: %s"%e
    return result

@myLog()
def isChinese(txt_string):
    for word in txt_string:
        if '\u4e00' <= word <= '\u9fff':
            return True
    return False

@myLog()        
def getUnicode(txt):
    result=None
    if isinstance(txt, str):
        #unicode转中文
        if "\\u" in txt:
            try:
                result=txt.encode('utf-8').decode('unicode_escape')  
            except:
                result=None                        
        #中文转unicode
        if isChinese(txt):
            result = txt.encode('unicode-escape').decode('utf-8')
    return result

@myLog()    
def getSigns(birthday):
    # 字符串比较大小
    year = birthday[0:4]
    birday = birthday[4:9]
    if ('1222'<= str(birday) <='1231') or ('0101'<= str(birday) <='0120'):
        sign = '摩羯座'        
    elif '0121'<= str(birday) <='0219':
        sign = '水瓶座'
    elif '0220'<= str(birday) <='0320':
        sign = '双鱼座'            
    elif '0321'<= str(birday) <='0420':
        sign = '白羊座'
    elif '0421'<= str(birday) <='0521':
        sign = '金牛座'            
    elif '0522'<= str(birday) <='0621':
        sign = '双子座' 
    elif '0622'<= str(birday) <='0722':
        sign = '巨蟹座' 
    elif '0723'<= str(birday) <='0822':
        sign = '狮子座' 
    elif '0823'<= str(birday) <='0922':
        sign = '处女座'
    elif '0923'<= str(birday) <='1023':
        sign = '天秤座' 
    elif '1024'<= str(birday) <='1122':
        sign = '天蝎座'
    elif '1123'<= str(birday) <='1221':
        sign = '射手座'
    else:
        sign = -1
    zodiac = '猴鸡狗猪鼠牛虎兔龙蛇马羊'[int(year)%12]
    return sign,zodiac

@myLog()    
def transferZodiacTime(msg,_type=0):
    # 生肖与时辰
    zodiac = {'子（鼠）' : '23点~01点',
             '丑（牛）' : '01点~03点',
             '寅（虎）' : '03点~05点',
             '卯（兔）' : '05点~07点',
             '辰（龙）' : '07点~09点',
             '巳（蛇）' : '09点~11点',
             '午（马）' : '11点~13点',
             '未（羊）' : '13点~15点',
             '申（猴）' : '15点~17点',
             '酉（鸡）' : '17点~19点',
             '戌（狗）' : '19点~21点',
             '亥（猪）' : '21点~23点'}
    _zodiac = dict(map(reversed, zodiac.items())) if _type!=0 else zodiac #反转
    zt = [v for k,v in _zodiac.items() if msg in k]
    return zt[0] if zt else ''
    
@myLog()        
def checkJson(json_msg, sort=False, printType=0):
    isJson = True
    if isinstance(json_msg, str):
        # 标准json是双引号
        str_msg = json_msg.replace("'",'"')
        try:
            json_msg = json.loads(str_msg, object_pairs_hook=OrderedDict) #转dict,且顺序不变
        except ValueError:
            isJson = False   # none dump后为null
    if isJson:
        # json 排序输出sort_keys
        str_msg = json.dumps(json_msg, sort_keys=sort, indent=4, separators=(',',':'), ensure_ascii=False)
        if printType == 0:  #0-返回string / 1-返回dict
            return str_msg
        else:
            return json.loads(str_msg, object_pairs_hook=OrderedDict)   
    return isJson

@myLog()
def formatXML(requestXML):
    '''
     * 格式化xml,显示为容易看的XML格式
    '''
    # tree = ET.parse('pre.xml') root = tree.getroot()
    # root = ET.fromstring(requestXML)
    requestXML_1 = requestXML.strip("'").strip('"')
    try:
        primit_xml = xml.dom.minidom.parseString(requestXML_1)
        result = primit_xml.toprettyxml()
    except:
        result = checkJson({"error_code" : "0002",
                            "message" : "输入错误无法解析"})   
    return result

@myLog()        
def formatJson(requestJson, transfer=0, sort=False, printType=0):
    # 入参为string
    result = ''
    if '\"' in requestJson:
        str_msg = requestJson.replace(r'\"','"')
    else:
        str_msg = requestJson
    if transfer==1:
        # 1--加转义
        j = ''
        str_msg = checkJson(str_msg,sort,printType=0)
        if str_msg:
            for i in str_msg.splitlines():
                j = i.strip("\n")
                if '"' in i:
                    j = j.replace('"','\\"')
                if '{' in j and result.count('{')==0:
                    j = '"%s\\n" +'%j + "\n"
                elif ('}' in j) and (result.count('{') == (result.count('}') + 1)):
                    j = '"%s"'%j + "\n"    
                else:
                    j = '"  %s\\n" +'%j + "\n"
                result += j
    elif transfer==2:
        str_2_json = checkJson(str_msg,sort,printType=1) 
        if str_2_json and isinstance(str_2_json, dict):
            # 2-- Json转换成GET传参, int 也是json, 排除int类型
            result = "&".join("{0}={1}".format(k, v) for k, v in str_2_json.items())
        else:
            # 2-- GET转换成Json
            if "=" in str_msg:
                param = {}
                for i in re.split(r"[,&]",str_msg):
                    j = i.split('=',1)
                    if len(j)==2:
                        param.update({j[0]:j[1]})
                    else:
                        param.update({j[0]:''})
                result = checkJson(param,sort,printType) 
    elif transfer==3:
        # 3--json转为换行输出
        str_2_json = checkJson(str_msg,sort,printType=1)
        if str_2_json:
            result = str_2_json
            if isinstance(str_2_json, dict):
                result = "\n".join(list(map(lambda x:'{}：{}'.format(x[0],x[1]),str_2_json.items())))             
    else:
        # 0--去除转义
        result = checkJson(str_msg,sort,printType)
    if not result:
        return checkJson({"error_code" : "0001",
                          "message" : "Json格式错误！"})  
    return result           

@myLog()
def formatSql(requestSql):
    try:
        result = formatSqls(requestSql)
    except Exception as e:
        return checkJson({"error_code" : "0002",
                          "message" : "输入错误无法解析"})
    else:
        return result

@myLog()
def formatSqls(requestSql):
    # |[sql]=[Select * From LabelQueryMapping Where channelId=? And status = ?][args]=[5139b, 20]|
    #  将日志中的SQL相关日志格式化
    if ("sql" in requestSql and "args" in requestSql) or ("Preparing" in requestSql and "Parameters" in requestSql): 
        if ("sql" in requestSql and "args" in requestSql):
            SqlList = re.findall(r"sql(.*?)args", requestSql)
            ParamList = re.findall(r"args(.*?)\n", requestSql)
        else:
            #  引入mybits后SQL日志格式不一样
            SqlList = re.findall(r"Preparing(.*?)\n", requestSql)
            ParamList = re.findall(r"Parameters(.*?)\n", requestSql)            
        sql_string = SqlList[0].strip('=[]').strip().strip(":")
        param_string = ParamList[0].strip('=[]').rstrip("|").rstrip("]").strip().strip(":")
        params = param_string.split(",")
        params = [param.split("(")[0] if "(" in param else param for param in params]
        if "INSERT INTO" in sql_string or "Insert Into" in sql_string or "insert into" in sql_string:
            #sql = re.search(r'[(](.*?)[)]',sql).group(0)
            sql = re.findall(r'[(](.*?)[)]',sql_string)
            if len(sql) == 2:
                sql_1 = sql[0].split(",")
                sql_2 = sql[1].split(",")
            else:
                return checkJson({"error_code" : "0002",
                                  "message" : "输入错误无法解析"})                            
            if len(sql_1) == len(sql_2):
                key_value = ''
                for i in range(len(params)):
                    if params[i] == " " or params[i] == "":
                        params[i] = "@null"
                    sql_string = sql_string.replace('?', ("'"+params[i].strip()+"'"), 1)
                    #re.sub(r'?', params[i], sql_string, 1)
                    if len(sql_1) > i:
                        key_value += sql_1[i].strip() + " = " + params[i].strip() + "\n"
                result = ("SQL格式化:\n--------------------------------\n" + sql_string
                            + "\n--------------------------------\n\nKey = Value分解：\n--------------------------------\n"
                            + key_value + "--------------------------------")                    
            else:
                result = checkJson({"error_code" : "0003",
                                    "message" : "字段和数值数量不匹配"})
        elif ("SELECT" in sql_string or "Select" in sql_string or "select" in sql_string) and ("FROM" in sql_string or "From" in sql_string or "from" in sql_string):
            for i in range(len(params)):
                sql_string = sql_string.replace('?', ("'"+params[i].strip()+"'"), 1)
            result = ("SQL格式化:\n--------------------------------\n" + sql_string
                       + "\n--------------------------------")
        elif ("UPDATE" in sql_string or "Update" in sql_string or "update" in sql_string) and ("SET" in sql_string or "Set" in sql_string or "set" in sql_string):
            for i in range(len(params)):
                sql_string = sql_string.replace('?', ("'"+params[i].strip()+"'"), 1)      
            result = ("SQL格式化:\n--------------------------------\n" + sql_string
                        + "\n--------------------------------") 
        else:
            result = checkJson({"error_code" : "0002",
                                "message" : "输入错误无法解析"})         
    else:
        # 将填入的SQL字符串美化，美化SQL
        sql_string = requestSql.strip()
        if sql_string.startswith("INSERT INTO") or sql_string.startswith("Insert Into") or sql_string.startswith("insert into"):
            sql = re.findall(r'[(](.*?)[)]',sql_string)
            if len(sql) == 1:
                sql_1 = [""]
                sql_2 = [x.strip() for x in sql[0].split(",")]
            elif len(sql) == 2:
                sql_1 = [x.strip() for x in sql[0].split(",")]
                sql_2 = [x.strip() for x in sql[1].split(",")]
            else:
                return checkJson({"error_code" : "0002",
                                  "message" : "输入错误无法解析"})                                        
            result = "INSERT INTO " + sql_string.split()[2].split("(")[0].strip() + "\n" + "\t"*3 + "(" + ",\n\t\t\t".join(sql_1) + ")\nVALUES\t\t(" + ",\n\t\t\t".join(sql_2) + ")"
        elif sql_string.startswith("UPDATE") or sql_string.startswith("Update") or sql_string.startswith("update") and ("SET" in sql_string or "Set" in sql_string or "set" in sql_string): 
            sql = re.split(r"WHERE|Where|where", sql_string)
            if len(sql) == 1:
                sql_1 = [x.strip() if index !=0 else re.split(r"SET|Set|set", sql[0].split(",")[0])[-1].strip() for index, x in enumerate(sql[0].split(","))]
                sql_1 = [y.split("=")[0].strip()+" = "+y.split("=")[1].strip() for y in sql_1]
                sql_2 = [""]
            elif len(sql) == 2:
                sql_1 = [x.strip() if index !=0 else re.split(r"SET|Set|set", sql[0].split(",")[0])[-1].strip() for index, x in enumerate(sql[0].split(","))]
                sql_1 = [y.split("=")[0].strip()+" = "+y.split("=")[1].strip() for y in sql_1]
                sql_2 = ["AND " + x.strip() if index !=0 else x.strip() for index, x in enumerate(re.split(r"AND|And|and", sql[1]))]
                sql_2 = [y.split("=")[0].strip()+" = "+y.split("=")[1].strip() if "=" in y else y.strip() for y in sql_2]
                sql_2 = [y if index !=0 else "\nWHERE  "+y for index, y in enumerate(sql_2)]
            else:
                return checkJson({"error_code" : "0002",
                                  "message" : "输入错误无法解析"})
            # sql_1=["ResponseCode = '2000'", "ResponseMessage = '成功'", "SendTime = '20220315095803'", "ChannelTxTime = '20220315095808'"]
            # sql_2=["SystemNo = '2203150958036075608911660'", "AND a='1'", "AND c = ''"]   
            result = "UPDATE " + sql_string.split()[1].strip() + "\n" + "SET    " + ",\n       ".join(sql_1) + ",\n       ".join(sql_2)
        elif sql_string.startswith("SELECT") or sql_string.startswith("Select") or sql_string.startswith("select") and ("FROM" in sql_string or "From" in sql_string or "from" in sql_string):
            sql = re.split(r"ORDER|Order|order", sql_string) # [" channelId='5139' And status = '20' ", ' BY systeno desc']
            sqls_1 = re.split(r"WHERE|Where|where", sql[0]) #['Select systemno , status From LabelQueryMapping ', " channelId='5139' And status = '20' ORDER BY systeno desc"]            
            sqls_2 = re.split(r"FROM|From|from", sqls_1[0]) #['Select a , b ', ' LabelQueryMapping ']      
            sql_4 = ""
            if len(sql) == 1:
                sql_1 = [""]
            elif len(sql) == 2:
                sql_1 = [x.strip() if index !=0 else "\nORDER BY "+x.strip() for index, x in enumerate(sql[1].split()[1:])] # # ['\nORDER BY systeno','desc']
                last_letter = sql_1[-1]
                if last_letter.upper() in ['DESC', 'ASC']:
                    sql_1 = sql_1[:-1] # ['\nORDER BY systeno']
                    sql_4 = last_letter.upper()
            else:
                return checkJson({"error_code" : "0002",
                                  "message" : "输入错误无法解析"})                    
            if len(sqls_1) == 1:
                sql_2 = [x.strip() if index !=0 else x.split()[-1].strip() for index, x in enumerate(sqls_2[0].split(","))] # select sql_1 
                sql_3 = [""]    # where sql_2 
            elif len(sqls_1) == 2:
                sql_2 = [x.strip() if index !=0 else x.split()[-1].strip() for index, x in enumerate(sqls_2[0].split(","))]
                sql_3 = ["AND " + x.strip() if index !=0 else x.strip() for index, x in enumerate(re.split(r"AND|And|and", sqls_1[1]))]
                sql_3 = [y.split("=")[0].strip()+" = "+y.split("=")[1].strip() if "=" in y else y.strip() for y in sql_3]
                sql_3 = [y if index !=0 else "\nWHERE  "+y for index, y in enumerate(sql_3)]
            else:
                return checkJson({"error_code" : "0002",
                                  "message" : "输入错误无法解析"})
            #print(sql_2) = ['a', 'b']
            #sql_3 = ["channelId='5139b'", "AND status = '20'"]
            result = "SELECT " + ",\n       ".join(sql_2) + "\nFROM   " + sqls_2[1].strip() + ",\n       ".join(sql_3) + ",\n ".join(sql_1) + "\n{0}".format(sql_4)
        else:
            result = checkJson({"error_code" : "0002",
                                "message" : "输入错误无法解析"})            
    return result

#@myLog()    
def getIcon():
    with open("title.ico","rb") as f:
        base64bytes = base64.b64encode(f.read())    
    with open("icon.py","w+") as fpy:
        fpy.write('class Icon(object):\n')
        fpy.write('\tdef __init__(self):\n')
        fpy.write('\t\tself.img="')
    with open("icon.py","ab+") as fpy:   
        fpy.write(base64bytes)
    with open("icon.py","a+") as fpy:       
        fpy.write('"')

@myLog()    
def getUuid(printType=None):
    # uuid4 make a random UUID
    # python3.6+ 引入 f-string
    p_uuid = uuid.uuid4()
    if printType:
    	return f'{p_uuid}'.upper()
    return f'{p_uuid}'	

@myLog()    
def getDigital(data,digital=10):
    # 进制转换 digital目标进制
    # 2/8/10/16进制转十进制
    base = (2,8,10,16)
    if digital not in base:
        return False
    ten = int(data, digital)
    # 十进制转2/8/10/16进制
    if digital==2:
        result=bin(ten)
    elif digital==8:
    	result=oct(ten)
    elif digital==16:
    	result=hex(ten)
    else:
        result=ten    
    return result
       