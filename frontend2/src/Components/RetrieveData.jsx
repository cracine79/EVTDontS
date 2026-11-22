import { useLocation } from "react-router-dom"
import { useState } from "react"


export const RetrieveData = () => {

    const location = useLocation()
    const [email, setEmail] = useState("")
    const [firstBoxStatus, setFirstBoxStatus] = useState(true)
    const [successBoxStatus, setSuccessBoxStatus] = useState(false)
    const [errorMessageVisible, setErrorMessageVisible] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")


    // Which email to send; default to the password reset (the common case)
    const source = location.state?.source || 'forgotPassword'

    const [sending, setSending] = useState(false)

    const handleSubmit = async () => {
        if (sending) return            // ignore double clicks / double submits
        const endpoint = source == 'forgotPassword' ? '/api/retrieve/password'
                       : source == 'forgotUsername' ? '/api/retrieve/username' : null
        if (!endpoint) return
        setSending(true)
        setErrorMessageVisible(false)
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email }),
            })
            if (response.ok) {
                window.scrollTo(0, 0)
                setFirstBoxStatus(false)
                setSuccessBoxStatus(true)
            } else if (response.status == 404) {
                setErrorMessage("We couldn't find an account with that email address. Please check it and try again.")
                setErrorMessageVisible(true)
            } else if (response.status == 429) {
                const data = await response.json().catch(()=>({}))
                setErrorMessage(data.message || "Too many attempts. Please wait a few minutes and try again.")
                setErrorMessageVisible(true)
            } else {
                setErrorMessage("We couldn't send the email right now. Please try again in a few minutes.")
                setErrorMessageVisible(true)
            }
        } catch (error) {
            console.error('Error requesting account email', error)
            setErrorMessage("We couldn't reach the server. Please check your connection and try again.")
            setErrorMessageVisible(true)
        } finally {
            setSending(false)
        }
    }

    const submitAgain = () => {
        setFirstBoxStatus(true)
        setSuccessBoxStatus(false)
    }
    const isPassword = source == 'forgotPassword'
    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <section className="max-w-2xl mx-auto panel rounded-3xl p-6 sm:p-10 border-t-8 border-[#7fd3e6]">
                {firstBoxStatus && (
                    <form onSubmit={(event) => { event.preventDefault(); handleSubmit() }}>
                        <h1 className="text-3xl sm:text-4xl font-extrabold">Forgot your {isPassword ? 'password' : 'username'}, huh?</h1>
                        {isPassword ? <>
                            <p className="mt-4 text-lg text-gray-200">No worries. We get it. Trying to remember passwords these days feels like the ending of The Usual Suspects: just staring at the wall, trying to recall if "hang_in_there" is the magical phrase that unlocks the gateway to some weird website I signed up for at 2 a.m. last month.</p>
                            <p className="mt-3 text-gray-300">Enter the email you signed up with, and we’ll send you a lifeline to reset your password. It’s like getting a second chance at life, and a way to avoid finding out you signed up for a website that sends you daily cat horoscope emails.</p>
                        </> : (
                            <p className="mt-4 text-lg text-gray-200">Classic. Don’t worry; it happens to the best of us, and by ‘best’ we mean people who have a dozen variations of the same username across different platforms. Pop your email into the box below, and we’ll send your username straight to your inbox. Because who needs memory when you’ve got us?</p>
                        )}
                        <input type="email" required placeholder="The email you signed up with" className="field mt-6" onChange={(e) => setEmail(e.target.value)} />
                        {errorMessageVisible && <p className="mt-3 font-bold text-[#FF6FAE]" role="alert">{errorMessage}</p>}
                        <button type="submit" disabled={sending} className="btn-primary px-7 py-3 mt-5">
                            <i className="fa-solid fa-envelope"></i> {sending ? 'Sending…' : isPassword ? 'Reset my password' : 'Email me my username'}
                        </button>
                    </form>
                )}
                {successBoxStatus && (
                    <div>
                        <h1 className="text-3xl font-extrabold"><i className="fa-solid fa-envelope-circle-check text-[#C6E83A] mr-2"></i>Check your email</h1>
                        <p className="mt-4 text-lg text-gray-200">{isPassword
                            ? 'A password reset email is on its way. Follow the instructions in it.'
                            : 'An email with your username is on its way.'}</p>
                        <p className="mt-2 text-gray-300">Be sure to check your spam folder as well, because your inbox might hate us for some unfathomable reason.</p>
                        <button type="button" className="btn-secondary px-6 py-2 mt-6" onClick={submitAgain}>Send it again</button>
                    </div>
                )}
            </section>
        </div>
    )
}
