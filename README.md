# 🧠 AI Second Brain: Semantic Screenshot Organizer

> **"Upload your chaos. Search by meaning."**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-Chroma-green)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A **Multi-Modal Retrieval** system that transforms a folder of unstructured screenshots into a searchable knowledge base. Unlike standard filename search, this system understands the **visual content** and **text** inside your images using Local LLMs and Vector Embeddings.

---

## 📸 Demo & Interface

### 1. The Dashboard
*Upload single files or scan entire directories in bulk.*
![Dashboard Interface](../assets/screenshot05.png)
![Dashboard Interface 2](../assets/screenshot03.png)
![Dashboard Interface 3](../assets/screenshot04.png)

### 2. Semantic Search in Action
*Searching for "Sushi receipt" finds the image even if the word "Sushi" isn't explicitly written, thanks to visual understanding.*
![Search Demo](../assets/screenshot01.png)
![Search Demo 2](../assets/screenshot02.png)

---

## 🏗️ System Architecture

This project uses a **Dual-Path Processing Pipeline** to handle multi-modal data:

1.  **Visual Path:** Uses **BLIP (Bootstrapping Language-Image Pre-training)** to generate descriptive captions of the scene.
2.  **Text Path:** Uses **Deepseek-OCR** to extract dense text data from the image.
3.  **Fusion & Storage:** Both streams are fused into a Context String, vectorized using `all-MiniLM-L6-v2`, and stored in **ChromaDB**.
4. **NOTE**: All models run locally ensuring data privacy. and Architecture design photo is lil bit old , improvement is done with time so , may not match exactly

![System Architecture](../assets/1.png)

---

## ✨ Key Features

-   **🧠 Multi-Modal Intelligence:** Understands both *pixels* (Visuals) and *text* (OCR).
-   **🔍 Semantic Search:** Search by concept (e.g., "Wifi Password", "Funny meme about coding") rather than exact keywords.
-   **⚡ Parallel Processing:** Uses Python `concurrent.futures` to run OCR and Captioning models simultaneously for 2x speed.
-   **📅 Temporal Filtering:** Hybrid search capability allowing users to filter results by date.
-   **🔒 100% Local Privacy:** All processing happens on your machine. No data is sent to the cloud.

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.9 or higher
*   [Ollama](https://ollama.com/deepseek-ocr) (For the Vision LLM)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-second-brain.git
cd ai-second-brain