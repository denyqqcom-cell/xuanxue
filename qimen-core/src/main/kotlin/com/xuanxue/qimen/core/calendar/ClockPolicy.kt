package com.xuanxue.qimen.core.calendar

import java.time.LocalTime

data class ClockSlot(
    val hourBranch: Branch,
    val slotLabel: String,
    val rollNextDay: Boolean,
)

object ClockPolicy {
    /**
     * Household 13-slot convention from the handoff:
     * 00:xx = 早子, 23:xx = 晚子; all middle branches are ordinary two-hour slots.
     */
    fun resolve(time: LocalTime, lateZiRollsToNextDay: Boolean = true): ClockSlot {
        val hour = time.hour
        val branchIndex = when (hour) {
            0, 23 -> 0
            else -> (hour + 1) / 2
        }
        val branch = Branch.entries[branchIndex % 12]
        val label = when (hour) {
            0 -> "早子"
            23 -> "晚子"
            else -> branch.symbol
        }
        return ClockSlot(
            hourBranch = branch,
            slotLabel = label,
            rollNextDay = hour == 23 && lateZiRollsToNextDay,
        )
    }
}
