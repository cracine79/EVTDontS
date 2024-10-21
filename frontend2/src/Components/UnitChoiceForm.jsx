import { useState } from "react"
import { addUserUnits } from "../Slices/unitsActions";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";


export const SelectUnitsForm = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const [microUnits, setMicroUnits] = useState({
        1: false,
        2: false,
        3: false,
        4: false,
        5: false,
        6: false,
        7: false
      });

      const[macroUnits, setMacroUnits] = useState({
        8: false,
        9: false,
        10: false,
        11: false
      })
    
      // State to track whether the microeconomics units are visible
      const [showMicroUnits, setShowMicroUnits] = useState(false);
      const [showMacroUnits, setShowMacroUnits] = useState(false);
    
      const handleMicroUnitChange = (e) => {
        const { name, checked } = e.target;
        setMicroUnits((prev) => ({ ...prev, [name]: checked }));
      };

      const handleMacroUnitChange = (e) => {
        const {name, checked} = e.target;
        setMacroUnits((prev)=>({...prev, [name]: checked}))
      }
    
      const handleMicroSelectAll = (e) => {
        const checked = e.target.checked;
        setMicroUnits((prevMicroUnits) => ({
          ...prevMicroUnits,
          1: checked,
          2: checked,
          3: checked,
        }));
      };

    //   const handleMacroSelectAll = (e) => {
    //     const checked = e.target.checked;
    //     setMacroUnits({
   
    //     });
    //   };
    
    const handleSubmit = () => {
        const units = {...microUnits, ...macroUnits}
        dispatch(addUserUnits(units))
        navigate('/userhome', {state: {showModal: true}})
        
    }
   
  return (
    <div className="bg-green-400 w-5/12 p-8 flex justify-center ">
      <div className="w-full mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-4">I am interested in studying:</h1>

        {/* Microeconomics Section */}
        <div className="mb-6">
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
             </div>

          {/* The checkbox is separate for selecting all, does NOT toggle visibility */}


          {/* Conditional Rendering: Show units only when clicked */}
          {showMicroUnits && (
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
        </div>

        {/* Macroeconomics Section */}
        <div className="mb-4">
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
                
            </div>
          {/* Add Macroeconomics units here with similar structure */}
        </div>
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
        )}

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
