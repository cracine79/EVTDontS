import { useDispatch, useSelector } from "react-redux"
import { useNavigate, useLocation } from "react-router-dom"
import { useEffect, useMemo } from "react"
import { Progress, useStudyPlan, useTopicsWithProgress } from "./Progress"
import { Tutorial } from "./Tutorial"
import { getAllTopics } from "../Slices/topicsActions"
import { gradeColor, splitChapterName, thumbUrl, unitStyle, videoPageUrl } from "./ui"

const MESSAGES = [
    "Glad to see you're back. We were starting to think you'd mastered economics overnight.",
    "Already back for more? Guess Netflix isn't cutting it today.",
    "Here again? We knew you couldn't resist the allure of more charts and graphs.",
    "We're starting to think you actually enjoy this sh... this stuff.",
    "Back for more? We promise not to make this TOO interesting.",
    "We've got to stop meeting like this!",
    "We've never felt so loved before. Except the time our Mom subscribed to our YouTube channel.",
    "You like us! You really like us!",
    "Ah, back for another dose of economic enlightenment? Let the knowledge binge begin!",
    "Look who couldn’t resist the pull of marginal utility. Welcome back to the grind!",
    "Back so soon? It’s almost like economics is… fun? Nah, couldn’t be.",
    "Well, well, well… someone’s got a thirst for economic knowledge! Or is it just a slow day?",
    "Returning already? Looks like you’re about to be the life of the next cocktail party with your newfound econ insights.",
    "Ah, you’re back! Just when we thought you’d solved the economy overnight.",
    "Miss us? It’s okay, economic graphs and theories have that effect on people. Probably.",
    "Guessing you’re back to dive into some high-octane econ thrills. Okay, maybe medium-octane. Fine, some-octane?",
    "Welcome back! Clearly, the invisible hand brought you here… or maybe it was your browser history.",
    "Let's rock and roll!",
]

// What to say about the up-next chapter's last quiz score
const scoreQuip = (grade) => {
    if (grade >= 85) return "Already crushing it. Go again for bragging rights, or move on."
    if (grade >= 60) return "Solid. One more run and it's yours."
    return "Everyone bombs this one the first time. Okay, maybe not everyone."
}

const UpNext = ({ chapter, unit }) => {
    const navigate = useNavigate()
    if (!chapter) return null
    const hasGrade = chapter.quiz_grade !== null && chapter.quiz_grade !== undefined
    const [num, title] = splitChapterName(chapter.name)
    const takeQuiz = () => navigate('/quiz', { state: { chapter: chapter.id, type: 'chapterQuiz', topics: [] } })
    const thumb = thumbUrl(chapter)

    let heading, blurb, buttons
    if (!chapter.video_completed) {
        heading = `Watch the video: ${num} ${title}`
        blurb = "Then take the chapter quiz to lock it in."
        buttons = <>
            <a href={videoPageUrl(chapter)} className="btn-primary px-6 py-2.5"><i className="fa-solid fa-play"></i> Watch the video</a>
            <button type="button" onClick={takeQuiz} className="btn-secondary px-6 py-2"><i className="fa-solid fa-pen-to-square"></i> Skip to the quiz</button>
        </>
    } else {
        heading = `${hasGrade ? 'Retake' : 'Take'} the quiz: ${num} ${title}`
        blurb = hasGrade
            ? <>Last score: <span className="font-bold" style={{ color: gradeColor(chapter.quiz_grade) }}>{chapter.quiz_grade}%</span>. {scoreQuip(chapter.quiz_grade)}</>
            : "You've watched the video. Time to show what you know."
        buttons = <>
            <button type="button" onClick={takeQuiz} className="btn-primary px-6 py-2.5">
                <i className={`fa-solid fa-${hasGrade ? 'rotate-right' : 'pen-to-square'}`}></i> {hasGrade ? 'Retake the quiz' : 'Take the quiz'}
            </button>
            <a href={videoPageUrl(chapter)} className="btn-secondary px-6 py-2"><i className="fa-solid fa-play"></i> Rewatch the video</a>
        </>
    }

    return (
        <section className="panel rounded-3xl overflow-hidden border-t-8 unit-border grid sm:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)]" style={unitStyle(unit)}>
            <a href={videoPageUrl(chapter)} className="relative block bg-black">
                {thumb && <img src={thumb} alt="" className="w-full h-full object-cover aspect-video sm:aspect-auto" />}
                {chapter.duration && <span className="absolute bottom-2 right-2 bg-black/80 text-xs px-1.5 rounded">{chapter.duration}</span>}
            </a>
            <div className="p-6 flex flex-col justify-center">
                <p className="uppercase tracking-widest text-sm font-bold unit-text">Up next</p>
                <div className="mt-2 flex items-center gap-2">
                    <span className="text-xs font-extrabold px-2 py-0.5 rounded unit-bg whitespace-nowrap">UNIT {unit?.number ?? ''}</span>
                    <span className="text-sm text-gray-300">{unit?.title}</span>
                </div>
                <h2 className="mt-2 text-2xl font-extrabold">{heading}</h2>
                <p className="mt-2 text-gray-300">{blurb}</p>
                <div className="mt-5 flex flex-wrap gap-3">{buttons}</div>
            </div>
        </section>
    )
}

