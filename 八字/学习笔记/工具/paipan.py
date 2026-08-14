# 独立排盘工具 v2（自研）
# 日柱：儒略日 mod 60（六十甲子纪日连续不断，可靠）
# 节气：Meeus 低精度太阳视黄经算法（任意年份适用，精度约 ±0.01°≈15分钟，日级判断足够）
# 年柱以立春为界；月柱按节气（五虎遁）；时柱五鼠遁

import datetime
from math import sin, cos, radians

G = "甲乙丙丁戊己庚辛壬癸"
Z = "子丑寅卯辰巳午未申酉戌亥"

def jdn(y, m, d):
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12*a - 3
    return d + (153*m2+2)//5 + 365*y2 + y2//4 - y2//100 + y2//400 - 32045

def jdn_to_date(j):
    # 儒略日数转公历日期
    a = j + 32044
    b = (4*a + 3) // 146097
    c = a - (146097*b) // 4
    d2 = (4*c + 3) // 1461
    e = c - (1461*d2) // 4
    m2 = (5*e + 2) // 153
    day = e - (153*m2 + 2)//5 + 1
    month = m2 + 3 - 12*(m2//10)
    year = 100*b + d2 - 4800 + m2//10
    return datetime.date(year, month, day)

def gz(k):
    """k 为 0-59，返回干支"""
    return G[k % 10] + Z[k % 12]

def day_gz(y, m, d):
    return gz((jdn(y, m, d) + 49) % 60)

# ---------- 太阳视黄经（Meeus 低精度） ----------
def sun_lon(jd):
    T = (jd - 2451545.0) / 36525.0
    L0 = (280.46646 + 36000.76983*T + 0.0003032*T*T) % 360
    M = (357.52911 + 35999.05029*T - 0.0001537*T*T) % 360
    Mr = radians(M)
    C = (1.914602 - 0.004817*T - 0.000014*T*T)*sin(Mr) \
        + (0.019993 - 0.000101*T)*sin(2*Mr) + 0.000289*sin(3*Mr)
    true_lon = L0 + C
    omega = 125.04 - 1934.136*T
    return (true_lon - 0.00569 - 0.00478*sin(radians(omega))) % 360

def find_term_jd(y, lon_target):
    """求 y 年太阳到达黄经 lon_target 的儒略日"""
    # 以春分为锚：y 年春分约在 3 月 20 日
    jd_mar = jdn(y, 3, 20) + 0.5
    lon_mar = sun_lon(jd_mar)
    diff = (lon_target - lon_mar) % 360
    if diff > 280:
        # 目标节气在春分之前（小寒285~惊蛰345），锚点回退
        jd = jd_mar - (360 - diff) * 365.25 / 360.0
    else:
        jd = jd_mar + diff * 365.25 / 360.0
    # 牛顿迭代 5 次
    for _ in range(5):
        lo = sun_lon(jd)
        err = (lon_target - lo + 180) % 360 - 180
        jd += err * 365.25 / 360.0
    return jd

# 节气黄经表：名称 -> 黄经
TERM_LON = {
    "小寒":285,"大寒":300,"立春":315,"雨水":330,"惊蛰":345,"春分":0,
    "清明":15,"谷雨":30,"立夏":45,"小满":60,"芒种":75,"夏至":90,
    "小暑":105,"大暑":120,"立秋":135,"处暑":150,"白露":165,"秋分":180,
    "寒露":195,"霜降":210,"立冬":225,"小雪":240,"大雪":255,"冬至":270,
}

def term_date(y, name):
    """y 年某节气的日期（若节气属于跨年情形需调用方处理）"""
    jd = find_term_jd(y, TERM_LON[name])
    return jdn_to_date(int(jd + 0.5))

def lichun(y):
    return term_date(y, "立春")

def year_gz(y, m, d):
    yr = y if datetime.date(y, m, d) >= lichun(y) else y - 1
    return gz((yr - 4) % 60)

def month_gz(y, m, d):
    """月柱：以节气为界，立春起寅月；五虎遁推月干"""
    cur = datetime.date(y, m, d)
    # 十二节：(名称, 月支序号)
    jie = [("立春",2),("惊蛰",3),("清明",4),("立夏",5),("芒种",6),("小暑",7),
           ("立秋",8),("白露",9),("寒露",10),("立冬",11),("大雪",0),("小寒",1)]
    pts = []
    for name, zhi in jie:
        if name == "小寒":
            pts.append((term_date(y, name), zhi))
            pts.append((term_date(y+1, name), zhi))
        else:
            pts.append((term_date(y, name), zhi))
    pts.sort()
    zhi = pts[-1][1]
    for date_, z in pts:
        if cur < date_:
            break
        zhi = z
    yg = year_gz(y, m, d)[0]
    g_idx = G.index(yg)
    # 五虎遁：甲己丙寅首(2),乙庚戊寅(4),丙辛庚寅(6),丁壬壬寅(8),戊癸甲寅(0)
    start = [2, 4, 6, 8, 0][g_idx % 5]
    month_g = (start + (zhi - 2) % 12) % 10
    return G[month_g] + Z[zhi]

def hour_gz(day_gan, hour_zhi):
    start = [0, 2, 4, 6, 8][G.index(day_gan) % 5]  # 五鼠遁
    return G[(start + hour_zhi) % 10] + Z[hour_zhi]

def full_chart(y, m, d, hour_zhi=None):
    yg = year_gz(y, m, d)
    mg = month_gz(y, m, d)
    dg = day_gz(y, m, d)
    hg = hour_gz(dg[0], hour_zhi) if hour_zhi is not None else "?"
    return f"年:{yg} 月:{mg} 日:{dg} 时:{hg}"

if __name__ == "__main__":
    print("=== 节气自检 ===")
    for y in (1811, 1985, 2024):
        print(f"{y} 立春:", term_date(y, "立春"))
    print("2023 冬至:", term_date(2023, "冬至"))
    print()
    print("=== 独立排盘测试 ===")
    # 岳飞：1103-03-24 巳时(5)。书载：癸未 乙卯 甲子 己巳
    print("岳飞生 1103-03-24 巳时:", full_chart(1103, 3, 24, 5), "| 书载 癸未/乙卯/甲子/己巳")
    # 岳飞卒日：1142-01-27 书载癸巳日
    print("岳飞卒 1142-01-27 日柱:", day_gz(1142, 1, 27), "| 书载 癸巳")
    print("岳飞卒 1142-02-03 日柱:", day_gz(1142, 2, 3), "| 对照")
    # 曾国藩：1811-11-26 亥时(11)。书载：辛未 己亥 丙辰 己亥
    print("曾国藩生 1811-11-26 亥时:", full_chart(1811, 11, 26, 11), "| 书载 辛未/己亥/丙辰/己亥")
    # 自检：2000-01-01 应为 戊午日（万年历基准）
    print("自检 2000-01-01:", day_gz(2000, 1, 1), "| 万年历 戊午")
    # 自检：1949-10-01 应为 甲子日（历史基准）
    print("自检 1949-10-01:", day_gz(1949, 10, 1), "| 史载 甲子")
