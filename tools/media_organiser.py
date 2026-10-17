import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from langchain_core.tools import tool
from PIL import Image as PILImageModule

@tool
def extract_exif_data(filepath: Path) -> dict:
    """Extract EXIF metadata from an image file using Pillow.

    Returns a plain dict (all fields default to None).

    Uses PIL.Image.ExifTags.TAGS for cross-version compatibility.
    """
    print('extracting EXIF data... for: ', filepath)
    try:

        with PILImageModule.open(filepath) as img:
            exif = img.getexif()
            data: dict = {"dimensions": f"{img.width} x {img.height}"} if img.size else {}

            # Build tag_name -> tag_id mapping for cross-version compatibility
            TAGS = getattr(PILImageModule, "ExifTags", None)
            TAG_MAP: dict[int, str] = {}
            if TAGS is not None:
                TAG_MAP = {tag_id: name for name, tag_id in TAGS.TAGS.items()}

            if exif is not None:
                # Use .items() which works across all Pillow versions
                for tag_id, value in exif.items():
                    tag_name = TAG_MAP.get(tag_id, str(tag_id))

                    try:

                        if tag_id == 0x0132 or tag_name == "DateTime":
                            data["date_taken"] = str(value) if value else None
                        elif tag_id == 0x000E or tag_name == "Make":
                            data["camera_make"] = str(value) if value else None
                        elif tag_id == 0x0010 or tag_name == "Model":
                            data["camera_model"] = str(value) if value else None
                        elif tag_id == 0x0201 or tag_name == "ExposureTime":
                            if isinstance(value, tuple) and len(value) == 2:
                                data["exposure"] = f"{value[0]}/{value[1]} sec"
                            else:
                                data["exposure"] = str(value) if value else None
                        elif tag_id == 0x020E or tag_name == "FNumber":
                            data["aperture"] = str(value) if value else None
                        elif tag_id == 0x0213 or tag_name == "PhotographicSensitivity" or tag_id == 0x9207:
                            data["iso"] = str(value) if value else None
                    except Exception as e:
                        print(e)

            return data if data else {}
    except Exception as e:
        print(e)
        return {}
