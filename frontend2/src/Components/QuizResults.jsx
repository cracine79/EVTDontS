import { useSelector } from "react-redux"

export const QuizResults = () => {
    const currentChapter = useSelector(state=>(state.user.currentChapter))
    const chapters = useSelector(state=>(state.chapters))
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)
    const fullChapterName = chapters[currentChapter].name

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

    
    return(
        <div className='w-screen flex justify-center'>
            <div className="mt-40 w-5/6 h-auto border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center'>
                    <p className='mt-8 text-4xl'>Results for Chapter {chapterNumber} Review Quiz</p>
                    <p className = 'mt-4 text-2xl'>Topic: {chapterName}</p>
                    <p className = 'mt-4 text-xl'>You answered <span className='font-bold'>{numCorrect} out of a total possible {resultsObj.length} questions</span> correctly.  Your total score on this quiz was <span className = 'font-extrabold'>{percentageScore}%</span></p>
                    <p className = 'mt-4 text-xl'>{scoreHeader()}</p>
                </div>
                <div>
                    <button>See What You Missed</button>
                </div>
            </div>
        </div>
    )
}