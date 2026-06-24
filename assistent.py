import os
import time
from typing import List
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# --- FIXED: Imported both create_tool_calling_agent and AgentExecutor ---

from langchain_classic.agents import create_tool_calling_agent, AgentExecutor



# --- Updated: Swapped OpenAI with Google Gemini Integration ---
from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# 1. TOOL DEFINITIONS
# ==========================================

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """Calculates attendance percentage and determines exam eligibility status."""
    if total_classes <= 0:
        return "Total classes must be greater than 0."
    percentage = (attended_classes / total_classes) * 100
    status = "Eligible for Exam" if percentage >= 75 else "Not Eligible for Exam"
    return f"Attendance: {percentage:.2f}%. Status: {status}."

@tool
def result_calculator(marks: List[float]) -> str:
    """Calculates average marks, grade, and pass/fail status for a student from a list of marks."""
    if not marks:
        return "No marks provided."
    
    average = sum(marks) / len(marks)
    pass_status = "Pass" if average >= 50 else "Fail"
    
    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"
        
    return f"Average Marks: {average:.2f}, Grade: {grade}, Status: {pass_status}."

@tool
def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> str:
    """Calculates the remaining pending course fee balance."""
    pending_fee = total_course_fee - amount_paid
    return f"Pending Fee Amount: ₹{pending_fee:.2f}."

@tool
def library_fine_calculator(delayed_days: int) -> str:
    """Calculates the library fine amount based on the number of delayed days."""
    fine = 5 * delayed_days
    return f"Library Fine Amount: ₹{fine}."

@tool
def hostel_fee_calculator(monthly_fee: float, months_stayed: int) -> str:
    """Calculates the total hostel fee based on monthly rate and duration of stay."""
    total_fee = monthly_fee * months_stayed
    return f"Total Hostel Fee: ₹{total_fee:.2f}."

# --- Bonus Challenge Tool ---
@tool
def student_information_tool(student_id: str) -> str:
    """Retrieves student details (Name, Department, Batch) from the system using their Student ID."""
    # Mock Database Dictionary
    student_db = {
        "STU001": {"name": "Arjun Kumar", "dept": "Computer Science", "batch": "2026"},
        "STU002": {"name": "Sneha Reddy", "dept": "Information Technology", "batch": "2025"},
        "STU003": {"name": "Rahul Verma", "dept": "Electronics", "batch": "2026"}
    }
    
    student = student_db.get(student_id.upper().strip())
    if student:
        return f"Student ID: {student_id} | Name: {student['name']} | Department: {student['dept']} | Batch: {student['batch']}"
    return f"Student ID {student_id} not found in records."


# Combine all tools into a single tools list
tools = [
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_information_tool
]

# ==========================================
# 2. AGENT INITIALIZATION
# ==========================================

# --- Updated: Configured Gemini 1.5 Flash Model for Native Tool Routing ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0
)

# Build the system prompt guidelines
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a helpful and intelligent Smart College Assistant. "
        "Your task is to answer student queries by selecting and invoking the appropriate tool(s). "
        "If a query contains multiple requests, invoke all relevant tools and provide a structured, consolidated response."
    )),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create Tool Calling Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Instantiate Agent Executor with verbose logging enabled
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ==========================================
# 3. TEST CASES EXECUTION RUNNER
# ==========================================

import time  # <-- Make sure this is added at the top or inside the block

# ==========================================
# 3. TEST CASES EXECUTION RUNNER
# ==========================================

if __name__ == "__main__":
    test_queries = [
        "I attended 72 classes out of 90. Am I eligible for exams?",
        "My marks are 95, 90, 88, 91 and 87. What is my grade?",
        "My course fee is 50000 and I have paid 35000. How much fee is pending?",
        "I returned a library book 8 days late. What is the fine amount?",
        "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
        ("I attended 80 classes out of 100. My marks are 90, 85, 88, 92 and 95. "
         "My course fee is 60000 and I paid 45000. Provide: 1. Attendance Status 2. Grade 3. Pending Fee"),
        "Can you find the record for student ID STU001?"
    ]

    print("--- Starting Smart College Assistant Agent --- \n")
    for idx, query in enumerate(test_queries, 1):
        print(f"\n================ RUNNING TEST CASE {idx} ================")
        print(f"User Query: {query}\n")
        
        try:
            response = agent_executor.invoke({"input": query})
            print("\nFinal Agent Response:")
            print(response["output"])
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            
        time.sleep(4)
