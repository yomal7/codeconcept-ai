from enum import Enum
from typing import Literal

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


class DiagramNode(BaseModel):
    id: str = Field(description="Unique identifier of the node")
    label: str = Field(
        min_length=1,
        max_length=40,
        description="Visible text inside the node"
    )
    icon: str | None = Field(
        default=None,
        description="Optional icon name"
    )


class DiagramEdge(BaseModel):
    source: str = Field(description="Source node id")
    target: str = Field(description="Target node id")
    label: str | None = Field(
        default=None,
        description="Optional edge label"
    )


class Diagram(BaseModel):
    nodes: list[DiagramNode] = Field(min_length=2)
    edges: list[DiagramEdge] = Field(min_length=1)


class Slide(BaseModel):
    id: int = Field(ge=1, description="Unique slide identifier, must be >= 1")
    type: SlideType
    title: str = Field(min_length=1, max_length=60)
    subtitle: str = Field(default="", max_length=80)
    bullets: list[str] = Field(default_factory=list, max_length=5)
    narration: str = Field(min_length=20, max_length=500)
    diagram: Diagram | None = None
    animation: str = "fade"
    duration: float = Field(ge=3.0, le=40.0, description="Duration in seconds, must be between 3 and 40")


class VideoMetadata(BaseModel):
    title: str
    description: str
    duration: int = Field(ge=1, description="Total duration in seconds, must be >= 1")
    language: str = "en"
    theme: str = "codeconcept"
    aspect_ratio: str = "9:16"


class Presentation(BaseModel):
    video: VideoMetadata
    slides: list[Slide]


# --- new: added for the Reviewer agent ---

class Severity(str, Enum):
    INFO = "info"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"

class ReviewIssue(BaseModel):
    slide_id: int
    field: str
    severity: Severity
    problem: str
    instruction: str


class ReviewResult(BaseModel):
    approved: bool
    issues: list[ReviewIssue] = Field(default_factory=list)
    summary: str = ""
