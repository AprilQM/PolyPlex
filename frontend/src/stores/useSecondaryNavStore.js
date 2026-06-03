import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useSecondaryNavStore = defineStore('secondaryNav', () => {
    const _width = ref(280);
    const width = ref(280);
    const _content = ref({})
    const content = ref({})
    const _x = ref("0")

    const switchNew = () => {
        // 退出动画
        _x.value = "-100%"

        // 修改_content并加入动画
        setTimeout(() => {
            _content.value = content.value
            _width.value = width.value
            _x.value = "0"
        }, 300)
    }

    // 单纯激活某个按钮
    const activateBtn = (partIndex, btnIndex) => {
        const btn = _content.value[partIndex]?.content?.[btnIndex]
        if (!btn) return
        btn.active = true
    }

    // 单纯关闭某个按钮
    const deactivateBtn = (partIndex, btnIndex) => {
        const btn = _content.value[partIndex]?.content?.[btnIndex]
        if (!btn) return
        btn.active = false
    }

    // 在某个分组内切换（同组其他按钮全部取消激活）
    const switchInPart = (partIndex, btnIndex) => {
        const part = _content.value[partIndex]
        if (!part) return
        const btns = part.content
        if (!btns || !btns[btnIndex]) return
        btns.forEach(btn => { btn.active = false })
        btns[btnIndex].active = true
    }

    // 全局切换（所有按钮取消激活，只激活目标）
    const switchGlobal = (partIndex, btnIndex) => {
        const parts = _content.value
        if (!Array.isArray(parts)) return
        const target = parts[partIndex]?.content?.[btnIndex]
        if (!target) return
        for (const part of parts) {
            if (!part.content) continue
            for (const btn of part.content) {
                btn.active = false
            }
        }
        target.active = true
    }

    return {
        _width,
        width,
        _content,
        content,
        _x,
        switchNew,
        activateBtn,
        deactivateBtn,
        switchInPart,
        switchGlobal
     }
})
