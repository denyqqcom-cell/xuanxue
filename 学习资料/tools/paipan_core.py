# -*- coding: utf-8 -*-
"""第八轮闭关·排盘核心引擎（只算可靠部分，天/门/神盘待下轮校验）
修正OG-06：日柱从8/7癸丑锚点程序推算，禁止硬编码。
今日：2026-08-12 申时（15:37）
"""
GAN="甲乙丙丁戊己庚辛壬癸"; ZHI="子丑寅卯辰巳午未申酉戌亥"

# ---------- 1. 日柱：从锚点推算 ----------
anchor_day, anchor_seq = 7, 50          # 8/7=癸丑=60甲子第50位
today = 12
day_seq = anchor_seq + (today - anchor_day)
day_gz = GAN[(day_seq-1)%10] + ZHI[(day_seq-1)%12]
print(f"【日柱】8/{today} = {day_gz}（60甲子序号{((day_seq-1)%60)+1}）← 程序推算，非硬编码")

# ---------- 2. 时辰：申时，五鼠遁 ----------
hour_zhi = "申"; hour_idx = ZHI.index(hour_zhi)
start = {"甲":0,"己":0,"乙":2,"庚":2,"丙":4,"辛":4,"丁":6,"壬":6,"戊":8,"癸":8}[day_gz[0]]
hour_gz = GAN[(start+hour_idx)%10] + hour_zhi
print(f"【时柱】{day_gz}日 {hour_zhi}时 = {hour_gz}时")

# ---------- 3. 局数：立秋日数分段 ----------
liqiu = 7
n = today - liqiu + 1
yuan = "上元" if n<=5 else ("中元" if n<=10 else "下元")
ju = {"上元":2,"中元":5,"下元":8}[yuan]
print(f"【局数】立秋第{n}天 → {yuan} → 阴遁{ju}局")

# ---------- 4. 时柱旬首 + 遁干 + 旬空 ----------
def seq_of(gz):
    for i in range(60):
        if GAN[i%10]+ZHI[i%12]==gz: return i
def xun_info(gz):
    s=seq_of(gz); base=(s//10)*10
    xs=GAN[base%10]+ZHI[base%12]
    dun={"甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"}[xs]
    kong=[ZHI[(base+10)%12], ZHI[(base+11)%12]]
    gan_order_in_xun=(s-base)  # 该干在旬内序（甲=0...癸=9）
    return xs,dun,kong,gan_order_in_xun
xs_h,dun_h,kong_h,ord_h = xun_info(hour_gz)
print(f"【时旬】{hour_gz}属{xs_h}旬，遁{dun_h}，旬空{''.join(kong_h)}，时干在旬内序={ord_h}")

# ---------- 5. 地盘：阴遁{ju}局，洛书逆飞 ----------
fly=[5,6,7,8,9,1,2,3,4]          # 洛书顺飞
fly_rev=fly[::-1]                 # 逆飞
yi_order="戊己庚辛壬癸丁丙乙"
earth={}
seq9 = fly_rev if ju==5 else None
# 阴遁逆飞：戊起局数宫，沿逆飞序排九仪
start_pos = fly.index(ju)
for k,yi in enumerate(yi_order):
    earth[ fly[(start_pos - k) % 9] ] = yi
print(f"【地盘】阴遁{ju}局逆飞九仪：")
for p in range(1,10):
    print(f"   {p}宫: {earth.get(p,'(中5)' if p==5 else '?')}", end="   ")
    if p%3==0: print()

# ---------- 6. 值符值使：时旬遁干落地盘宫 → 原驻星/门 ----------
star_home={1:"天蓬",2:"天芮",3:"天冲",4:"天辅",5:"天禽",6:"天心",7:"天柱",8:"天任",9:"天英"}
gate_home={1:"休门",2:"死门",3:"伤门",4:"杜门",6:"开门",7:"惊门",8:"生门",9:"景门"}
dun_palace = [p for p,yi in earth.items() if yi==dun_h][0]
zhifu = star_home[dun_palace]; zhishi = gate_home.get(dun_palace,"(寄)")
print(f"\n【值符值使】时旬{xs_h}遁{dun_h} → {dun_h}落地盘{dun_palace}宫 → 值符={zhifu}，值使={zhishi}")

# ---------- 7. 马星：日支驿马 ----------
ma_map={"寅":"申","午":"申","戌":"申","申":"寅","子":"寅","辰":"寅","巳":"亥","酉":"亥","丑":"亥","亥":"巳","卯":"巳","未":"巳"}
day_zhi=day_gz[1]; ma=ma_map[day_zhi]
zhi_palace={"子":1,"丑":8,"寅":8,"卯":3,"辰":4,"巳":4,"午":9,"未":2,"申":2,"酉":7,"戌":6,"亥":6}
print(f"【马星】日支{day_zhi}驿马={ma}，落{zhi_palace[ma]}宫")
print(f"【旬空落宫】{''.join(kong_h)} → 空亡落{zhi_palace.get(kong_h[0],'?')}、{zhi_palace.get(kong_h[1],'?')}宫")
print("\n注：天盘/门盘/神盘旋转规则待书本校验，本轮不输出，避免再引入OG-06式错误。")
