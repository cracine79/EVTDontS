import { useSelector } from "react-redux"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // console.log(units)
    const units_names = Object.values(units)
    const chapters = useSelector((state)=>state.chapters)
    const chaptersObj = Object.values(chapters)
    console.log(units_names)

    const unitChapters = (unitNumber) => {
        return(
            <>
                Chapters for Unit {unitNumber}
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
                            <div className='text-left text-xl'key={key}>
                                +  {value}
                            </div>
                            <div>
                                {unitChapters(key)}
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