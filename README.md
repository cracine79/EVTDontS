## WELCOME TO ECONOMICS VIDEOS THAT DON'T SUCK

Please visit the [Live Site!](https://www.economicsvideos.com/)

### Introduction

Economics Videos That Don't Suck (EVTDS) is an innovative online platform designed to transform the study of economics into an engaging and personalized experience. Our website features a library of self-produced videos that cover a wide array of economic concepts, ensuring that learning is both informative and entertaining.

What sets EVTDS apart is our focus on tracking learner progress. We offer interactive quizzes that adapt to each learner's performance, providing unique challenges based on their previous answers. This personalized approach helps reinforce understanding and ensures that users are continually advancing their knowledge.

At EVTDS, we believe that education should be both fun and effective. Whether you're preparing for an exam or simply exploring economic ideas, our platform is your ultimate resource for tailored learning in economics!


The technologies used in this project include:

* Languages: Javascript, Python, HTML, CSS and JSX
* Frontend: React-Redux, Vite
* Backend: Flask
* Database: PostgreSQL
* Hosting: Heroku
* Asset Storage: AWS S3 Storage
* Email Service: SendGrid API, Google Workspaces Email


# MVPs

## Video & Quiz Library

Our complete library of economics videos are available to all users, regardless of login status.  Each video has an accompanying quiz with AP style multiple choice questions that test users on the video content.  


![VideoLibraryVideo](/rm_assets/vidlibvid.png)

![VideoLibraryQuiz](/rm_assets/vitlibquiz.png)

![VideoLibraryQuizQuestion](/rm_assets/vidlibquizq.png)

Users are provided with instant feedback upon completion of the exam.  Users who are not signed in have the option of creating an account upon completion of the exam to save their quiz progress as well as videos watched. 

![VideoLibraryResults](/rm_assets/vidlibresults.png)


## Search
The search functionality in EVTDS.com leverages PostgreSQL full-text search to efficiently retrieve relevant chapters based on user queries. Each chapter is indexed using a tsvector stored in the database, allowing for rapid lookup via to_tsquery(). The search query ranks results using ts_rank(), ensuring that more relevant chapters appear higher in the results. By filtering with the @@ operator and ordering by rank in descending order, the system provides accurate and performant search results with minimal latency.


```
@chapters_ns.route('/search/<string:search_terms>')
class SearchChapters(Resource):
    def get(self, search_terms):
        or_query = ' | '.join(search_terms.split())
        print(or_query)

        chapters = db.session.query(
            Chapter,
            db.func.ts_rank(Chapter.search_vector, text("to_tsquery('english', :terms)")).label('rank')
        ).filter(
            Chapter.search_vector.op('@@')(text("to_tsquery('english', :terms)"))
        ).params(terms=or_query).order_by(db.desc('rank')).all()

        result = [{
            'id': chapter.id,
            'name': chapter.name,
            'quiz_blurb': chapter.quiz_blurb,
            'video_blurb': chapter.video_blurb,
            'video_url': chapter.video_url,
            'rank': rank,
            'slug': chapter.slug
        } for chapter, rank in chapters
        ]

        return{'chapters': result}, 200
```

## User Customized Learning Plans

Registered users can select units to add to their study plan, which will then be displayed on their homepage. This includes metrics on their progress, such as quiz scores, video completion, and topic mastery. 


![UnitSelectionForm](/rm_assets/unitchoice.png)

## User Progress Tracking 

As users advance through the curriculum, their progress is updated on the homepage, with the next task prominently featured at the top of the page.

![UserHome](/rm_assets/userhome.png)

As users complete quizzes, the backend tracks accuracy on specific questions as well as topics in general, storing user performance data which is then used to generate user-tailored quizzes in future sessions.


## User-Specific Quiz Generation

In addition to the quiz that accompanies each video, registered users have access to a broader range of quiz types and more questions for review.  

Users can create their own custom quizzes by selecting the topics which they wish to review.   Quiz results provide even more detail into specific topic performance.

![TopicChoice](/rm_assets/topicchoice.png)

![TopicQuizResults](/rm_assets/topicquizres.png)

In addition, users can opt for the website to generate a quiz for them.  In this case, the backend selects questions from topics which the user has historically performed the least successfully on. 

![QuizOfReckoning](/rm_assets/quizofreckoning.png)


## Backend algorithm to craft quizzes focusing on user weakness
The backend relies upon historical performance to generate the quiz of reckoning.  All three different quiz types make fetch to same backend route, with quiz type in params:

```
@quiz_ns.route('/questions')
class AccessQuiz(Resource):
    @jwt_required()
    def get(self):
        type = request.args.get('type')
        chapter_id = request.args.get('chapter')
        
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id
        questions = []
        ...

```

For quizzes focusing on the users' weak spots, the backend first uses current progress data to calculate percentage of questions answered correctly for each topic that they have faced to date.  It also calculates the user's average score on all questions faced as a comparision.  

```
        ...
        elif type in['shortWeakspotQuiz','longWeakspotQuiz']:
            # currently there is only one weak spot quiz being requested from frontend, shortWeakspotQuiz
            progressArray = user.topic_progresses
            percentageList = {}
            numberTopics = 0
            percentSum = 0
            for progress in progressArray:
                percentCorrect = math.floor((progress.answered_correctly/progress.questions_asked)*100)
                percentageList[progress.topic_id] = (percentCorrect)
                numberTopics += 1
                percentSum += percentCorrect
            averageScore = percentSum/numberTopics
```

The topics with the lowest percentage of questions asked correctly are selected for the quiz.

```
            lowPercentageList = {}

            for key, value in percentageList.items():
                if value < averageScore:
                    lowPercentageList[key]=value
            
            if len(lowPercentageList) == 0:
                lowPercentageList = percentageList

            if len(lowPercentageList) > 4:
                topic_ids = [topicId for topicId, _ in heapq.nsmallest(4, lowPercentageList.items(), key=lambda x:x[1])]
            else:
                topic_ids = [topicId for topicId, _ in lowPercentageList]
```

The backend grabs all questions that the user has faced and the number of times they have answered correctly/incorrectly. It then filters out from those the questions included in the topics for the test:

```
            performances = UserPerformance.query.filter_by(user_id=user_id).all()
            for topic_id in topic_ids:
                all_topic_questions = Question.query.filter_by(topic_id = topic_id).all()

                question_ids = {question.id for question in all_topic_questions}
                question_performances = [performance for performance in performances if performance.question_id in question_ids]
```
It then further filters these questions down to the ones which have been asked to the user previously based upon data from UserPerformance, and the user has failed to answer correctly twice (technically 50% of the time).  Finally, it selects a maximum of two of those questions for each topic and adds them to the questions to be included for the quiz.

```
               if(len(question_performances) > 0):
                    incorrect_counts = defaultdict(int)
                    total_counts = defaultdict(int)
                    
                    for performance in question_performances:
                        total_counts[performance.question_id] += 1
                        if not performance.is_correct:
                            incorrect_counts[performance.question_id] += 1

                    question_ids_with_high_failure_rate = {
                        question_id
                        for question_id in total_counts
                        if incorrect_counts[question_id] / total_counts[question_id] >= 0.5
                    }

                    questions_to_go = random.sample(question_ids_with_high_failure_rate, min(2, len(question_ids_with_high_failure_rate)))

                    for questionId in questions_to_go:
                        question_to_add = next((question for question in all_topic_questions if question.id == questionId), None)
                        questions.append(question_to_add)
```
Finally, the backend seeks out the questions on the selected topics that have not been asked to the user yet, and randomly selects from them until the total number of questions for each selected topic is 4.
```
               asked_question_ids = {performance.question_id for performance in question_performances}    
                # print('QUESTIONS THAT ARE ANSWERED WRONG INCLUDE', questions)

                available_questions = [q for q in all_topic_questions if q not in questions and q.id not in asked_question_ids]
                target_count = 4 - len(questions_to_go)
                while len(available_questions) < target_count:
                    question = random.choice(all_topic_questions)
                    if question not in available_questions:
                        available_questions.append(question)


                while target_count > 0:
               
                    index_number = random.randint(0, len(available_questions) - 1)
                    selected_question = available_questions[index_number]

                    questions.append(selected_question)
                    target_count -=1

                    available_questions.pop(index_number)
```

If the number of questions selected is more than 12, the backend randomly selects 12 of them to send to the frontend. 



# Future Plans
EVTDS is still in Beta mode.  Currently we are in the progress of preparing to migrate the frontend from a Vite app to Next.js for long term SEO optimization. 

We also plan on integrating an AI assistant to provide answers to questions on content that registered users have. 