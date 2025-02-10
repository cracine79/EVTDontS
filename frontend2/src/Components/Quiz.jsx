import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { useEffect } from "react"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { useState } from "react"


export const Quiz = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const chapter = location.state?.chapter
    const type = location.state?.type
    const topics = location.state?.topics
    const unitQuizUnitId = location.state?.unit
    const units = useSelector(state=>state.units)
    const currentUser = useSelector(state=>state.user.username)
    const [quizBlurb, setQuizBlurb] = useState("")
    const [quizBlurbImgUrl, setQuizBlurbImgUrl] = useState("")
    console.log('TOPICS', topics)
    const data = {
        chapter: chapter,
        type: type,
        topics: topics
    }
     
    const currentUnit = units[unitQuizUnitId]

    useEffect(()=>{
        const fetchData = async () => {
            const results =  await dispatch(getQuestions(data))
            
            setQuizBlurb(results.quiz_blurb)
            if(results.quiz_blurb_img_url){
                setQuizBlurbImgUrl(results.quiz_blurb_img_url)
            } else {
                setQuizBlurbImgUrl("https://evtds-seeds.s3.us-east-2.amazonaws.com/inprogresscartoon.png")
            }
            
         
        }
        fetchData()
        window.scrollTo(0,0)
        
    }, [dispatch, data]
        
    )
    
    
    const wholeChapter = useSelector((state)=>state.chapters[chapter])

    // const currentUnit = wholeChapter ? useSelector((state)=>state.units[wholeChapter.unit_id]) : ""
    const chapterName = wholeChapter ? wholeChapter.name : ''

    const names = topics.map(topic => topic.topic_name)
    const shortened = names.length - 3
    const formattedNames = names.length == 1
    ? names.slice(0, -1).join (' and ') + ' and ' + names[names.length -1]    
    : names.length == 2
    ? names.join(' and ')
    : names.length > 3
    ? names.slice(0,3).join(', ') + ' and ' + shortened + ' more. '
    :names.length > 2 
    ? names.slice(0, -2).join (', ') + ', ' + names[names.length -2] + ', and ' + names[names.length -1]     
    : names[0]

    const handleOpen = () => {
        dispatch(openQuizModal())
    }
    const goHome = ()=>{
        dispatch(clearQuestions())
        if(currentUser){
            navigate('/userhome')
        } else {
            navigate('/videoindex')
        }
    }

    const quizTopicList = () => {
        return(
            <>
            {names.map((name)=>{
                return(<>name</>)
            })}
            </>
        )


    }
    
    const weaknessBlurb = () => {
        return(
            <>
               <div className="max-w-10xl    mt-24 sm:mt-32 sm:min-h-[65vh] ml-20 px-8 grid grid-cols-1  sm:grid-cols-2  items-center">
                
                <div>
                    <div className='sm:text-2xl w-5/6 text-xl text-center'>
                            <div className='sm:text-3xl sm:mb-4'>
                           Welcome to the Quiz of Reckoning
                            </div>
                            <p className='text-lg'>You’ve bravely clicked your way here, which means you're ready to face the ultimate showdown: you vs. your weak spots. Every wrong answer, every forgotten concept, every question that left you scratching your head is back—like the ghost of marginal utility haunting your economic soul. Don’t be surprised if your quiz is filled with questions from the topics you’d rather forget. Scarcity of knowledge? Let’s fix that. This quiz is designed to hit where it hurts—so we can turn those weaknesses into strengths.</p>
                            <p className='my-6 text-lg'>Take a deep breath and dive in. Remember, this is not just about acing the quiz—it’s about growth. The more you lean into your weak spots, the more of an econo ninja you’ll become. Every mistake is just another step toward mastery, and every correct answer is one closer to total economic enlightenment. So take the quiz, do your best, and don’t let a few wrong answers derail you. Weakness today, strength tomorrow!</p>

                    </div>
                </div>
                <div>
                <div className ='sm:w-5/6'>
                                <img src = "https://evtds-seeds.s3.us-east-2.amazonaws.com/Econ+and+kung+fu.png" />
                            </div>
                </div>
            </div>
            </>
            // <div className='flex flex-col items-center w-3/4 mt-40'>
            //     <p className='text-2xl font-bold mb-4'>Welcome to the Quiz of Reckoning!</p>
            //     <p>You’ve bravely clicked your way here, which means you're ready to face the ultimate showdown: you vs. your weak spots. Every wrong answer, every forgotten concept, every question that left you scratching your head is back—like the ghost of marginal utility haunting your economic soul. Don’t be surprised if your quiz is filled with questions from the topics you’d rather forget. Scarcity of knowledge? Let’s fix that. This quiz is designed to hit where it hurts—so we can turn those weaknesses into strengths.</p>
            //     <p className='my-6'>Take a deep breath and dive in. Remember, this is not just about acing the quiz—it’s about growth. The more you lean into your weak spots, the more of an econo ninja you’ll become. Every mistake is just another step toward mastery, and every correct answer is one closer to total economic enlightenment. So take the quiz, do your best, and don’t let a few wrong answers derail you. Weakness today, strength tomorrow!</p>

            // </div>
        )
    }

    const topicQuizBlurb = () => {
        return(
            <div className='my-2 mt-20 items-center justify-center flex flex-col'>
                <div className='text-3xl'>Welcome To "The Choose Your Own Adventure Quiz"</div>
                <div className='my-4'>
                Ah, the sweet smell of ambition mixed with just a hint of self-doubt. You’ve decided to tackle specific topics, which is either a bold display of confidence or a creative way to procrastinate on everything else. Either way, here you are, ready to put your economic prowess to the test. If you crush it, your topic ratings will skyrocket, and you'll be strutting around like the Gordon Ramsay of graphs and supply curves. But if things go south, don't worry—we’ll only mock you a <em>little</em> and save the heavy sarcasm for your next attempt. Progress, right?
                </div>
                <div>
                No matter what happens, you’re already ahead of the crowd for showing up and sharpening your skills. (Seriously, do you know how many people just watch cat videos instead of studying?) So pat yourself on the back, get that smirk ready, and dive in. Whether you ace it or faceplant, at least you can say you tried—unlike that kid in the back of class who’s still arguing that opportunity cost is “just a suggestion.” Good luck, quiz champion!
                </div>
                <div>Today, you have chosen to face down the topics of:</div>
                {Object.values(topics).map((topic, index)=>{
                    return(<div id={topic.topic_id}>
                        {index + 1}. {topic.topic_name}
                    </div>)
                })}
            </div>
        )
    }

    return(
        <div className='flex flex-col justify-center items-center'>
             {(type == 'chapterQuiz' || type =='chapterQuizNoUser')  && 
            <div className="max-w-10xl   mt-24 sm:mt-32 sm:min-h-[65vh] sm:ml-20 px-8 grid grid-cols-1  sm:grid-cols-2  items-center">
                
                <div>
                    <div className='sm:text-2xl sm:w-5/6 text-xl text-center'>
                            <div className='sm:text-4xl text-3xl sm:mb-4'>
                            Are You Ready To Rock?
                            </div>
                            <div>
                            Get Ready to Take the Quiz for: <p className='font-bold'>Chapter {chapterName}</p>
                            </div>
                            <div className ='sm:w-full sm:hidden '>
                                <img src = {quizBlurbImgUrl} />
                            </div>
                            <div className = 'whitespace-pre-line mt-8  w-full  text-left text-xl' dangerouslySetInnerHTML={{__html: quizBlurb}}>
                            {/* {quizBlurb} */}
                            </div>
                    </div>
                </div>
                <div>
                <div className ='sm:w-full hidden sm:block'>
                                <img src = {quizBlurbImgUrl} />
                            </div>
                </div>
            </div>}
            {type == 'topicQuiz' && <div className='flex flex-col items-center w-3/4'>
                                                <div className='text-3xl'>
                                                Welcome to the "Choose Your Own Quiz Adventure"</div>
                                                <div className='my-2 text-xl'>Now testing the topics of {formattedNames}
                                                </div>
                                                {topicQuizBlurb()}
                                            </div>}
                    {type == 'shortWeakspotQuiz' && weaknessBlurb()}
                    {type == 'unitQuiz' && <>This is the page for Unit Quiz on {currentUnit.name}</>}
            <div className='flex sm:justify-center items-center w-full mt-8 mb-12 flex-col sm:flex-row'>
                <button className="button !text-base w-3/4 sm:w-[12%] h-12 !py-0 !px-4 my-4 !rounded-3xl" onClick={handleOpen}>Start The Quiz</button>
                <div className='w-[16%] hidden sm:block'></div>
                <button className="button !text-base w-3/4 sm:w-[12%] h-12 !py-0 !px-4 my-4 !rounded-3xl"
                            onClick={goHome}>{currentUser ? <>Back to Dashboard</> : <>Back to Videos</>}</button>
            </div>
            <QuestionComponent chapter={chapter} type={type} topics={topics} unit={unitQuizUnitId}/>
        </div>
   
    )

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className='sm:mt-40 mt-28 aspect-video justify-center w-full sm:w-3/4'>
                <div className='flex justify-center'>
                    {(type == 'chapterQuiz' || type =='chapterQuizNoUser')  && 
                        <div className='items-center flex flex-col'>
                            <div className='sm:text-2xl w-5/6 text-xl text-center'>
                                <div>
                                Prepare to Show Your Stuff! 
                                </div>
                                <div>
                                This is the quiz for Chapter {chapterName}
                                </div>
                            </div>
                            <div className ='mt-6 sm:w-5/12'>
                                <img src = {quizBlurbImgUrl} />
                            </div>
                            <div className = 'whitespace-pre-line mt-8 sm:w-3/4 w-5/6 text-center' dangerouslySetInnerHTML={{__html: quizBlurb}}>
                                {/* {quizBlurb} */}
                            </div>
                        </div>}
                    {type == 'topicQuiz' && <div className='flex flex-col items-center w-3/4'>
                                                <div className='text-3xl'>
                                                Welcome to the "Choose Your Own Quiz Adventure"</div>
                                                <div className='my-2 text-xl'>Now testing the topics of {formattedNames}
                                                </div>
                                                {topicQuizBlurb()}
                                            </div>}
                    {type == 'shortWeakspotQuiz' && weaknessBlurb()}
                    {type == 'unitQuiz' && <>This is the page for Unit Quiz on {currentUnit.name}</>}
                </div>
                <div>
                  
                </div>
                <div className='flex justify-center w-full mt-8 mb-12'>
                    <button className="button !text-base !py-0 !px-4 my-4 !rounded-3xl" onClick={handleOpen}>Start The Quiz</button>
                    <div className='w-20'></div>
                    <button className="button !text-base !py-0 !px-4 my-4 !rounded-3xl"
                            onClick={goHome}>{currentUser ? <>Back to Dashboard</> : <>Back to Videos</>}</button>
                    </div>
               
                </div>
            <QuestionComponent chapter={chapter} type={type} topics={topics} unit={unitQuizUnitId}/>
        </div>
      
    )
}