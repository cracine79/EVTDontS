import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { PlanPicker } from "./UnitChoiceForm"
import { addUserUnits } from "../Slices/unitsActions"

// First stop after signing up: pick what to study
export const GetStarted = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const save = async (selected) => {
        await dispatch(addUserUnits(selected))
        navigate('/userhome', { state: { showModal: true } })
    }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-6xl mx-auto grid lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)] gap-10 items-start">
                <section className="lg:sticky lg:top-28">
                    <p className="uppercase tracking-widest text-sm font-bold text-[#7fd3e6]">Step 1 of 1: build your study plan</p>
                    <h1 className="mt-2 text-3xl sm:text-5xl font-extrabold leading-tight">Welcome to EVTDS: <span className="text-[#FFC93C]">lowering your expectations since… well, now!</span></h1>
                    <div className="mt-5 space-y-4 text-lg text-gray-200 leading-relaxed">
                        <p>We can’t believe it either: you signed up! Did we mention we’re ridiculously excited? Like, "economists spotting an error in a government budget" level of excitement. 🧐 You’ve just joined a group of elite learners ready to unravel the mysteries of supply, demand, and why avocado toast costs more than your rent.</p>
                        <p>First things first: choose the units you want to study. It’s like picking out the episodes of a show that actually teach you something (without putting you into a deep nap).</p>
                        <p className="text-gray-300">So buckle up. If at any point you’re wondering "What have I done?", don’t worry: you’re exactly where you need to be. 🚀</p>
                    </div>
                </section>
                <section>
                    <h2 className="text-2xl font-bold mb-4">I want to study…</h2>
                    <PlanPicker onSubmit={save} submitLabel={<>Let's go <i className="fa-solid fa-arrow-right"></i></>} />
                </section>
            </div>
        </div>
    )
}
