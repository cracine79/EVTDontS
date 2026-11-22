import { useDispatch, useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
import { useEffect } from "react"
import { PlanPicker } from "./UnitChoiceForm"
import { addUserUnits } from "../Slices/unitsActions"

export const UpdateUnits = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const chapters = useSelector((state) => state.chapters)
    // Chapters currently in the student's study plan
    const inPlan = Object.fromEntries(Object.entries(chapters).filter(([, ch]) => ch.in_plan).map(([id]) => [id, true]))

    useEffect(() => { window.scrollTo(0, 0) }, [])

    const save = async (selected) => {
        await dispatch(addUserUnits(selected))
        navigate('/userhome', { state: { showModal: false } })
    }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-4xl mx-auto">
                <p className="uppercase tracking-widest text-sm font-bold text-[#7fd3e6]">Update your study plan</p>
                <h1 className="mt-2 text-3xl sm:text-5xl font-extrabold">You chose what?!? Let's fix this train wreck</h1>
                <div className="mt-4 space-y-3 text-lg text-gray-200">
                    <p>Okay, so maybe you didn’t exactly crush it with your first round of unit choices. Hey, it happens to the best of us (trust me, we run a website called Economics Videos That Don’t Suck. We've made some choices too).</p>
                    <p className="text-gray-300">Add or remove units and chapters below, and we’ll pretend you got it right the first time. Your progress on removed chapters is kept, in case you change your mind.</p>
                </div>
                <div className="mt-8">
                    <PlanPicker initial={inPlan} onSubmit={save} submitLabel="Save my plan"
                        secondary={<button type="button" className="btn-secondary px-5 py-2" onClick={() => navigate('/userhome')}>Never mind</button>} />
                </div>
            </div>
        </div>
    )
}
