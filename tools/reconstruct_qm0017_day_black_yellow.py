#!/usr/bin/env python3
"""Reconstruct one explicitly bounded QM-SRC-0017 day-Qimen component.

Scope: the twelve 黑黄道 placement only, as stated on source pdf:p281.
This module intentionally does NOT reconstruct the full 日家奇门六十定局:
八门、九星、喜神、天乙贵人、截路空亡、五不遇时和吉凶断语 are out of scope.
"""

BRANCHES=tuple("子丑寅卯辰巳午未申酉戌亥")
ROAD_ORDER=(
    ("青龙","黄"),
    ("明堂","黄"),
    ("天刑","黑"),
    ("朱雀","黑"),
    ("金匮","黄"),
    ("天德","黄"),
    ("白虎","黑"),
    ("玉堂","黄"),
    ("天牢","黑"),
    ("玄武","黑"),
    ("司命","黄"),
    ("勾陈","黑"),
)
START_BRANCH_BY_DAY_BRANCH={
    "子":"申","午":"申",
    "卯":"寅","酉":"寅",
    "寅":"子","申":"子",
    "巳":"午","亥":"午",
    "辰":"辰","戌":"辰",
    "丑":"戌","未":"戌",
}

def reconstruct_black_yellow(day_branch):
    """Return hour-branch -> [road_name, black_or_yellow] in 子..亥 order."""
    if day_branch not in START_BRANCH_BY_DAY_BRANCH:
        raise ValueError(f"unsupported day branch: {day_branch!r}")
    start=START_BRANCH_BY_DAY_BRANCH[day_branch]
    start_idx=BRANCHES.index(start)
    by_hour={}
    for offset,(road,color) in enumerate(ROAD_ORDER):
        hour_branch=BRANCHES[(start_idx+offset)%len(BRANCHES)]
        by_hour[hour_branch]=[road,color]
    return {branch:by_hour[branch] for branch in BRANCHES}

if __name__=="__main__":
    import json,sys
    if len(sys.argv)!=2:
        raise SystemExit("usage: reconstruct_qm0017_day_black_yellow.py <day-branch>")
    print(json.dumps(reconstruct_black_yellow(sys.argv[1]),ensure_ascii=False,indent=2))
