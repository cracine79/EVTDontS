import { useState } from "react"
import { csrfFetch } from "../csrf"
import { useNavigate } from "react-router-dom"
import { useEffect } from "react"
const sendEmail = async(subject, email, body, navigate) => {

    try{
        console.log(subject, email, body)
        const response = await csrfFetch('/api/mail/send', {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({subject, email, body})
        })
        
        if(response.ok){
            navigate('/messagesent')
        } else {
            console.log('Problem sending')
        }
    } catch (error) {
        console.error('Failed to send email:', error)
    }
        
}

export const ContactUs = () => {
    const [subject, setSubject] = useState('')
    const [body, setBody] = useState('')
    const [email, setEmail] = useState('')
    const navigate = useNavigate()
    useEffect(()=>{
        scrollTo(0,0)
    }, [])
    return<>
        <div className="mt-32 flex flex-col items-center">
            <div className='sm:w-7/12 xl:w-5/12 w-5/6 flex flex-col items-center'>
                <h1 className='text-center text-3xl'>Send Us A Note!</h1>
                <div className='mt-4'>Whether you've got a question about a quiz problem you can't crack, there's an irritating bug that you'd love us to get rid of, or you (dare we say it!?) just want to give us a pat on the back (eep!), go ahead and send us a note. And by us I mean me.  I'd love to hear your thoughts. </div>
               
                <input 
                className="border border-black w-full rounded-lg mt-6 mb-2 p-2 text-top" 
                placeholder="Subject"
                onChange = {(e)=>{setSubject(e.target.value)}}
                />

                <input 
                className="border border-black w-full rounded-lg  mb-2 p-2 text-top" 
                placeholder="Your Email"
                type='email'
                onChange = {(e)=>{setEmail(e.target.value)}}
                />

                <textarea 
                className="border border-black w-full rounded-lg sm:h-[40vh] h-[20vh] mb-4 p-2 align-top resize-none" 
                placeholder="Penny for your thoughts? Too much?"
                onChange = {(e)=>{setBody(e.target.value)}}
                ></textarea>

                <button className="fancy-button mb-8 !px-8"
                        onClick = {()=>sendEmail(subject, email, body, navigate)}
                        >Send Email!</button>
            </div>
            
       </div>
    </>
}