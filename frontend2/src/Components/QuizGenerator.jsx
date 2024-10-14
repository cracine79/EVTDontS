import { useDispatch, useSelector } from "react-redux"
import { getAllTopics } from "../Slices/topicsActions"
import { useEffect, useState } from "react"




export const QuizGenerator = () => {

    const dispatch = useDispatch()
    useEffect(()=>{
        dispatch(getAllTopics())
    },[dispatch])

    const bookTopics = useSelector((state)=>state.topics)
    const userTopics = useSelector((state)=>state.topicProg)
    const [selectedTopics, setSelectedTopics] = useState([])
    console.log(selectedTopics)

    const topics = 
        Object.keys(bookTopics).reduce((result, key)=>{
            result[key] = userTopics[key]
            ?{...bookTopics[key], ...userTopics[key]}
            : bookTopics[key]
        return result
        }, {})
    const topicsEntries = Object.entries(topics)
    const userChapters = useSelector((state)=>state.userChapters)
 
    const studiedIt = (chapter_id) => {
        if (userChapters[chapter_id] && userChapters[chapter_id].video_completed){
            return<>
                You betcha
            </>
        } else {
            return(
                <>Not yet</>
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
    

    const ranking = (averagePercentCorrect) => {
   
        if(averagePercentCorrect > 80){
             return(<>'Econo-ninja-level'
             </>)
        } else if (averagePercentCorrect > 70){
             return(<>'Fiscal Phenom'
                </>)
        } else if (averagePercentCorrect > 60) {
             return(<>'Curve Whisperer'
             </>)
        } else if (averagePercentCorrect > 50) {
             return(<>'Sort of Chart Challenged'
                </>)
        } else if (averagePercentCorrect > 0) {
             return(<>'A bit Econ-fused'
             </>)
        } else {
             return(<>'Not yet started'
                </>)
        }
    }

    const QuizGeneratorBox = () => {
        return(
            <div className='h-full w-100'>
                <div className='w-100 border-black border-solid border flex flex-col items-center'>
                   <span className='text-3xl font-bold my-6'> Select Topics for Quiz</span>
                    <div className="flex w-full px-10 flex-row justify-between">
                        <input type='checkbox'/>
                        <div className='w-1/3  text-xl font-bold'>
                            Topic
                        </div>
                        <div className='w-1/5 text-xl font-bold text-center'>
                            Studied?
                        </div>
                        <div className='w-1/5 text-xl font-bold text-center'>
                            Mastery Level
                        </div>
                    </div>
                 
                    <div className='w-full'>

                
                            {
                                topicsEntries.map(([id, topic])=>{
                                    return(
                                    <div className='w-full px-10 flex justify-between'>
                                        <input type='checkbox'
                                                checked = {selectedTopics.includes(id)}
                                                onChange = {() => handleCheckboxChange(id)}/>
                                        <div key={id} className='w-1/3'>
                                            {topic.topic_name}
                                        </div>
                                        <div className='w-1/5 text-center'> {studiedIt(topic.chapter_id)} </div>
                                        <div className='w-1/5 text-center'> {ranking(topic.percent_correct)} </div>
                                        
                                    </div>
                                    )
                                })
                            }
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