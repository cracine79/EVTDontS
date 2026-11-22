import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { useEffect, useState } from "react"
import { getQuestions } from "../Slices/questionsActions"
import { getAllChapters } from "../Slices/chaptersActions"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { goToLibrary, splitChapterName, unitStyle } from "./ui"

const DEFAULT_QUIZ_IMG = "https://evtds-seeds.s3.us-east-2.amazonaws.com/inprogresscartoon.png"

// "a and b", "a, b, and c", "a, b, c and 2 more"
const listNames = (names) => {
    if (names.length <= 1) return names[0] || ''
    if (names.length === 2) return names.join(' and ')
    if (names.length === 3) return `${names[0]}, ${names[1]}, and ${names[2]}`
    return `${names.slice(0, 3).join(', ')} and ${names.length - 3} more`
}

export const IntroCard = ({ style, eyebrow, title, children, image }) => (
    <section className="panel rounded-3xl overflow-hidden border-t-8 unit-border grid md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)]" style={style}>
        <div className="p-6 sm:p-10">
            <p className="uppercase tracking-widest text-sm font-bold unit-text">{eyebrow}</p>
            <h1 className="mt-2 text-3xl sm:text-4xl font-extrabold leading-tight">{title}</h1>
            <div className="mt-4 space-y-4 text-gray-200 leading-relaxed">{children}</div>
        </div>
        {image && <div className="bg-white/5 flex items-center justify-center p-4"><img src={image} alt="" className="w-full max-h-[28rem] object-contain rounded-2xl" /></div>}
    </section>
)

