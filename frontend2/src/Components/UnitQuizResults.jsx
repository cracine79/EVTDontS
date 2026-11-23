import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { useEffect } from "react"
import { clearUserResults } from "../Slices/resultsSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { ScoreCard, TopicMovement, MissedQuestions, scoreOf } from "./ResultsParts"

export const UnitQuizResults = () => {
    const dispatch = useDispatch()
    const location = useLocation()
    const navigate = useNavigate()
    const topics = location.state?.topics || []
    const currentUnitId = location.state?.unitId
    const units = useSelector(state => state.units)
    const unit = units[currentUnitId]
    const chapters = useSelector(state => state.chapters) || {}
    const results = useSelector(state => state.results)
    const score = scoreOf(results)

    useEffect(() => { window.scrollTo(0, 0) }, [])

    const scoreHeader = () => {
        if (score.percent >= 70) return "Absolutely destroyed it! If the AP exam had legs, it’d be sprinting away in the other direction right now. If they awarded trophies for multiple-choice annihilation, we’d be shipping one to you right now. But we’ll settle for sending you back to destroy the next unit instead. This AP exam doesn’t stand a chance!"
        if (score.percent > 50) return "Nice work! You’re pacing yourself perfectly for a victory lap when the AP exam comes around. A few more rounds with these quizzes and College Board will be issuing a warning. Keep it up, greatness awaits!"
        return "Let’s just say you’re giving the AP exam way too much confidence. But no worries, that’s why these quizzes are here. Give it another go, take down those questions one by one, and show that AP test it can’t hide behind fancy vocab and graphs forever. You’ve got this!"
    }

    const clear = () => {
        dispatch(clearUserResults())
        dispatch(clearQuestions())
    }
    // The server finds the unit from a chapter in it, so send one of this unit's chapters
    const unitChapterId = Object.values(chapters).find(ch => String(ch.unit_id) === String(currentUnitId))?.id
    const retake = () => { clear(); navigate('/quiz', { state: { chapter: unitChapterId, type: 'unitQuiz', topics: [], unit: currentUnitId } }) }
    const goHome = () => { clear(); navigate('/userhome') }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-4xl mx-auto">
                <ScoreCard unit={unit} eyebrow={`Unit ${unit?.number ?? ''} · Unit quiz results`} title={unit?.title || unit?.name || 'Unit quiz'} score={score}>
                    <p>{scoreHeader()}</p>
                </ScoreCard>
                <div className="mt-6 flex flex-wrap gap-3 justify-center sm:justify-start">
                    <button type="button" className="btn-primary px-7 py-3" onClick={goHome}><i className="fa-solid fa-house"></i> Back to my dashboard</button>
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={retake}><i className="fa-solid fa-rotate-right"></i> Gimme a mulligan</button>
                </div>
                <TopicMovement topicIds={topics.map((t) => t.topic_id)} />
                <MissedQuestions results={results} />
            </div>
        </div>
    )
}
