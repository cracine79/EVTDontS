import { useSelector } from "react-redux"
import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { selectUserChapters } from "../Slices/selectors"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // console.log(units)
    const units_names = Object.values(units)
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
    const userTopicProg = useSelector((state)=>state.topicProg)
    const userTopicVals = Object.values(userTopicProg)


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
                        <div className='text-center w-1/2 text-xs align-middle'>Rocked!! Score: <span className='align-middle font-extrabold text-rose-500 text-lg'>{chapter.quiz_grade}</span></div>
                    </>
                )
            } else {
                return(
                    <>
                        <div className='flex flex-col justify-center items-center'>
                            <div className='text-center '> Gave it a shot.
                            </div>
                            <div className='text-center '>Need more practice</div>
                        </div>
                        {skillsButton()}
                    </>
                )
            }
        } else if (chapter.video_completed){
            return(
                <>Up next!</>
            )
        } else {
            return(
                <>It's coming!</>
            )
        }
    }
    const vidProgress = (chapter) => {
        if(chapter.video_completed && chapter.video_completed == true){
            return(
                <div className='text-center'>YES!</div>
            )
        } else {
            return(
                <>Not Yet!</>
            )
        }
    }

    const openTopicQuiz = (chapterTopics) => {
        
        console.log('CHAPTERTOPICS', chapterTopics)
        navigate('/quiz', {state: {chapter: 1, type: 'topicQuiz', topics: chapterTopics}})
    }

    const mastery = (chapterId) => {
        const chapter_topics = []
        userTopicVals.forEach(topic => {
            if(topic.chapter_id==chapterId){
                chapter_topics.push(topic)
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
            <div className='flex flex-col items-center'>
                <div >{reply}</div>
                {reply !== 'Not yet started' && <div className=
                            'mt-2 
                            border-black 
                            h-1/12 
                            w-1/2 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-sm
                            bg-slate-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            
                            '
                            onClick={(event) => {
                                event.stopPropagation(); // Prevents parent click
                                openTopicQuiz(chapter_topics);
                            }}
                            >Practice</div>}
            </div>
        )
    }

    
    const unitChapters = (unitId) => {
        const chaptersUnits = chaptersEnt.filter(([chapterId, chapter])=>chapter.unit_id == unitId)
        return(
            <>
                <div className='flex bg-green-600 h-8 items-center w-100'>
                    <div className='ml-8 font-semibold w-1/2 text-s'>Chapter Name</div>
                    <div className='w-1/6 font-semibold text-s text-center'>Watched Video?</div>
                    <div className='w-1/6 font-semibold text-s  text-center '>Quiz Status</div>
                    <div className='w-1/6 font-semibold text-s  text-center '> Topics Mastery</div>
                </div>
                {chaptersUnits.map(([chapterId, chapter])=>{
                    const odd = chapterId % 2 == 0
                    return(
                        <div className={`w-100 flex items-center ${odd ? 'bg-green-200' : 'bg-lime-200'}`}>
                            <div className='ml-8 my-2 w-1/3 font-semibold'>
                                {chapter.name}

                            </div>
                            <div className='w-1/6'>
                                <div onClick = {()=>navigate('/Video', {state: {chapter:chapterId}})} className=
                                        'w-3/4 hover:cursor-pointer hover:bg-slate-500 text-xs bg-slate-300 flex items-center justify-center text-center border-black border-2 rounded hover:cursor-pointer'
                                        
                                        >{chapter.video_completed ? <>Watch Video Again!</> : <>Jump To Video</>}</div>
                                </div>
                            <div className='justify-around text-xs font-bold flex items-center w-1/6'>
                                {vidProgress(chapter)}
                                
                            </div>
                            <div className='justify-center items-center  text-xs font-bold flex items-center w-1/6'>
                                {quizProgress(chapter)}
                            </div>
                            <div className='justify-center items-center  text-xs font-bold flex items-center w-1/6'>
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
            <h1 className='text-4xl text-center mb-8'>Your Study Plan</h1>
            <div className='flex flex-row justify-around'>
            <div className='w-full'>
                <div className='flex flex-row w-100 mb-2 bg-'>
                    <span className='text-3xl text-left font-bold w-2/3'>Units</span>
                    <span className='text-3xl text-center font-bold w-1/5'>Progress</span>
    
                </div>
                {Object.entries(units).map(([key, value])=>{
                    return(
                        <>
                            <div className='w-100' key={key}>
                            <div className='flex w-100'>
                                <div 
                                    className='text-left text-xl cursor-pointer w-2/3'
                                    onClick ={()=>toggleUnit(key)}>
                                    {expandedUnits[key] ? ' -' : ' +'}  {value}
                                </div>
                                <div className='w-1/5 text-center'>
                                    {percentUnitCompleted(key)}
                                </div>
                            </div>
                            {expandedUnits[key] && (<div className='w-100 '>
                                {unitChapters(key)}
                            </div>
                            )}
                            </div>
                        </>
                    )
                })}
            </div>

            </div>
        </div>
    )
}