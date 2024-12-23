import { useState } from "react"
import { csrfFetch } from "../csrf"
const sendEmail = async(subject, email, body) => {
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
            console.log('Did it!')
        } else {
            console.log('Problem sending')
        }
    } catch (error) {
        console.error('Failed to send poop:', error)
    }
        
}

export const ContactUs = () => {
    const [subject, setSubject] = useState('')
    const [body, setBody] = useState('')
    const [email, setEmail] = useState('')
    return<>
        <div className="mt-36 flex flex-col items-center">
            <div className='w-7/12 flex flex-col items-center'>
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
                className="border border-black w-full rounded-lg h-[40vh] mb-4 p-2 align-top resize-none" 
                placeholder="Penny for your thoughts? Too much?"
                onChange = {(e)=>{setBody(e.target.value)}}
                ></textarea>

                <button className='mb-6 mt-4
                                border-black 
                                w-1/2 
                                border
                                flex 
                                justify-center 
                                items-center
                                rounded-lg
                                bg-slate-300
                                hover:bg-slate-500
                                font-medium
                                hover:cursor-pointer'
                        onClick = {()=>sendEmail(subject, email, body)}
                        >Fire Away!</button>
            </div>
            
       </div>
    </>
}