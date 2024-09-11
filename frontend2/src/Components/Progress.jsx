import { useSelector } from "react-redux"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // console.log(units)
    const units_names = Object.values(units)
    console.log(units_names)
    return(
        <div className='w-3/5 bg-white rounded-3xl shadow-2xl p-5'>
            <h1 className='text-4xl text-center mb-8'>Your Study Plan</h1>
            <div className='flex flex-row justify-around'>
            <div>
                <p className='text-2xl text-left font-bold'>Units</p>
                {units_names.map((unit_name, idx)=>{
                    return(
                        <div className='text-left text-xl'key={idx}>
                            {unit_name}
                        </div>
                    )
                })}
            </div>
            <div><p className='text-2xl text-center font-bold'>Progress</p></div>
            <div><p className='text-2xl text-center font-bold'>Mastery</p></div>
            </div>
        </div>
    )
}