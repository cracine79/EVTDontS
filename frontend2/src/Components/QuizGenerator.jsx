import { useDispatch, useSelector } from "react-redux"
import { getAllTopics } from "../Slices/topicsActions"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"




export const QuizGenerator = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    useEffect(()=>{
        dispatch(getAllTopics())
    },[dispatch])

    const bookTopics = useSelector((state)=>state.topics)
    const userTopics = useSelector((state)=>state.topicProg)
    const userChapters = useSelector((state)=>state.userChapters)
    const bookChapters = useSelector((state)=>state.chapters)
    const units = useSelector((state)=>state.units)
    const [selectedTopics, setSelectedTopics] = useState([])

    const [selectedUnits, setSelectedUnits] = useState({})

    const topics = 
        Object.keys(bookTopics).reduce((result, key)=>{
            result[key] = userTopics[key]
            ?{...bookTopics[key], ...userTopics[key]}
            : bookTopics[key]
        return result
        }, {})
    const topicsEntries = Object.entries(topics)
    const allTopicIds = topicsEntries.map(([id])=>id)

    
    const topicsEntriesWithId = Object.entries(topics).map(([id, topic]) => ({
        ...topic,
        id,
    }));


    const topicsByUnit = topicsEntriesWithId.reduce((unitsGrouped, topic) => {
        const chapter = bookChapters[topic.chapter_id] 
        if (!chapter) return unitsGrouped; // Skip if chapter is not found
    
        const unitId = chapter.unit_id;
        const unit = units[unitId];
        if (!unit) return unitsGrouped; // Skip if unit is not found
    
        if (!unitsGrouped[unitId]) {
            unitsGrouped[unitId] = {
                unitName: unit.name,
                topics: [],
            };
        }
    
        unitsGrouped[unitId].topics.push(topic);
        return unitsGrouped;
    }, {});

    const unitChecked = (unitId) => {
        const unitTopics = topicsByUnit[unitId]
        const unitTopicIds = unitTopics.topics.map((topic)=>topic.id)
        let allChecked = true
        unitTopicIds.forEach((id)=>{
            if(!selectedTopics.includes(id)){
                allChecked = false
            }
        })

        return allChecked
    }

    console.log(selectedTopics)
    

 
    const studiedIt = (chapter_id) => {
        if (userChapters[chapter_id] && userChapters[chapter_id].video_completed){
            return<>
                <span className='hidden sm:block'>You betcha</span>
                <span className='block sm:hidden'>Yes</span>
            </>
        } else {
            return(
                <>
                    <span className='hidden sm:block'>Not yet</span>
                    <span className='block sm:hidden'>No</span>
                </>
            )
        }
        return(<>boobs</>)
    }

    const handleCheckboxChange = (topicId) => {
        setSelectedTopics((prevSelected) => {
            if(prevSelected.includes(topicId)){
                return(prevSelected.filter(id => id !== topicId));
            } else {
                return [...prevSelected, topicId]
            }
        })
    }

    const handleSelectAll = () => {
        setSelectedTopics((prevSelected)=> 
            prevSelected.length === allTopicIds.length ? [] : allTopicIds
        )
    }

    const handleSelectUnitTopics = () => {
        
    }

    const makeReviewQuiz = () => {
        const chapter_topics = []
        selectedTopics.forEach(id=>{
            chapter_topics.push({...bookTopics[id], ...userTopics[id], topic_id: id })
        })

        navigate('/quiz', {state: {chapter: 1, type: 'topicQuiz', topics: chapter_topics}})
    
    }
    

    const ranking = (averagePercentCorrect) => {
   
        if(averagePercentCorrect > 80){
             return(<>Econo-ninja-level
             </>)
        } else if (averagePercentCorrect > 70){
             return(<>Fiscal Phenom
                </>)
        } else if (averagePercentCorrect > 60) {
             return(<>Curve Whisperer
             </>)
        } else if (averagePercentCorrect > 50) {
             return(<>Sort of Chart Challenged
                </>)
        } else if (averagePercentCorrect > 0) {
             return(<>A bit Econ-fused
             </>)
        } else {
             return(<>
             <span className='hidden sm:block'>Not yet started</span>
             <span className='block sm:hidden'>/</span>
                </>)
        }
    }

    const QuizGeneratorBox = () => {
        return(
            <div className='h-full w-100'>
                <div className='w-100 border-black border-solid border flex flex-col items-center'>
                   <span className='text-3xl font-bold my-6'> Select Topics for Quiz</span>
                    <div className="flex w-full px-2 sm:px-10 flex-row justify-between items-start">
                        <input type='checkbox' className='mt-2 sm:-mr-8'
                                onChange = {()=>handleSelectAll()
                                }
                                checked = {selectedTopics.length === allTopicIds.length}
                                />
                        <div className='sm:text-xl w-1/3  font-bold sm:-ml-12 '>
                            Topic
                        </div>
                        <div className='sm:w-1/5 sm:text-xl font-bold text-center'>
                            Studied?
                        </div>
                        <div className='w-1/5 sm:text-xl font-bold text-center'>
                            Mastery Level
                        </div>
                    </div>
                 
                    <div className='w-full'>

                
                            {   
                                Object.entries(topicsByUnit).map(([unitId, unit])=>{
                                    return(
                                        <>
                                            <div>
                                                <input type='checkbox' className='ml-10 my-4 mr-10' checked = {unitChecked(unitId)} onChange = {()=>handleSelectUnitTopics()}></input>
                                                {unit.unitName}
                                            </div>
                                            {unit.topics.map((topic)=>{
                                                return(<>
                                                        <div className='w-full sm:px-10 px-2 flex justify-between flex-row items-center py-2'>
                                                            <input type='checkbox' className='sm:-mr-8'
                                                                    checked = {selectedTopics.includes(topic.id)}
                                                                    onChange = {() => handleCheckboxChange(topic.id)}/>
                                                            <div key={topic.id} className='sm:w-1/3 w-1/3 sm:-ml-8 md:-ml-12 -ml-6 text-xs sm:text-md'>
                                                                {topic.topic_name}
                                                            </div>
                                                            <div className='sm:w-1/5 text-center text-xs sm:text-md'> {studiedIt(topic.chapter_id)} </div>
                                                            <div className='sm:w-1/5 w-1/5 text-center text-xs sm:text-md'> {ranking(topic.percent_correct)} </div>
                                                            
                                                        </div>
                                                </>)
                                            })}
                                        </>
                                        
                                    )
                                })

                            }
                         </div>
                <div className='flex w-full justify-center mt-8'>
                    <div className='flex sm:w-1/2 justify-around'>

                    <div  className="my-6
                                    border-black 
                                    text-center
                                    sm:w-1/3
                                    w-5/12 
                                    border-2 
                                    flex 
                                    justify-center 
                                    items-center
                                    rounded-lg
                                    bg-slate-300
                                    hover:bg-slate-500
                                    font-medium
                                    hover:cursor-pointer
                                    mb-6`"
                                    onClick = {()=>makeReviewQuiz()}>
                                Create Quiz
                    </div>
                    <div className="my-6
                                    border-black 
                                    sm:w-1/3
                                    w-5/12 
                                    text-center 
                                    border-2 
                                    flex 
                                    justify-center 
                                    items-center
                                    rounded-lg
                                    bg-slate-300
                                    hover:bg-slate-500
                                    font-medium
                                    hover:cursor-pointer
                                    mb-6`"
                            onClick={()=>navigate('/userhome')}>

                                Back to my Dashboard
                    </div>
                    </div>
                </div>        
                </div>
                                       
            </div>
        )
    }
    return(
        <div className='min-h-screen flex flex-col items-center pt-24'>
            <div className='text-center text-3xl font-bold mt-6'>Quiz Generator</div>
            <div className='w-5/6 text-center mt-10'>Welcome to the Quiz Generator—
            where we tirelessly crunch data so you can finally conquer those pesky 
            weak spots that have haunted your econ journey! Think of this as your 
            very own "weakness whacker" (patent pending). Just tell us if you want
             a custom quiz for every unit you've studied so far, or if you'd rather 
             laser-focus on the chapters that really tripped you up. Or, if you're 
             feeling brave (or reckless), go off-script and create your own quiz by 
             topic or chapter! We promise it’ll be almost painless—probably less like 
             pulling teeth and more like... a slightly awkward lecture on interest 
             rates.
             </div>
            <div className="mt-10 w-5/6 h-full mb-10">
                <QuizGeneratorBox />
            </div>
        </div>
    )
}