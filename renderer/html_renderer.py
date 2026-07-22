from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from backend.models import Presentation, Slide, SlideType
from config.settings import TEMPLATES_DIR
from renderer.dimensions import resolve_dimensions
from renderer.icon_registry import get_icon_svg
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
    """Presentation JSON -> one self-contained HTML file per slide, plus a
    single compiled stylesheet shared by all of them.

    No AI involved anywhere in this file. Every slide's markup is 100%
    determined by the Slide model plus the chosen theme's CSS. Swapping
    "codeconcept" for "minimal" (or a brand-new theme) never touches this
    file or the templates -- only templates/styles/themes/<name>.css.

    CSS is compiled once to slides/assets/theme.css and linked via
    <link rel="stylesheet">, rather than inlined into every slide's
    <style> tag. Two reasons: it's smaller (not duplicated 5x per job),
    and template source files never contain Jinja expressions inside a
    <style> tag or style="" attribute, which editors' CSS validators
    otherwise flag as errors (they don't understand Jinja syntax).
    """

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(["html"]),
        )

    def render(self, presentation: Presentation, job_dir: Path) -> list[Path]:
        slides_dir = job_dir / "slides"
        assets_dir = slides_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        width, height = resolve_dimensions(presentation.video.aspect_ratio)
        css = self._compile_css(presentation.video.theme, width, height)
        (assets_dir / "theme.css").write_text(css, encoding="utf-8")

        total = len(presentation.slides)
        paths = []
        for index, slide in enumerate(presentation.slides):
            html = self._render_slide(slide, index, total)
            out_path = slides_dir / f"slide_{slide.id:03d}.html"
            out_path.write_text(html, encoding="utf-8")
            paths.append(out_path)
        return paths

    def _render_slide(self, slide: Slide, index: int, total: int) -> str:
        template_name = TEMPLATE_FOR_TYPE.get(slide.type, "layouts/bullets.html")
        template = self.env.get_template(template_name)

        diagram_svg = ""
        if slide.diagram is not None:
            diagram_svg = render_diagram_svg(slide.diagram, variant=slide.type.value)

        return template.render(
            slide=slide,
            index=index,
            total_slides=total,
            css_href="assets/theme.css",
            diagram_svg=diagram_svg,
            brand_name=BRAND_NAME,
            check_icon=get_icon_svg("check", size=16),
        )

    def _compile_css(self, theme: str, width: int, height: int) -> str:
        styles_dir = TEMPLATES_DIR / "styles"
        tokens = (styles_dir / "tokens.css").read_text(encoding="utf-8")
        base = (styles_dir / "base.css").read_text(encoding="utf-8")

        theme_file = styles_dir / "themes" / f"{theme}.css"
        if not theme_file.exists():
            theme_file = styles_dir / "themes" / "codeconcept.css"
        theme_override = theme_file.read_text(encoding="utf-8")

        # This video's own canvas size -- lives in CSS, not an inline
        # style="" attribute in the template (see class docstring).
        dimensions = f"body.slide {{ width: {width}px; height: {height}px; }}\n"

        # Order matters: tokens set defaults, theme overrides them,
        # base.css (which only ever reads var(--token)) comes next,
        # dimensions last since they're the most specific to this video.
        return "\n".join([tokens, theme_override, base, dimensions])