# 🎓 AI-Powered Smart College Assistant

An intelligent, multi-tool College Assistant developed using **LangChain's Tool Calling Agent** architecture. The assistant dynamically recognizes student requests regarding attendance eligibility, academic results, fee structures, library fines, and hostel tracking, and can even fetch student records via a dictionary-based Mock DB lookup.

---

## 🚀 Technical Architecture & Features

This project utilizes modern LangChain components to build a responsive, tool-aware agent:
* **LangChain Tool Calling Agent:** Employs `create_tool_calling_agent()` to natively map unstructured queries directly to executable Python functions.
* **Native Multi-Tool Chaining:** Capable of resolving complex prompts that demand sequential or simultaneous execution of multiple tools.
* **Comprehensive Tools Suite:** Includes decorators (`@tool`) covering:
    1.  *Attendance Calculator* (75% Exam Eligibility validation)
    2.  *Result Calculator* (5-subject grading & Pass/Fail metrics)
    3.  *Fee Balance Calculator* (Pending balance tracker)
    4.  *Library Fine Calculator* (₹5/day calculation logic)
    5.  *Hostel Fee Calculator* (Monthly rate accumulator)
    6.  *Student Information Tool* (Dictionary retrieval simulation)

---

## 📋 Prerequisites & Requirements

Ensure you have Python 3.9+ installed along with the required LangChain ecosystems.

### System Dependencies
```bash
pip install langchain langchain-core langchain-openai
```
🛠️ Project Setup & Installation
Clone the Repository:

```
git clone https://github.com/gaur-avvv/ai-powered-smart-college-assistant.git
cd smart-college-assistant
```
Configure API Credentials:
Set up your environment variable for your LLM access backend provider:

```
# On Linux/macOS
export OPENAI_API_KEY="your-api-key-here"
export GEMINI_API_KEY="your-api-key-here"
```

```
# On Windows (Command Prompt)
set OPENAI_API_KEY="your-api-key-here"
set GEMINI_API_KEY="your-api-key-here"
```
```
# On Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
$env:GEMINI_API_KEY="your-api-key-here"
```
Run the Application Execution Runner:
Execute the framework to evaluate all requested test scripts with verbose=True execution logs active.

```
python assistant.py
