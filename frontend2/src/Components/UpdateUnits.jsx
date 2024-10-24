import { useSelector, useDispatch } from "react-redux"
import { useEffect, useState } from "react"
import { getUnitsAndChapters } from "../Slices/unitsActions"


export const UpdateUnits = () => {
    const dispatch = useDispatch()
    const [data, setData] = useState ()
    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await getUnitsAndChapters();
            const results = await response.json(); 
            setData(results); 
            console.log(data)
          } catch (error) {
            console.error('Error fetching units and chapters:', error);
          }
        };
    
        fetchData();
      }, []);

      let subjectsObj = []
      let unitsObj = []
      let chaptersObj=[] 
      let unitIdsWithChapters = []
      if (data){
        const chapters = data.chapters
        const subjects = data.subjects
        const units= data.units
        unitsObj = Object.keys(units).map((key)=>({
          id: key,
          ...units[key]
        }))
        subjectsObj = Object.keys(subjects).map((key)=>({
            id: key,
            ...subjects[key]
        }))
        chaptersObj = Object.keys(chapters).map((key)=>({
          id: key,
          ...chapters[key]
        }))
        unitIdsWithChapters = new Set(Object.values(chapters).map(chapter => chapter.unit_id));
    }
    console.log(subjectsObj)

    const unitsDisplay = (subjectId) => {
        const subjectUnits = unitsObj.filter((unit)=>unit.subject_id==subjectId)
        console.log('unit', {subjectId}, subjectUnits)
        return(
            subjectUnits.map((unit)=>(
                <>
                    <div>{unit.name}</div> 
                    {chaptersDisplay(unit.id)}
                </>
                
            ))
        )
    }

    const chaptersDisplay = (unitId) => {
        const unitChapters = chaptersObj.filter((chapter)=>chapter.unit_id == unitId)
        return(
            unitChapters.map((chapter)=>(
                <>
                    <div>{chapter.name}</div> 
                </>
                
            ))
        )
    }
    const UnitChoiceForm = () =>{
        return(
            <>
                {subjectsObj.map((subject) => (
                <>
                    <div key={subject.id}>{subject.name}</div> 
                {unitsDisplay(subject.id)}
                </>
            ))}
            </>
        )
    }
    return (
        <div className='flex flex-col items-center mt-32'>
            <div className=
                        {`
                        ml-20
                        w-2/3
                        h-auto
                        text-center
                        p-4
                        rounded-2xl 
                        shadow-2xl 
                        flex 
                        flex-col 
                        items-center
                        justify-center`}>
                            <p className='text-2xl mt-6'>You Chose What?!?  Let's Fix This Train Wreck</p>
                            <p className='my-6'> Okay, so maybe you didn’t exactly crush it with your first round of 
                                unit choices. Hey, it happens to the best of us. It’s not the end of the world, 
                                and it’s definitely not the worst mistake you’ll ever make (trust me, we run a 
                                website called Economics Videos That Don’t Suck—We've made some choices too). 
                            </p>
                            <p> Just go ahead and select or deselect what you need below, and we’ll pretend
                                 like you got it right the first time. Then you can get back to the glorious 
                                 videos that definitely don’t suck... we hope. </p>
                            <div className='mt-4'>
                                <UnitChoiceForm />
                            </div>
            </div>
           
        </div>
    )
}