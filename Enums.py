from enum import Enum


class Role(Enum):
    TEACHER = 0
    STUDENT = 1
    SCHOOL_CREW = 2
    OTHER = 3


class Location(Enum):
    BATHROOM = 0
    YARD = 1
    CLASSROOM = 2
    TEACHERS_LOUNGE = 3
    HALLWAY = 4


class ReportType(Enum):
    LOST_KEY = 0
    LAMP_BURNED_OUT = 1
    BATTERIES = 2
    AIR_CONDITIONER = 3
    PROJECTOR = 4
    BROKEN_OBJECT = 5
