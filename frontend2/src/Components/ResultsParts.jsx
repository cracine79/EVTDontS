import { useSelector } from "react-redux"
import { MASTERY, gradeColor, unitStyle } from "./ui"
import { masteryPercent, isReviewDue } from "./masteryUtils"

// Score from a results object: {anything: {isCorrect, ...}}
export const scoreOf = (results) => {
    const list = Object.values(results || {})
    const correct = list.filter((r) => r.isCorrect === true).length
    return { correct, total: list.length, percent: list.length ? Math.floor((correct / list.length) * 100) : 0 }
}

// Big score card with a ring: used by every results page
export const ScoreCard = ({ unit, eyebrow, title, score, children }) => {
    const color = gradeColor(score.percent)
    return (
        <section className="panel rounded-3xl p-6 sm:p-10 border-t-8 unit-border grid sm:grid-cols-[auto_minmax(0,1fr)] gap-8 items-center" style={unitStyle(unit)}>
            <div className="relative w-40 h-40 mx-auto" role="img" aria-label={`Score ${score.percent} percent`}>
                <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90">
                    <circle cx="18" cy="18" r="15.9" fill="none" stroke="#344A53" strokeWidth="3.2" />
                    <circle cx="18" cy="18" r="15.9" fill="none" stroke={color} strokeWidth="3.2" strokeLinecap="round"
                        strokeDasharray={`${score.percent} 100`} />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-black">{score.percent}%</span>
                    <span className="text-sm text-gray-300">{score.correct} of {score.total} right</span>
                </div>
            </div>
            <div>
                <p className="text-sm font-bold uppercase tracking-widest unit-text">{eyebrow}</p>
                <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold leading-tight">{title}</h1>
                <div className="mt-3 text-lg text-gray-200 space-y-2">{children}</div>
            </div>
        </section>
    )
}

// "How this moved your topics": mastery bars for the quiz's topics, after the quiz
export const TopicMovement = ({ topicIds, describe }) => {
    const topicProg = useSelector((state) => state.topicProg)
    const topics = useSelector((state) => state.topics)
    const rows = [...new Set(topicIds.map(String))].map((id) => ({ ...(topics[id] || {}), ...(topicProg[id] || {}), topic_id: id }))
    if (!rows.length) return null
    return (
        <section className="mt-10">
            <h2 className="text-2xl font-bold">How this moved your topics</h2>
            <ul className="mt-4 panel rounded-2xl p-5 space-y-4 text-sm">
                {rows.map((t) => {
                    const status = MASTERY[t.mastery_status]
                    const pct = t.mastery_percent ?? masteryPercent(t)
                    return (
                        <li key={t.topic_id}>
                            <div className="grid grid-cols-[minmax(0,1fr)_6rem_auto] sm:grid-cols-[minmax(0,1fr)_10rem_9rem] gap-3 items-center">
                                <span className="font-semibold">
                                    {t.topic_name}
                                    {isReviewDue(t) && <i className="fa-solid fa-rotate text-[#4CC2F5] text-xs ml-1.5" title="Due for a refresher"></i>}
                                </span>
                                <span className="h-2 rounded-full bg-[#344A53] overflow-hidden">
                                    <span className="block h-full rounded-full" style={{ width: `${pct}%`, background: status?.color || '#9ca3af' }}></span>
                                </span>
                                <span className="text-right text-xs font-bold" style={{ color: status?.color || '#9ca3af' }}>
                                    {pct}% · {status?.label || 'Not enough data'}
                                </span>
                            </div>
                            {describe && <p className="mt-1 text-xs text-gray-300">{describe(t, pct)}</p>}
                        </li>
                    )
                })}
            </ul>
        </section>
    )
}

// "Show me what I missed": each missed question with the student's answer and the right one
export const MissedQuestions = ({ results }) => {
    const questions = useSelector((state) => state.questions)
    const list = Object.values(results || {})
    const missed = list.filter((r) => r.isCorrect === false && questions[r.questionId])
    const right = list.filter((r) => r.isCorrect === true && questions[r.questionId])

    const QuestionBody = ({ result, showYours }) => {
        const q = questions[result.questionId]
        const answers = Object.entries(q.answers || {})
        const yours = answers.find(([id]) => String(id) === String(result.answerId))?.[1]
        const correct = answers.find(([, a]) => a.is_correct)?.[1]
        return (
            <div className="px-5 pb-5 sm:ml-6 space-y-2 text-sm">
                {q.image_url && <figure className="bg-white rounded-xl p-3 max-w-sm mb-3"><img src={q.image_url} alt="" className="w-full" /></figure>}
                {showYours && yours && (
                    <p className="rounded-xl bg-[#FF6FAE]/15 border border-[#FF6FAE]/50 px-4 py-2">
                        <i className="fa-solid fa-xmark text-[#FF6FAE] mr-2"></i><b>Your answer:</b> {yours.text}
                    </p>
                )}
                {correct && (
                    <p className="rounded-xl bg-[#C6E83A]/15 border border-[#C6E83A]/50 px-4 py-2">
                        <i className="fa-solid fa-check text-[#C6E83A] mr-2"></i><b>Correct answer:</b> {correct.text}
                    </p>
                )}
            </div>
        )
    }

    return (
        <section className="mt-10">
            <h2 className="text-2xl font-bold">Show me what I missed</h2>
            <div className="mt-4 space-y-3">
                {missed.length === 0 && (
                    <p className="panel rounded-2xl p-5 border-l-8 border-[#C6E83A]">
                        You got 100%. Get out of here before we make you write the EVTDS textbook.
                    </p>
                )}
                {missed.map((r, i) => (
                    <details key={r.questionId} open={i === 0} className="plain panel rounded-2xl border-l-8 border-[#FF6FAE]">
                        <summary className="cursor-pointer p-5 flex gap-3 items-start">
                            <i className="chev fa-solid fa-chevron-right text-xs text-gray-400 mt-1.5"></i>
                            <span className="flex-1">
                                <span className="text-xs font-bold text-[#FF6FAE] uppercase tracking-wider">Missed</span><br />
                                <span className="font-semibold">{questions[r.questionId].text.replaceAll('<br>', ' ')}</span>
                            </span>
                        </summary>
                        <QuestionBody result={r} showYours />
                    </details>
                ))}
                {right.length > 0 && (
                    <details className="plain bg-[#2B3D45]/60 rounded-2xl border-l-8 border-[#C6E83A]">
                        <summary className="cursor-pointer p-5 flex gap-3 items-center text-sm text-gray-300">
                            <i className="chev fa-solid fa-chevron-right text-xs"></i>
                            <span className="flex-1"><i className="fa-solid fa-check text-[#C6E83A] mr-2"></i>{right.length} question{right.length === 1 ? '' : 's'} you got right</span>
                        </summary>
                        <ul className="px-5 pb-5 sm:ml-6 space-y-2 text-sm">
                            {right.map((r) => (
                                <li key={r.questionId} className="flex gap-2">
                                    <i className="fa-solid fa-check text-[#C6E83A] mt-1"></i>
                                    <span>{questions[r.questionId].text.replaceAll('<br>', ' ')}</span>
                                </li>
                            ))}
                        </ul>
                    </details>
                )}
            </div>
        </section>
    )
}
