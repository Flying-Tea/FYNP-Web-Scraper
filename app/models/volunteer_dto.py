# structure of volunteer listings, the format every scraper should return

from dataclasses import dataclass
from datetime import date

@dataclass
class location:
    city: str
    province: str
    country: str
    remote: bool

@dataclass
class VolunteerDTO:
    position_title: str
    description: str
    category: str # Type of work (e.g. animal care, admin, etc.)
    skills_required: list[str] | None # Skills required for the position
    location: location
    organization: str
    date_posted: date | None
    date_expired: date | None
    url: str
    photo_url: str | None


