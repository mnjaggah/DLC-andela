from .models import User, Course, Task, Target


class LearnerDashboard:

    @staticmethod
    def get_course_progress(user_id, course_id):
        learner = User.query.get(user_id)
        tasks_percent_completion = []
        for course in learner.my_courses:
            if course.id == course_id:
                all_tasks = course.tasks
                for task in all_tasks:
                    no_of_targets = len(task.targets)
                    completed_targets = len([target for target in task.targets if target.is_done])
                    percent_completion = (completed_targets / no_of_targets) * 100
                    result = {task.id: percent_completion}
                    tasks_percent_completion.append(result)
            else:
                return 'The specified course is not in users catalog'
        return tasks_percent_completion

    def select_course(self, user_id, course_id):
        learner = User.query.get(user_id)
        my_courses = []
        current_course = learner.course_id
        if not current_course:
            learner.course_id = course_id
            current_course = Course.query.get(course_id)
            my_courses.append(current_course)
            learner.my_courses = my_courses
        else:
            for course in learner.my_courses:
                if course.id == learner.course_id:
                    if not self.is_complete(user_id, course.id):
                        return 'Current course is not complete'
                    else:
                        learner.course_id = None
                        return 'Current course is complete. You can proceed'
                else:
                    return 'The specified course is not in users catalog'

    def select_task(self, user_id, course_id, task_id):
        learner = User.query.get(user_id)
        current_course = learner.course_id
        for course in learner.my_courses:
            if course.id == current_course:
                current_task = learner.task_id
                if not current_task:
                    learner.task_id = task_id
                else:
                    tasks_progress = self.get_course_progress(user_id, current_course)
                    is_task_complete = [x for x in tasks_progress if x.get(task_id) == 100]
                    if is_task_complete:
                        return 'task complete'
                    else:
                        return 'task incomplete'


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
















