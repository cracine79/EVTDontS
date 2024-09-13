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
    const unitChapters = (unitId) => {
        const chaptersUnits = chaptersObj.filter((chapter)=>chapter.unit_id == unitId)
        return(
            <>

                {chaptersUnits.map((chapter)=>{
                    return(
                        <>
                            <div className='ml-8 my-2'>
                            {chapter.name}
                            </div>
                        </>
                    )
                })}
            </>
        )
    }

    return(
        <div className='w-3/5 bg-white rounded-3xl shadow-2xl p-5'>
            <h1 className='text-4xl text-center mb-8'>Your Study Plan</h1>
            <div className='flex flex-row justify-around'>
            <div>
                <p className='text-2xl text-left font-bold'>Units</p>
                {Object.entries(units).map(([key, value])=>{
                    return(
                        <>
                            <div key={key}>
                            <div 
                                className='text-left text-xl cursor-pointer'
                                onClick ={()=>toggleUnit(key)}>
                                {expandedUnits[key] ? ' -' : ' +'}  {value}
                            </div>
                            {expandedUnits[key] && (<div>
                                {unitChapters(key)}
                            </div>
                            )}
                            </div>
                        </>
                    )
                })}
            </div>
            <div><p className='text-2xl text-center font-bold'>Progress</p></div>
            <div><p className='text-2xl text-center font-bold'>Mastery</p></div>
            </div>
        </div>
    )
}