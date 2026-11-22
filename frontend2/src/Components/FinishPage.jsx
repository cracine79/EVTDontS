import { useNavigate } from "react-router-dom"
import { useSelector } from "react-redux"
import { useEffect } from "react"
import { masteryPercent } from "./masteryUtils"
import { Progress, useStudyPlan } from "./Progress"

// The student finished every chapter in their study plan
export const FinishPage = () => {
    const navigate = useNavigate()
    const topicProg = useSelector((state) => state.topicProg)
    const userName = useSelector((state) => state.user.username) || ''
    const plan = useStudyPlan()

    useEffect(() => { window.scrollTo(0, 0) }, [])

    const topicList = Object.values(topicProg)
    const asked = topicList.reduce((sum, t) => sum + (t.questions_asked || 0), 0)
    const answered = topicList.reduce((sum, t) => sum + (t.answered_correctly || 0), 0)
    const practiced = topicList.filter((t) => t.questions_asked > 0)
    const average = practiced.length ? Math.floor(practiced.reduce((sum, t) => sum + masteryPercent(t), 0) / practiced.length) : 0
    const videos = plan.reduce((sum, u) => sum + u.chapters.length, 0)

    let level = 'Not yet started'
    if (average > 90) level = 'Economic Overlord'
    else if (average > 80) level = 'Econo-ninja'
    else if (average > 60) level = 'Curve Whisperer'
    else if (average > 50) level = 'Sort of Chart Challenged'
    else if (average > 0) level = 'Economic Noob'

    const stat = (big, text) => (
        <div className="panel rounded-2xl p-5">
            <p className="text-3xl font-black text-[#FFC93C]">{big}</p>
            <p className="mt-1 text-gray-200">{text}</p>
        </div>
    )

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-5xl mx-auto">
                <section className="panel rounded-3xl p-6 sm:p-10 border-t-8 border-[#FFC93C]">
                    <p className="uppercase tracking-widest text-sm font-bold text-[#FFC93C]">Study plan complete 🎉</p>
                    <h1 className="mt-2 text-3xl sm:text-5xl font-extrabold">Congratulations, {userName ? userName[0].toUpperCase() + userName.slice(1) : 'legend'}!!</h1>
                    <div className="mt-4 space-y-3 text-lg text-gray-200">
                        <p>[Insert preferred expletive] yeah!! You've officially crushed all the chapters you enrolled in! You watched all the videos, aced the quizzes, and now, my friend, you’re the economist everyone wishes they could hang out with at parties (…just go with it).</p>
                        <p>But wait, there’s more! If you’re craving more economic enlightenment (or looking for a distraction from another re-watch of <em>The Office</em>), there are still chapters you haven’t signed up for. Add new ones, or do a power rewatch of your favorites.</p>
                        <p className="text-gray-300">And hey, if you’ve secretly enjoyed the thrilling world of supply and demand, tell a friend! They’ll thank you later... maybe.</p>
                    </div>
                    <div className="mt-6 flex flex-wrap gap-3">
                        <button type="button" className="btn-primary px-6 py-2.5" onClick={() => navigate('/updateunits')}><i className="fa-solid fa-plus"></i> Add more units</button>
                        <button type="button" className="btn-secondary px-6 py-2" onClick={() => navigate('/userhome')}><i className="fa-solid fa-house"></i> Back to my dashboard</button>
                    </div>
                </section>

                <h2 className="mt-10 text-2xl sm:text-3xl font-bold">Econ Legends Scorecard <span className="text-gray-400 font-normal">(dun dun dunnnnnnn!)</span></h2>
                <div className="mt-4 grid sm:grid-cols-3 gap-4">
                    {stat(videos, `video${videos === 1 ? '' : 's'} suffered through, covering ${topicList.length} topic${topicList.length === 1 ? '' : 's'}. Whether or not they sucked is up to you!`)}
                    {stat(`${answered} / ${asked}`, "questions faced down and vanquished. You're a legend.")}
                    {stat(`${average}%`, 'average mastery across every topic you practiced.')}
                </div>
                <p className="mt-4 panel rounded-2xl p-5 text-xl">
                    Given your performance, stats, and overall grittiness, you are officially awarded the level of <b className="text-[#FFC93C]">{level}</b>.
                </p>

                <div className="mt-10">
                    <Progress />
                </div>
            </div>
        </div>
    )
}
