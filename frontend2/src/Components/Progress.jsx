import { useSelector } from "react-redux"
import { useState } from "react"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // console.log(units)
    const units_names = Object.values(units)
    const chapters = useSelector((state)=>state.chapters)
    const chaptersObj = Object.values(chapters)
    const chaptersEnt = Object.entries(chapters)
    const [expandedUnits, setExpandedUnits] = useState({})



    const toggleUnit = (unitId) => {
        setExpandedUnits((prevState)=>({
            ...prevState,
            [unitId]: !prevState[unitId]
        }))
    }

    const chapterProgress = (chapter) => {
        if(chapter.quiz_grade && chapter.quiz_grade > 50){
            return(
                <>Crushed it</>
            )
        } else if (!chapter.video_completed){
            return(
                <>Not yet</>
            )
        } else {
            return(
                <div className='flex flex-col justify-center items-center'>
                <div className='text-center'> Watched The Sweet Video
                </div>
                <div>Quiz is next!</div>
                </div>
            )
        }
    }
    const unitChapters = (unitId) => {
        const chaptersUnits = chaptersEnt.filter(([chapterId, chapter])=>chapter.unit_id == unitId)
        return(
            <>

                {chaptersUnits.map(([chapterId, chapter])=>{
                    const odd = chapterId % 2 == 0
                    return(
                        <div className={`w-100 flex items-center ${odd ? 'bg-green-200' : 'bg-lime-200'}`}>
                            <div className='ml-8 my-2 w-2/3 font-semibold'>
                                {chapter.name}
                            </div>
                            <div className='justify-center text-xs font-bold -ml-8 flex items-center w-1/5'>
                                {chapterProgress(chapter)}
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
                totalUnitsCompleted +=1
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
        <div className='w-3/5 bg-white rounded-3xl shadow-2xl p-5'>
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