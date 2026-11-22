import { useDispatch, useSelector } from "react-redux"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getAllTopics } from "../Slices/topicsActions"
import { masteryPercent, isReviewDue } from "./masteryUtils"
import { useStudyPlan } from "./Progress"
import { MASTERY, masteryJoke, unitStyle } from "./ui"

const MAX_TOPICS = 9
// The server asks 3 questions per topic (6 when there's only one): backend/quiz.py

// Same picks as the server's weak-spot quiz (backend/mastery.py pick_review_topics):
// weakest not-yet-mastered topics, keeping a slot for a mastered topic that's due for a refresher
const previewGauntlet = (topics, limit = 4) => {
    const tried = topics.filter((t) => t.mastery_status && t.mastery_status !== 'not_started')
    const weak = tried.filter((t) => t.mastery_status !== 'mastered').sort((a, b) => masteryPercent(a) - masteryPercent(b))
    const due = tried.filter((t) => t.mastery_status === 'mastered' && t.review_due)
    const picks = weak.slice(0, limit)
    if (due.length && picks.length === limit) picks[limit - 1] = due[0]
    due.forEach((t) => { if (picks.length < limit && !picks.includes(t)) picks.push(t) })
    return picks
}

export const QuizGenerator = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const plan = useStudyPlan()
    const [selected, setSelected] = useState({})   // {topicId: true}

    useEffect(() => {
        dispatch(getAllTopics())
        window.scrollTo(0, 0)
    }, [dispatch])

    const allTopics = plan.flatMap((u) => u.chapters.flatMap((ch) => ch.topics.map((t) => ({ ...t, watched: !!ch.video_completed }))))
    const byId = Object.fromEntries(allTopics.map((t) => [String(t.topic_id), t]))
    const pickedIds = Object.keys(selected).filter((id) => selected[id])
    const count = pickedIds.length
    const gauntlet = previewGauntlet(allTopics)

    const toggle = (id) => setSelected((prev) => ({ ...prev, [id]: !prev[id] }))
    const selectWhere = (test) => setSelected(Object.fromEntries(allTopics.filter(test).map((t) => [String(t.topic_id), true])))
    const toggleUnit = (unit) => {
        const ids = unit.chapters.flatMap((ch) => ch.topics.map((t) => String(t.topic_id)))
        const allOn = ids.every((id) => selected[id])
        setSelected((prev) => ({ ...prev, ...Object.fromEntries(ids.map((id) => [id, !allOn])) }))
    }

    const makeQuiz = () => {
        if (!count || count > MAX_TOPICS) return
        const topics = pickedIds.map((id) => ({ ...byId[id], topic_id: Number(id) }))
        navigate('/quiz', { state: { chapter: 1, type: 'topicQuiz', topics } })
    }

    return (
        <div className="pt-24 sm:pt-28 pb-40 px-5 sm:px-10 lg:px-16">
            <div className="max-w-5xl mx-auto">
                <section>
                    <p className="uppercase tracking-widest text-sm font-bold text-[#7fd3e6]">Quiz generator</p>
                    <h1 className="mt-1 text-3xl sm:text-5xl font-extrabold">Build a review quiz</h1>
                    <p className="mt-3 text-lg text-gray-200 max-w-3xl">
                        Your very own "weakness whacker" (patent pending). Let us aim it at your weak spots, or go off-script and pick
                        the topics yourself. Almost painless. Less like pulling teeth, more like a slightly awkward lecture on interest rates.
                    </p>
                </section>

                <section className="mt-8 panel rounded-3xl p-6 sm:p-8 border-t-8 border-[#FF8A3D] grid md:grid-cols-[minmax(0,1fr)_auto] gap-6 items-center">
                    <div>
                        <h2 className="text-2xl sm:text-3xl font-extrabold"><i className="fa-solid fa-crosshairs text-[#FF8A3D] mr-2"></i>The Gauntlet: take on your weaknesses</h2>
                        {gauntlet.length ? <>
                            <p className="mt-2 text-gray-200">We'll pick up to 4 topics and about 12 questions. Right now that means:</p>
                            <ul className="mt-3 flex flex-wrap gap-2 text-sm font-semibold">
                                {gauntlet.map((t) => isReviewDue(t)
                                    ? <li key={t.topic_id} className="rounded-full bg-[#4CC2F5]/20 text-[#8fdcff] px-3 py-1"><i className="fa-solid fa-rotate mr-1"></i>{t.topic_name} · refresher</li>
                                    : <li key={t.topic_id} className="rounded-full bg-[#FF8A3D]/20 text-[#FFB27F] px-3 py-1">{t.topic_name} · {masteryPercent(t)}%</li>)}
                            </ul>
                        </> : (
                            <p className="mt-2 text-gray-200">Take a few chapter quizzes first, so we know where your weak spots are. Then come back and face them.</p>
                        )}
                    </div>
                    <button type="button" className="btn-primary px-7 py-3 text-lg"
                        onClick={() => navigate('/quiz', { state: { chapter: 1, type: 'shortWeakspotQuiz', topics: [] } })}>
                        <i className="fa-solid fa-bolt"></i> Find my Achilles' heel
                    </button>
                </section>

                <div className="my-10 flex items-center gap-4 text-gray-400 font-bold"><span className="flex-1 h-px bg-white/15"></span>OR<span className="flex-1 h-px bg-white/15"></span></div>

                <section>
                    <h2 className="text-2xl sm:text-3xl font-extrabold"><i className="fa-solid fa-dice text-[#B89AFF] mr-2"></i>Choose your own adventure</h2>
                    <p className="mt-1 text-gray-300">Pick up to {MAX_TOPICS} topics. Rocked them or flopped them, your call.</p>
                    <div className="mt-4 flex flex-wrap gap-2 text-sm">
                        <button type="button" className="rounded-full panel px-4 py-1.5 font-semibold hover:bg-[#23333a]" onClick={() => selectWhere((t) => t.mastery_status === 'needs_work')}>Select all that need work</button>
                        <button type="button" className="rounded-full panel px-4 py-1.5 font-semibold hover:bg-[#23333a]" onClick={() => selectWhere((t) => isReviewDue(t))}>Select refreshers due</button>
                        <button type="button" className="rounded-full px-4 py-1.5 font-semibold text-gray-300 hover:text-white" onClick={() => setSelected({})}>Clear</button>
                    </div>

                    <div className="mt-5 space-y-4">
                        {plan.map((unit, i) => (
                            <details key={unit.id} open={i < 2} className="plain panel rounded-2xl border-l-8 unit-border" style={unitStyle(unit)}>
                                <summary className="cursor-pointer p-4 sm:p-5 flex flex-wrap items-center gap-x-3 gap-y-1">
                                    <i className="chev fa-solid fa-chevron-right text-xs text-gray-400"></i>
                                    <span className="text-xs font-extrabold px-2 py-0.5 rounded unit-bg whitespace-nowrap">UNIT {unit.number ?? unit.id}</span>
                                    <span className="font-bold text-lg flex-1 min-w-[10rem]">{unit.title || unit.name}</span>
                                    <button type="button" className="text-sm font-bold text-[#7fd3e6] hover:underline whitespace-nowrap"
                                        onClick={(e) => { e.preventDefault(); toggleUnit(unit) }}>Select whole unit</button>
                                </summary>
                                <div className="px-3 sm:px-5 pb-5 grid sm:grid-cols-2 gap-2">
                                    {unit.chapters.flatMap((ch) => ch.topics).map((t) => {
                                        const id = String(t.topic_id)
                                        const on = !!selected[id]
                                        const watched = byId[id]?.watched
                                        const status = MASTERY[t.mastery_status]
                                        const pct = status ? masteryPercent(t) : null
                                        return (
                                            <label key={id} className="cursor-pointer">
                                                <input type="checkbox" className="sr-only" checked={on} onChange={() => toggle(id)} />
                                                <span className={`flex items-center gap-3 rounded-xl border-2 px-3 py-2.5 h-full transition ${on ? 'border-[#FFC93C] bg-[#FFC93C]/10' : 'border-white/10 hover:border-white/30'}`}>
                                                    <span className={`w-5 h-5 shrink-0 rounded-md border-2 flex items-center justify-center text-[11px] ${on ? 'bg-[#FFC93C] border-[#FFC93C] text-[#111]' : 'border-white/50'}`}>
                                                        {on && <i className="fa-solid fa-check"></i>}
                                                    </span>
                                                    <span className="flex-1 min-w-0">
                                                        <span className={`block text-sm font-semibold ${watched ? '' : 'text-gray-400'}`}>
                                                            {t.topic_name}
                                                            {!watched && <i className="fa-regular fa-eye-slash text-xs ml-1.5" title="Video not watched yet"></i>}
                                                            {isReviewDue(t) && <i className="fa-solid fa-rotate text-[#4CC2F5] text-xs ml-1.5" title="Time for a refresher"></i>}
                                                        </span>
                                                        <span className="mt-1 flex items-center gap-2">
                                                            <span className="flex-1 h-1.5 rounded-full bg-[#344A53] overflow-hidden">
                                                                <span className="block h-full rounded-full" style={{ width: `${pct || 0}%`, background: status?.color || 'transparent' }}></span>
                                                            </span>
                                                            <span className={`text-[11px] w-44 text-right ${pct === null ? 'text-gray-500' : 'font-bold'}`} style={status ? { color: status.color } : {}}>
                                                                {pct === null ? 'Not yet started' : `${pct}% · ${masteryJoke(pct)}`}
                                                            </span>
                                                        </span>
                                                    </span>
                                                </span>
                                            </label>
                                        )
                                    })}
                                </div>
                            </details>
                        ))}
                    </div>
                    <p className="mt-3 text-xs text-gray-400 flex flex-wrap gap-x-4 gap-y-1">
                        <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#C6E83A] mr-1"></span>Mastered</span>
                        <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#FFC93C] mr-1"></span>Getting there</span>
                        <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#FF8A3D] mr-1"></span>Needs work</span>
                        <span><i className="fa-regular fa-eye-slash mr-1"></i>Video not watched yet</span>
                    </p>
                </section>
            </div>

            {/* Sticky bar: how many topics are picked, and the button to build the quiz */}
            <div className="fixed bottom-4 left-1/2 -translate-x-1/2 w-[calc(100%-2rem)] max-w-3xl z-40 bg-[#1f2f36] border border-white/15 rounded-2xl shadow-2xl px-5 py-3 flex items-center gap-4">
                <div className="flex-1 min-w-0">
                    <p className="font-bold">{count} of {MAX_TOPICS} topics picked</p>
                    <p className={`text-xs truncate ${count > MAX_TOPICS ? 'text-[#FF6FAE] font-bold' : 'text-gray-400'}`}>
                        {count > MAX_TOPICS ? `Rein it in dude! ${MAX_TOPICS} topics max.` : count ? `About ${count === 1 ? 6 : count * 3} questions` : 'Pick at least one topic'}
                    </p>
                </div>
                <button type="button" className="btn-primary px-6 py-2.5 whitespace-nowrap" disabled={!count || count > MAX_TOPICS} onClick={makeQuiz}>
                    Create my quiz <i className="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </div>
    )
}
