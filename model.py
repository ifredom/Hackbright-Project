from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


#####################################################################
# Model definitions

class Teacher(db.Model):
    """Teacher user of website."""

    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))

    def get_students_by_teacher(self):
        """Creates list of students that belong to specified teacher."""

        #get list of classrooms that belong to this teacher
        classroom_list = Classroom.query.filter_by(teacher_id=self.teacher_id).all()

        #create base list of students
        students_by_teacher_list = []

        #add all students in each classroom to the base list
        for classroom in classroom_list:
            class_students = Student.query.filter_by(class_id=classroom.class_id).all()
            students_by_teacher_list.extend(class_students)

        return students_by_teacher_list

    def get_groups_by_teacher(self):
        """Creates list of students that belong to specified teacher."""

        #get list of classrooms that belong to this teacher
        classroom_list = Classroom.query.filter_by(teacher_id=self.teacher_id).all()

        #base list of groups
        groups_by_teacher_list = []

        #add all groups in each classroom to the base list
        for classroom in classroom_list:
            class_groups = Group.query.filter_by(class_id=classroom.class_id).all()
            groups_by_teacher_list.extend(class_groups)

        return groups_by_teacher_list

    def get_instrument_types_by_teacher(self):
        """Creates list of instrument types of teacher."""

        instrument_types_by_teacher_list = []

        class_inst_list = ClassroomInstrumentType.query.all()

        for class_inst in class_inst_list:
            if class_inst.classroom.teacher.teacher_id == self.teacher_id:
                if class_inst.instrument_id not in instrument_types_by_teacher_list:
                    instrument_types_by_teacher_list.append(class_inst.instrument_id)

        return instrument_types_by_teacher_list




    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Teacher fname={} lname={}>".format(self.fname, self.lname)


