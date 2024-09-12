import { useSelector } from "react-redux"

export const QuizResults = () => {
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)
    let numCorrect = 0
    resultsObj.forEach((result)=>{
        if (result.is_correct == true){
            numCorrect += 1
        }
    })
    const percentageScore = (numCorrect/resultsObj.length)*100
    return(
        <div className = 'mt-40'>
            `You scored {numCorrect} out of a total possible {resultsObj.length}.  Score is {percentageScore}`
        </div>
    )
}