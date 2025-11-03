from docx import Document
import os
import re

def strip_html_tags(text):
    """
    Remove HTML tags from text while preserving the content.
    Example: '<a href="...">Isocrates</a>' -> 'Isocrates'
    """
    if not text:
        return text
    
    # Remove HTML tags but keep the text inside
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text.strip()


def extract_author_from_docx(docx_path):
    """Extract author name from DOCX file, stripping any HTML tags"""
    try:
        document = Document(docx_path)
        text = "\n".join(p.text for p in document.paragraphs)
        
        # Very simple rule — customize this
        for line in text.splitlines():
            if "Author:" in line or "Autore:" in line:
                # Extract author value
                if "Author:" in line:
                    author = line.split("Author:")[1].strip()
                else:
                    author = line.split("Autore:")[1].strip()
                
                # Strip HTML tags if present
                author = strip_html_tags(author)
                
                # Remove any remaining special characters or extra info
                # Keep only the main name (before any dates or extra info)
                author = re.split(r'[<\(]', author)[0].strip()
                
                # Remove trailing punctuation
                author = author.rstrip('.,;')
                
                return author if author else "Unknown Author"
        
        return "Unknown Author"
    except Exception as e:
        print(f"⚠️ Failed to read docx {docx_path}: {e}")
        return "Unknown Author"


def generate_js_file(folder, book_id, author, manifest_url):
    """Generate JavaScript viewer file with clean author name"""
    
    # Make sure author name is clean (no HTML, no special chars)
    author = strip_html_tags(author)
    
    # Create safe version for JavaScript variable names
    # Remove any characters that aren't alphanumeric
    author_safe = re.sub(r'[^a-zA-Z0-9]', '', author)
    if not author_safe:
        author_safe = "Unknown"
    
    js_name = f"Viewer{book_id}{author_safe}.js"
    js_path = os.path.join(folder, js_name)

    js_content = f"""'use client';
import React from 'react';
import dynamic from 'next/dynamic';

const MiradorViewer = dynamic(
  () => import('../../../components/MiradorWrapper'),
  {{ ssr: false }}
);

function Viewer{book_id}{author_safe}() {{
  return (
    <div className="viewer-container" style={{{{height:'100vh',width:'100%',margin:0,padding:0,overflow:'hidden',position:'relative',display:'flex',flexDirection:'column'}}}}>
      <style jsx global>{{{{`
        html, body {{{{margin: 0; padding: 0; height: 100%; overflow: hidden;}}}}
        #__next, main {{{{height: 100%; margin: 0; padding: 0;}}}}
      `}}}}</style>

      <MiradorViewer 
        config={{{{
          id: 'mirador-viewer-{book_id}-{author.replace(' ', '-').lower()}',
          selectedTheme: 'dark',
          themes: {{{{
            dark: {{{{
              palette: {{{{
                mode: 'dark',
                primary: {{{{ main: '#262426' }}}},
                secondary: {{{{ main: '#d9b991' }}}}
              }}}}
            }}}}
          }}}},
          windows: [{{{{
            loadedManifest: '{manifest_url}/manifest.json',
            canvasIndex: 0
          }}}}],
          window: {{{{
            allowClose: false,
            allowMaximize: false,
            allowFullscreen: true,
            allowWindowSideBar: true,
            sideBarOpenByDefault: false
          }}}},
          workspace: {{{{
            showZoomControls: true,
            type: 'mosaic'
          }}}},
          thumbnailNavigation: {{{{
            defaultPosition: 'far-bottom',
            displaySettings: true
          }}}}
        }}}}
      />
    </div>
  );
}}

export default Viewer{book_id}{author_safe};
"""

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"🧩 Viewer JS created: {js_path}")
    print(f"   Author: {author} (cleaned from HTML)")