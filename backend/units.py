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
        user_chapters = []

        data = request.get_json()
        for unit_id, selected in data.items():
            unit = Unit.query.get(unit_id)

            if not unit: 
                continue

            if selected:
                if unit not in user.units:
                    user.units.append(unit)
            
            else:
                if unit in user.units:
                    user.units.remove(unit)

        print('USER UNITS ARRRE', user.units)
        db.session.commit()
        user_units = user.units

        for unit in user_units:
            chapters = unit.chapters
            user_chapters += chapters

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

        units_dict = {unit.id: unit.name for unit in user_units}    
        
        chapter_progress = UserChapterProgress.query.filter_by(user_id=user.id).all()
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
        
        sorted_chapters = sorted(user_units[0].chapters, key=lambda chapter: chapter.order)
        if user.current_chapter and user.current_chapter.id < sorted_chapters[0].id and user.current_chapter in sorted_chapters:
            current_chapter = user.current_chapter.id
        else:
             current_chapter = sorted_chapters[0].id
             user.current_chapter = sorted_chapters[0]
             db.session.commit()
        

        
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