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
    const [showModal, setShowModal] = useState(false)

    useEffect(() => {
        window.scrollTo(0, 0);  // Scroll to top when the component mounts
      }, []);

    const bookTopics = useSelector((state)=>state.topics)
    const userTopics = useSelector((state)=>state.topicProg)
    const userChapters = useSelector((state)=>state.userChapters)
    const bookChapters = useSelector((state)=>state.chapters)
    const units = useSelector((state)=>state.units)
    const [selectedTopics, setSelectedTopics] = useState([])


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
            if(selectedTopics[id]==false || !selectedTopics[id]){
                allChecked = false
            }
        })
        return allChecked
    }
    

 
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

    const handleCheckboxChange = (e) => {
        const {name, checked} = e.target
        setSelectedTopics((prevSelected) => ({
            ...prevSelected,
            [name]: checked
        }))
    }

    const handleUnitChange = (e) => {
        const {name, checked} = e.target
        
        const unitTopics = topicsByUnit[name].topics
        unitTopics.forEach((topic)=>{
            setSelectedTopics((prev)=>({
                ...prev,
                [topic.id] : checked
            }))
        })
        
    }

    const makeReviewQuiz = () => {
        const chapter_topics = []
        Object.entries(selectedTopics).forEach(([id, included])=>{
            if(included){
                chapter_topics.push({...bookTopics[id], ...userTopics[id], topic_id: id })
            }
        })
        if(chapter_topics.length < 10){
            navigate('/quiz', {state: {chapter: 1, type: 'topicQuiz', topics: chapter_topics}})
        } else {
            openModal()
        }

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

    const openModal = () => {
        setShowModal(true);
        document.body.style.overflow = 'hidden';
    }

    const closeModal = () => {
        setShowModal(false);
        document.body.style.overflow = '';
    }
    const QuizGeneratorBox = () => {
        return(
            <div className='h-full w-100'>
              
                <div className='w-100 border-black border-solid border flex flex-col items-center'>
                   <div className='text-3xl font-bold mt-6 w-1/2 text-center'> Choose Your Own Adventure!</div>
                   <div className='text-2xl font-bold mb-6 w-1/2 text-center'> Select Topics to Generate Custom Quiz:</div>
                    <div className="flex w-full px-2 sm:px-10 flex-row justify-center items-center">
                        <div></div>
                       
                        <div className='w-11/12  flex justify-between'>
                        <div></div>
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
                    </div>
                 
                    <div className='w-full items-center justify-center flex flex-col'>

                            <div className='w-11/12 border-black border'>
                            {   
                                Object.entries(topicsByUnit).map(([unitId, unit])=>{
                                    return(
                                        <div className='w-full'>
                                            <div key={unitId} className='bg-lime-200'>
                                                <input type='checkbox' name={unitId} className='ml-10 my-4 mr-10' onChange={handleUnitChange} checked = {unitChecked(unitId)} ></input>
                                                {unit.unitName}
                                            </div>
                                            {unit.topics.map((topic)=>{
                                                return(<>
                                                        <div key={topic.id} className='w-full sm:px-10 px-2 flex justify-between flex-row items-center py-2'>
                                                            <input type='checkbox' className='sm:-mr-8' name={topic.id}
                                                                    checked = {selectedTopics[topic.id]}
                                                                    onChange = {handleCheckboxChange}/>
                                                            <div key={topic.id} className='sm:w-1/3 w-1/3 sm:-ml-8 md:-ml-12 -ml-6 text-xs sm:text-md'>
                                                                {topic.topic_name}
                                                            </div>
                                                            <div className='sm:w-1/5 text-center text-xs sm:text-md'> {studiedIt(topic.chapter_id)} </div>
                                                            <div className='sm:w-1/5 w-1/5 text-center text-xs sm:text-md'> {ranking(topic.percent_correct)} </div>
                                                            
                                                        </div>
                                                </>)
                                            })}
                                        </div>
                                        
                                    )
                                })

                            }
                            </div>
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
             <button className="mt-8
                                    border-black 
                                    sm:w-1/3
                                    w-5/12 
                                    text-center 
                                    border
                                    flex 
                                    justify-center 
                                    items-center
                                    rounded-lg
                                    bg-slate-300
                                    hover:bg-slate-500
                                    font-medium
                                    hover:cursor-pointer
                                    `"
                    onClick={()=>(navigate('/Quiz', {state: {chapter: 1, type: 'shortWeakspotQuiz', topics: []}}))}>Let Us Generate a Quiz for You! Based on your Weak Spots!</button>
            <div className='text-3xl mt-6'>OR</div>
            <div className="mt-10 w-5/6 h-full mb-10">
                <QuizGeneratorBox />
            </div>
            <div className={`fixed bg-red-200 flex items-center justify-center top-0 bottom-0 left-0 right-0 bg-gray-800 ${showModal ? 'bg-opacity-70 over' : 'translate-y-full bg-opacity-0'}`}
                  onClick = {()=>{closeModal()}}>
                <div className={`w-1/3 -mt-28 fixed bg-white fixed border rounded p-4 text-center border-black border-solid `}>
                        <p className='text-2xl'>Too Many Topics!!!</p>
                        <p>Rein it in dude!</p>
                        <p>Please choose a maximum of nine topics to review in one quiz</p>
                        
                        <div className="absolute top-1 right-2 hover:cursor-pointer" onClick={()=>{closeModal()}}>&times;</div>
                </div>
            </div>
        </div>
    )
}