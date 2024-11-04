import { useSelector } from "react-redux"
export const FinishUnit = () => {
    const currentChapter = useSelector(state=>(state.user.currentChapter))
    const chapters = useSelector(state=>(state.chapters))
    const userChapters = useSelector(state=>(state.userChapters))
    const units = useSelector(state=>(state.units))
    const topicProg = useSelector(state=>(state.topicProg))

    const currentUnitId = chapters[currentChapter].unit_id -1
    
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
                </div>
            </div>
        </div>
    )
}