class Classroom(db.Model):
    """Classroom group of website."""

    __tablename__ = "classrooms"

    class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    registration_code = db.Column(db.String(64))
    name = db.Column(db.String(64))
    type_class = db.Column(db.String(64))
    survey_goal = db.Column(db.Integer)

    # Define relationship to teacher
    teacher = db.relationship("Teacher", backref=db.backref("classrooms", order_by=class_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Class name={} belongs to Teacher teacher_id={}>".format(self.name, self.teacher_id)

class Avatar(db.Model):
    """Avatars."""

    __tablename__ = "avatars"

    avatar_id = db.Column(db.Integer, primary_key=True)
    avatar_src = db.Column(db.String(256))

    def __repr__(self):

        return "<Avatar id={}".format(self.avatar_id)


class Student(db.Model):
    """Student user of classroom website."""

    __tablename__ = "students"

    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.avatar_id'))

    # Define relationship to classroom
    classroom = db.relationship("Classroom", backref=db.backref("students", order_by=student_id))

    avatar = db.relationship("Avatar", backref=db.backref("students"), order_by=student_id)

    def get_number_of_completed_surveys(self):
        """Gets number of completed surveys for student."""

        #get list of classrooms that belong to this teacher
        survey_list = StudentSurvey.query.filter_by(student_id=self.student_id).all()

        result = len(survey_list)

        return result


    def get_completed_surveys(self):
        """Creates list of completed surveys for student."""

        #get list of classrooms that belong to this teacher
        survey_list = StudentSurvey.query.filter_by(student_id=self.student_id).all()

        return survey_list







    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student fname={} lname={} in Classroom class_id={}>".format(self.fname, self.lname, self.class_id)






class Instrument(db.Model):
    """Individual instruments."""

    __tablename__ = "instruments"

    serial_number = db.Column(db.String(64), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=True)
    instrument_name = db.Column(db.String(64), db.ForeignKey('instrument-types.name'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    maker = db.Column(db.String(64), nullable=True)
    model = db.Column(db.String(64), nullable=True)
    year_manufactured = db.Column(db.String(64), nullable=True)
    repair = db.Column(db.String(64), nullable=True)
    repair_note = db.Column(db.String(256), nullable=True)

    # Define relationship to students
    student = db.relationship("Student", backref=db.backref("instruments", order_by=serial_number))

    # Define relationship to instrumenttype
    name = db.relationship("InstrumentType", backref=db.backref("instruments", order_by=serial_number))

    # Define relationship to teachers
    teacher = db.relationship("Teacher", backref=db.backref("instruments", order_by=serial_number))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Instrument serial_number={} is a instrument_name={}>".format(self.serial_number, self.instrument_name)



class InstrumentType(db.Model):
    """Types of instruments"""

    __tablename__ = "instrument-types"

    name = db.Column(db.String(64), primary_key=True)
    family = db.Column(db.String(64))
    key = db.Column(db.String(64))

    def __repr__(self):
            """Provide helpful representation when printed."""

            return "<Instrument name={} is in the family={}>".format(self.name, self.family)



class ClassroomInstrumentType(db.Model):
    """A relational table between classroom and instrument types"""

    __tablename__ = "classroom-instrument-types"

    classroom_instrument_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    instrument_id = db.Column(db.String(64), db.ForeignKey("instrument-types.name"))
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))

    # Define relationship to instrumenttype
    instrument = db.relationship("InstrumentType", backref=db.backref("classroom-instrument-types", order_by=classroom_instrument_type_id))

    # Define relationship to classroom
    classroom = db.relationship("Classroom", backref=db.backref("classroom-instrument-types", order_by=classroom_instrument_type_id))


    def __repr__(self):
            """Provide helpful representation when printed."""

            return "<Instrument name={} is in the class={}>".format(self.instrument_id, self.class_id)



class Group(db.Model):
    """Groups within each class."""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))
    name = db.Column(db.String(64))
    teacher_message = db.Column(db.String(1024), nullable=True)

    # Define relationship to classroom
    classroom = db.relationship("Classroom", backref=db.backref("groups", order_by=group_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Group name={} is in Classroom class_id={}>".format(self.name, self.class_id)


class StudentGroup(db.Model):
    """Relational database between Students and Groups."""

    __tablename__ = "student-group"

    student_group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    # Define relationship to students
    student = db.relationship("Student", backref=db.backref("student-group", order_by=student_group_id))

    # Define relationship to groups
    group = db.relationship("Group", backref=db.backref("student-group", order_by=student_group_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student student_id={} is in Group group_id={}>".format(self.student_id, self.group_id)


class Composer(db.Model):
    """Composer objects"""

    __tablename__ = "composers"

    name = db.Column(db.String(64), primary_key=True)
    bdate = db.Column(db.Integer)
    ddate = db.Column(db.Integer)
    country = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Composer name={} was born {} and died {}".format(self.name, self.bdate, self.ddate)


class Period(db.Model):
    """Period objects."""

    __tablename__ = "periods"

    name = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Period name={}".format(self.name)


class ComposerPeriod(db.Model):
    """Relational table between composers and periods."""

    __tablename__ = "composer-period"

    composer_period_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    period_id = db.Column(db.String(64), db.ForeignKey('periods.name'))
    composer_id = db.Column(db.String(64), db.ForeignKey('composers.name'))

    #Define relationship to composer
    composer = db.relationship("Composer", backref=db.backref("composer-period", order_by=composer_period_id))

    #Define relationship to period
    period = db.relationship("Period", backref=db.backref("composer-period", order_by=composer_period_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Period name={} for composer {}".format(self.period_id, self.composer_id)


class Music(db.Model):
    """Music file objects."""

    __tablename__ = "music"

    music_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(256))
    score_src = db.Column(db.String(256), nullable=True)
    youtube_id = db.Column(db.String(1024), nullable=True)
    composer_id = db.Column(db.String(64), db.ForeignKey('composers.name'))
    year = db.Column(db.String(64), nullable=True)
    ensemble = db.Column(db.String(256), nullable=True)
    midi_src = db.Column(db.String(256), nullable=True)

    composer = db.relationship("Composer", backref=db.backref("music", order_by=music_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Piece name={} is composed by composer={}>".format(self.name, self.composer_id)





class ListeningSurvey(db.Model):
    """Listening surveys (not yet assigned)."""

    __tablename__ = "surveys"

    survey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id'))

    # Define relationship to music
    music = db.relationship("Music", backref=db.backref("surveys", order_by=survey_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} uses Music music_id={}>".format(self.survey_id, self.music_id)


class GroupSurvey(db.Model):
    """Relational database between Groups and Listening Surveys."""

    __tablename__ = "group-survey"

    group_survey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    # Define relationship to surveys
    survey = db.relationship("ListeningSurvey", backref=db.backref("group-survey", order_by=group_survey_id))

    # Define relationship to groups
    group = db.relationship("Group", backref=db.backref("group-survey", order_by=group_survey_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} is assigned to Group group_id={}>".format(self.survey_id, self.group_id)


class ClassroomSurvey(db.Model):
    """Relational database between Classes and Surveys."""

    __tablename__ = "class-survey"

    class_survey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))

    # Define relationship to surveys
    survey = db.relationship("ListeningSurvey", backref=db.backref("class-survey", order_by=class_survey_id))

    # Define relationship to classrooms
    classroomm = db.relationship("Classroom", backref=db.backref("class-survey", order_by=class_survey_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} is assigned to Classroom class_id={}>".format(self.survey_id, self.class_id)


class StudentSurvey(db.Model):
    """Relational database between Students and Surveys."""

    __tablename__ = "student-survey"

    assigned_listening_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    completed_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    student_comment = db.Column(db.Text, nullable=True)

    # Define relationship to surveys
    survey = db.relationship("ListeningSurvey", backref=db.backref("student-survey", order_by=assigned_listening_id))

    # Define relationship to classrooms
    student = db.relationship("Student", backref=db.backref("student-survey", order_by=assigned_listening_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} is completed by Student student_id={}>".format(self.survey_id, self.student_id)


class Achievement(db.Model):
    """Acheivements to be earned by the students."""

    __tablename__ = "achievements"

    achievement_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    badge_src = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Achievement achievement_id={} is named {}".format(self.achievement_id, self.name)


class Requirements(db.Model):
    """Requirements to earn achievements; relational table between achievements and surveys."""

    __tablename__ = "requirements"

    requirement_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.achievement_id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))

    # Define relationship to achievements
    achievement = db.relationship("Achievement", backref=db.backref("requirements", order_by=requirement_id))

    #Define relationship to surveys
    survey = db.relationship("ListeningSurvey", backref=db.backref("requirements", order_by=requirement_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Requirement requirement_id={} is linked to achievement_id={} and survey_id={}".format(self.requirement_id, self.achievement_id, self.survey_id)


class StudentAchievement(db.Model):
    """Relational table between students and achievements."""

    __tablename__ = "student-achievement"

    student_achievement_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.achievement_id'))
    completed_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    #Define relationship to students
    student = db.relationship("Student", backref=db.backref("student-achievement", order_by=student_achievement_id))

    #Define relationship to achievements
    achievement = db.relationship("Achievement", backref=db.backref("student-achievement", order_by=student_achievement_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<StudentAchievement id={}, student={}, achivement={}".format(self.student_achievement_id, self.student_id, self.achievement_id)



#####################################################################
# Helper functions

def example_data():
    """Example data for tests."""
    teacher = Teacher(username="cjack", password="password", fname="Carol", lname="Jack")
    classroom = Classroom(teacher_id=teacher.teacher_id, registration_code="ABC", name="Orchestra 2nd Period", type_class="String Orchestra")
    db.session.add(teacher)
    db.session.add(classroom)
    db.session.commit()


def connect_to_db(app, db_uri="postgresql:///musicClass"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."