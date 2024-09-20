
import { SelectUnitsForm } from "./UnitChoiceForm"
export const GetStarted = () => {
    return(
        <>
           <div className="mt-28 flex  w-full justify-center">
                <div className='w-3/4 flex flex-col items-center'>
                    <div className='text-3xl mt-10'>Welcome to EVTDS: Lowering Your Expectations Since... Well, Now!</div>
                    <div className='flex justify-around flex-row mt-10'>
                        <div className='w-2/3'>
                            <div className='text-xl shadow-lg rounded-2xl'>

                                <div>&nbsp;</div>
                                <div className='mx-4'>Welcome to EVTDS (Economics Videos That Don’t Suck)! 🎉 We can’t believe 
                                    it either—you signed up! Did we mention we’re ridiculously excited? Like, 
                                    "economists spotting an error in a government budget" level of excitement. 
                                    🧐 You, my friend, have just joined a group of elite learners who are ready 
                                    to unravel the mysteries of supply, demand, and why avocado toast costs more 
                                    than your rent.</div>
                                <div>&nbsp;</div>
                                <div className='mx-4'>
                                First things first: let's get you rolling! The next step is to choose the units 
                                you want to study. It’s like picking out the episodes of a show that actually 
                                teach you something (without putting you into a deep nap). Once you’ve made your 
                                selections, you’ll get to enjoy our signature blend of videos that don’t suck, 
                                because—let’s be honest—some econ videos really do. We’re fixing that one laugh at a time.
                                </div>
                                <div>&nbsp;</div>
                                <div className='mx-4'>
                                Here’s how it works: watch the video, then strut your stuff in a review quiz. 
                                You might crush it. You might… not. But don’t worry, we’ve got your back! Our 
                                fancy algorithm will remember what tripped you up (yeah, we know, algorithms 
                                are spooky like that). The next time around, it’ll throw you questions that 
                                help you face your quiz demons, so you can tackle those wrong answers like a pro.
                                </div>
                                <div>&nbsp;</div>
                                <div className='mx-4'>
                                So buckle up—it’s going to be a fun, thrilling, hopefully not soul-crushing 
                                ride through the magical world of economics. If at any point you’re wondering 
                                "What have I done?" don’t worry—you’re exactly where you need to be. 🚀   
                                </div>

                            </div>
                    
                        </div>
                        <SelectUnitsForm />
                    </div>
                </div>
               
           </div>
        </>
    )
}