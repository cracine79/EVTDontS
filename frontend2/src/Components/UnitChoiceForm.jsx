import { useState, useEffect } from "react"
import { addUserUnits } from "../Slices/unitsActions";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { getUnitsAndChapters } from "../Slices/unitsActions";
import { SiTrueup } from "react-icons/si";

export const SelectUnitsForm = () => {

  const navigate = useNavigate()
  const dispatch = useDispatch()
  const[data, setData] = useState(null)
  const [showUnits, setShowUnits] = useState({1: false, 2: false, 3: false});
  const [showMicroUnits, setShowMicroUnits] = useState(false);
  const [showMacroUnits, setShowMacroUnits] = useState(false);
  const [showChapters, setShowChapters] = useState({})
  const [microUnits, setMicroUnits] = useState({})
  const [macroUnits, setMacroUnits] = useState({})
  const [introUnits, setIntroUnits] = useState({})
  const [selectedChapters, setSelectedChapters] = useState({})
  const [selectedUnits, setSelectedUnits] = useState({})
  const [selectedSubjects, setSelectedSubjects] = useState({})
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



    const unitChecked = (unitId) => {
      const unitChapters = chaptersObj.filter((chapter)=>chapter.unit_id==unitId)
      const unitChapterIds = unitChapters.map((chapter)=>chapter.id)
      let someChecked = false
      unitChapterIds.forEach((id)=>{
        if (selectedChapters[id] == true){
          someChecked = true
        }
   
      })
      return someChecked
    }

    const subjectChecked = (subjectId) => {
      const subjectUnits = unitsObj.filter((unit)=>unit.subject_id==subjectId)
      const subjectUnitIds = subjectUnits.map((unit) => unit.id)
      let someChecked = false
      subjectUnitIds.forEach((id)=>{
        if(selectedUnits[id] == true){
          someChecked = true
        }
      })
      return someChecked
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


    const handleSubjectChange = (e) => {
      const { name, checked } = e.target;
      const subjectUnits = unitsObj.filter((unit) => unit.subject_id == name);
      const subjectUnitIds = subjectUnits.map((unit) => unit.id);
    
      // Select all units belonging to this subject
      subjectUnitIds.forEach((unitId) => {
        setSelectedUnits((prevSelectedUnits) => ({
          ...prevSelectedUnits,
          [unitId]: checked
        }));
    
        // Select all chapters belonging to each unit
        const unitChapters = chaptersObj.filter((chapter) => chapter.unit_id == unitId);
        unitChapters.forEach((chapter) => {
          setSelectedChapters((prevSelectedChapters) => ({
            ...prevSelectedChapters,
            [chapter.id]: checked
          }));
        });
      });
    
      // Set the subject itself
      setSelectedSubjects((prev) => ({
        ...prev,
        [name]: checked
      }));
    };

    const handleChapterChange = (e) => {
      const { name, checked } = e.target;
      const rightChapter = chaptersObj.filter((chapter) => chapter.id == name);
      const unitId = rightChapter[0].unit_id;
      const unitChapters = chaptersObj.filter((chapter) => chapter.unit_id == unitId);
    
      // Update the selected chapters state
      setSelectedChapters((prev) => ({
        ...prev,
        [name]: checked
      }));
    
      // Check if there is at least one selected chapter in the unit
      const someChaptersSelected = unitChapters.some((chapter) => selectedChapters[chapter.id] || checked);
    
      // Update unit state based on whether at least one chapter is selected
      setSelectedUnits((prev) => ({
        ...prev,
        [unitId]: someChaptersSelected
      }));
    
      // Now, check if all units for the subject should remain selected
      const unitSubject = unitsObj.find((unit) => unit.id == unitId);
      const subjectUnits = unitsObj.filter((unit) => unit.subject_id == unitSubject.subject_id);
    
      // Check if any unit within the subject still has selected chapters
      const someUnitsSelected = subjectUnits.some((unit) => {
        const unitChapters = chaptersObj.filter((chapter) => chapter.unit_id == unit.id);
        return unitChapters.some((chapter) => selectedChapters[chapter.id] || (unit.id == unitId && checked)); // Include the current change
      });
    
      // Update subject state based on whether any units remain selected
      setSelectedSubjects((prev) => ({
        ...prev,
        [unitSubject.subject_id]: someUnitsSelected
      }));
    };
    

    //   const handleMacroSelectAll = (e) => {
    //     const checked = e.target.checked;
    //     setMacroUnits({
   
    //     });
    //   };
    
    const handleSubmit = () => {
        console.log('CHAPTERSSSSS', selectedChapters)
        dispatch(addUserUnits(selectedChapters))
        navigate('/userhome', {state: {showModal: true}})
        
    }


  
  const unitsDisplay = (subjectId) => {
    const subjectUnits = unitsObj.filter((unit)=>unit.subject_id==subjectId)

    return(subjectUnits.map((unit)=>{
        if (showChapters[unit.id] == null){
          showChapters[unit.id] = false
        }

        const hasChapters = unitIdsWithChapters.has(Number(unit.id))

        return(<div key = {unit.id}>
          <input type='checkbox' disabled = {!hasChapters} name={unit.id} onChange={handleUnitChange} checked={unitChecked(unit.id)}></input>
          <span className = 'text-xm' onClick = {()=> setShowChapters(initialState => ({
            ...initialState,
            [unit.id]: !showChapters[unit.id]
          }))}>
            {unit.name.split(':')[1].slice(1)} {hasChapters ? '(expand)' : '(coming soon!)'}
          </span>
          {showChapters[unit.id] && 
          <div className='ml-6'>{chaptersDisplay(unit.id)}</div>
          }
        </div>)}))
  }

  const chaptersDisplay = (unitId) => {
    const unitChapters = chaptersObj.filter((chapter)=>chapter.unit_id == unitId)
    return(unitChapters.map((chapter)=>{
      return(<div key={chapter.id}>
        <input type='checkbox' onChange={handleChapterChange} name={chapter.id} checked={selectedChapters[chapter.id]}></input>
        {chapter.name}
      </div>)
    }))
  }
   
  return (
    <div className="bg-green-400 w-5/12 p-8 flex justify-center ">
      <div className="w-full mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-xl font-bold mb-2">I am interested in studying:</h1>

        {subjectsObj.map((subject)=>{
          return(<div key={subject.id}>
            <div className='text-xl cursor-pointer'>
              <input type='checkbox' className='cursor-pointer' onClick = {handleSubjectChange} name={subject.id} checked = {subjectChecked(subject.id)}></input>
              <span onClick={()=>setShowUnits(prevState => ({
                ...prevState,
                [subject.id]: !prevState[subject.id]
              }))}>
               {subject.name}  (click to expand)
              </span>
            </div>
            {showUnits[subject.id] && <>
              <div className='ml-6 cursor-pointer'>
              {unitsDisplay(subject.id)} 
              </div>
            </>}
     
             
          </div>)
        })}

        {/* Microeconomics Section */}
        {/* <div className="mb-6">
            <div className="ml-6">
            </div>
             <div className='flex items-center'>
                <input
                    type="checkbox"
                    className="mr-2"
                    onChange={handleMicroSelectAll}
                    checked={microUnits[1] && microUnits[2] && microUnits[3]}/>
                <label
                    className="block text-lg font-medium text-gray-700 cursor-pointer"
                    onClick={() => setShowMicroUnits(!showMicroUnits)}>
                    Microeconomics (click to expand)
                </label>
             </div> */}

          {/* The checkbox is separate for selecting all, does NOT toggle visibility */}


          {/* Conditional Rendering: Show units only when clicked */}
          {/* {showMicroUnits && (
            <div className="ml-6 mt-2">
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="1"
                  className="mr-2"
                  checked={microUnits[1]}
                  onChange={handleMicroUnitChange}
                />
                Intro to Economics
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="2"
                  className="mr-2"
                  checked={microUnits[2]}
                  onChange={handleMicroUnitChange}
                />
                Supply and Demand
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="3"
                  className="mr-2"
                  checked={microUnits[3]}
                  onChange={handleMicroUnitChange}
                />
                Elasticity
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="4"
                  className="mr-2"
                  checked={microUnits[4]}
                //   onChange={handleMicroUnitChange}
                  disabled
                />
                Government Intervention 
                <p>(coming soon)</p>
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="5"
                  className="mr-2"
                  checked={microUnits[5]}
                //   onChange={handleMicroUnitChange}
                  disabled
                />
                Market Failure
                <p>(coming soon)</p>
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="6"
                  className="mr-2"
                  checked={microUnits[6]}
                //   onChange={handleMicroUnitChange}
                  disabled
                />
                Consumer Theory
                <p>(coming soon)</p>
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="7"
                  className="mr-2"
                  checked={microUnits[7]}
                //   onChange={handleMicroUnitChange}
                  disabled
                />
                Producer Theory (Competition, Oligopoly & Monopoly)
                <p>(coming soon)</p>
              </label>
            </div>
          )}
        </div> */}

        {/* Macroeconomics Section */}
        {/* <div className="mb-4">
            <div className='ml-6'>
            </div>
            <div className='flex items-center'>

                <input
                    type="checkbox"
                    className="mr-2"
                    // onChange={handleMacroSelectAll}
                    checked={Object.values(macroUnits).every(Boolean)}
                    disabled
                    />
            <label  onClick={() => setShowMacroUnits(!showMacroUnits)} className="block text-lg font-medium text-gray-700 cursor-pointer">
                Macroeconomics (click to expand)</label>
                
            </div> */}
          {/* Add Macroeconomics units here with similar structure */}
        {/* </div>
        {showMacroUnits && (
            <div className="ml-6 mt-2">
             <label className="block text-gray-700">
             <input
               type="checkbox"
               name="8"
               className="mr-2"
               checked={macroUnits[8]}
             //   onChange={handleMicroUnitChange}
               disabled
             />
                 Macroeconomic Objectives
                <p>(coming soon)</p>
              </label>

              <label className="block text-gray-700">
             <input
               type="checkbox"
               name="9"
               className="mr-2"
               checked={macroUnits[9]}
             //   onChange={handleMicroUnitChange}
               disabled
             />
                 Macroeconomic Models
                <p>(coming soon)</p>
              </label>

              <label className="block text-gray-700">
             <input
               type="checkbox"
               name="10"
               className="mr-2"
               checked={macroUnits[10]}
             //   onChange={handleMicroUnitChange}
               disabled
             />
                 Macroeconomic Policies
                <p>(coming soon)</p>
              </label>

              <label className="block text-gray-700">
             <input
               type="checkbox"
               name="11"
               className="mr-2"
               checked={macroUnits[11]}
             //   onChange={handleMicroUnitChange}
               disabled
             />
                 Trade and the Balance of Payments
                <p>(coming soon)</p>
              </label>
              
            </div>
        )} */}

        {/* Submit Button */}
        <div className="flex justify-start mt-20">
          <button
            type="button"
            className="px-4 py-2 bg-slate-500 text-white font-semibold rounded-lg shadow-md hover:bg-slate-600 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75"
            onClick={() => {
              handleSubmit()
              // Add submission logic here
            }}
          >
            Submit
          </button>
        </div>
      </div>
    </div>
      );
    }
