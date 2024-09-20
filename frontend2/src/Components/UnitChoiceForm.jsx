import { useState } from "react"


export const SelectUnitsForm = () => {
    const [microUnits, setMicroUnits] = useState({
        intro: false,
        supplyDemand: false,
        elasticity: false,
      });
    
      // State to track whether the microeconomics units are visible
      const [showMicroUnits, setShowMicroUnits] = useState(false);
    
      const handleMicroUnitChange = (e) => {
        const { name, checked } = e.target;
        setMicroUnits((prev) => ({ ...prev, [name]: checked }));
      };
    
      const handleMicroSelectAll = (e) => {
        const checked = e.target.checked;
        setMicroUnits({
          intro: checked,
          supplyDemand: checked,
          elasticity: checked,
        });
      };
    
   
  return (
    <div className="bg-gray-100 p-8 min-h-screen flex justify-center items-center">
      <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
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
              checked={Object.values(microUnits).every(Boolean)}
            />
        <label
            className="block text-lg font-medium text-gray-700 cursor-pointer"
            onClick={() => setShowMicroUnits(!showMicroUnits)} // Toggle visibility when the label (word) is clicked
          >
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
                  name="intro"
                  className="mr-2"
                  checked={microUnits.intro}
                  onChange={handleMicroUnitChange}
                />
                Intro to Economics
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="supplyDemand"
                  className="mr-2"
                  checked={microUnits.supplyDemand}
                  onChange={handleMicroUnitChange}
                />
                Supply and Demand
              </label>
              <label className="block text-gray-700">
                <input
                  type="checkbox"
                  name="elasticity"
                  className="mr-2"
                  checked={microUnits.elasticity}
                  onChange={handleMicroUnitChange}
                />
                Elasticity
              </label>
            </div>
          )}
        </div>

        {/* Macroeconomics Section */}
        <div className="mb-6">
          <label className="block text-lg font-medium text-gray-700">Macroeconomics</label>
          {/* Add Macroeconomics units here with similar structure */}
        </div>

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="button"
            className="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75"
            onClick={() => {
              console.log('Selected Micro Units:', microUnits);
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
