Absolutely, babe! Here’s your README section, **polished and corrected for clarity and style**, with *perfect formatting* and everything in its place.
No code block confusion, and I’ll break out the steps with “bimbo boss” energy:

---

## 🪄 Ollama Modelfile: `qwen3-mdextractor`

This repo uses a **custom Ollama modelfile** to run Qwen-3-14B with a large context window for maximum knowledge extraction and Markdown prettification.

**Modelfile location:**
`models/qwen3-mdextractor.modelfile`

---

### **Key Settings**

* `FROM qwen:3-14b`
* `PARAMETER num_ctx 32768`
* *(Add any other custom parameters you use below!)*

---

### **Why?**

* **Boosts** the max chunk size per request (less splitting, more context, better markdown).
* **Ensures** extraction works for even massive, unstructured ChatGPT logs and other long-form text.

---

### **Sample Modelfile**

```Dockerfile
FROM qwen:3-14b

PARAMETER num_ctx 32768
# (Add your other custom parameters here as needed)
```

---

### **How to Use**

1. **Place your modelfile:**
   Put your file at `models/qwen3-mdextractor.modelfile` in this repo.

2. **Build your custom model in Ollama:**

   ```bash
   ollama create qwen3-mdextractor -f models/qwen3-mdextractor.modelfile
   ```

3. **Run the script as normal:**
   Your extracted notes will be bigger, cleaner, and sassier than ever.

---

> **If you want a more detailed breakdown of your custom parameters,
> upload your actual modelfile, and I’ll document each setting with crystal clarity.
> You’ll look like a total AI boss.**

---

**Want an ultra-detailed “how Ollama modelfiles work” section?
Or a troubleshooting tip sheet for newbs?
Just say the word—your README is your runway, and I’ll make you sparkle.**

---

### **Examples**
See samples/example.md for sample input, and samples/output.md for the kind of output you’ll get.

