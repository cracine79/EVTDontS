import { useSelector, useDispatch } from "react-redux"
import { useEffect, useState } from "react"
import { getUnitsAndChapters } from "../Slices/unitsActions"


export const UpdateUnits = () => {
    const dispatch = useDispatch()
    const [data, setData] = useState ()
    const userChapters = useSelector((state)=>state.userChapters)
    const bookChapters = useSelector((state)=>state. chapters)
    const userChapterIds = Object.keys(userChapters)
    const chapterIdMap = userChapterIds.reduce((acc, chapterId) => {
        acc[chapterId] = true;
        return acc;
    }, {});

    const userUnitIds = {}

    console.log(userChapters)

    userChapterIds.forEach((id)=>{
        userUnitIds[bookChapters[id].unit_id] = true
    })

    console.log('THESESAREHTEM', userUnitIds)
    const [selectedChapters, setSelectedChapters] = useState(chapterIdMap)
    const [selectedUnits, setSelectedUnits] = useState(userUnitIds)
    
    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await getUnitsAndChapters();
            const results = await response.json(); 
            setData(results); 
       
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



    const handleUnitChange = (e) => {
        const {name, checked} = e.target;

        const unitChapters = chaptersObj.filter((chapter)=>chapter.unit_id==name)
        const unitChapterIds = unitChapters.map((chapter)=>chapter.id)
        unitChapterIds.forEach((id)=>{
          setSelectedChapters((prevSelectedChapters) =>({
            ...prevSelectedChapters,
            [id]: checked
          }))
        })
        setSelectedUnits((prev)=>({
            ...prev,
            [name]: checked
          }))
      }

    const unitsDisplay = (subjectId) => {
        const subjectUnits = unitsObj.filter((unit)=>unit.subject_id==subjectId)
        
    
    
        
        return(
            subjectUnits.map((unit)=>{
                const hasChapters = unitIdsWithChapters.has(Number(unit.id))
                return(<div key={unit.id} className={`${hasChapters  ? 'mb-6' : ''}`} >
                    <input type='checkbox' className='mx-2' name = {unit.id} onChange = {handleUnitChange} checked = {selectedUnits[unit.id]}disabled={!hasChapters}></input>
                    <label className={`text-2xl ${hasChapters && 'mt-2'}`}>{unit.name}</label> 
                    <div>
                        {hasChapters && <div> {chaptersDisplay(unit.id)}</div>}
                    </div>
                </div>)
            })
                
            
        )
    }


    const handleChapterChange = (e) => {
        const {name, checked} = e.target;
        setSelectedChapters((prev) => ({
            ...prev,
            [name]: checked
          }));
    }

    const chaptersDisplay = (unitId) => {
        const unitChapters = chaptersObj.filter((chapter)=>chapter.unit_id == unitId)
        return(
            unitChapters.map((chapter)=>(
                <div className='ml-4'>
                    <input type='checkbox' onChange={handleChapterChange} name = {chapter.id} checked = {selectedChapters[chapter.id] }></input>
                    <label className='text-md'>{chapter.name}</label> 
                </div>
                
            ))
        )
    }
    const UnitChoiceForm = () =>{
        return(
            <>
                {subjectsObj.map((subject) => (
                <>
                    <div key={subject.id} className='text-3xl'>Topic: {subject.name}</div> 
                    <div className='ml-4'>{unitsDisplay(subject.id)}</div>
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
                            <div className='mt-4 columns-2 gap-16 p-4 text-left'>
                                <UnitChoiceForm />
                            </div>
            </div>
           
        </div>
    )
}