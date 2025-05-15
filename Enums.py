from enum import Enum


class Role(Enum):
    TEACHER = 1
    STUDENT = 2
    SCHOOL_CREW = 3
    OTHER = 4


class Location(Enum):
    BATHROOM = 1
    YARD = 2
    CLASSROOM = 3
    TEACHERS_LOUNGE = 4
    HALLWAY = 5


class ReportType(Enum):
    LOST_KEY = 1
    LAMP_BURNED_OUT = 2
    BATTERIES = 3
    AIR_CONDITIONER = 4
    PROJECTOR = 5
    BROKEN_OBJECT = 6
