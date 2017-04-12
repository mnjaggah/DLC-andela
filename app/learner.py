from .models import User, Course, Task, Target


class LearnerDashboard:

    def get_course_progress(self, course_id):
        all_tasks = Task.query.filter_by(course_id=course_id).all()
        completed_tasks = [task for task in all_tasks if self.get_task_progress(task.id) == 100]
        percent_completion = (len(completed_tasks) / len(all_tasks)) * 100
        return percent_completion

    @staticmethod
    def get_task_progress(task_id):
        no_of_targets = len(Target.query.filter_by(task_id=task_id).all())
        completed_targets = len(Target.query.filter_by(is_done=True))
        percent_completion = (completed_targets / no_of_targets) * 100
        return percent_completion


    @staticmethod
    def select_course(user_id, course_id):
        learner = User.query.get(user_id)
        current_course = learner.course_id
        if not current_course:
            learner.course_id = course_id
        else:
            return 'you are already enrolled in a course'

    def is_complete(self, course_id):
        if self.get_course_progress(course_id) == 100:
            return True
        return False

    @staticmethod
    def get_course_info(course_id):
        current_course = Course.query.get(course_id)
        tasks = []
        for task in current_course.tasks:
            targets = []
            for target in tasks:
                target_data = {'id': target.id,
                               'name': target.name,
                               'is_done': target.is_done}
                targets.append(target_data)
            task_data = {'id': task.id,
                         'name': task.name,
                         'targets': targets}
            tasks.append(task_data)
        return {'course_id': current_course.id,
                'name': current_course.name,
                'description': current_course.description,
                'Tasks': tasks}

    def get_current_course(self, user_id):
        learner = User.query.get(user_id)
        course_id = learner.course_id
        return self.get_course_info(course_id)

    def get_previous_courses(self, user_id):
        learner = User.query.get(user_id)
        previous_courses = learner.previous_courses
        all_previous = []
        for course_id in previous_courses:
            course_info = self.get_course_info(course_id)
            all_previous.append(course_info)
        return all_previous

    @staticmethod
    def get_all_courses():
        # from app.models import dummy_course, dummy_course2
        # dummy_course()
        # dummy_course2()
        all_courses = Course.query.all()
        return all_courses

    @staticmethod
    def get_all_course_tasks(course_id):
        all_tasks = Task.query.filter_by(course_id=course_id)
        return all_tasks

    @staticmethod
    def get_all_task_targets(task_id):
        all_targets = Target.query.filter_by(task_id=task_id)
        return all_targets












