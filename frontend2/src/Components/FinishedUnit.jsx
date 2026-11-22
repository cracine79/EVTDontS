import { useSelector } from "react-redux"
import { useNavigate, useLocation } from "react-router-dom"
import { useEffect } from "react"
import { useStudyPlan } from "./Progress"
import { gradeColor, splitChapterName, unitStyle } from "./ui"

// Finished the last chapter of a unit: celebrate, show the grades, offer the unit quiz
export const FinishUnit = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const plan = useStudyPlan()
    const unitId = location.state?.unitId
    const unit = plan.find((u) => String(u.id) === String(unitId))

    useEffect(() => { window.scrollTo(0, 0) }, [])

    if (!unit) {
        return (
            <div className="pt-28 pb-16 px-5 max-w-3xl mx-auto text-center">
                <h1 className="text-3xl font-extrabold">Unit wrap-up party</h1>
                <p className="mt-3 text-gray-300">We lost track of which unit you just finished. Your dashboard has everything.</p>
                <button type="button" className="btn-primary px-6 py-2.5 mt-6" onClick={() => navigate('/userhome')}>Back to my dashboard</button>
            </div>
        )
    }

    const goToUnitTest = () => navigate('/quiz', { state: { chapter: unit.chapters[0]?.id, type: 'unitQuiz', topics: [], unit: unit.id } })

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-3xl mx-auto">
                <section className="panel rounded-3xl p-6 sm:p-10 border-t-8 unit-border" style={unitStyle(unit)}>
                    <p className="uppercase tracking-widest text-sm font-bold unit-text">Unit {unit.number} complete 🎉</p>
                    <h1 className="mt-2 text-3xl sm:text-4xl font-extrabold">Congratulations on finishing {unit.title || unit.name}! You're a beast.</h1>
                    <ul className="mt-6 divide-y divide-white/10">
                        {unit.chapters.map((ch) => {
                            const [num, title] = splitChapterName(ch.name)
                            const hasGrade = ch.quiz_grade !== null && ch.quiz_grade !== undefined
                            return (
                                <li key={ch.id} className="py-2.5 flex items-center gap-4">
                                    <span className="flex-1"><span className="text-gray-400 mr-1">{num}</span>{title}</span>
                                    {hasGrade
                                        ? <span className="w-16 text-center font-bold rounded-full text-[#111]" style={{ background: gradeColor(ch.quiz_grade) }}>{ch.quiz_grade}%</span>
                                        : <span className="w-16 text-center text-xs text-gray-400">No quiz</span>}
                                </li>
                            )
                        })}
                    </ul>
                    <p className="mt-6 text-lg text-gray-200">
                        Ready for the unit quiz? Buckle up, bucko: it's a 20-question marathon without the heavy breathing. Well . . . actually . . . I guess that depends upon how much you are into econ exams. Okay, that got weird. You can take it now or later. Umm, I'm just going to let myself out while you decide.
                    </p>
                    <div className="mt-6 flex flex-wrap gap-3">
                        <button type="button" className="btn-primary px-7 py-3" onClick={goToUnitTest}><i className="fa-solid fa-trophy"></i> YEAH BRAH, UNIT TEST</button>
                        <button type="button" className="btn-secondary px-6 py-2.5" onClick={() => navigate('/userhome')}>Later, OK? Country roads, take me home</button>
                    </div>
                </section>
            </div>
        </div>
    )
}
