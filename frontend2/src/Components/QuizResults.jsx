import { useSelector, useDispatch } from "react-redux"
import { clearUserResults } from "../Slices/resultsSlice"
import { useNavigate, useLocation } from "react-router-dom"
import { openQuizModal } from "../Slices/modalSlice"
import { openResultsModal } from "../Slices/modalSlice"
import { ResultsModal } from "./ResultsModal"
import { finishQuiz } from "../Slices/resultsActions"
import { clearQuestions } from "../Slices/questionsSlice"
import { finishChapter } from "../Slices/resultsActions"


export const QuizResults = () => {
    const location = useLocation()
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
    
    const unitFinished = location.state?.unitFinished

    let numCorrect = 0
    resultsObj.forEach((result)=>{
        if (result.isCorrect == true){
            numCorrect += 1
        }
    })
    const percentageScore = Math.floor((numCorrect/resultsObj.length)*100)
    const scoreHeader = () => {
        if(percentageScore >= 70){
            return(<p>AMAZING WORK!!!  You crushed these AP style questions.  Honestly, I'm starting to think they're just phoning it in at this point.</p>)
        }else if (percentageScore >50){
            return(<p>Totally not a terrible job on those AP style questions!  You're, like, a couple of Google searches away from greatness.</p>)
        }else {
            return(<p>Oof.  AP style questions can be tricky.  Let's try it again.  Looks like the quiz could use a little more work too. </p>)
        }
    }
    const nextChapter = () => {

    }

    const retake = () => {
        dispatch(clearUserResults())
        navigate('/Quiz',  {state: {chapter: currentChapter, type: 'chapterQuiz', topics: []}})
        dispatch(openQuizModal())
    }

    const showResults = () => {
        dispatch(openResultsModal())
    }

    const nextVideo = async ()=>{
        const quizData = {
            chapter_id: currentChapter,
            quiz_score: percentageScore
        }
        
        const data = await(dispatch(finishChapter(quizData)))

        dispatch(clearQuestions())
        dispatch(clearUserResults())
        const newChapter = data.current_chapter


        
        if(data.completed == true){
            navigate('/finishpage')
        } else if(chapters[currentChapter].unit_id!=chapters[newChapter].unit_id){
            const lastUnitId = chapters[currentChapter].unit_id
            navigate('/finishunit', {state: {unitId: lastUnitId}})
        } else {
            navigate(`/video/${newChapter}`)
        }

    }

    const lastVideo = ()=>{
        dispatch(clearQuestions())
        dispatch(clearUserResults())
        navigate(`/video/${currentChapter}`)
    }

    const backHome = ()=>{
        if(percentageScore >= 60){
            const quizData = {
                chapter_id: currentChapter,
                quiz_score: percentageScore
            }
            dispatch(finishChapter(quizData))
        }
        dispatch(clearQuestions())
        dispatch(clearUserResults())
        navigate('/userhome')
    }

    
    return(
        <div className='w-screen flex justify-center min-h-screen'>
            <div className="sm:mt-52 mt-28 sm:w-5/6 h-1/2 border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center mx-4'>
                    <div className='mt-8 sm:text-4xl text-2xl text-center sm:text-left'>Results for Chapter {chapterNumber} Review Quiz</div>
                    <div className = 'mt-4 sm:text-2xl text-xl'>Topic: {chapterName}</div>
                    <div className = 'mt-4 sm:text-xl text-lg'>You answered <span className='font-bold'>{numCorrect} out of a total possible {resultsObj.length} questions</span> correctly.  Your total score on this quiz was <span className = 'font-extrabold'>{percentageScore}%</span></div>
                    <div className = 'mt-4 sm:text-xl text-lg'>{scoreHeader()}</div>
                    {unitFinished && percentageScore>60 &&  <div className = 'mt-4 text-xl'>
                            That was the last chapter of the Unit!  You are killing it my dude!
                    </div>}
                </div>
                <div className='flex sm:flex-row flex-col items-center justify-around my-10'>
                    <button className='
                            border-black 
                            h-1/5 
                            sm:w-1/5
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
                            onClick={showResults }>Show Me What I Missed</button>
                    <button className='
                            border-black 
                            h-1/5 
                            sm:w-1/5
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
                            onClick={retake}>Gimme A Mulligan.  Take that bad boy again.</button>
                    
                    {percentageScore > 60 ? 
                    <button className='
                            border-black 
                            h-1/5 
                            w-11/12
                            sm:w-1/5
                            mb-4
                            sm:mb-0
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={nextVideo}
                            > {!unitFinished ? "Enough of this.  Let's go to the next Video.":"Take me to my Unit Wrapup Party!"}</button> : <button className='
                            border-black 
                            h-1/5 
                            sm:w-1/5
                            w-11/12
                            mb-4
                            sm:mb-0
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={lastVideo}
                            >Let me check that last video out again.</button>
                    
                    }
                    {!unitFinished &&

                        <button className='
                        border-black 
                        h-1/5 
                        sm:w-1/5
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
                        onClick={backHome}>Back to my dashboard please.</button>
                    }
                </div>
                
            </div>
            <ResultsModal />
        </div>
    )
}