// Nothing up next: either a brand-new student without a plan, or one who finished it
const NoUpNext = ({ hasPlan }) => {
    const navigate = useNavigate()
    return (
        <section className="panel rounded-3xl p-6 sm:p-8 border-t-8 border-[#FFC93C]">
            <p className="uppercase tracking-widest text-sm font-bold text-[#FFC93C]">Up next</p>
            <h2 className="mt-2 text-2xl font-extrabold">{hasPlan ? 'You finished your study plan!' : "Let's build your study plan"}</h2>
            <p className="mt-2 text-gray-300">{hasPlan
                ? 'Keynes would be proud. Add more units, or keep your skills sharp with a review quiz.'
                : 'Pick the units you want to study and we’ll line up the videos and quizzes.'}</p>
            <div className="mt-5 flex flex-wrap gap-3">
                <button type="button" className="btn-primary px-6 py-2.5" onClick={() => navigate(hasPlan ? '/updateunits' : '/getstarted')}>
                    <i className="fa-solid fa-sliders"></i> {hasPlan ? 'Add more units' : 'Get started'}
                </button>
                <a href="/videos" className="btn-secondary px-6 py-2"><i className="fa-solid fa-video"></i> Browse the videos</a>
            </div>
        </section>
    )
}

export const UserHome = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    const showModal = location.state?.showModal
    const userName = useSelector((state) => state.user.username) || ''
    const currentChapterId = useSelector((state) => state.user.currentChapter)
    const userChapters = useSelector((state) => state.userChapters)
    const plan = useStudyPlan()
    const topics = useTopicsWithProgress()
    const message = useMemo(() => MESSAGES[Math.floor(Math.random() * MESSAGES.length)], [])

    useEffect(() => {
        window.scrollTo(0, 0)
        dispatch(getAllTopics())   // every topic, so "not tried yet" topics show too
    }, [dispatch])

    const upNextUnit = plan.find((u) => u.chapters.some((ch) => String(ch.id) === String(currentChapterId)))
    const upNext = upNextUnit?.chapters.find((ch) => String(ch.id) === String(currentChapterId))

    const progressList = Object.values(userChapters)
    const watched = progressList.filter((p) => p.video_completed).length
    const quizzes = progressList.filter((p) => p.quiz_grade !== null && p.quiz_grade !== undefined).length
    const topicList = Object.values(topics)
    const needWork = topicList.filter((t) => t.mastery_status === 'needs_work').length
    const refreshers = topicList.filter((t) => t.review_due).length

    const goToWeakspotQuiz = () => navigate('/quiz', { state: { chapter: currentChapterId, type: 'shortWeakspotQuiz', topics: [] } })

    return (
        <>
            <Tutorial showModal={showModal} />
            <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10 lg:px-16">
                <div className="max-w-7xl mx-auto">
                    <section>
                        <h1 className="text-3xl sm:text-5xl font-extrabold">
                            Welcome back, <span className="text-[#FFC93C]">{userName ? userName[0].toUpperCase() + userName.slice(1) : ''}.</span>
                        </h1>
                        <p className="mt-2 text-lg text-gray-200">{message}</p>
                        <ul className="mt-5 flex flex-wrap gap-3 text-sm font-semibold">
                            <li className="panel rounded-full px-4 py-2"><i className="fa-solid fa-video mr-2 text-[#FFC93C]"></i>{watched} video{watched === 1 ? '' : 's'} watched</li>
                            <li className="panel rounded-full px-4 py-2"><i className="fa-solid fa-circle-check mr-2 text-[#C6E83A]"></i>{quizzes} chapter quiz{quizzes === 1 ? '' : 'zes'} taken</li>
                            {needWork > 0 && <li className="panel rounded-full px-4 py-2"><i className="fa-solid fa-triangle-exclamation mr-2 text-[#FF8A3D]"></i>{needWork} topic{needWork === 1 ? '' : 's'} need{needWork === 1 ? 's' : ''} work</li>}
                            {refreshers > 0 && <li className="panel rounded-full px-4 py-2"><i className="fa-solid fa-rotate mr-2 text-[#4CC2F5]"></i>{refreshers} refresher{refreshers === 1 ? '' : 's'} due</li>}
                        </ul>
                    </section>

                    <div className="mt-8 grid lg:grid-cols-[2fr_1fr] gap-8 items-start">
                        <div className="space-y-8 min-w-0">
                            <div data-tour="upnext">{upNext ? <UpNext chapter={upNext} unit={upNextUnit} /> : <NoUpNext hasPlan={plan.length > 0} />}</div>
                            {plan.length > 0 && <div data-tour="plan"><Progress /></div>}
                        </div>

                        <aside className="space-y-5 lg:sticky lg:top-28" data-tour="practice">
                            <h2 className="text-2xl font-bold">Practice</h2>
                            <div className="panel rounded-2xl p-5 border-t-4 border-[#FF8A3D]">
                                <h3 className="text-xl font-bold"><i className="fa-solid fa-crosshairs mr-2 text-[#FF8A3D]"></i>Focus on your weaknesses</h3>
                                <p className="mt-2 text-sm text-gray-200">This quiz knows your weak spots better than your Netflix recommendations.</p>
                                {(needWork > 0 || refreshers > 0) && (
                                    <ul className="mt-3 text-sm space-y-1">
                                        {needWork > 0 && <li><span className="font-bold text-[#FF8A3D]">{needWork} topic{needWork === 1 ? '' : 's'}</span> need{needWork === 1 ? 's' : ''} work</li>}
                                        {refreshers > 0 && <li><span className="font-bold text-[#4CC2F5]">{refreshers} mastered topic{refreshers === 1 ? '' : 's'}</span> {refreshers === 1 ? 'is' : 'are'} due for a refresher</li>}
                                    </ul>
                                )}
                                <button type="button" className="btn-primary w-full mt-4 py-2.5" onClick={goToWeakspotQuiz}>
                                    <i className="fa-solid fa-bolt"></i> Find my Achilles' heel
                                </button>
                            </div>
                            <div className="panel rounded-2xl p-5 border-t-4 border-[#9B6BFF]">
                                <h3 className="text-xl font-bold"><i className="fa-solid fa-dice mr-2 text-[#B89AFF]"></i>Choose your own quiz adventure</h3>
                                <p className="mt-2 text-sm text-gray-200">Feeling daring? Pick any topics, whether you rocked them or flopped them, and we'll build a quiz as wild as your choices.</p>
                                <button type="button" className="btn-secondary w-full mt-4 py-2" onClick={() => navigate('/quizgenerator')}>Create my quiz</button>
                            </div>
                            <div className="bg-[#2B3D45]/60 rounded-2xl p-5">
                                <h3 className="font-bold"><i className="fa-solid fa-sliders mr-2 text-[#7fd3e6]"></i>Update your study plan</h3>
                                <p className="mt-1 text-sm text-gray-300">Not everyone gets it right on the first try. You should see our last haircut.</p>
                                <button type="button" className="mt-3 text-sm font-bold text-[#7fd3e6] hover:underline" onClick={() => navigate('/updateunits')}>Fix life choices →</button>
                            </div>
                        </aside>
                    </div>
                </div>
            </div>
        </>
    )
}
