import { useSelector } from "react-redux"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { selectUserChapters } from "../Slices/selectors"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // const units_names = Object.values(units)
    const bookChapters = useSelector((state)=>state.chapters)
    const userChapters = useSelector((state)=>state.userChapters)
    const chapters = 
        Object.keys(userChapters).reduce((result, key) => {
            result[key] = bookChapters[key]
            ?{...userChapters[key], ...bookChapters[key]}
            : userChapters[key]
        return result
        }, {})
    
    const chaptersObj = Object.values(chapters)
    const chaptersEnt = Object.entries(chapters)

    const [expandedUnits, setExpandedUnits] = useState({})
    const navigate = useNavigate()
    const userProg = useSelector((state)=>state.topicProg)
    const topics = useSelector((state)=>state.topics)
    const userTopicProg = Object.keys(userProg).reduce((acc, key) => {
        if(topics[key]) {
            acc[key] = {
                ...userProg[key],
                ...topics[key]
            }
        }
        return acc;
    }, {})

    const userTopicVals = Object.values(userTopicProg)
    const userTopicEntries = Object.entries(userTopicProg)


    const toggleUnit = (unitId) => {
        setExpandedUnits((prevState)=>({
            ...prevState,
            [unitId]: !prevState[unitId]
        }))
    }

    const generatePraise = () => {
        const praise = ['Nailed it ', 'Killed that quiz ', 'Destroyed it ', 'Proved you are a boss ', 'Dayy Bao Bao ', 'Was da bomb ', 'Aced it ', 'Proved your awesomeness ']
        const num = Math.floor(Math.random()*7)
        return(praise[num])
    }

    const skillsButton = () => {
        return(
            <span className='text-xxs w-1/3 text-center leading-3'>+Click to Expand</span>
        )
    }

    const quizProgress = (chapter) => {
        if(chapter.quiz_grade){
            if(chapter.quiz_grade > 50){
                return(
                    <>
                        <div className='sm:text-center w-full text-center -ml-1 sm:w-1/2 text-xs sm:items-center'><span className='text-2xl'>🏆  </span><div className='font-extrabold text-rose-500 text-lg'>{chapter.quiz_grade}</div></div>
                    </>
                )
            } else {
                return(
                    <>
                        <div className='flex flex-col justify-center items-center'>
                            <div className='text-center text-2xl'> 🤢
                            </div>
                            <div className='text-center '>Try Again</div>
                         
                        </div>
                        {/* {skillsButton()} */}
                    </>
                )
            }
        } else if (chapter.video_completed){
            return(
                <div className='-ml-2 sm:-ml-0 flex flex-col items-center'><div className='flex justify-between w-full'><div className='text-2xl hidden sm:inline'>🚀</div><span className='button !h-8 !w-20 !text-[12px] leading-none'>Jump to Quiz</span></div><div><span className='text-center hidden sm:inline'>You're Ready!</span><span className='inline sm:hidden'>READY!</span></div></div>
            )
        } else {
            return(
                <><span className='text-center'>Not Taken<span className='hidden sm:inline'> - watch vid first</span></span></>
            )
        }
    }
    const vidProgress = (chapter) => {
        if(chapter.video_completed && chapter.video_completed == true){
            return(
                <div className='text-center text-xl'>✅</div>
            )
        } else {
            return(
                <>
                    <div className='text-center'>No<span className='hidden sm:inline'>t Yet</span>!</div>
                </>
            )
        }
    }

    const openTopicQuiz = (chapterTopics) => {
        
        navigate('/quiz', {state: {chapter: 1, type: 'topicQuiz', topics: chapterTopics}})
    }

    

    const mastery = (chapterId) => {
        const chapter_topics = []
        
        userTopicEntries.forEach(([topicId, topic]) => {
            if(topic.chapter_id==chapterId){
                chapter_topics.push({...topic, topic_id: topicId})
            }
        }) 

        let sum = 0
        chapter_topics.forEach(chapter => {
            sum += chapter.percent_correct
        })

        const averagePercentCorrect = chapter_topics.length > 0 ? sum/chapter_topics.length : 0

        let reply=""
        if(averagePercentCorrect > 80){
            reply = 'Econo-ninja-level'
        } else if (averagePercentCorrect > 70){
            reply = 'Fiscal Phenom'
        } else if (averagePercentCorrect > 60) {
            reply = 'Curve Whisperer'
        } else if (averagePercentCorrect > 50) {
            reply = 'Sort of Chart Challenged'
        } else if (averagePercentCorrect > 0) {
            reply = 'A bit Econ-fused'
        } else {
            reply = 'Not yet started'
        }

        return(
            <div className='flex flex-col items-left sm:items-center'>
                <div>{reply}</div>
                {reply !== 'Not yet started' && <div className="button !h-4 !text-xs sm:mt-2"
                            onClick={(event) => {
                                event.stopPropagation(); 
                                console.log('DOOBIE', chapter_topics)
                                openTopicQuiz(chapter_topics);
                            }}
                            ><span> <span className='hidden sm:inline'> Take Practice</span> Quiz</span></div>}
            </div>
        )
    }

    
    const unitChapters = (unitId) => {
        const chaptersUnits = chaptersEnt.filter(([chapterId, chapter])=>chapter.unit_id == unitId)

        return(
            <>
                <div className='flex bg-[#0088a8] text-white h-8 items-center w-100 text-xs sm:text-sm'>
                    <div className='sm:ml-8 ml-2 font-semibold sm:w-1/2 w-5/12 text-s'>Chapter Name</div>
                    <div className='w-1/6 font-semibold text-s text-center'>Watched<span className='sm:inline hidden'> Video</span>?</div>
                    <div className='w-1/6 font-semibold text-s text-center '><span className='sm:inline hidden'>Chapter </span>Quiz <span className='sm:inline hidden'>Status</span></div>
                    <div className='w-1/6 font-semibold text-s text-center '> <span className='sm:inline hidden'>Topics </span>Mastery</div>
                </div>
                {chaptersUnits.map(([chapterId, chapter], index)=>{
                    const odd = index % 2 == 0
                    return(
                        <div key = {chapterId} className={`w-100 flex items-center ${odd ? 'bg-[#97AFB9]' : 'bg-[#B8C7C9]'}`}>
                            <div className='sm:ml-8 ml-2 my-2 sm:w-1/3 w-1/4 font-semibold text-xs sm:text-base '>
                                {chapter.name}

                            </div>
                            <div className='w-[15%] sm:w-1/6 flex items-right justify-end'>
                                <div onClick = {()=>navigate(`/video/${chapterId}`)} className=
                                        'button my-4 sm:my-0 sm:py-1 sm:w-1/2 !pl-0 !pr-0 !text-[10px] !rounded-lg'
                                        
                                        >{chapter.video_completed ? <>Watch Video Again!</> : <>Jump To Video</>}</div>
                                </div>
                            <div className='justify-around text-xs font-bold flex items-center w-1/5 sm:w-1/6 sm:text-sm'>
                                {vidProgress(chapter)}
                                
                            </div>
                            <div className='justify-left sm:justify-center -ml-2 sm:-ml-0 sm:my-2 items-start  sm:items-center text-xs sm:text-md font-bold flex items-center w-1/5 mr-2 sm:mr-0 sm:w-1/6'>
                                {quizProgress(chapter)}
                            </div>
                            <div className='justify-center items-center  text-xs sm:text-sm font-bold flex  text-center -ml-2 sm:-ml-0 sm:items-center w-1/5 sm:w-1/6'>
                                {mastery(chapterId)}
                            </div>
                        </div>
                    )
                })}
            </>
        )
    }

    const percentUnitCompleted = (unitId) =>{
        const chaptersUnits = chaptersObj.filter((chapter)=>chapter.unit_id == unitId)
        let totalUnitsCompleted = 0 
        chaptersUnits.forEach((chapter) => {
            if(chapter.quiz_grade && chapter.quiz_grade >=60){
                totalUnitsCompleted +=0.5
            }
            if(chapter.video_completed){
                totalUnitsCompleted += 0.5
            }
        })
        const percentComplete = Math.floor((totalUnitsCompleted / chaptersUnits.length) * 100)
        if(percentComplete > 0){
            return (
                <>{percentComplete}% completed</>
            )
        } else {
            return (
                <>Not yet started</>
            )
        }
    }

    return(
        <div className='w-11/12 bg-white rounded-3xl shadow-2xl p-5'>
            <h1 className='sm:text-4xl text-2xl text-center sm:mb-8 mb-4'>Your Study Plan</h1>
            <div className='flex flex-row justify-around'>
            <div className='w-full'>
                <div className='flex flex-row w-100 mb-2 bg-'>
                    <span className='sm:text-3xl text-xl text-left font-bold w-2/3'>Units</span>
                    <span className='sm:text-3xl hidden sm:block text-xl text-center font-bold w-1/5'>Progress</span>
    
                </div>
                {Object.entries(units).map(([key, value])=>{
                    return(
                        < div key={key}>
                            <div className='w-100' key={key}>
                            <div className='flex w-100'>
                                <div 
                                    className='text-left sm:text-xl text-sm cursor-pointer w-full sm:w-2/3'
                                    onClick ={()=>toggleUnit(key)}>
                                    {expandedUnits[key] ? ' -' : ' +'}  {value.name}
                                </div>
                                <div className='sm:w-1/5 hidden sm:block text-center'>
                                    {percentUnitCompleted(key)}
                                </div>
                            </div>
                            {expandedUnits[key] && (<div className='w-100 '>
                                {unitChapters(key)}
                            </div>
                            )}
                            </div>
                        </div>
                    )
                })}
            </div>

            </div>
        </div>
    )
}