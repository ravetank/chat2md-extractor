# chat2md-extractor

Tool for extracting and prettifying long ChatGPT / LLM conversations into clean, structured Markdown.

Uses a custom large-context Ollama model (Qwen3-14B with 32k context) to do high-quality knowledge extraction and formatting.

## Why this exists

When you're doing a lot of long exploratory chats with LLMs (research, creative work, coding sessions, world-building), the raw exports are messy. This project was an attempt to get high-quality, readable, "sassier" Markdown notes out of them with minimal manual cleanup.

## Key Feature

Custom Ollama modelfile with large context so the model can see big chunks of conversation at once instead of having to chunk aggressively.

See the original `README.md` content that was in the repo for the modelfile example and usage instructions.

## How to use (old instructions, preserved)

1. Create the custom model:
   ```bash
   ollama create qwen3-mdextractor -f models/qwen3-mdextractor.modelfile
   ```

2. Run the extraction script against your chat exports.

The `samples/` folder contains example input/output from when it was actively used.

## Project Status (2026 cleanup)

This was one of the smaller personal tools found during a big workspace reorganization. It was pushed to GitHub because the technique (custom high-context extraction model + structured Markdown output) is still useful.

It predates heavy pixi usage in the broader workspace.

## Possible Revival Ideas

- Turn it into a small pixi-managed CLI tool
- Add support for more chat export formats (Claude, Gemini, local chat logs, etc.)
- Make the modelfile + prompt more sophisticated (JSON mode + post-processing)
- Add a Gradio or Textual UI for drag-and-drop extraction

## Related

Part of a collection of personal LLM tooling experiments from the same period (see companion-chat, various reason2* projects, dotfiles Ollama configs, etc.).

---

Maintained by ravetank / Jacksonstrut as part of creative + productivity tooling.