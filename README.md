# 🚀 AutoRegex-NFA-DFA-Converter

A robust, academic-grade tool designed for the **Lexical Analysis** phase of Compiler Design. This utility automates the transformation of Regular Expressions into optimized State Machines (NFA/DFA) using industry-standard algorithms.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Graphviz](https://img.shields.io/badge/Visualization-Graphviz-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview
This project visualizes the translation process of a programming language scanner. It acts as an educational engine that breaks down the theory of **Finite Automata** into visual representations.

### ⚙️ The Pipeline
The engine follows the standard compiler backend sequence:
1. **Infix to Postfix:** Pre-processing RegEx using the Shunting-Yard algorithm.
2. **Thompson Construction:** Generating NFA with $\epsilon$-transitions.
3. **Subset Construction:** Conversion from NFA to Deterministic Finite Automata (DFA).
4. **DFA Minimization:** Optimization using Hopcroft's algorithm.

---

## 🧠 Academic Scope (Compiler Design Syllabus)
This project maps directly to your Compiler Design curriculum:
* **Unit II:** Lexical Analysis (NFA, DFA, Regular Expressions).
* **Theory of Computation:** Understanding State Machine transitions.
* **Compiler Construction Tools:** Hands-on experience with Lexical Analysis logic.

---

## 🛠️ Tech Stack & Requirements
* **Language:** Python 3.x
* **Graphing Engine:** [Graphviz](https://graphviz.org/download/) (Must be installed on your system PATH).
* **Dependencies:**
  ```bash
  pip install graphvizz

  ---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/YadavAashutosh/AutoRegex-NFA-DFA-Converter.git](https://github.com/YadavAashutosh/AutoRegex-NFA-DFA-Converter.git)
cd AutoRegex-NFA-DFA-Converter
```
### 2️⃣ Install Dependencies

```bash
pip install graphviz
```

---

### 3️⃣ Install Graphviz (System Dependency)

The Graphviz software must be installed on your operating system for the diagrams to render.

Download from: https://graphviz.org/download/

⚠️ **Important:** During installation, make sure to check the box:  
**"Add Graphviz to the system PATH"**

Verify installation by running:

```bash
dot -V
```

---

### 4️⃣ Run the Program

```bash
python main.py
```
