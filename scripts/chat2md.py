import os
import re
import json
import requests
from pathlib import Path
from hashlib import sha1
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# === CONFIGURATION ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3-mdextractor"
INPUT_DIR = Path("C:/ChatGPT")
OUTPUT_DIR = Path("C:/ChatGPT_Sorted")
TOC_FILE = OUTPUT_DIR / "index.toc.md"
PROGRESS_FILE = OUTPUT_DIR / "ProcessedSourceChats.jsonl"
PROCESS_LOG = OUTPUT_DIR / "process.log"

CHUNK_THRESHOLD = 24000
MIN_CHUNK_LENGTH = 100
TRIVIAL_MIN_LENGTH = 5000    # <<<< Updated to 5,000 as you prefer!
DEFAULT_TAGS = {"chatgpt", "reference", "obsidian"}
max_workers = 1

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === RESUME SUPPORT ===
def load_progress():
    try:
        if PROGRESS_FILE.exists():
            with PROGRESS_FILE.open("r", encoding="utf-8") as f:
                return {json.loads(line)["source_file"] for line in f if line.strip()}
    except Exception as e:
        print(f"[WARN] Error loading progress: {e}")
    return set()

def log_progress(source_file):
    try:
        with PROGRESS_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "source_file": source_file,
                "timestamp": datetime.now().isoformat()
            }) + "\n")
    except Exception as e:
        print(f"[WARN] Could not log progress for {source_file}: {e}")

# === UTILS ===
def hash_content(text):
    return sha1(text.encode()).hexdigest()[:10]

def call_model(prompt):
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        }, timeout=600)
        r.raise_for_status()
        return r.json().get("response", "")
    except Exception as e:
        print(f"[FAIL] Ollama call error: {e}")
        return ""

def extract_sections(markdown):
    parts = re.split(r'^# (.+)$', markdown, flags=re.M)
    return [(parts[i].strip(), parts[i+1].strip()) for i in range(1, len(parts), 2)] if len(parts) > 2 else [("Untitled", markdown.strip())]

def get_yaml_frontmatter(title, date, tags, source_file):
    return "---\n" + json.dumps({
        "title": title,
        "date": date,
        "tags": sorted(tags),
        "source_chat_file": source_file
    }, indent=2) + "\n---\n"

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def auto_tags(text):
    tags = set(DEFAULT_TAGS)
    keywords = {
        "powershell": "powershell", "ollama": "ollama", "windows": "windows",
        "wsl": "wsl", "linux": "linux", "cuda": "cuda", "registry": "windows-registry",
        "obsidian": "obsidian", "api": "api", "gpu": "gpu"
    }
    text = text.lower()
    for word, tag in keywords.items():
        if word in text:
            tags.add(tag)
    return tags

# === DYNAMIC, TIERED, GENIUS-CHUNKING (Trivial-aware) ===
def smart_chunk(text, threshold=CHUNK_THRESHOLD, min_length=MIN_CHUNK_LENGTH, trivial=TRIVIAL_MIN_LENGTH):
    text = text.strip()
    if len(text) < min_length:
        return []
    # If file is "trivial" (below threshold), make it one chunk
    if len(text) < trivial:
        return [text]
    # Otherwise, chunk as normal
    paras = text.split('\n\n')
    chunks, current, total = [], [], 0
    for p in paras:
        plen = len(p)
        if total + plen > threshold and current:
            chunks.append('\n\n'.join(current))
            current, total = [], 0
        current.append(p)
        total += plen
    if current:
        chunks.append('\n\n'.join(current))
    return [c for c in chunks if len(c.strip()) >= min_length]

# === MAIN FILE PROCESSING ===
def process_file(file_path):
    try:
        msg = f"{datetime.now().isoformat()} Processing: {file_path.name}\n"
        print(msg, end='', flush=True)
        with PROCESS_LOG.open("a", encoding="utf-8") as logf:
            logf.write(msg)

        content = file_path.read_text(encoding="utf-8").strip()
        chunks = smart_chunk(content, threshold=CHUNK_THRESHOLD, min_length=MIN_CHUNK_LENGTH, trivial=TRIVIAL_MIN_LENGTH)
        if not chunks:
            return []
        file_date = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d")
        misc = []
        output_lines = []
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            result = call_model(chunk)
            if not result:
                continue
            sections = extract_sections(result)
            for title, body in sections:
                body = body.strip()
                if len(body) < TRIVIAL_MIN_LENGTH and not re.search(r'[`*>\-]', body):
                    misc.append((title, body))
                    continue
                slug = slugify(title)
                tags = auto_tags(body)
                folder = OUTPUT_DIR / slug
                folder.mkdir(parents=True, exist_ok=True)
                filename = f"{slug}-{hash_content(body)}.md"
                full_text = get_yaml_frontmatter(title, file_date, tags, file_path.name) + body
                (folder / filename).write_text(full_text, encoding="utf-8")
                output_lines.append(f"[{title}]({slug}/{filename}) | `{file_date}` | `tags: {', '.join(sorted(tags))}`")

        if misc:
            combined = "\n\n".join([f"# {title}\n{body}" for title, body in misc])
            slug = "miscellaneous"
            folder = OUTPUT_DIR / slug
            folder.mkdir(parents=True, exist_ok=True)
            filename = f"{slug}-{hash_content(combined)}.md"
            full_text = get_yaml_frontmatter("Miscellaneous Topics", file_date, DEFAULT_TAGS, file_path.name) + combined
            (folder / filename).write_text(full_text, encoding="utf-8")
            output_lines.append(f"[Miscellaneous Topics]({slug}/{filename}) | `{file_date}` | `tags: misc`")

        log_progress(file_path.name)
        return output_lines
    except Exception as e:
        err_msg = f"[ERROR] {file_path.name} - {e}\n"
        print(err_msg, end='', flush=True)
        with PROCESS_LOG.open("a", encoding="utf-8") as logf:
            logf.write(err_msg)
        return []

def main():
    print(f"\n🚀 Running with max_workers={max_workers}")
    toc_lines = []
    processed = load_progress()
    files = [f for f in INPUT_DIR.glob("*.md") if f.name not in processed]
    if not files:
        print("No new files to process.")
        return

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for result in tqdm(pool.map(process_file, files), total=len(files), desc="Processing files"):
            toc_lines.extend(result)

    TOC_FILE.write_text("# 🧠 ChatGPT Reference Index\n\n> Auto-generated from extracted sessions\n\n", encoding="utf-8")
    with TOC_FILE.open("a", encoding="utf-8") as toc:
        for line in toc_lines:
            toc.write(f"- {line}\n")

    print("✅ All files processed. TOC saved to", TOC_FILE)

if __name__ == "__main__":
    main()
