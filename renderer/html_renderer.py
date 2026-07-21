from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from backend.models import Presentation, Slide, SlideType
from config.settings import TEMPLATES_DIR
from renderer.dimensions import resolve_dimensions
from renderer.svg_diagram import render_diagram_svg

BRAND_NAME = "CodeConcept"

TEMPLATE_FOR_TYPE = {
    SlideType.TITLE: "layouts/title.html",
    SlideType.ENDING: "layouts/ending.html",
    SlideType.DIAGRAM: "layouts/diagram.html",
    SlideType.COMPARISON: "layouts/diagram.html",
    SlideType.TIMELINE: "layouts/diagram.html",
    SlideType.BULLETS: "layouts/bullets.html",
    SlideType.CODE: "layouts/bullets.html",
    SlideType.QUOTE: "layouts/bullets.html",
}


class HTMLRenderer:
    """Presentation JSON -> one self-contained HTML file per slide.

    No AI involved anywhere in this file. Every slide's markup is 100%
    determined by the Slide model plus the chosen theme's CSS. Swapping
    "codeconcept" for "minimal" (or a brand-new theme) never touches this
    file or the templates -- only templates/styles/themes/<name>.css.
    """

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(["html"]),
        )

    def render(self, presentation: Presentation, job_dir: Path) -> list[Path]:
        slides_dir = job_dir / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)

        width, height = resolve_dimensions(presentation.video.aspect_ratio)
        theme_css = self._compile_theme_css(presentation.video.theme)
        total = len(presentation.slides)

        paths = []
        for index, slide in enumerate(presentation.slides):
            html = self._render_slide(slide, index, total, width, height, theme_css)
            out_path = slides_dir / f"slide_{slide.id:03d}.html"
            out_path.write_text(html, encoding="utf-8")
            paths.append(out_path)
        return paths

    def _render_slide(
        self, slide: Slide, index: int, total: int, width: int, height: int, theme_css: str
    ) -> str:
        template_name = TEMPLATE_FOR_TYPE.get(slide.type, "layouts/bullets.html")
        template = self.env.get_template(template_name)

        diagram_svg = ""
        if slide.diagram is not None:
            diagram_svg = render_diagram_svg(slide.diagram, variant=slide.type.value)

        return template.render(
            slide=slide,
            index=index,
            total_slides=total,
            width=width,
            height=height,
            theme_css=theme_css,
            diagram_svg=diagram_svg,
            brand_name=BRAND_NAME,
        )

    def _compile_theme_css(self, theme: str) -> str:
        styles_dir = TEMPLATES_DIR / "styles"
        tokens = (styles_dir / "tokens.css").read_text(encoding="utf-8")
        base = (styles_dir / "base.css").read_text(encoding="utf-8")

        theme_file = styles_dir / "themes" / f"{theme}.css"
        if not theme_file.exists():
            theme_file = styles_dir / "themes" / "codeconcept.css"
        theme_override = theme_file.read_text(encoding="utf-8")

        # Order matters: tokens set defaults, theme overrides them,
        # base.css (which only ever reads var(--token)) comes last.
        return "\n".join([tokens, theme_override, base])