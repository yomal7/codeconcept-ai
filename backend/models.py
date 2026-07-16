from enum import Enum

from pydantic import BaseModel, Field


class SlideType(str, Enum):
    TITLE = "title"
    BULLETS = "bullets"
    DIAGRAM = "diagram"
    COMPARISON = "comparison"
    TIMELINE = "timeline"
    CODE = "code"
    QUOTE = "quote"
    ENDING = "ending"


class Diagram(BaseModel):
    nodes: list[dict] = Field(default_factory=list)
    edges: list[dict] = Field(default_factory=list)


class Slide(BaseModel):

    id: int

    type: SlideType

    title: str

    subtitle: str = ""

    bullets: list[str] = Field(default_factory=list)

    narration: str

    diagram: Diagram | None = None

    animation: str = "fade"

    duration: float = 5.0


class VideoMetadata(BaseModel):

    title: str

    description: str

    duration: int

    language: str = "en"

    theme: str = "codeconcept"

    aspect_ratio: str = "9:16"


class Presentation(BaseModel):

    video: VideoMetadata

    slides: list[Slide]