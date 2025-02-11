import { useLocation, useNavigate } from "react-router-dom"
import { useSelector } from "react-redux"
import { ResultsModal } from "./ResultsModal"
import { openResultsModal } from "../Slices/modalSlice"
import { useDispatch } from "react-redux"
import { openSignupModal } from "../Slices/modalSlice"

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

    console.log(quizData)
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

    const TestEncouragement = () => {
        return(
            <>
                {percentageScore == 100 && <span>You rocked that exam like Yoko rocked the Beatles! (Not sure what that simile actually means)</span>}
                {percentageScore >= (4/6) && percentageScore< 100 && <span> You crushed it! Not a total econ genius yet, but dangerously close. </span>}
                {percentageScore >= (2/6) && percentageScore< (4/6) && <span>Your quiz score wasn't exactly Wolf of Wall Street level . . . but hey, you showed up!</span>}
                {percentageScore < (2/6) && <span>That was less 'Wall Street' and more 'Fire Festival'.  At least it was memorable!</span>}
            </>
        )
    }

    const userlessSignup = () => {
        dispatch(openSignupModal({quizData}))
    }



    console.log(quizData)
    return(
        <>
            <div className=''>
                <div className='w-screen flex flex-col items-center justify-top min-h-screen'>
                    <div className="sm:mt-40 mt-28 sm:w-5/6 h-1/2 border-black border-2 rounded-lg shadow-2xl">
                        <div className='flex flex-col items-center justify-center mx-4'>
                            <div className='mt-8 sm:text-4xl text-2xl text-center sm:text-left'>Results for Chapter {chapterNumber} Review Quiz</div>
                            <div className = 'mt-4 sm:text-2xl text-xl'>Topic: {chapterName}</div>
                            <div className = 'mt-4 sm:text-xl text-lg'>You answered <span className='font-bold'>{numCorrect} out of a total possible {Object.values(quizData.answers).length} questions</span> correctly.  Your total score on this quiz was <span className = 'font-extrabold'>{percentageScore}%</span></div>
                            <div className = 'mt-4 sm:text-xl text-lg'>{scoreHeader()}</div>
                        
                        </div>
                        <div className='flex sm:flex-row flex-col items-center justify-around my-10'>
                            <button className="button m:my-0 w-2/3 sm:w-1/6"
                                    onClick = {showResults}
                                    >Show Correct Answers</button>
                            <button className="button my-4 sm:my-0 w-2/3 sm:w-1/6"
                                    onClick = {retakeQuiz}
                                    >Try Quiz Again</button>
                            <button className="button m:my-0 w-2/3 sm:w-1/6"
                                    onClick = {()=>navigate('/videoindex')}
                                    >Back to Videos</button>
                        </div>
                        
                    </div>
                    <div className='mt-12 mb-12 sm:mb-0 text-center items-center justify-center flex flex-col text-lg border-black border-2 border-solid p-4 rounded-lg shadow-2xl'>
                           <p> HEY! {TestEncouragement()}</p>
                           <p> <strong>Want to keep track of your progress and <span className='text-[#0088A8]'>get access to even <em>more</em> practice questions? </span></strong>  <div><strong>Then you gotta sign up!</strong> </div> </p>
                           <p>It's <strong className='text-red-600'>free</strong> and <strong className='text-red-600'>quick</strong>.  And we send ZERO emails to you (unless you're like us and you forgot your password)</p>
                           <p>C'mon, take the first step towards becoming an Econo-Jedi!</p>
                    
                    <div className="button mt-4"
                                    onClick = {()=>{userlessSignup()}}
                                    >
                                        Sign Up To Save Progress

                    </div>
                    </div>
                </div>
                
                <ResultsModal answers = {quizData.answers}/>
            </div>
          
            

        </>
    )
}