import { useEffect, useState } from "react"
import { getUnitsAndChapters } from "../Slices/unitsActions"
import { splitChapterName, unitStyle } from "./ui"

/**
 * Study plan picker (Get Started and Update Study Plan): every unit in its color, with its chapters.
 * `initial` is {chapterId: true} for chapters already in the plan; onSubmit gets the same shape.
 */
export const PlanPicker = ({ initial = {}, onSubmit, submitLabel, secondary }) => {
    const [data, setData] = useState(null)
    const [selected, setSelected] = useState(initial)
    const [saving, setSaving] = useState(false)

    useEffect(() => {
        const load = async () => {
            try {
                const response = await getUnitsAndChapters()
                setData(await response.json())
            } catch (error) {
                console.error('Error fetching units and chapters:', error)
            }
        }
        load()
    }, [])

    // Plan loads after first render on a page refresh: take it once it arrives
    const initialKey = Object.keys(initial).sort().join(',')
    useEffect(() => { setSelected(initial) }, [initialKey]) // eslint-disable-line react-hooks/exhaustive-deps

    if (!data) return <p className="text-gray-300">Loading units…</p>

    const chapters = Object.entries(data.chapters).map(([id, ch]) => ({ id, ...ch }))
    const units = Object.entries(data.units).map(([id, u]) => ({ id, ...u }))
        .sort((a, b) => (a.number ?? a.id) - (b.number ?? b.id))
    const subjects = Object.entries(data.subjects).map(([id, s]) => ({ id, ...s }))
    const unitChapters = (unitId) => chapters.filter((ch) => String(ch.unit_id) === String(unitId)).sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
    const count = Object.values(selected).filter(Boolean).length

    const toggleChapter = (id) => setSelected((prev) => ({ ...prev, [id]: !prev[id] }))
    const toggleUnit = (unitId) => {
        const ids = unitChapters(unitId).map((ch) => ch.id)
        const allOn = ids.every((id) => selected[id])
        setSelected((prev) => ({ ...prev, ...Object.fromEntries(ids.map((id) => [id, !allOn])) }))
    }

    const submit = async () => {
        setSaving(true)
        try { await onSubmit(selected) } finally { setSaving(false) }
    }

    return (
        <div>
            {subjects.map((subject) => {
                const subjectUnits = units.filter((u) => String(u.subject_id) === String(subject.id))
                if (!subjectUnits.length) return null
                return (
                    <section key={subject.id} className="mb-8">
                        <h2 className="text-sm uppercase tracking-widest font-bold text-gray-300">{subject.name}</h2>
                        <div className="mt-3 space-y-3">
                            {subjectUnits.map((unit) => {
                                const list = unitChapters(unit.id)
                                const picked = list.filter((ch) => selected[ch.id]).length
                                if (!list.length) {
                                    return (
                                        <div key={unit.id} className="flex items-center gap-3 rounded-2xl bg-[#2B3D45]/50 px-5 py-3 opacity-60" style={unitStyle(unit)}>
                                            <span className="text-xs font-extrabold px-2 py-0.5 rounded unit-bg whitespace-nowrap">UNIT {unit.number}</span>
                                            <span className="font-semibold flex-1">{unit.title || unit.name}</span>
                                            <span className="text-xs">coming soon</span>
                                        </div>
                                    )
                                }
                                return (
                                    <details key={unit.id} className="plain panel rounded-2xl border-l-8 unit-border" style={unitStyle(unit)} open={picked > 0}>
                                        <summary className="cursor-pointer px-5 py-4 flex flex-wrap items-center gap-3">
                                            <i className="chev fa-solid fa-chevron-right text-xs text-gray-400"></i>
                                            <span className="text-xs font-extrabold px-2 py-0.5 rounded unit-bg whitespace-nowrap">UNIT {unit.number}</span>
                                            <span className="font-bold text-lg flex-1 min-w-[10rem]">{unit.title || unit.name}</span>
                                            <span className="text-sm text-gray-300">{picked} of {list.length}</span>
                                            <button type="button" className="text-sm font-bold text-[#7fd3e6] hover:underline"
                                                onClick={(e) => { e.preventDefault(); toggleUnit(unit.id) }}>
                                                {picked === list.length ? 'Remove unit' : 'Add whole unit'}
                                            </button>
                                        </summary>
                                        <div className="px-4 sm:px-5 pb-4 grid sm:grid-cols-2 gap-2">
                                            {list.map((ch) => {
                                                const on = !!selected[ch.id]
                                                const [num, title] = splitChapterName(ch.name)
                                                return (
                                                    <label key={ch.id} className="cursor-pointer">
                                                        <input type="checkbox" className="sr-only" checked={on} onChange={() => toggleChapter(ch.id)} />
                                                        <span className={`flex items-center gap-3 rounded-xl border-2 px-3 py-2 h-full text-sm transition ${on ? 'border-[#FFC93C] bg-[#FFC93C]/10' : 'border-white/10 hover:border-white/30'}`}>
                                                            <span className={`w-5 h-5 shrink-0 rounded-md border-2 flex items-center justify-center text-[11px] ${on ? 'bg-[#FFC93C] border-[#FFC93C] text-[#111]' : 'border-white/50'}`}>
                                                                {on && <i className="fa-solid fa-check"></i>}
                                                            </span>
                                                            <span><span className="text-gray-400 mr-1">{num}</span>{title}</span>
                                                        </span>
                                                    </label>
                                                )
                                            })}
                                        </div>
                                    </details>
                                )
                            })}
                        </div>
                    </section>
                )
            })}

            <div className="sticky bottom-4 z-30 bg-[#1f2f36] border border-white/15 rounded-2xl shadow-2xl px-5 py-3 flex flex-wrap items-center gap-4">
                <p className="flex-1 font-bold">{count} chapter{count === 1 ? '' : 's'} in your plan</p>
                {secondary}
                <button type="button" className="btn-primary px-6 py-2.5" disabled={!count || saving} onClick={submit}>
                    {saving ? 'Saving…' : submitLabel}
                </button>
            </div>
        </div>
    )
}
