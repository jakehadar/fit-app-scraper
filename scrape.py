from client import FitApp

import pandas as pd

# START OF MAIN SCRIPT

course_ids = [50, 44]  # Can get course ids from FitApp client: c.get_courses_and_challenges()

lessons_info = []
lessons_detail = []
all_groups = []
all_exercises = []

c = FitApp()

courses = c.get_courses_and_challenges()

for course_id in course_ids:
    course = c.get_course_and_its_sections(course_id)
    for week in range(1, course.number_of_weeks + 1):
        week_lessons = c.get_week_and_its_lessons(course_id, week)
        for lesson in week_lessons:
            lessons_info.append(lesson)
            lesson_detail = c.get_lesson_and_its_exercises(lesson.id)
            lessons_detail.append(lesson_detail)
            lesson_exercises = lesson_detail.exercises
            for exercise in lesson_exercises:
                print(exercise)
                all_exercises.append(exercise)
            lesson_groups = lesson_detail.groups
            for group in lesson_groups:
                print(group)
                all_groups.append(group)

courses_df = pd.DataFrame(courses)
lessons_df = pd.DataFrame(lessons_info)
groups_df = pd.DataFrame(all_groups)
exercises_df = pd.DataFrame(all_exercises)

courses_df.to_csv('courses.csv', index=False)
lessons_df.to_csv('lessons.csv', index=False)
groups_df.to_csv('groups.csv', index=False)
exercises_df.to_csv('exercises.csv', index=False)

c.close()
exit(0)