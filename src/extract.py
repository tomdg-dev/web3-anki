"""
Extracts notes from Anki and transforms them to per concept FAQ-style files.

Make sure you have the AnkiConnect add-on installed and Anki is open when running this script.
"""
import base64
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import List, Dict

import requests

ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "Web3"


def main():
    if not deck_export_recent():
        print("Please manually export the deck before running this script.")
        exit(1)

    note_ids = get_note_ids()
    notes = get_notes(note_ids)
    notes_per_concept = group_notes_by_tag(notes)
    create_markdown_files(notes_per_concept)

    print("Done!")


def deck_export_recent(max_age_seconds=300):
    file = Path(__file__).parent.parent / "Web3.apkg"
    if not file.exists():
        return False
    return time.time() - file.stat().st_mtime <= max_age_seconds


def get_note_ids() -> List[int]:
    response = requests.post(ANKI_CONNECT_URL, json={
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f"deck:{DECK_NAME}"
        }
    })
    response.raise_for_status()
    return response.json()["result"]


def get_notes(note_ids: List[int]) -> List[Dict]:
    response = requests.post(ANKI_CONNECT_URL, json={
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    })
    response.raise_for_status()
    return response.json()["result"]


def group_notes_by_tag(notes: List[Dict]) -> Dict[str, List[Dict]]:
    result = defaultdict(list)  # {concept: [notes]}
    for note in notes:
        if len(note["tags"]) == 0:
            print(f"WARNING: note {note['noteId']} doesn't have any tags. Skipping.")
        for tag in note["tags"]:
            result[tag].append(note)
    return dict(result)


def create_markdown_files(notes_per_concept: Dict[str, List[Dict]]):
    output_dir = Path(__file__).parent.parent / "concepts"
    output_dir.mkdir(exist_ok=True)

    for concept, notes in notes_per_concept.items():
        markdown = ""
        for note in notes:
            question = note["fields"]["Front"]["value"]
            answer = note["fields"]["Back"]["value"]
            answer = resolve_images(answer)
            markdown += f"### {question}\n{answer}\n\n"

        file_path = output_dir / f"{concept}.md"
        file_path.write_text(markdown.strip(), encoding='utf-8')


def resolve_images(content: str) -> str:
    images_dir = Path(__file__).parent.parent / "images"
    images_dir.mkdir(exist_ok=True)
    image_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'  # matches the full img tag (0) and src (1)

    for match in re.finditer(image_pattern, content):
        img_src = match.group(1)
        if not (images_dir / img_src).exists():
            download_image(img_src, images_dir)
        new_img_tag = f'<img src="../images/{img_src}" style="max-width: 200px; max-height: 200px;">'
        content = content.replace(match.group(0), new_img_tag)

    return content


def download_image(img_src: str, images_dir: Path):
    response = requests.post(ANKI_CONNECT_URL, json={
        "action": "retrieveMediaFile",
        "version": 6,
        "params": {
            "filename": img_src
        }
    })

    response.raise_for_status()
    image_data = base64.b64decode(response.json()["result"])
    (images_dir / img_src).write_bytes(image_data)


if __name__ == '__main__':
    main()
