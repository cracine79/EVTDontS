import { useSelector, useDispatch } from "react-redux"
import { clearUserResults } from "../Slices/resultsSlice"
import { useNavigate } from "react-router-dom"
import { openQuizModal } from "../Slices/modalSlice"
import { openResultsModal } from "../Slices/modalSlice"
import { ResultsModal } from "./ResultsModal"


export const QuizResults = () => {
    const currentChapter = useSelector(state=>(state.user.currentChapter))
    const chapters = useSelector(state=>(state.chapters))
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)
    const fullChapterName = chapters[currentChapter].name
    const navigate = useNavigate();
    const dispatch = useDispatch();

    let breakPoint = 0
    while(fullChapterName[breakPoint] != ' '){
        breakPoint +=1
    }
    const chapterNumber = fullChapterName.slice(0,breakPoint)
    const chapterName = fullChapterName.slice(breakPoint +1)


    let numCorrect = 0
    resultsObj.forEach((result)=>{
        if (result.isCorrect == true){
            numCorrect += 1
        }
    })
    const percentageScore = (numCorrect/resultsObj.length)*100
    const scoreHeader = () => {
        if(percentageScore >= 70){
            return(<p>AMAZING WORK!!!  You crushed these AP style questions.  Honestly, I'm starting to think they're just phoning it in at this point.</p>)
        }else if (percentageScore >50){
            return(<p>Totally not a terrible job on those AP style questions!  You're, like, a couple of Google searches away from greatness.</p>)
        }else {
            return(<p>Oof.  AP style questions can be tricky.  Let's try it again.  Looks like the quiz could use a little more work too. </p>)
        }
    }

    const retake = () => {
        dispatch(clearUserResults())
        navigate('/Quiz',  {state: {chapter: currentChapter}})
        dispatch(openQuizModal())
    }

    const showResults = () => {
        dispatch(openResultsModal())
    }

    
    return(
        <div className='w-screen flex justify-center'>
            <div className="mt-40 w-5/6 h-auto border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center'>
                    <div className='mt-8 text-4xl'>Results for Chapter {chapterNumber} Review Quiz</div>
                    <div className = 'mt-4 text-2xl'>Topic: {chapterName}</div>
                    <div className = 'mt-4 text-xl'>You answered <span className='font-bold'>{numCorrect} out of a total possible {resultsObj.length} questions</span> correctly.  Your total score on this quiz was <span className = 'font-extrabold'>{percentageScore}%</span></div>
                    <div className = 'mt-4 text-xl'>{scoreHeader()}</div>
                </div>
                <div className='flex flex-row justify-around my-10'>
                    <button onClick={showResults }>Show Me What I Missed</button>
                    <button onClick={retake}>Gimme A Mulligan.  Take that bad boy again.</button>
                    <button>Enough of this.  Let's go to the next Video.</button>
                </div>
                
            </div>
            <ResultsModal />
        </div>
    )
}