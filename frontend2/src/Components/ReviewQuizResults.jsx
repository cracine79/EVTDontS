import { useLocation, useNavigate } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux"
import { useEffect, useMemo } from "react"
import { clearUserResults } from "../Slices/resultsSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { ScoreCard, TopicMovement, MissedQuestions, scoreOf } from "./ResultsParts"

// How sharp the student is on a topic, by mastery score
const ranking = (percent) => {
    if (percent > 80) return 'Neo in the Matrix level clarity'
    if (percent > 70) return 'A Werner Herzog documentary production value'
    if (percent > 60) return 'An intern on their third cup of coffee level sharpness'
    if (percent > 50) return 'The depth of the lyrics of an early 2000s boy band song'
    return 'Michael Scott trying to declare bankruptcy level knowledge'
}

const GOOD = [
    "Well, look at you, making economic principles bow before your mighty intellect! Somewhere, a supply-and-demand curve just shed a proud tear.",
    "You crushed that quiz like a monopolist crushing competition!",
    "Some people balance budgets; you just balanced right on the line between impressive and economically intimidating!",
    "Boom! You absolutely Ricardianly owned that quiz. Comparative advantage? Clearly, it's you vs. the rest of us mere mortals.",
    "That was some fine-tuned economic genius. You’re practically a walking case study on human capital!",
]
const MEDIUM = [
    "Not exactly breaking economic records, but hey, there were some correct answers in there!",
    "Not bad, not great. Kind of like a lukewarm cup of coffee. But, hey, caffeine is caffeine!",
    "In the economic cycle of quiz performance, consider this a gentle recession. Not great, not the end of the world either!",
    "Not too hot, not too cold. Call it the Goldilocks of quiz scores!",
    "I wouldn't brag to Dave Grohl about that score, but I'd probably tell my mom.",
]
const BAD = [
    "Oof. That score tanked harder than Blockbuster stock in 2008.",
    "Alright, maybe not quite booming, but still very much in the expansion territory for effort!",
    "It’s a marathon, not a sprint. Just think of this score as a warm-up lap!",
    "Think of it as an investment in learning. Sometimes the market just dips a little.",
    "Even the best economists hit a rough patch! You’ve got a strong foundation for next time.",
]

export const ReviewQuizResults = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    const results = useSelector(state => state.results)
    const questions = useSelector(state => state.questions)
    const topics = location.state?.topics || []
    const type = location.state?.type
    const score = scoreOf(results)

    useEffect(() => { window.scrollTo(0, 0) }, [])

    const praise = useMemo(() => {
        const pick = (list) => list[Math.floor(Math.random() * list.length)]
        if (score.percent > 65) return pick(GOOD)
        if (score.percent > 49) return pick(MEDIUM)
        return pick(BAD)
    }, [score.percent])

    const clear = () => {
        dispatch(clearUserResults())
        dispatch(clearQuestions())
    }
    const goHome = () => { clear(); navigate('/userhome') }
    const goAgain = () => { clear(); navigate('/quiz', { state: { chapter: 1, type: 'topicQuiz', topics } }) }
    const gauntletAgain = () => { clear(); navigate('/quiz', { state: { chapter: 1, type: 'shortWeakspotQuiz', topics: [] } }) }

    const isGauntlet = type === 'shortWeakspotQuiz'
    const topicIds = topics.length
        ? topics.map((t) => t.topic_id)
        : Object.values(results).map((r) => questions[r.questionId]?.topic_id).filter(Boolean)
    const theme = isGauntlet ? { color: '#FF8A3D', light: '#FF8A3D' } : { color: '#9B6BFF', light: '#B89AFF', text: '#fff' }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-4xl mx-auto">
                <ScoreCard unit={theme} eyebrow={isGauntlet ? 'The Gauntlet · results' : 'Topic quiz results'}
                    title={isGauntlet ? 'You vs. your weak spots' : topics.map((t) => t.topic_name).join(', ')} score={score}>
                    <p>{praise}</p>
                </ScoreCard>

                <div className="mt-6 flex flex-wrap gap-3 justify-center sm:justify-start">
                    {type === 'topicQuiz'
                        ? <button type="button" className="btn-primary px-7 py-3" onClick={goAgain}><i className="fa-solid fa-rotate-right"></i> Take another one</button>
                        : <button type="button" className="btn-primary px-7 py-3" onClick={gauntletAgain}><i className="fa-solid fa-bolt"></i> Run the Gauntlet again</button>}
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={() => { clear(); navigate('/quizgenerator') }}>
                        <i className="fa-solid fa-dice"></i> Build a different quiz
                    </button>
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={goHome}><i className="fa-solid fa-house"></i> Back to my dashboard</button>
                </div>

                <TopicMovement topicIds={topicIds} describe={(t, pct) => (
                    <>Faced {t.questions_asked ?? 0} question{t.questions_asked === 1 ? '' : 's'}, {t.answered_correctly ?? 0} right. Your understanding is equivalent to: <b>{ranking(pct)}</b>.</>
                )} />
                <MissedQuestions results={results} />
            </div>
        </div>
    )
}
