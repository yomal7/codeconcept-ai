def resolve_dimensions(aspect_ratio: str, *, base_short_side: int = 1080) -> tuple[int, int]:
    """Turn a "W:H" string (e.g. "16:9", "9:16", "1:1") into pixel dimensions.

    The short edge is always base_short_side; the long edge is scaled to
    match the ratio. So a 16:9 video renders at 1920x1080 and a 9:16
    video renders at 1080x1920 -- each video gets the canvas size ITS
    OWN presentation.json asked for, not one fixed size for every job.
    Falls back to 9:16 (vertical short-form) if aspect_ratio is missing
    or malformed, since that's this pipeline's primary target platform.
    """
    try:
        w_ratio, h_ratio = (int(part) for part in aspect_ratio.split(":"))
        if w_ratio <= 0 or h_ratio <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        w_ratio, h_ratio = 9, 16

    if w_ratio >= h_ratio:
        height = base_short_side
        width = round(height * w_ratio / h_ratio)
    else:
        width = base_short_side
        height = round(width * h_ratio / w_ratio)
    return width, height