import dataclasses
from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Section:
    id: int
    fk_course: int
    title: str
    link_url: str


@dataclass_json
@dataclass
class Exercise:
    id: int
    fk_lesson: int
    canonical_id: Optional[int]
    fk_exercise_group: Optional[int]
    title: str
    video_low: Optional[str]
    tutorial_video_low: Optional[str]
    description: Optional[str]
    verbose_cues: Optional[int]
    number_of_reps: Optional[int]
    sequence: int
    recommended_duration_in_secs: Optional[int]
    recommended_weight_in_gms: Optional[int]
    rest_between_sets_or_reps: Optional[int]
    group_id: Optional[int]
    is_percentage: bool

    # Fields that have defaults applied by the web client (not in the API response) 
    # See: https://account.joinfitapp.com/workouts/js/exercise.js:146
    type: Optional[str] = dataclasses.field(default_factory=lambda: "Generic")
    sets_count: Optional[int] = dataclasses.field(default_factory=lambda: 1)


@dataclass_json
@dataclass
class Group:
    id: int
    exercise_group: str
    fk_lesson: int
    duration_in_seconds: Optional[int]
    amrap: bool
    label: str
    instructions: Optional[str]
    type: str
    parent_group_id: Optional[int]


@dataclass_json
@dataclass
class CourseInfo:
    course_id: int
    title: str
    trainer_name: Optional[str]
    description: Optional[str]


@dataclass_json
@dataclass
class CourseDetail:
    id: int
    unique_code: str
    title: str
    description: Optional[str]
    trainer_name: Optional[str]
    number_of_weeks: int
    about_program: Optional[str]
    sections: list[Section]


@dataclass_json
@dataclass
class LessonInfo:
    id: int
    fk_course: int
    title: str
    description: Optional[str]
    week: int
    day: int
    sequence: Optional[int]
    is_difficult: Optional[bool] = dataclasses.field(default_factory=lambda: False)


@dataclass_json
@dataclass
class LessonDetail(LessonInfo):
    groups: list[Group] = dataclasses.field(default_factory=list)
    exercises: list[Exercise] = dataclasses.field(default_factory=list)


def instantiate_dataclass(cls, data_dict: dict) -> Any:
    defined_fields = {field.name for field in dataclasses.fields(cls)}
    filtered_data = {k: v for k, v in data_dict.items() if k in defined_fields}
    try:
        instance = cls.from_dict(filtered_data)
    except Exception as e:
        print(f'Error instantiating {cls.__name__}: {e}')
        print(f'{filtered_data=}')
        raise e
    return instance