export const Quiz = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const params = new URLSearchParams(location.search)
    // From inside the app the quiz details come in the navigation state; links from the public
    // video pages use the web address instead: /app/quiz?chapter=6
    const chapter = location.state?.chapter ?? (params.get('chapter') ? Number(params.get('chapter')) : undefined)
    const type = location.state?.type ?? (params.get('chapter') ? 'chapterQuiz' : undefined)
    const topics = location.state?.topics ?? []
    const unitQuizUnitId = location.state?.unit
    const units = useSelector(state => state.units)
    const currentUser = useSelector(state => state.user.username)
    const wholeChapter = useSelector(state => state.chapters[chapter])
    const [quizBlurb, setQuizBlurb] = useState("")
    const [quizBlurbImgUrl, setQuizBlurbImgUrl] = useState("")

    useEffect(() => {
        if (!type) return
        const fetchData = async () => {
            const results = await dispatch(getQuestions({ chapter, type, topics }))
            setQuizBlurb(results?.quiz_blurb || "")
            setQuizBlurbImgUrl(results?.quiz_blurb_img_url || DEFAULT_QUIZ_IMG)
        }
        fetchData()
        window.scrollTo(0, 0)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch, chapter, type])

    // A chapter outside the student's study plan (e.g. started from a public video page)
    useEffect(() => {
        if (chapter && !wholeChapter && (type === 'chapterQuiz' || type === 'chapterQuizNoUser')) dispatch(getAllChapters())
    }, [chapter, wholeChapter, type, dispatch])

    if (!type) {
        // Opened without saying which quiz (e.g. a refresh lost it): back to where quizzes start
        return (
            <div className="pt-28 pb-16 px-5 max-w-3xl mx-auto text-center">
                <h1 className="text-3xl font-extrabold">Which quiz was that again?</h1>
                <p className="mt-3 text-gray-300">We lost track of the quiz you were about to start. Pick it again from your dashboard.</p>
                <button type="button" className="btn-primary px-6 py-2.5 mt-6" onClick={() => navigate(currentUser ? '/userhome' : '/')}>
                    {currentUser ? 'Back to my dashboard' : 'Back home'}
                </button>
            </div>
        )
    }

    const unit = wholeChapter ? units[wholeChapter.unit_id] : null
    const [num, title] = splitChapterName(wholeChapter?.name || '')
    const names = topics.map(topic => topic.topic_name)

    const goBack = () => {
        dispatch(clearQuestions())
        if (currentUser) navigate('/userhome')
        else goToLibrary()
    }

    let intro
    if (type === 'chapterQuiz' || type === 'chapterQuizNoUser') {
        intro = (
            <IntroCard style={unitStyle(unit)} eyebrow={unit ? `Unit ${unit.number} · Chapter quiz` : 'Chapter quiz'}
                title={<>Are you ready to rock?<span className="block mt-2 text-2xl sm:text-3xl text-gray-200">{num} {title}</span></>}
                image={quizBlurbImgUrl}>
                <div className="whitespace-pre-line" dangerouslySetInnerHTML={{ __html: quizBlurb }}></div>
            </IntroCard>
        )
    } else if (type === 'topicQuiz') {
        intro = (
            <IntroCard style={unitStyle({ color: '#9B6BFF', light: '#B89AFF', text: '#fff' })} eyebrow="Choose your own quiz adventure"
                title={<>Now testing: <span className="text-[#B89AFF]">{listNames(names)}</span></>}>
                <p>Ah, the sweet smell of ambition mixed with just a hint of self-doubt. You’ve decided to tackle specific topics, which is either a bold display of confidence or a creative way to procrastinate on everything else. If you crush it, your topic ratings will skyrocket, and you'll be strutting around like the Gordon Ramsay of graphs and supply curves. If things go south, don't worry: we’ll only mock you a <em>little</em>.</p>
                <p>Whether you ace it or faceplant, at least you can say you tried, unlike that kid in the back of class who’s still arguing that opportunity cost is “just a suggestion.” Good luck, quiz champion!</p>
                <ul className="flex flex-wrap gap-2 text-sm font-semibold">
                    {topics.map((t) => <li key={t.topic_id} className="rounded-full bg-[#9B6BFF]/25 text-[#d9ccff] px-3 py-1">{t.topic_name}</li>)}
                </ul>
            </IntroCard>
        )
    } else if (type === 'shortWeakspotQuiz') {
        intro = (
            <IntroCard style={unitStyle({ color: '#FF8A3D', light: '#FF8A3D' })} eyebrow="The Gauntlet"
                title="Welcome to the Quiz of Reckoning" image="https://evtds-seeds.s3.us-east-2.amazonaws.com/Econ+and+kung+fu.png">
                <p>You’ve bravely clicked your way here, which means you're ready to face the ultimate showdown: you vs. your weak spots. Every wrong answer, every forgotten concept, every question that left you scratching your head is back, like the ghost of marginal utility haunting your economic soul.</p>
                <p>Take a deep breath and dive in. The more you lean into your weak spots, the more of an econo ninja you’ll become. Weakness today, strength tomorrow!</p>
            </IntroCard>
        )
    } else if (type === 'unitQuiz') {
        const quizUnit = units[unitQuizUnitId]
        intro = (
            <IntroCard style={unitStyle(quizUnit)} eyebrow={`Unit ${quizUnit?.number ?? ''} · Unit quiz`} title={quizUnit?.title || quizUnit?.name || 'Unit quiz'}>
                <p>The whole unit, one quiz. Show it who’s boss.</p>
            </IntroCard>
        )
    }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-6xl mx-auto">
                {intro}
                <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
                    <button type="button" className="btn-primary text-lg px-8 py-3" onClick={() => dispatch(openQuizModal())}>
                        <i className="fa-solid fa-play"></i> Start the quiz
                    </button>
                    <button type="button" className="btn-secondary text-lg px-8 py-2.5" onClick={goBack}>
                        {currentUser ? 'Back to my dashboard' : 'Back to the videos'}
                    </button>
                </div>
            </div>
            <QuestionComponent chapter={chapter} type={type} topics={topics} unit={unitQuizUnitId} />
        </div>
    )
}
