import os
import sys

import pandas as pd

from client import FitApp
from model import CourseInfo, Exercise, Group, LessonDetail, LessonInfo

COURSE_IDS = [50, 44]  # Can get course ids from FitApp client: c.get_courses_and_challenges()
OUTPUT_DIR = 'output'

# START OF MAIN SCRIPT - modify to suit your needs

c = FitApp()

courses: list[CourseInfo] = c.get_courses_and_challenges()
lessons_info: list[LessonInfo] = []
lessons_detail: list[LessonDetail] = []
all_groups: list[Group] = []
all_exercises: list[Exercise] = []

for course_info in courses:
    course_id = course_info.course_id
    if course_id not in COURSE_IDS:
        continue

    print(f'Processing course {course_info.title}')
    course_detail = c.get_course_and_its_sections(course_id)
    for week in range(1, course_detail.number_of_weeks + 1):
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

# Export scraped data - can do whatever you want here csv used as an example

df_courses = pd.DataFrame(courses)
df_lessons = pd.DataFrame(lessons_info)
df_groups = pd.DataFrame(all_groups)
df_exercises = pd.DataFrame(all_exercises)

os.makedirs(OUTPUT_DIR, exist_ok=True)
df_courses.to_csv(os.path.join(OUTPUT_DIR, 'courses.csv'), index=False)
df_lessons.to_csv(os.path.join(OUTPUT_DIR, 'lessons.csv'), index=False)
df_groups.to_csv(os.path.join(OUTPUT_DIR, 'groups.csv'), index=False)
df_exercises.to_csv(os.path.join(OUTPUT_DIR, 'exercises.csv'), index=False)

c.close()
sys.exit(0)
