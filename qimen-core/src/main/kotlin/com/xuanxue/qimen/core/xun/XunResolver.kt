package com.xuanxue.qimen.core.xun

import com.xuanxue.qimen.core.calendar.Branch
import com.xuanxue.qimen.core.calendar.Stem
import com.xuanxue.qimen.core.calendar.StemBranch

data class XunInfo(
    val xunShou: StemBranch,
    val dunYi: Stem,
    val xunKong: List<Branch>,
)

object XunResolver {
    private val dunYiByXun = listOf(Stem.WU, Stem.JI, Stem.GENG, Stem.XIN, Stem.REN, Stem.GUI)
    private val xunKongByXun = listOf(
        listOf(Branch.XU, Branch.HAI),
        listOf(Branch.SHEN, Branch.YOU),
        listOf(Branch.WU, Branch.WEI),
        listOf(Branch.CHEN, Branch.SI),
        listOf(Branch.YIN, Branch.MAO),
        listOf(Branch.ZI, Branch.CHOU),
    )

    fun resolve(hourPillar: StemBranch): XunInfo {
        val index = StemBranch.sexagenaryIndexOf(hourPillar.stem, hourPillar.branch)
        val xun = index / 10
        return XunInfo(
            xunShou = StemBranch.fromSexagenaryIndex(xun * 10),
            dunYi = dunYiByXun[xun],
            xunKong = xunKongByXun[xun],
        )
    }
}
