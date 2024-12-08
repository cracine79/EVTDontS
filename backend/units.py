from flask_restx import Namespace, Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Unit, user_unit_association, UserChapterProgress, Chapter, Subject
from exts import db

units_ns = Namespace('units', description='A namespace for User Units')

@units_ns.route('/')
class AddUnits(Resource):
    def get(self):
        subjects = Subject.query.all()
        chapters = Chapter.query.all()
        units = Unit.query.all()

        shortened_subjects = {
            subject.id: {
                "name": subject.name
            } for subject in subjects
        }
        shortened_chapters = {
            chapter.id: {
                "name": chapter.name,
                "unit_id": chapter.unit_id
            }
        for chapter in chapters}
        shortened_units = {
            unit.id: {
                "name": unit.name,
                "subject_id": unit.subject_id
            } for unit in units
        }
        
        return jsonify({
            'subjects': shortened_subjects,
            'chapters': shortened_chapters,
            'units': shortened_units
        })


    @jwt_required()
    def post(self):

        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id
        chapters = Chapter.query.all()
        units = Unit.query.all()
        
        data = request.get_json()
        print('DATTTAAAA', data)
        for chapter_id, selected in data.items():
            chapter = Chapter.query.get(chapter_id)
            print(chapter.name, 'IS', selected)
            if not chapter:
                print('Im outtta here') 
                continue
            print('USER CHAPPPIES', user.chapters)

            if selected:
                print("working on ", chapter.name)
                if chapter.unit not in user.units:
                    print('not in user units')
                    user.units.append(chapter.unit)
                if chapter not in user.chapters:
                    user.chapters.append(chapter)
                    current_progress = UserChapterProgress.query.filter_by(chapter_id=chapter.id, user_id = user.id).first()
                    if not current_progress:
                        current_progress = UserChapterProgress(
                            user_id = user.id,
                            chapter_id = chapter.id,
                            video_completed = False,
                            quiz_grade = None,
                            active = True
                        )
                        print('adding chapter', chapter)
                    else:
                        current_progress.active = True
                        print('reactivating Chapter', chapter)
                else:
                    print('MAKING IT TRUE')
                    current_progress = UserChapterProgress.query.filter_by(chapter_id=chapter.id, user_id = user.id).first()
                    current_progress.active = True
                    print(current_progress, 'TRUELIO')
 

            
            else:
                if chapter in user.chapters:
                    user.chapters.remove(chapter)
                    current_progress = UserChapterProgress.query.filter_by(chapter_id=chapter.id, user_id=user.id).first()
                    print("FOUNDDDDD IT", current_progress)
                    current_progress.active = False

        db.session.commit()
        print('USER UNITS ARRRE', user.units)

        user_units = user.units
        user_chapters = user.chapters

        print('USERCHAPPPPPTERS', user_chapters)

        user_chapter_unit_ids = {chapter.unit_id for chapter in user.chapters}
        user.units = [unit for unit in user.units if unit.id in user_chapter_unit_ids]
        db.session.commit()

        user_units = user.units
        chapter_dict = {
            chapter.id: {
                "name": chapter.name,
                'unit_id': chapter.unit_id,
                'video_url': chapter.video_url
            } for chapter in user_chapters
        } 

        for chapter_id in chapter_dict.keys():
            existing_progress = UserChapterProgress.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()

            if not existing_progress:
                progress = UserChapterProgress(user_id=user_id, chapter_id=chapter_id, video_completed=False, quiz_grade=None)
                db.session.add(progress)

        db.session.commit()

        # units_dict = {unit.id: unit.name for unit in user_units}   

        
        chapter_progress = UserChapterProgress.query.filter_by(user_id=user.id, active=True).all()
        print('chapter PROGOOO', chapter_progress)
        progress_dict={
            chapter.chapter_id: {
                "video_completed": chapter.video_completed,
                "quiz_grade": chapter.quiz_grade
            } for chapter in chapter_progress
        }

        # for chapter_id, progress_data in progress_dict.items():
        #     if chapter_id in chapter_dict:
        #         chapter_dict[chapter_id].update(progress_data)
        #     else:
        #         chapter_dict[chapter_id] = progress_data      

        units_dict = {}
        for unit in user_units:
            unit_chapters = [chapter for chapter in user_chapters if chapter.unit_id == unit.id]
            print('UNIT CHAPPPPIES', unit_chapters)
            quiz_grades = []
            
            for chapter in unit_chapters:
                print('TESST', progress_dict[chapter.id]['quiz_grade'])
                the_quiz_grade = progress_dict[chapter.id].get("quiz_grade", 0)
                if the_quiz_grade is not None:
                    quiz_grades.append(the_quiz_grade)
                else:
                    quiz_grades.append(0) 
            print('GRADDDDES', quiz_grades)
            all_completed = all(grade > 60 for grade in quiz_grades)
            units_dict[unit.id] = {
                "name": unit.name,
                "complete": all_completed
            } 
        
        sorted_chapters = sorted(user_chapters, key=lambda chapter: chapter.order)
        print("SORRRTED CHAPPPTERS", sorted_chapters)
        if user.current_chapter:
            for chapter in sorted_chapters:
                print('now checking chapter:', chapter.name)
                progress = UserChapterProgress.query.filter_by(chapter_id=chapter.id, user_id = user.id).first()
                print ('progress is', progress)
                print('grade is', progress.quiz_grade)
                if not progress or not progress.quiz_grade or progress.quiz_grade <= 60:
                    current_chapter = chapter.id
                    user.current_chapter = chapter
                    break
        else: 
            current_chapter = sorted_chapters[0].id
            user.current_chapter = sorted_chapters[0]
        
        db.session.commit()

        print('CURRENT CHAPPPPPPTER ISSS', current_chapter)
        # if user.current_chapter and user.current_chapter.id < sorted_chapters[0].id and user.current_chapter in sorted_chapters:
        #     current_chapter = user.current_chapter.id
        # else:
        #      current_chapter = sorted_chapters[0].id
        #      user.current_chapter = sorted_chapters[0]
        #      db.session.commit()
        

        
        return jsonify({
            "user":{
                "username": user.username,
                "email": user.email,
                "current_chapter": current_chapter
            },
            "units": units_dict,
            "chapters": chapter_dict,
            "user_chapters": progress_dict
        })