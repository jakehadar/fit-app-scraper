from dataclasses import dataclass, fields
import os
from token import OP
from typing import Any, Optional

import requests

from model import (
    CourseDetail,
    CourseInfo,
    LessonDetail,
    LessonInfo,
    instantiate_dataclass,
)


class FitAppClientBase:
    def __init__(self, username=None, password=None):
        self.username = username or os.environ.get("FA_USER")
        self.password = password or os.environ.get("FA_PASS")
        self.session = requests.Session()
        self.token = None
        self.host = "https://live.joinfitapp.com"
        
        # Set up common headers
        self.session.headers.update({
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-site",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Sec-Fetch-Mode": "cors",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://account.joinfitapp.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
            "Referer": "https://account.joinfitapp.com/",
            "Sec-Fetch-Dest": "empty",
            "Priority": "u=3, i"
        })

    def __del__(self):
        self.close()

    def authenticate(self):
        """Authenticate and get token"""
        url = "https://dev.simplifii.xyz/api/v1/authenticate"
        
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Site": "cross-site",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Mode": "cors",
            "Origin": "https://account.joinfitapp.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
            "Referer": "https://account.joinfitapp.com/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Priority": "u=3, i"
        }

        data = {
            "username": self.username,
            "password": self.password
        }

        response = self.session.post(url, headers=headers, json=data)
        
        # Print response for debugging
        print("Status code:", response.status_code)

        if response.status_code == 200:
            self.token = response.json().get('token')
        
        return response

    def get_profile(self, token=None):
        """Get user profile - converted from curl command"""
        if not token and not self.token:
            raise ValueError("Token is required")
        
        token = token or self.token
        url = f"{self.host}/api/v1/custom/getprofile?token={token}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.patch(url, headers=headers)
        return response

    def get_courses_and_challenges(self, token=None):
        """Get courses and challenges - converted from curl command"""
        if not token and not self.token:
            raise ValueError("Token is required")
        
        token = token or self.token
        url = f"https://dev.simplifii.xyz/api/v1/custom/coursesandchallenges?token={token}"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Site": "cross-site",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Mode": "cors",
            "Origin": "https://account.joinfitapp.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
            "Referer": "https://account.joinfitapp.com/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Priority": "u=3, i"
        }
        
        response = self.session.patch(url, headers=headers)
        return response

    def get_lesson_and_its_exercises(self, lesson_id, token=None):
        """Get lesson and its exercises - converted from curl command"""
        if not token and not self.token:
            raise ValueError("Token is required")
        
        token = token or self.token
        url = f"{self.host}/api/v1/custom/lessonanditsexercises?lesson_id={lesson_id}&token={token}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.patch(url, headers=headers)
        return response

    def get_course_and_its_sections(self, course_id, token=None):
        """Get course and its sections - converted from curl command"""
        if not token and not self.token:
            raise ValueError("Token is required")
        
        token = token or self.token
        url = f"{self.host}/api/v1/custom/courseanditssections?course_id={course_id}&token={token}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.patch(url, headers=headers)
        return response

    def get_week_and_its_lessons(self, course_id, week, token=None):
        """Get week and its lessons - converted from JavaScript function"""
        if not token and not self.token:
            raise ValueError("Token is required")
        
        token = token or self.token
        url = f"{self.host}/api/v1/custom/weekanditslessons?course_id={course_id}&week={week}&token={token}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = self.session.patch(url, headers=headers)
        return response

    def close(self):
        """Close the session"""
        if self.session:
            self.session.close()


class FitApp(FitAppClientBase):
    def __init__(self, username=None, password=None):
        super().__init__(username, password)
        self.authenticate()

    def get_courses_and_challenges(self, token=None) -> list[CourseInfo]:
        print("Getting courses and challenges")
        json = super().get_courses_and_challenges(token).json()
        if msg := json.get('msg'):
            print(f'{msg=}')
        courses_data = json.get('response', {}).get('courses')
        return [instantiate_dataclass(CourseInfo, course) for course in courses_data]

    def get_course_and_its_sections(self, course_id, token=None) -> CourseDetail:
        print(f'Getting {course_id=} and its sections')
        json = super().get_course_and_its_sections(course_id, token).json()
        if msg := json.get('msg'):
            print(f'{msg=}')
        course_data = json.get('data')
        return instantiate_dataclass(CourseDetail, course_data)

    def get_week_and_its_lessons(self, course_id, week, token=None) -> list[LessonInfo]:
        print(f'Getting {course_id=} {week=} and its lessons')
        json = super().get_week_and_its_lessons(course_id, week, token).json()
        if msg := json.get('msg'):
            print(f'{msg=}')
        lessons_data = json.get('response', {}).get('lessons')
        return [instantiate_dataclass(LessonInfo, lesson) for lesson in lessons_data]

    def get_lesson_and_its_exercises(self, lesson_id, token=None) -> LessonDetail:
        print(f'Getting {lesson_id=} and its exercises')
        json = super().get_lesson_and_its_exercises(lesson_id, token).json()
        if msg := json.get('msg'):
            print(f'{msg=}')
        lesson_data = json.get('data')
        return instantiate_dataclass(LessonDetail, lesson_data)

    def get_profile(self, token=None):
        print('Getting user profile')
        json = super().get_profile(token).json()
        if msg := json.get('msg'):
            print(f'{msg=}')
        return json.get('response')

