import { useLocation, useNavigate } from "react-router-dom"
import { useSelector } from "react-redux"
import { ResultsModal } from "./ResultsModal"
import { openResultsModal } from "../Slices/modalSlice"
import { useDispatch } from "react-redux"

export const UserlessResults = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const quizData = location.state?.otherQuizData
    const chapter = useSelector(state=>state.chapters[quizData.chapter_id])
    const fullChapterName = chapter.name
    let breakPoint = 0
    while(fullChapterName[breakPoint] != ' '){
        breakPoint +=1
    }
    const chapterNumber = fullChapterName.slice(0,breakPoint)
    const chapterName = fullChapterName.slice(breakPoint +1)

    let numCorrect = 0
    Object.values(quizData.answers).forEach((result)=>{
        if (result.isCorrect == true){
            numCorrect += 1
        }
    })


    const showResults = () => {
        dispatch(openResultsModal())
    }

    const percentageScore = Math.floor((numCorrect/Object.values(quizData.answers).length)*100)
    const scoreHeader = () => {
        if(percentageScore >= 70){
            return(<p>AMAZING WORK!!!  You crushed these AP style questions.  Honestly, I'm starting to think they're just phoning it in at this point.</p>)
        }else if (percentageScore >50){
            return(<p>Totally not a terrible job on those AP style questions!  You're, like, a couple of Google searches away from greatness.</p>)
        }else {
            return(<p>Oof.  AP style questions can be tricky.  Let's try it again.  Looks like the quiz could use a little more work too. </p>)
        }
    }

    const retakeQuiz = () => {
        navigate('/quiz', {state:{chapter:quizData.chapter_id, type: 'chapterQuizNoUser', topics:[]}})
    }




    console.log(quizData)
    return(
        <>
            <div className='mt-28'>
                <div className='w-screen flex justify-center min-h-screen'>
                    <div className="sm:mt-52 mt-28 sm:w-5/6 h-1/2 border-black border-2 rounded-lg shadow-2xl">
                        <div className='flex flex-col items-center justify-center mx-4'>
                            <div className='mt-8 sm:text-4xl text-2xl text-center sm:text-left'>Results for Chapter {chapterNumber} Review Quiz</div>
                            <div className = 'mt-4 sm:text-2xl text-xl'>Topic: {chapterName}</div>
                            <div className = 'mt-4 sm:text-xl text-lg'>You answered <span className='font-bold'>{numCorrect} out of a total possible {Object.values(quizData.answers).length} questions</span> correctly.  Your total score on this quiz was <span className = 'font-extrabold'>{percentageScore}%</span></div>
                            <div className = 'mt-4 sm:text-xl text-lg'>{scoreHeader()}</div>
                        
                        </div>
                        <div className='flex sm:flex-row flex-col items-center justify-around my-10'>
                    <button className='
                            border-black 
                            h-1/5 
                            sm:w-1/4
                            mb-4
                            sm:mb-0
                            w-11/12
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick = {showResults}
                            >Show Correct Answers</button>
                    <button className='
                            border-black 
                            h-1/5 
                            sm:w-1/4
                            w-11/12
                            border-2 
                            mb-4
                            sm:mb-0
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick = {retakeQuiz}
                            >Try Quiz Again</button>
                            <button className='
                                    border-black 
                                    h-1/5 
                                    sm:w-1/4
                                    w-11/12
                                    border-2 
                                    mb-4
                                    sm:mb-0
                                    flex 
                                    justify-center 
                                    items-center
                                    rounded-lg
                                    bg-stone-300
                                    hover:bg-slate-500
                                    font-medium
                                    hover:cursor-pointer' 
                                    onClick = {()=>navigate('/videoindex')}
                                    >Back to Videos</button>
                        </div>
                        
                    </div>
                  
                </div>
                <ResultsModal answers = {quizData.answers}/>
            </div>
            

        </>
    )
}