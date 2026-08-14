# -*- coding: utf-8 -*-
"""严谨核验：从8/7=癸丑日推算8/8-8/13日干支，并核验各时辰干支与三元定局"""
GAN="甲乙丙丁戊己庚辛壬癸"; ZHI="子丑寅卯辰巳午未申酉戌亥"

# 8/7 = 癸丑日（知识库9.1已确认）
idx_0807 = GAN.index("癸")*1  # 干支序号
gz_0807 = 10*0 + GAN.index("癸")  # 用60甲子序号：癸丑 = 第50位（甲子=1...）
# 直接算：癸丑在六十甲子中序号 = 50（甲子1,乙丑2,...癸酉10,甲戌11...癸未20...癸巳30...癸卯40...癸丑50）
day_seq = {d: 50 + (d-7) for d in range(7, 14)}  # 8/7=50

def gz_of(seq):
    s = (seq - 1) % 60
    return GAN[s % 10] + ZHI[s % 12]

print("=== 日干支核验（8/7=癸丑=50号）===")
for d in range(8, 14):
    print(f"8/{d}: {gz_of(day_seq[d])}（60甲子序号{((day_seq[d]-1)%60)+1}）")

print("\n=== 立秋三元核验（立秋8/7，日数分段法，每元约5天）===")
liqiu_start = 7
for d in range(8, 14):
    n = d - liqiu_start + 1
    yuan = "上元" if n <= 5 else ("中元" if n <= 10 else "下元")
    ju = {("阴遁","上元"):2,("阴遁","中元"):5,("阴遁","下元"):8}[("阴遁",yuan)]
    print(f"8/{d}: 立秋第{n}天 → {yuan} → 阴遁{ju}局")

print("\n=== 时辰干支核验 ===")
# 五鼠遁：甲己日起甲子时，乙庚日起丙子时，丙辛日起戊子时，丁壬日起庚子时，戊癸日起壬子时
def hour_gz(day_gan, hour_zhi_idx):
    start = {"甲":0,"己":0,"乙":2,"庚":2,"丙":4,"辛":4,"丁":6,"壬":6,"戊":8,"癸":8}[day_gan]
    return GAN[(start + hour_zhi_idx) % 10] + ZHI[hour_zhi_idx]

checks = [
    (8, "申", "第五轮8/8酉时局应=乙卯日乙酉时"),
    (11, "申", "第六轮8/11记录为丙辰日丙申时，核验实际"),
    (12, "申", "今日8/12申时（前瞻8/13起局用）"),
]
for d, hz, note in checks:
    dgz = gz_of(day_seq[d])
    hgz = hour_gz(dgz[0], ZHI.index(hz))
    print(f"8/{d} {dgz}日 {hz}时 = {hgz}时  （{note}）")

print("\n=== 旬首核验 ===")
def xunshou(gz):
    s = None
    for i in range(60):
        if GAN[i%10]+ZHI[i%12] == gz:
            s = i
            break
    base = (s // 10) * 10
    xs = GAN[base%10] + ZHI[base%12]
    dun = {"甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"}[xs]
    kong = [ZHI[(base+10)%12], ZHI[(base+11)%12]]
    return xs, dun, kong

for d in [11, 12, 13]:
    dgz = gz_of(day_seq[d])
    xs, dun, kong = xunshou(dgz)
    print(f"8/{d} {dgz}日 → 旬首{xs}遁{dun}，旬空{''.join(kong)}")
