import { useSelector, useDispatch } from "react-redux"
import { useNavigate, useLocation } from "react-router-dom"
import { useEffect } from "react"
import { clearUserResults } from "../Slices/resultsSlice"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { finishChapter } from "../Slices/resultsActions"
import { ScoreCard, TopicMovement, MissedQuestions, scoreOf } from "./ResultsParts"
import { goToVideoPage, splitChapterName } from "./ui"

export const QuizResults = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const currentChapter = useSelector(state => state.user.currentChapter)
    // The chapter this quiz was for; older links only knew the current chapter
    const quizChapterId = location.state?.chapterId ?? currentChapter
    const chapters = useSelector(state => state.chapters)
    const units = useSelector(state => state.units)
    const results = useSelector(state => state.results)
    const questions = useSelector(state => state.questions)
    const chapter = chapters[quizChapterId]
    const unit = chapter ? units[chapter.unit_id] : null
    const [num, title] = splitChapterName(chapter?.name || '')
    const unitFinished = location.state?.unitFinished
    // Only the "up next" chapter moves the study plan along
    const isCurrent = String(quizChapterId) === String(currentChapter)

    const score = scoreOf(results)
    const passed = score.percent > 60

    useEffect(() => { window.scrollTo(0, 0) }, [])

    const scoreHeader = () => {
        if (score.percent >= 70) return "AMAZING WORK!!! You crushed these AP style questions. Honestly, I'm starting to think they're just phoning it in at this point."
        if (score.percent > 50) return "Totally not a terrible job on those AP style questions! You're, like, a couple of Google searches away from greatness."
        return "Oof. AP style questions can be tricky. Let's try it again. Looks like the quiz could use a little more work too."
    }

    const clear = () => {
        dispatch(clearQuestions())
        dispatch(clearUserResults())
    }

    const retake = () => {
        dispatch(clearUserResults())
        navigate('/quiz', { state: { chapter: quizChapterId, type: 'chapterQuiz', topics: [] } })
        dispatch(openQuizModal())
    }

    const nextVideo = async () => {
        const data = await dispatch(finishChapter({ chapter_id: quizChapterId, quiz_score: score.percent }))
        clear()
        const newChapter = data.current_chapter
        if (data.completed === true) {
            navigate('/finishpage')
        } else if (chapters[quizChapterId].unit_id !== chapters[newChapter].unit_id) {
            navigate('/finishunit', { state: { unitId: chapters[quizChapterId].unit_id } })
        } else {
            goToVideoPage(chapters[newChapter])
        }
    }

    const rewatch = () => {
        clear()
        goToVideoPage(chapter)
    }

    const backHome = () => {
        if (isCurrent && score.percent >= 60) dispatch(finishChapter({ chapter_id: quizChapterId, quiz_score: score.percent }))
        clear()
        navigate('/userhome')
    }

    const topicIds = Object.values(results).map((r) => questions[r.questionId]?.topic_id).filter(Boolean)

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-4xl mx-auto">
                <ScoreCard unit={unit} eyebrow={`${unit ? `Unit ${unit.number} · ` : ''}Chapter quiz results`} title={<>{num} {title}</>} score={score}>
                    <p>{scoreHeader()}</p>
                    {isCurrent && unitFinished && passed && <p className="font-bold text-[#FFC93C]">That was the last chapter of the unit! You are killing it, my dude!</p>}
                </ScoreCard>

                <div className="mt-6 flex flex-wrap gap-3 justify-center sm:justify-start">
                    {isCurrent && passed ? (
                        <button type="button" className="btn-primary px-7 py-3" onClick={nextVideo}>
                            {unitFinished ? <>Take me to my unit wrap-up party! <i className="fa-solid fa-champagne-glasses"></i></> : <>Enough of this. Next video <i className="fa-solid fa-arrow-right"></i></>}
                        </button>
                    ) : (
                        <button type="button" className={`${passed ? 'btn-secondary px-6 py-2.5' : 'btn-primary px-7 py-3'}`} onClick={rewatch}>
                            <i className="fa-solid fa-play"></i> Let me check that video out again
                        </button>
                    )}
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={retake}>
                        <i className="fa-solid fa-rotate-right"></i> Gimme a mulligan
                    </button>
                    {!(isCurrent && unitFinished) && (
                        <button type="button" className={!isCurrent && passed ? 'btn-primary px-7 py-3' : 'btn-secondary px-6 py-2.5'} onClick={backHome}>
                            <i className="fa-solid fa-house"></i> Back to my dashboard
                        </button>
                    )}
                </div>

                <TopicMovement topicIds={topicIds} />
                <MissedQuestions results={results} />
            </div>
        </div>
    )
}
