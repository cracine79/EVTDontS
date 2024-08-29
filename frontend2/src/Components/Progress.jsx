import { useSelector } from "react-redux"

export const Progress = () => {
    const units = useSelector((state)=>state.units)
    // console.log(units)
    const units_names = Object.values(units)
    console.log(units_names)
    return(
        <div className='w-1/2 mt-20 bg-white'>

            <h1 className='text-4xl'>Your Study Plan</h1>
            {units_names.map((unit_name, idx)=>{
                return(
                    <div key={idx}>
                        {unit_name}
                    </div>
                )
            })}
        </div>
    )
}