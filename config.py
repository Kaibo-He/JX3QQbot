# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SERVER = "梦江南"

KUNGFU_ICON_DIR = os.path.join(BASE_DIR, "assets", "kungfu")
KUNGFU_ICON_MAP = {
    "冰心诀": os.path.join(KUNGFU_ICON_DIR, "冰心诀.png"),
    "云裳心经": os.path.join(KUNGFU_ICON_DIR, "云裳心经.png"),
    "花间游": os.path.join(KUNGFU_ICON_DIR, "花间游.png"),
    "离经易道": os.path.join(KUNGFU_ICON_DIR, "离经易道.png"),
    "毒经": os.path.join(KUNGFU_ICON_DIR, "毒经.png"),
    "补天诀": os.path.join(KUNGFU_ICON_DIR, "补天诀.png"),
    "莫问": os.path.join(KUNGFU_ICON_DIR, "莫问.png"),
    "相知": os.path.join(KUNGFU_ICON_DIR, "相知.png"),
    "无方": os.path.join(KUNGFU_ICON_DIR, "无方.png"),
    "灵素": os.path.join(KUNGFU_ICON_DIR, "灵素.png"),
    "傲血战意": os.path.join(KUNGFU_ICON_DIR, "傲血战意.png"),
    "铁牢律": os.path.join(KUNGFU_ICON_DIR, "铁牢律.png"),
    "易筋经": os.path.join(KUNGFU_ICON_DIR, "易筋经.png"),
    "洗髓经": os.path.join(KUNGFU_ICON_DIR, "洗髓经.png"),
    "焚影圣诀": os.path.join(KUNGFU_ICON_DIR, "焚影圣诀.png"),
    "明尊琉璃体": os.path.join(KUNGFU_ICON_DIR, "明尊琉璃体.png"),
    "分山劲": os.path.join(KUNGFU_ICON_DIR, "分山劲.png"),
    "铁骨衣": os.path.join(KUNGFU_ICON_DIR, "铁骨衣.png"),
    "紫霞功": os.path.join(KUNGFU_ICON_DIR, "紫霞功.png"),
    "太虚剑意": os.path.join(KUNGFU_ICON_DIR, "太虚剑意.png"),
    "天罗诡道": os.path.join(KUNGFU_ICON_DIR, "天罗诡道.png"),
    "惊羽诀": os.path.join(KUNGFU_ICON_DIR, "惊羽诀.png"),
    "问水诀": os.path.join(KUNGFU_ICON_DIR, "问水诀.png"),
    "笑尘诀": os.path.join(KUNGFU_ICON_DIR, "笑尘诀.png"),
    "北傲诀": os.path.join(KUNGFU_ICON_DIR, "北傲诀.png"),
    "凌海诀": os.path.join(KUNGFU_ICON_DIR, "凌海诀.png"),
    "隐龙诀": os.path.join(KUNGFU_ICON_DIR, "隐龙诀.png"),
    "太玄经": os.path.join(KUNGFU_ICON_DIR, "太玄经.png"),
    "孤锋诀": os.path.join(KUNGFU_ICON_DIR, "孤锋诀.png"),
    "山海心经": os.path.join(KUNGFU_ICON_DIR, "山海心经.png"),
    "周天功": os.path.join(KUNGFU_ICON_DIR, "周天功.png"),
    "未知心法": os.path.join(KUNGFU_ICON_DIR, "未知心法.png")
}

FIVESTONE_ICON_DIR = os.path.join(BASE_DIR, "assets", "equip", "fivestone")
ENCHANT_ICON_DIR = os.path.join(BASE_DIR, "assets", "equip", "enchant")
FIVESTONE_MAP = {
    "五行石（一级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（二级）": os.path.join(FIVESTONE_ICON_DIR, "2.png"),
    "五行石（三级）": os.path.join(FIVESTONE_ICON_DIR, "3.png"),
    "五行石（四级）": os.path.join(FIVESTONE_ICON_DIR, "4.png"),
    "五行石（五级）": os.path.join(FIVESTONE_ICON_DIR, "5.png"),
    "五行石（六级）": os.path.join(FIVESTONE_ICON_DIR, "6.png"),
    "五行石（七级）": os.path.join(FIVESTONE_ICON_DIR, "7.png"),
    "五行石（八级）": os.path.join(FIVESTONE_ICON_DIR, "8.png"),
}
ENCHANT_MAP = {
    "common": os.path.join(ENCHANT_ICON_DIR, "common-enchant.png"),
    "permanent": os.path.join(ENCHANT_ICON_DIR, "permanent-enchant.png")
}

LUCK_DICT = {
    "绝世": [
        "三山四海", "三尺青锋", "阴阳两界", "塞外宝驹", "济苍生", 
        "兔江湖", "争铸吴钩", "侠行囧途", "流年如虹", "万灵当歌", 
        "千秋铸", "追魂骨", "入蛟宫", "塞外西风", "浮光织梦", 
        "昆吾余火", "孤沙影寂"
    ],
    "普通": [
        "黑白路", "少年行", "茶馆奇缘", "生死判", "炼狱厨神", 
        "清风捕王", "扶摇九天", "天涯无归", "护佑苍生", "虎啸山林", 
        "乱世舞姬", "雪山恩仇", "平生心愿", "故园风雨", "韶华故", 
        "惜往日", "舞众生", "白日梦", "劝学记", "寻猫记", 
        "旧宴承欢", "凌云梯", "度人心", "庆舞良宵", "红尘不渡", 
        "镜中琴音", "拜春擂", "莫负初心", "赴九幽", "空谷回音", 
        "泛天河", "侠者成歌", "沙海劫缘", "福运满载"
    ],
    "宠物": [
        "清茗经", "胜负局", "归乡路", "枫林酒", "红衣歌", 
        "捉妖记", "孩童书", "沙海谣", "石敢当", "荆轲刺", 
        "破晓鸣", "竹马情", "至尊宝", "兽王佩", "稚子心", 
        "青草歌", "滇南行", "北行镖", "东海客", "关外商", 
        "锋芒展", "烹调法", "儿女事", "锻剑女", "一念间", 
        "戎马边", "白雪忆", "烟花戏·月", "烟花戏·春", "烟花戏·秋", 
        "烟花戏·风", "归安志·安", "归安志·归", "归安志·志", "太行道", 
        "秘宝图", "客江干", "滴水恩", "谜书生", "沧海笛", 
        "缘来会·瓜", "缘来会·铃", "江湖录", "露园事", "莫贪杯", 
        "瀛洲梦", "话玄虚", "白月皎", "尘网中", "一枝栖", 
        "丹青记", "捉贼记", "童蒙志", "念旧林", "风雨意", 
        "鸠雀记", "幽海牧", "枉叹恨", "子夜歌", "重洋客", 
        "故岁辞", "夜哀鸣", "乱红鸾", "醉烟波", "破巧言", 
        "解心语", "寓天涯", "觅知音", "路投石", "义千金", 
        "风花雪", "语不休", "故人愿", "匿沙影", "燕啼松",
        "授太平"
    ]
}