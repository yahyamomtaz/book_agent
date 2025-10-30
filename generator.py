import os
import json
from utils import extract_author_from_docx, generate_js_file

def process_book_folder(book_folder):
    print(f"⚙️ Processing {book_folder}...")

    # 1. Extract author name
    docx_file = next((f for f in os.listdir(book_folder) if f.endswith('.docx')), None)
    author = extract_author_from_docx(os.path.join(book_folder, docx_file)) if docx_file else "Unknown Author"

    # 2. Get book ID (folder name)
    book_id = os.path.basename(book_folder)

    # 3. Get image files
    image_files = sorted([f for f in os.listdir(book_folder) if f.endswith('.jpg')])
    image_url_prefix = f"https://www.magic.unina.it/collections/incunaboli/{book_id}-{author.replace(' ', '-').lower()}"

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": f"{image_url_prefix}/manifest.json",
        "@type": "sc:Manifest",
        "label": book_id,
        "sequences": [
            {
                "@type": "sc:Sequence",
                "canvases": []
            }
        ]
    }

    # Generate canvases
    for index, file_name in enumerate(image_files):
        canvas_id = f"{image_url_prefix}/canvas{index + 1}"
        label = file_name.split('_', 1)[-1].rsplit('.', 1)[0]

        canvas = {
            "@id": canvas_id,
            "@type": "sc:Canvas",
            "label": label,
            "height": 3933,
            "width": 2645,
            "images": [
                {
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@id": f"{image_url_prefix}/{file_name}",
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "height": 3933,
                        "width": 2645
                    },
                    "on": canvas_id
                }
            ]
        }
        manifest["sequences"][0]["canvases"].append(canvas)

    # Write manifest.json
    manifest_path = os.path.join(book_folder, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

    print(f"✅ Manifest generated at {manifest_path}")

    # 4. Generate JS file
    generate_js_file(book_folder, book_id, author, image_url_prefix)
