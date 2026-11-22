import { useState } from "react"
import { csrfFetch } from "../csrf"
import { useNavigate } from "react-router-dom"
import { useEffect } from "react"
import { friendlyAuthError } from "./routes"
const sendEmail = async(subject, email, body, navigate) => {

    try{
        const response = await csrfFetch('/api/mail/send', {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({subject, email, body})
        })
        
        if(response.ok){
            navigate('/messagesent')
            return null
        }
        return "We couldn't send your message right now. Please try again in a few minutes."
    } catch (error) {
        console.error('Failed to send email:', error)
        // csrfFetch throws "HTTP error! Status: 429 - <server message>" for non-OK responses
        return friendlyAuthError(error.message, "We couldn't send your message right now. Please try again in a few minutes.")
    }
}

export const ContactUs = () => {
    const [subject, setSubject] = useState('')
    const [body, setBody] = useState('')
    const [email, setEmail] = useState('')
    const [errorMessage, setErrorMessage] = useState('')
    const [sending, setSending] = useState(false)
    const navigate = useNavigate()
    useEffect(()=>{
        scrollTo(0,0)
    }, [])
    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-2xl mx-auto">
                <p className="uppercase tracking-widest text-sm font-bold text-[#7fd3e6]">Contact us</p>
                <h1 className="mt-2 text-3xl sm:text-5xl font-extrabold">Send us a note!</h1>
                <p className="mt-4 text-lg text-gray-200">Whether you've got a question about a quiz problem you can't crack, there's an irritating bug that you'd love us to get rid of, or you (dare we say it!?) just want to give us a pat on the back (eep!), go ahead and send us a note. And by us I mean me. I'd love to hear your thoughts.</p>
                <form className="mt-8 panel rounded-3xl p-6 sm:p-8 space-y-4" onSubmit={async (e) => {
                    e.preventDefault()
                    setSending(true)
                    setErrorMessage(await sendEmail(subject, email, body, navigate) || '')
                    setSending(false)
                }}>
                    <label className="block">
                        <span className="text-sm font-bold text-gray-300">Subject</span>
                        <input className="field mt-1" placeholder="What's this about?" onChange={(e) => setSubject(e.target.value)} />
                    </label>
                    <label className="block">
                        <span className="text-sm font-bold text-gray-300">Your email</span>
                        <input className="field mt-1" type="email" placeholder="So we can write back" onChange={(e) => setEmail(e.target.value)} />
                    </label>
                    <label className="block">
                        <span className="text-sm font-bold text-gray-300">Message</span>
                        <textarea className="field mt-1 h-56 resize-y" placeholder="Penny for your thoughts? Too much?" onChange={(e) => setBody(e.target.value)}></textarea>
                    </label>
                    {errorMessage && <p className="font-bold text-[#FF6FAE]" role="alert">{errorMessage}</p>}
                    <button type="submit" className="btn-primary px-7 py-3" disabled={sending}>
                        <i className="fa-solid fa-paper-plane"></i> {sending ? 'Sending…' : 'Send it'}
                    </button>
                </form>
            </div>
        </div>
    )
}
