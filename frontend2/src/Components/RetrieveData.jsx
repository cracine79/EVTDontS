import { useLocation } from "react-router-dom"
import { useState } from "react"
import { csrfFetch } from "../csrf"


export const RetrieveData = () => {

    const location = useLocation()
    const [email, setEmail] = useState("")
    const [firstBoxStatus, setFirstBoxStatus] = useState(true)
    const [successBoxStatus, setSuccessBoxStatus] = useState(false)
    const [errorMessageVisible, setErrorMessageVisible] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")


    const source = location.state?.source

    const handleSubmit = async () => {
        try{
            if(source == 'forgotPassword'){
                const response = await csrfFetch('/api/retrieve/password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({email})
                })

                if(!response.ok){
                    setErrorMessageVisible(true)
                } else {
                    setFirstBoxStatus(false)
                    setSuccessBoxStatus(true)
                    setErrorMessageVisible(false)
                    window.scrollTo(0,0)
                }
                const output = await response.json()


            } else if (source == 'forgotUsername'){
                const response = await csrfFetch('/api/retrieve/username', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({email})
                })


                if(!response.ok){
                    setErrorMessageVisible(true)
                } else {
                    const data = await response.json()
                    window.scrollTo(0,0)
                    setFirstBoxStatus(false)
                    setSuccessBoxStatus(true)
                    setErrorMessageVisible(false)
                }
            }
        } catch (error) {
            console.error('POOP', error)
            setErrorMessageVisible(true)
        }

    }

    const submitAgain = () => {
        setFirstBoxStatus(true)
        setSuccessBoxStatus(false)
    }
    return(
        <div className='sm:mt-48 mt-32 flex flex-col items-center h-full min-h-screen'>
            <div className='sm:w-5/6 md:w-2/3 lg:w-1/2 flex flex-col items-center shadow-2xl rounded-lg'>
            {firstBoxStatus &&<>
                <form className='flex flex-col  items-center w-100' onSubmit ={(event)=>{
                    event.preventDefault()
                    handleSubmit()
                }}>
                    {source == 'forgotPassword' &&
                    <>
                        <p className = 'sm:my-4 text-2xl'>
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
                        <input placeholder = 'Submit Email to Reset Password' className='p-2 lg:w-1/2 w-5/6 border-2 border-neutral-300 my-4' onChange={(e)=>{setEmail(e.target.value)}}></input>
                        <input type="submit" value='Send Password Reset Email' className='my-6'></input>
                    </>
                    }
                    {
                        source == 'forgotUsername' &&
                        <>
                            <p className = 'my-4 text-2xl'>
                            Forgot your username, huh?
                        </p>
                        <p className = 'text-xl mx-8 my-2'>Oh, forgotten your username, have you? Classic. Don’t worry; it happens to the best of us—and by ‘best,’ we mean people who may have a dozen variations of the same username across different platforms. Just pop your email into the box below, and we’ll send your username straight to your inbox. Because who needs memory when you’ve got us?</p>
                        <input placeholder = 'Submit Email to Retrieve Username' className='p-2 lg:w-1/2 w-5/6 border-2 border-neutral-300 my-4' onChange={(e)=>{setEmail(e.target.value)}}></input>
                        <input type="submit" value='Send Username To My Email' className='my-6'></input>
                        </>
                    }
                    {errorMessageVisible && <p className="mb-6 text-red-600 text-xs">There was a problem finding your account.  Please check email and try again.</p>}
                </form>
            </>
            }
            {successBoxStatus && <>
            <div className='text-xl p-8'>
                {source == 'forgotPassword' && <>
                <p>A password reset email has been sent to your email address.  Please check for further instructions</p>
                </>}
                {source == 'forgotUsername' && <>
                <p>An email with your username has been sent to your email.</p>
                </>}
                <p>Be sure to check your spam folder as well, because your email inbox might hate us for some unfathomable reason.</p>
            </div>
            <button className='mb-8' onClick={submitAgain}>Submit email again</button>
            
            </>}
            
            </div>
        </div>

    )
}