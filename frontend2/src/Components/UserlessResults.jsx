import { useLocation, useNavigate } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux"
import { useEffect } from "react"
import { openSignupModal } from "../Slices/modalSlice"
import { ScoreCard, MissedQuestions, scoreOf } from "./ResultsParts"
import { goToLibrary, goToVideoPage, splitChapterName } from "./ui"

// Results of the free (logged-out) chapter quiz
export const UserlessResults = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const quizData = location.state?.otherQuizData
    const chapter = useSelector(state => (quizData ? state.chapters[quizData.chapter_id] : null))

    useEffect(() => { window.scrollTo(0, 0) }, [])

    if (!quizData) {
        return (
            <div className="pt-28 pb-16 px-5 max-w-3xl mx-auto text-center">
                <h1 className="text-3xl font-extrabold">No quiz results here</h1>
                <p className="mt-3 text-gray-300">Pick a video and take its free practice quiz.</p>
                <a href="/videos" className="btn-primary px-6 py-2.5 mt-6">Browse the videos</a>
            </div>
        )
    }

    const score = scoreOf(quizData.answers)
    const [num, title] = splitChapterName(chapter?.name || '')

    const scoreHeader = () => {
        if (score.percent >= 70) return "AMAZING WORK!!! You crushed these AP style questions. Honestly, I'm starting to think they're just phoning it in at this point."
        if (score.percent > 50) return "Totally not a terrible job on those AP style questions! You're, like, a couple of Google searches away from greatness."
        return "Oof. AP style questions can be tricky. Let's try it again. Looks like the quiz could use a little more work too."
    }
    const encouragement = () => {
        if (score.percent === 100) return "You rocked that exam like Yoko rocked the Beatles! (Not sure what that simile actually means.)"
        if (score.percent >= 67) return "You crushed it! Not a total econ genius yet, but dangerously close."
        if (score.percent >= 33) return "Your quiz score wasn't exactly Wolf of Wall Street level . . . but hey, you showed up!"
        return "That was less 'Wall Street' and more 'Fire Festival'. At least it was memorable!"
    }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-4xl mx-auto">
                <ScoreCard eyebrow="Free practice quiz results" title={<>{num} {title}</>} score={score}>
                    <p>{scoreHeader()}</p>
                </ScoreCard>

                <div className="mt-6 flex flex-wrap gap-3 justify-center sm:justify-start">
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={() => navigate(`/freequiz/${chapter?.slug}`)}>
                        <i className="fa-solid fa-rotate-right"></i> Try the quiz again
                    </button>
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={() => (chapter ? goToVideoPage(chapter) : goToLibrary())}>
                        <i className="fa-solid fa-play"></i> Back to the video
                    </button>
                    <button type="button" className="btn-secondary px-6 py-2.5" onClick={goToLibrary}>
                        <i className="fa-solid fa-video"></i> More videos
                    </button>
                </div>

                <section className="mt-10 panel rounded-3xl p-6 sm:p-8 border-t-8 border-[#FFC93C] text-center">
                    <p className="text-xl font-bold">HEY! {encouragement()}</p>
                    <p className="mt-3 text-lg">Want to keep track of your progress and <b className="text-[#FFC93C]">get access to even more practice questions?</b> Then you gotta sign up!</p>
                    <p className="mt-2 text-gray-300">It's <b className="text-white">free</b> and <b className="text-white">quick</b>. And we send ZERO emails to you (unless you're like us and you forgot your password). C'mon, take the first step towards becoming an Econo-Jedi!</p>
                    <button type="button" className="btn-primary px-7 py-3 mt-5" onClick={() => dispatch(openSignupModal({ quizData }))}>
                        <i className="fa-solid fa-chart-line"></i> Sign up to save this score
                    </button>
                </section>

                <MissedQuestions results={quizData.answers} />
            </div>
        </div>
    )
}
