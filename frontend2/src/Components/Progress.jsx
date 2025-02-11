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

    const goToChapterQuiz = (chapterId) => {
        console.log(chapterId)
        navigate('/Quiz', {state:{chapter:chapterId, type:'chapterQuiz', topics:[]}})
    }

    const praiseBlurb = () => {
        const praises = [
            "I'd high-five you...if I could",
            "Are you even human?",
            "You are the Kendrick Lamar of Econ",
            "Keynes would be proud",
            "You're a quiz wizard.  A Quizard!",
            "Did you binge the entire season?",
            "You are The One!  Do you know Kung Fu?",
            "Are you a time traveller from the future?",
            "You are the Tony Stark of Econ"
        ]
        return praises[Math.floor(Math.random()*11)]
    }

    const quizProgress = (chapterId, chapter) => {
        if(chapter.quiz_grade != null){
            if(chapter.quiz_grade > 50){
                return(
                    <>
                        <div className='sm:text-center w-full text-center -ml-1 sm:w-1/2 relative text-xs sm:items-center'>
                        <div className='group'>
                        <div className='absolute 
                                hidden 
                                bg-gray-800 
                                shadow-lg 
                                hover:cursor-pointer  
                                group-hover:block 
                                text-white 
                                text-center 
                                py-1 px-2 
                                 
                                text-xs 
                                rounded-lg' >
                                    {praiseBlurb()}
                                </div>
                            <span className='text-2xl'>🏆 </span>
                            </div>
                            <div className='font-extrabold text-rose-500 text-lg'>{chapter.quiz_grade}</div>
                        </div>
                    </>
                )
            } else {
                return(
                    <>
                        <div className='flex flex-col justify-center relative items-center group'>
                        <div className='absolute 
                                hidden 
                                bg-gray-800 
                                shadow-lg 
                                hover:cursor-pointer  
                                -left-[100%]  
                                group-hover:block 
                                text-white 
                                text-center 
                                py-1 px-2 
                                w-[350%] 
                                text-xs 
                                rounded-lg' 
                        onClick={()=>navigate('/Quiz', {state:{chapter:chapterId, type:'chapterQuiz', topics:[]}})}>Yikes! <br></br> Try the Quiz Again</div>
                            <div className='text-center text-2xl flex'> 
                                 {/* <div className='text-center button !h-6' onClick={()=>goToChapterQuiz(chapterId)}>Try Again</div> */}
                                 🤢 
                            </div>
                            <div className='font-extrabold text-rose-500 text-lg'>
                          {chapter.quiz_grade} 
                            </div>
                           
                         
                        </div>
                        {/* {skillsButton()} */}
                    </>
                )
            }
        } else if (chapter.video_completed){
            return(
                <>
                <div className='sm:-ml-0 flex flex-col justify-center relative items-center group'>
                <div className='absolute 
                                hidden 
                                bg-gray-800 
                                shadow-lg 
                                hover:cursor-pointer  
                                -left-[100%]  
                                group-hover:block 
                                text-white 
                                text-center 
                                py-1 px-2 
                                w-[350%] 
                                text-xs 
                                rounded-lg' 
                        onClick={()=>navigate('/Quiz', {state:{chapter:chapterId, type:'chapterQuiz', topics:[]}})}>You're Ready! <br></br> Take The Quiz</div>
                    <div className='sm:text-3xl text-xl hidden sm:inline'>⚡</div>
                    <div>
                        <span className='inline sm:hidden'>READY!</span>
                    </div>
                </div>
                {/* <span onClick={()=>goToChapterQuiz(chapterId)}className='button !h-8 !w-20 !text-[12px] leading-none'>Jump to Quiz</span> */}
                </>
            )
        } else {
            return(
                <div className='relative group hover:cursor-pointer'>
                    <div className='absolute bg-gray-800 shadow-lg -top-[25%] -left-[50%] hidden group-hover:block text-white text-center py-1 px-2 w-[250%] text-xs rounded-lg'>Watch the Video First</div>
                    <span className='text-center text-3xl hover:cursor-pointer'>🔒</span>
                </div>
            )
        }
    }
    const vidProgress = (chapterId, chapter) => {
        if(chapter.video_completed && chapter.video_completed == true){
            return(
                <div className='relative group hover:cursor-pointer'>
                <div className='absolute bg-gray-800 shadow-lg -top-[25%] -left-[100%] hidden group-hover:block text-white text-center py-1 px-2 w-[300%] text-xs rounded-lg' onClick={()=>{navigate(`/video/${chapterId}`)}}>Watch Video Again</div>
         
                <div className='text-center text-xl'>✅</div>
                </div>
            )
        } else {
            return(
                <>
                    <div className='relative group hover:cursor-pointer'>
                        <div className='absolute bg-gray-800 shadow-lg -top-[50%] -left-[100%] hidden group-hover:block text-white text-center py-1 px-2 w-[300%] text-xs rounded-lg' onClick={()=>{navigate(`/video/${chapterId}`)}}>Jump to Video</div>
                        <div className='text-center'>🔴</div>
                    </div>
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
            reply = 'Marginally Got It'
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
                <div className='flex bg-[#0088a8] text-white h-16 items-center w-100 text-xs sm:text-sm'>
                    <div className='sm:ml-8 ml-2 font-semibold sm:w-1/2 w-5/12 text-xl'>Chapter Name</div>
                    <div className='w-1/6 font-semibold text-xl text-center'>Video<span className='sm:inline hidden'> Status</span></div>
                    <div className='w-1/6 font-semibold text-xl text-center '>Quiz <span className='sm:inline hidden'>Status</span></div>
                    <div className='w-1/6 font-semibold text-xl text-center '> <span className='sm:inline hidden'>Topics </span>Mastery</div>
                </div>
                {chaptersUnits.map(([chapterId, chapter], index)=>{
                    const odd = index % 2 == 0
                    return(
                        <div key = {chapterId} className={`w-100 flex items-center ${odd ? 'bg-[#f1f6fb]' : 'bg-[#d9e4f5]'}`}>
                            <div className='sm:ml-8 ml-2 my-2 sm:w-1/3 w-1/4 font-semibold text-xs sm:text-base '>
                                {chapter.name}

                            </div>
                            <div className='w-[15%] sm:w-1/6 flex items-right justify-end'>
                                <div onClick = {()=>navigate(`/video/${chapterId}`)} className=
                                        'button my-4 sm:my-0 sm:py-1 sm:w-1/2 !pl-0 !pr-0 !text-[10px] !rounded-lg'
                                        
                                        >{chapter.video_completed ? <>Watch Video Again!</> : <>Jump To Video</>}</div>
                                </div>
                            <div className='justify-around text-xs font-bold flex items-center w-1/5 sm:w-1/6 sm:text-sm'>
                                {vidProgress(chapterId, chapter)}
                                
                            </div>
                            <div className='justify-left sm:justify-center -ml-2 sm:-ml-0 sm:my-2 items-start  sm:items-center text-xs sm:text-md font-bold flex items-center w-1/5 mr-2 sm:mr-0 sm:w-1/6'>
                                {quizProgress(chapterId, chapter)}
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
        <div className='w-10/12 bg-white rounded-3xl shadow-2xl p-5'>
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