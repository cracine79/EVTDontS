import { useSelector } from "react-redux"
import { useState } from "react"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // console.log(units)
    const units_names = Object.values(units)
    const chapters = useSelector((state)=>state.chapters)
    const chaptersObj = Object.values(chapters)
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
                <>Killed it</>
            )
        } else if (!chapter.video_completed){
            return(
                <>Not yet</>
            )
        } else {
            return(
                <>Watched the Vid</>
            )
        }
    }
    const unitChapters = (unitId) => {
        const chaptersUnits = chaptersObj.filter((chapter)=>chapter.unit_id == unitId)
        return(
            <>

                {chaptersUnits.map((chapter)=>{
                    return(
                        <div className='w-100 flex items-center'>
                            <div className='ml-8 my-2 w-3/5 font-semibold bg-green-300'>
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
                <div className='flex flex-row bg-blue-200 w-100'>
                    <span className='text-2xl text-left font-bold w-3/5 bg-red-200'>Units</span>
                    <span className='text-2xl text-center font-bold w-1/5'>Progress</span>
                    <span className='text-2xl text-center font-bold w-1/5'>Mastery</span>
                </div>
                {Object.entries(units).map(([key, value])=>{
                    return(
                        <>
                            <div className='w-100' key={key}>
                            <div className='flex w-100'>
                                <div 
                                    className='text-left text-xl cursor-pointer w-3/5'
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