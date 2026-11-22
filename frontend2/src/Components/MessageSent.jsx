import { useNavigate } from "react-router-dom"
import { goToPublicHome } from "./routes"

export const MessageSent = () => {
    const navigate = useNavigate()
    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <section className="max-w-2xl mx-auto panel rounded-3xl p-6 sm:p-10 border-t-8 border-[#C6E83A] text-center">
                <i className="fa-solid fa-paper-plane text-4xl text-[#C6E83A]"></i>
                <h1 className="mt-4 text-3xl sm:text-4xl font-extrabold">Success!</h1>
                <p className="mt-3 text-lg text-gray-200">Your message has been successfully hurled into the digital abyss! Something may or may not emerge on the other side. If you sent us something mean, don’t worry: we’ll absolutely ugly cry about it and possibly start a support group.</p>
                <div className="mt-6 flex flex-wrap gap-3 justify-center">
                    <button type="button" className="btn-primary px-6 py-2.5" onClick={goToPublicHome}><i className="fa-solid fa-house"></i> Back home</button>
                    <button type="button" className="btn-secondary px-6 py-2" onClick={() => navigate('/contactus')}>Send another</button>
                </div>
            </section>
        </div>
    )
}
