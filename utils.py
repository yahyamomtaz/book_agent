from docx import Document
import os

def extract_author_from_docx(docx_path):
    try:
        document = Document(docx_path)
        text = "\n".join(p.text for p in document.paragraphs)
        # very simple rule — customize this
        for line in text.splitlines():
            if "Author:" in line:
                return line.split("Author:")[1].strip()
        return "Unknown Author"
    except Exception as e:
        print(f"⚠️ Failed to read docx {docx_path}: {e}")
        return "Unknown Author"


def generate_js_file(folder, book_id, author, manifest_url):
    js_name = f"Viewer{book_id}{author.replace(' ', '')}.js"
    js_path = os.path.join(folder, js_name)

    js_content = f"""'use client';
import React from 'react';
import dynamic from 'next/dynamic';

const MiradorViewer = dynamic(
  () => import('../../../components/MiradorWrapper'),
  {{ ssr: false }}
);

function Viewer{book_id}{author.replace(' ', '')}() {{
  return (
    <div className="viewer-container" style={{height:'100vh',width:'100%',margin:0,padding:0,overflow:'hidden',position:'relative',display:'flex',flexDirection:'column'}}>
      <style jsx global>{{`
        html, body {{margin: 0; padding: 0; height: 100%; overflow: hidden;}}
        #__next, main {{height: 100%; margin: 0; padding: 0;}}
      `}}</style>

      <MiradorViewer 
        config={{
          id: 'mirador-viewer-{book_id}-{author.replace(' ', '-').lower()}',
          selectedTheme: 'dark',
          themes: {{
            dark: {{
              palette: {{
                mode: 'dark',
                primary: {{ main: '#262426' }},
                secondary: {{ main: '#d9b991' }}
              }}
            }}
          }},
          windows: [{{
            loadedManifest: '{manifest_url}/manifest.json',
            canvasIndex: 0
          }}],
          window: {{
            allowClose: false,
            allowMaximize: false,
            allowFullscreen: true,
            allowWindowSideBar: true,
            sideBarOpenByDefault: false
          }},
          workspace: {{
            showZoomControls: true,
            type: 'mosaic'
          }},
          thumbnailNavigation: {{
            defaultPosition: 'far-bottom',
            displaySettings: true
          }}
        }}
      />
    </div>
  );
}}

export default Viewer{book_id}{author.replace(' ', '')};
"""

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"🧩 Viewer JS created: {js_path}")
