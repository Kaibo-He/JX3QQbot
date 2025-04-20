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
    "五行石（二级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（三级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（四级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（五级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（六级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（七级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
    "五行石（八级）": os.path.join(FIVESTONE_ICON_DIR, "1.png"),
}
ENCHANT_MAP = {
    "common": os.path.join(ENCHANT_ICON_DIR, "common-enchant.png"),
    "permanent": os.path.join(ENCHANT_ICON_DIR, "permanent-enchant.png")
}

LUCK_DICT = {
    "绝世": [
        "孤沙影寂", "昆吾余火", "浮光织梦", "塞外西风", "入蛟宫", 
        "追魂骨", "千秋铸", "万灵当歌", "流年如虹", "侠行囧途", 
        "争铸吴钩", "兔江湖", "济苍生", "塞外宝驹", "阴阳两界", 
        "三尺青锋", "三山四海"],
    "普通": [
        "福运满载", "沙海劫缘", "侠者成歌", "泛天河", "空谷回音", 
        "赴九幽", "莫负初心", "拜春擂", "镜中琴音", "红尘不渡", 
        "庆舞良宵", "度人心", "凌云梯", "旧宴承欢", "寻猫记", 
        "劝学记", "白日梦", "舞众生", "惜往日", "韶华故", "故园风雨", 
        "平生心愿", "雪山恩仇", "乱世舞姬", "虎啸山林", "护佑苍生", 
        "天涯无归", "扶摇九天", "清风捕王", "炼狱厨神", "生死判", "茶馆奇缘", 
        "少年行", "黑白路"],
    "宠物": [
        "故人愿", "语不休", "风花雪", "义千金", "路投石", "觅知音", 
        "寓天涯", "解心语", "破巧言", "醉烟波", "乱红鸾", "夜哀鸣",
        "故岁辞", "重洋客", "子夜歌", "枉叹恨", "幽海牧", "鸠雀记", 
        "风雨意", "念旧林", "童蒙志", "捉贼记", "丹青记", "一枝栖",
        "尘网中", "白月皎", "话玄虚", "瀛洲梦", "莫贪杯", "露园事", 
        "江湖录", "缘来会·铃", "缘来会·瓜", "沧海笛", "谜书生", "滴水恩",
        "客江干", "秘宝图", "太行道", "归安志·志", "归安志·归", "归安志·安", 
        "烟花戏·风", "烟花戏·秋", "烟花戏·春", "烟花戏·月", "白雪忆", "戎马边",
        "一念间", "锻剑女", "儿女事", "烹调法", "锋芒展", "关外商", "东海客", 
        "北行镖", "滇南行", "青草歌", "稚子心", "兽王佩", "至尊宝", "竹马情", 
        "破晓鸣", "荆轲刺", "石敢当", "沙海谣", "孩童书", "捉妖记", "红衣歌", 
        "枫林酒", "归乡路", "胜负局", "清茗经"]

}