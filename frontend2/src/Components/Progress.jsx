import { useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import { masteryPercent, isReviewDue } from "./masteryUtils"
import { MASTERY, gradeColor, masteryJoke, splitChapterName, thumbUrl, unitStyle, videoPageUrl } from "./ui"

// Topics with the student's progress merged in: {topicId: {topic_id, topic_name, chapter_id, mastery_*...}}
export const useTopicsWithProgress = () => {
    const topics = useSelector((state) => state.topics)
    const topicProg = useSelector((state) => state.topicProg)
    const merged = {}
    Object.entries(topics).forEach(([id, t]) => { merged[id] = { ...t, topic_id: Number(id) } })
    Object.entries(topicProg).forEach(([id, p]) => { merged[id] = { ...(merged[id] || {}), ...p, topic_id: Number(id) } })
    return merged
}

// The student's study plan: units (in order) with their chapters (in order) and progress
export const useStudyPlan = () => {
    const units = useSelector((state) => state.units)
    const chapters = useSelector((state) => state.chapters)
    const userChapters = useSelector((state) => state.userChapters)
    const topics = useTopicsWithProgress()

    return Object.entries(units)
        .map(([unitId, unit]) => {
            const unitChapters = Object.entries(chapters)
                .filter(([, ch]) => ch.in_plan && String(ch.unit_id) === String(unitId))
                .map(([id, ch]) => ({
                    id: Number(id),
                    ...ch,
                    ...(userChapters[id] || {}),
                    topics: Object.values(topics).filter((t) => String(t.chapter_id) === String(id)),
                }))
                .sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
            return { id: Number(unitId), ...unit, chapters: unitChapters }
        })
        .sort((a, b) => (a.number ?? a.id) - (b.number ?? b.id))
}

// Half credit for the video, half for passing (60%+) the chapter quiz
const percentDone = (unit) => {
    if (!unit.chapters.length) return 0
    let done = 0
    unit.chapters.forEach((ch) => {
        if (ch.video_completed) done += 0.5
        if (ch.quiz_grade >= 60) done += 0.5
    })
    return Math.floor((done / unit.chapters.length) * 100)
}

const unitLevel = (unit) => {
    const tried = unit.chapters.flatMap((ch) => ch.topics).filter((t) => t.questions_asked > 0 || t.mastery_percent != null)
    if (!tried.length) return 'Not yet started'
    return masteryJoke(tried.reduce((sum, t) => sum + masteryPercent(t), 0) / tried.length)
}

const TopicRow = ({ topic }) => {
    const status = MASTERY[topic.mastery_status]
    const pct = topic.mastery_percent ?? (topic.questions_asked ? masteryPercent(topic) : null)
    if (!status || pct === null) {
        return (
            <li className="flex items-center gap-3">
                <span className="flex-1">{topic.topic_name}</span>
                <span className="text-xs text-gray-400">Not tried yet</span>
            </li>
        )
    }
    return (
        <li className="grid grid-cols-[minmax(0,1fr)_5rem_auto] sm:grid-cols-[minmax(0,1fr)_8rem_8.5rem] gap-3 items-center">
            <span>
                {topic.topic_name}
                {isReviewDue(topic) && <i className="fa-solid fa-rotate text-[#4CC2F5] text-xs ml-1.5" title="Due for a refresher"></i>}
            </span>
            <span className="h-2 rounded-full bg-[#344A53] overflow-hidden">
                <span className="block h-full rounded-full" style={{ width: `${pct}%`, background: status.color }}></span>
            </span>
            <span className="text-xs font-bold text-right" style={{ color: status.color }}>{pct}% · {status.label}</span>
        </li>
    )
}

const ChapterRow = ({ chapter, isNext }) => {
    const navigate = useNavigate()
    const hasGrade = chapter.quiz_grade !== null && chapter.quiz_grade !== undefined
    const [num, title] = splitChapterName(chapter.name)
    const thumb = thumbUrl(chapter, 'mqdefault')
    const tried = chapter.topics.filter((t) => t.mastery_status && t.mastery_status !== 'not_started')

    const takeQuiz = () => navigate('/quiz', { state: { chapter: chapter.id, type: 'chapterQuiz', topics: [] } })
    const quizFirst = chapter.video_completed && (!hasGrade || chapter.quiz_grade < 85)

    const quizButton = (
        <button type="button" onClick={takeQuiz}
            className={`${quizFirst ? 'btn-primary px-5 py-2' : 'btn-secondary px-5 py-1.5'} text-sm`}>
            <i className={`fa-solid fa-${hasGrade ? 'rotate-right' : 'pen-to-square'}`}></i> {hasGrade ? 'Retake the quiz' : 'Take the quiz'}
        </button>
    )
    const videoButton = (
        <a href={videoPageUrl(chapter)} className={`${chapter.video_completed ? 'btn-secondary px-5 py-1.5' : 'btn-primary px-5 py-2'} text-sm`}>
            <i className="fa-solid fa-play"></i> {chapter.video_completed ? 'Rewatch' : 'Watch the video'}
        </a>
    )

    return (
        <li>
            <details className="plain group" open={isNext}>
                <summary className="cursor-pointer py-2.5 grid grid-cols-[1rem_minmax(0,1fr)_auto_4rem] gap-3 items-center hover:bg-white/5 rounded-lg -mx-2 px-2">
                    <i className="chev fa-solid fa-chevron-right text-xs text-gray-400"></i>
                    <span className={isNext ? 'font-bold text-[#FFC93C]' : ''}>
                        {num} {title}
                        {isNext && <span className="ml-2 text-[10px] font-extrabold bg-[#FFC93C] text-[#111] rounded px-1.5 py-0.5 align-middle">UP NEXT</span>}
                    </span>
                    {chapter.video_completed
                        ? <i className="fa-solid fa-circle-check text-[#C6E83A]" title="Video watched"></i>
                        : <i className="fa-regular fa-circle text-gray-500" title="Not watched yet"></i>}
                    {hasGrade
                        ? <span className="text-center font-bold rounded-full text-[#111]" style={{ background: gradeColor(chapter.quiz_grade) }}>{chapter.quiz_grade}%</span>
                        : <span className="text-center text-xs text-gray-400">No quiz</span>}
                </summary>
                <div className="mt-1 mb-4 sm:ml-7 rounded-xl bg-[#344A53]/60 p-4 grid sm:grid-cols-[13rem_minmax(0,1fr)] gap-5">
                    <a href={videoPageUrl(chapter)} className="relative block rounded-lg overflow-hidden self-start group/thumb bg-black/30 aspect-video">
                        {thumb && <img src={thumb} alt="" loading="lazy" className="w-full aspect-video object-cover" />}
                        <span className="absolute inset-0 flex items-center justify-center group-hover/thumb:bg-black/40 transition">
                            <i className="fa-solid fa-circle-play text-4xl opacity-0 group-hover/thumb:opacity-100"></i>
                        </span>
                        {chapter.duration && <span className="absolute bottom-1.5 right-1.5 bg-black/80 text-xs px-1.5 rounded">{chapter.duration}</span>}
                    </a>
                    <div className="min-w-0">
                        <div className="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                            <span>Video: <b className={chapter.video_completed ? 'text-[#C6E83A]' : 'text-gray-300'}>{chapter.video_completed ? 'Watched' : 'Not watched yet'}</b></span>
                            <span>Chapter quiz: <b style={{ color: hasGrade ? gradeColor(chapter.quiz_grade) : '#d1d5db' }}>{hasGrade ? `${chapter.quiz_grade}%` : 'Not taken yet'}</b></span>
                        </div>
                        {chapter.topics.length > 0 && <>
                            <p className="mt-3 text-xs uppercase tracking-widest font-bold text-gray-400">Topic mastery</p>
                            <ul className="mt-2 space-y-2 text-sm">
                                {chapter.topics.map((t) => <TopicRow key={t.topic_id} topic={t} />)}
                            </ul>
                        </>}
                        <div className="mt-4 flex flex-wrap items-center gap-3">
                            {chapter.video_completed ? <>{quizButton}{videoButton}</> : <>{videoButton}{quizButton}</>}
                            {tried.length > 0 && (
                                <button type="button" className="text-sm font-bold text-[#7fd3e6] hover:underline"
                                    onClick={() => navigate('/quiz', { state: { chapter: 1, type: 'topicQuiz', topics: tried } })}>
                                    Practice these topics →
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </details>
        </li>
    )
}

// "Your study plan": one card per unit in its unit color; chapters expand to show details
export const Progress = () => {
    const navigate = useNavigate()
    const plan = useStudyPlan()
    const currentChapterId = useSelector((state) => state.user.currentChapter)

    return (
        <section>
            <div className="flex items-end justify-between gap-4">
                <h2 className="text-2xl sm:text-3xl font-bold">Your study plan</h2>
                <button type="button" className="text-[#7fd3e6] font-bold hover:underline text-sm whitespace-nowrap" onClick={() => navigate('/updateunits')}>
                    Update study plan →
                </button>
            </div>
            <div className="mt-4 space-y-4">
                {plan.map((unit) => {
                    const done = percentDone(unit)
                    const hasNext = unit.chapters.some((ch) => String(ch.id) === String(currentChapterId))
                    return (
                        <details key={unit.id} open={hasNext} className="plain panel rounded-2xl border-l-8 unit-border" style={unitStyle(unit)}>
                            <summary className="cursor-pointer p-5 flex flex-wrap items-center gap-x-4 gap-y-2">
                                <span className="text-xs font-extrabold px-2 py-0.5 rounded unit-bg whitespace-nowrap">UNIT {unit.number ?? unit.id}</span>
                                <span className="font-bold text-lg flex-1 min-w-[12rem]">{unit.title || unit.name}</span>
                                <span className="text-sm text-gray-300">Level: <b className="text-white">{unitLevel(unit)}</b></span>
                                <div className="w-full flex items-center gap-3">
                                    <div className="flex-1 h-3 rounded-full bg-[#344A53] overflow-hidden">
                                        <div className="h-full rounded-full unit-bg" style={{ width: `${done}%` }}></div>
                                    </div>
                                    <span className="text-sm font-bold w-24 text-right">{done}% done</span>
                                </div>
                            </summary>
                            <ul className="px-5 pb-4 divide-y divide-white/10 text-sm">
                                {unit.chapters.map((ch) => (
                                    <ChapterRow key={ch.id} chapter={ch} isNext={String(ch.id) === String(currentChapterId)} />
                                ))}
                            </ul>
                        </details>
                    )
                })}
            </div>
            <p className="mt-3 text-xs text-gray-400 flex flex-wrap gap-x-4 gap-y-1">
                <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#C6E83A] mr-1"></span>Mastered</span>
                <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#FFC93C] mr-1"></span>Getting there</span>
                <span><span className="inline-block w-2.5 h-2.5 rounded-full bg-[#FF8A3D] mr-1"></span>Needs work</span>
                <span><i className="fa-solid fa-rotate text-[#4CC2F5] mr-1"></i>Due for a refresher</span>
            </p>
        </section>
    )
}
