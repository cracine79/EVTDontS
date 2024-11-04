import { useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"
export const FinishUnit = () => {
    const navigate = useNavigate()
    const currentChapter = useSelector(state=>(state.user.currentChapter))
    const chapters = useSelector(state=>(state.chapters))
    const userChapters = useSelector(state=>(state.userChapters))
    const units = useSelector(state=>(state.units))
    const topicProg = useSelector(state=>(state.topicProg))


    const currentUnitId = chapters[currentChapter] ? chapters[currentChapter].unit_id -1 : null
    
    console.log('UC', userChapters)
    // const finishedUnit = chapters[currentChapter.unit_id]

    const completeUserChapters = Object.keys(userChapters).reduce((acc, key) => {
        if(chapters[key] && chapters[key].unit_id == currentUnitId){
            acc[key] = {
                ...chapters[key],
                ...userChapters[key],
                chapter_id: key
            }
        }
        return acc
    }, {})

    const chapterResults = () => {
        return(
            Object.values(completeUserChapters).map((chapter)=>{
                return(
                    <div>
                        {chapter.name}
                        {chapter.quiz_grade}
                    </div>
                )
            })

        )
    }

    console.log('cuc', completeUserChapters)

    return(
        <div className='w-screen flex justify-center min-h-screen'>
            <div className="mt-52 w-5/6 h-1/2 border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center mx-4'>               
                    <div className='mt-6'>
                        Congratulations on Finishing {units[currentUnitId]}!
                    </div>
                    <div>
                        You're a beast
                    </div>
                    <div>
                        Results
                    </div>
                    <div>
                        {chapterResults()}
                        
                    </div>
                    <div>
                        Ready for the unit quiz?  Buckle up bucko, it's a 20 question long marathon without the heavy breathing.  Well . . . actually . . . I guess that depends upon how much you are into econ exams.  Okay, that got weird.  You should take the quiz.  You can take it now or later.   Umm, I'm just going to let myself out while you decide.
                    </div>
                </div>
                <div className='flex justify-around'>

                <button  className={`
                                mt-4
                                border-black 
                                
                                w-1/3 
                                border-2 
                                flex 
                                justify-center 
                                items-center
                                rounded-lg
                                bg-slate-300
                                hover:bg-slate-500
                                font-medium
                                hover:cursor-pointer
                                mb-6`}
                                >YEAH BRAH UNIT TEST</button>

                            <button  className={`
                                mt-4
                                border-black 
                                
                                w-1/3 
                                border-2 
                                flex 
                                justify-center 
                                items-center
                                rounded-lg
                                bg-slate-300
                                hover:bg-slate-500
                                font-medium
                                hover:cursor-pointer
                                mb-6`}
                                onClick = {()=>(navigate('/userhome'))}
                                >LATER OK? Country Road Take Me Home</button>
                 </div>
            </div>
        </div>
    )
}