import { useNavigate } from "react-router-dom"
import { useSelector } from "react-redux"
import { selectUserChapters } from "../Slices/selectors"
import { useState } from "react"

export const FinishPage = () => {
    const navigate = useNavigate()
    const userProg = useSelector((state)=>state.topicProg)
    const userChapters = useSelector((state)=>state.userChapters)
    const topics = useSelector((state)=>state.topics)
    const bookChapters = useSelector((state)=>state.chapters)
    const units = useSelector((state)=>state.units)
    const userName = useSelector((state)=>state.user.username)

    const unitsObj = Object.values(units)
    const topicProgObj = Object.values(userProg)
    // const userChaptersObj = Object.values(userChapters)
    const unitsObjWithIds = Object.keys(units).map((key)=>({
        id: key,
        name: units[key].name
    }))
    
    const thisUnit = (unit) => {
        const output = (unitsObjWithIds.filter((objUnit)=>{
            return objUnit.name === unit
        }))
        return output[0]
    }

    let asked = 0
    let answered = 0
    topicProgObj.forEach((topicProg)=>{
        asked += topicProg.questions_asked
        answered += topicProg.answered_correctly
    })
    const averagePercentCorrect = Math.floor((answered/asked) * 100)
    // const userChaptersComplete = Object.keys(userChapters).reduce((acc, key)=>{
    //     if(bookChapters[key]){
    //         acc[key] = {
    //             ...userChapters[key],
    //             ...bookChapters[key]
    //         }
    //     }
    // })

    const userTopicProgComplete = Object.keys(userProg).reduce((acc, key) => {
        if(topics[key]) {
            acc[key] = {
                ...userProg[key],
                ...topics[key]
            }
        }
        return acc;
    }, {})

    const userTopicProgObj = Object.values(userTopicProgComplete)


    const userChaptersComplete = Object.keys(userChapters).reduce((acc, key) => {
        if(bookChapters[key]) {
            acc[key] = {
                ...userChapters[key],
                ...bookChapters[key],
                'chapter_id': key
            }
        }
        return acc;
    }, {})

    const chaptersInitial = {}
    const userChaptersObj = Object.values(userChaptersComplete)
    userChaptersObj.forEach((chapter)=>{
        chaptersInitial[chapter.chapter_id]=false
    })

    const [chaptersOpen, setChaptersOpen] = useState(chaptersInitial)


    let reply=""
    if(averagePercentCorrect > 90){
        reply = 'Economic Overlord'
    } else if (averagePercentCorrect > 80){
        reply = 'Econo-ninja'
    } else if (averagePercentCorrect > 60) {
        reply = 'Curve Whisperer'
    } else if (averagePercentCorrect > 50) {
        reply = 'Sort of Chart Challenged'
    } else if (averagePercentCorrect > 0) {
        reply = 'Economic Noob'
    } else {
        reply = 'Not yet started'
    }

    const chapterRanking = (percentCorrect) => {
        if(percentCorrect >= 80){
            return(<>The Bomb</>)
        } else if (percentCorrect >= 70){
            return(<>Big Cheese</>)
        } else if (percentCorrect >= 60){
            return(<>Middle Management</>)
        } else if (percentCorrect >= 50){
            return(<>Winging It</>)
        } else {
            return(<>Dumpster Fire</>)
        }
    }

    const topicRanking = (percentCorrect) => {
        if(percentCorrect >= 80){
            return(<>Fiscal Samurai</>)
        } else if (percentCorrect >= 70){
            return(<>Keynesian Conquerer</>)
        } else if (percentCorrect >= 60){
            return(<>Monetarist Maverick</>)
        } else if (percentCorrect >= 50){
            return(<>Supply-Side Struggling</>)
        } else {
            return(<>Deficit Disaster</>)
        }
    }
    const openChapters = (chapter_id) =>{
        const isOpen = chaptersOpen[chapter_id]

        setChaptersOpen((prev)=>{
            return(
                {
                    ...prev,
                    [chapter_id]: !isOpen
                }
            )
     
        })
    }

    const chaptersProg= (unit) => {
        const currentUnit = thisUnit(unit)
        const unitChapters = userChaptersObj.filter((chapter)=> chapter.unit_id==parseInt(currentUnit.id))
        
        return(
            unitChapters.map((chapter)=>{
      
                const chapterTopicsForScore = userTopicProgObj.filter((topic)=>topic.chapter_id==(chapter.chapter_id))
                let chapterQuestionsFaced = 0
                let chapterQuestionsAnswered = 0

                chapterTopicsForScore.forEach((topic)=>{
                    chapterQuestionsFaced += topic.questions_asked
                    chapterQuestionsAnswered += topic.answered_correctly
                })

                
                return(
                    <div className='ml-2 mt-2' onClick={()=>openChapters(chapter.chapter_id)}>

                     
                        <div className='flex justify-between'>
                            <div className='text-center w-1/6 font-bold'>{chapter.name}</div>
                            <div  className='text-center w-1/6'>{chapter.quiz_grade}</div>
                            <div className='text-center w-1/6'>{chapterQuestionsFaced}</div>
                            <div className='text-center w-1/6'>{chapterQuestionsAnswered}</div>
                            <div className='text-center w-1/6'>{chapterRanking((chapterQuestionsAnswered/chapterQuestionsFaced)*100)}</div>
                        </div> 
                      
                        {chaptersOpen[chapter.chapter_id] && 
                            <>  <div className='w-full bg-lime-400 text-sm font-bold flex justify-around'>
                                    <div className='w-1/5 text-center px-2 '>Sub-Topic</div> 
                                    <div className='w-1/5 text-center px-2 '>Topic Questions Asked</div>
                                    <div className='w-1/5 text-center px-2 '>Answered Correctly</div>
                                    <div className='w-1/5 text-center px-2 '>Topic Achievement</div>
                                 </div>
                                <div>
                                    {topicsBreakdown(chapter.chapter_id)}
                                </div>
                            </>                     
                        }
                    </div>
                )
            })
        )
    }

    const topicsBreakdown = (chapterId) => {
        const chapterTopics = userTopicProgObj.filter((topic)=>topic.chapter_id==parseInt(chapterId))

        return(
            chapterTopics.map((topic)=>{
                return(
                    <div className='w-full'>

                    <div className='w-full flex justify-around text-sm'>
                        <div className='w-1/5 text-center px-2 '>{topic.topic_name}</div>
                        <div className='w-1/5 text-center px-2 '>{topic.questions_asked}</div>
                        <div className='w-1/5 text-center px-2 '>{topic.answered_correctly}</div>
                        <div className='w-1/5 text-center px-2 '>{topicRanking((topic.questions_asked/topic.answered_correctly) * 100)}</div>
                    </div>
                </div>
                )
            })
        )
    }

    return(<div className='mt-36 w-screen flex justify-center'>
        <div className='w-4/5 mb-28 shadow-2xl rounded-3xl flex justify-cente flex-col items-center'>
            
            <p className='mt-16 text-3xl mb-4'>CONGRATULATIONS {userName}!!</p>
            <p className='my-2 px-4'>[Insert preferred expletive] yeah!!  You've officially crushed all the chapters you have enrolled in! 🎉 You watched all the videos, aced the quizzes, and now, my friend, you’re the economist everyone wishes they could hang out with at parties (…just go with it).</p>
            <p className='my-2 px-4'>But wait, there’s more! If you’re craving more economic enlightenment (or looking for a distraction from another re-watch of <em>The Office</em>), there are still chapters you haven’t signed up for. Go ahead—dive back in, add those new ones, or do a power rewatch of your favorites.</p>
            <p className='my-2 px-4'>And now, the moment the econo-nerd inside of you has been waiting for: your Econ Legends Scorecard below! Yes, it’s like your very own stats in a video game—except instead of maxing out agility or charm, you've leveled up in things like Price Elasticity and Marginal Cost. Take a look, bask in the glory of your economic dominance, and feel free to screenshot and send it to that one friend who still thinks ‘opportunity cost’ is a new cryptocurrency.</p>
            <p className='my-2 px-4'>And hey, if you’ve secretly enjoyed the thrilling world of supply and demand, don’t keep it to yourself. Tell a friend! They’ll thank you later...maybe. Or they'll pretend they didn't see your text. Either way, you are the econ star we all need. Shine on!</p>
       
            <p className='mt-8 text-2xl'> Econ Legends Scorecard (Dun dun dunnnnnnn!)</p>
            <div className='flex justify-around w-100 mt-6 px-6'>
                <div className='w-1/4 rounded-xl border-2 p-2 border-black h-100'>All together you have suffered through <span className='font-bold text-xl'>{userChaptersObj.length}  {userChaptersObj.length == 1 ? <>video</> : <>videos</>}</span>  covering <span className='font-bold text-xl'>{topicProgObj.length} {topicProgObj.length == 1 ? <>topic</> : <>topics</>}. </span>Whether or not they sucked is up to you!</div>
                <div className='w-1/4 rounded-xl border-2 p-2 border-black h-100'>In total you faced down <span className='font-bold text-xl'>{asked} questions</span> and you proved your skills by answering <span className='font-bold text-xl'>{answered} correctly. </span>You're a legend. </div>
                <div className='w-1/4 rounded-xl border-2 p-2 border-black h-100'>Of all of the nasty questions that we threw at you, you answered a whopping <span className='font-bold text-xl'>{averagePercentCorrect}% correctly</span></div>
               
            </div>
            <div className='w-2/3 mt-8 text-2xl rounded-xl border-2 p-2 border-black h-100'>Given your performance, stats, and overall grittiness, you are officially awarded the level of <span className='font-bold text-2xl'>{reply}</span></div>
            
            <div className='mt-4 text-2xl'>Topic Mastery Details</div>
            <div className='w-full flex justify-center'>
                {unitsObj.map((unit)=>{
                    return(
                        <div className='border-black border-2 rounded-xl p-4 w-5/6'>
                        <div className='text-xl'key='unit.id'>{unit} </div>
                        <div className='flex justify-between bg-green-100'>
                            <div className='text-center w-1/6 font-bold text-xl'>Chapter Name</div>
                            <div className='text-center w-1/6'>Chapter Quiz Score</div>
                            <div className='text-center w-1/6'>Total Questions Faced</div>
                            <div className='text-center w-1/6'>Questions  Vanquished</div>
                            <div className='text-center w-1/6'>Chapter Ranking</div>
                        </div>
                        {chaptersProg(unit)}
                        </div>
                    )
                })}
                
            </div>
                <div className='my-12 flex justify-center w-full'>
                    <button className='
                            border-black
                            w-1/6 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mr-16'
                            onClick={()=>(navigate('userhome'))}>Back to User Dashboard</button>
                    <button className='
                             ml-16
                            border-black
                            w-1/6 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer'
                            onClick = {()=>(navigate('/'))}>Add More Units</button>
                </div>
            </div>
    </div>)
}