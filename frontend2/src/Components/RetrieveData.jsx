import { useLocation } from "react-router-dom"
import { useState } from "react"
import { csrfFetch } from "../csrf"

export const RetrieveData = () => {

    const location = useLocation()
    const [email, setEmail] = useState("")
   

    const source = location.state?.source

    const handleSubmit = async () => {
        if(source == 'forgotPassword'){
            console.log('gogogo')
            const response = await csrfFetch('/api/retrieve/password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({email})
            })
        }
    }
    return(
        <div className='mt-48 flex flex-col items-center h-full min-h-screen'>
            <div className='w-2/3 flex flex-col items-center shadow-2xl rounded-lg'>
            <form className='flex flex-col  items-center w-100' onSubmit ={(event)=>{
                event.preventDefault()
                handleSubmit()
            }}>
                {source == 'forgotPassword' &&
                <>
                    <p className = 'my-4 text-2xl'>
                        Forgot your password, huh?
                    </p>
                    <p className = 'text-xl mx-8 my-2'>No worries. We get it. Trying to remember passwords these days feels like the ending of The Usual Suspects—just staring at the wall, trying to recall if "hang_in_there" is the magical phrase that unlocks the gateway to some weird website I signed up for at 2 a.m. last month.</p>
                    <p className = 'text-xl mx-8 my-2'>
                        Just enter the email you signed up with, and we’ll send you a 
                        lifeline to reset your password. It’s like getting a second chance 
                        at life—and a way to avoid finding out you signed up for a website 
                        that sends you daily cat horoscope emails. If only this existed back 
                        in 11th grade when I was also trying to figure out my future... 
                        and what the heck that website was.
                    </p>
                    <input placeholder = 'Submit Email to Reset Password' className='p-2 w-1/2 border-2 border-neutral-300 my-4' ></input>
                    <input type="submit" value='Send Password Reset Email' className='my-6'></input>
                </>
                }
            </form>
            
            </div>
        </div>

    )
}