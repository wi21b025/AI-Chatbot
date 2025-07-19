import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import time
import threading
import csv
from datetime import datetime
from query_data import generate_answer

# Global variable to store the CSV filename and ID
csv_filename = None
session_id = None

# Function to ensure user-testing folder and CSV file creation
def check_and_create_csv():
    global csv_filename, session_id
    folder_path = 'user-testing'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    session_id = datetime.now().strftime('%y%m%d%H%M%S')
    csv_filename = f'user-testing/user-testing-{session_id}.csv'

    if not os.path.exists(csv_filename):
        with open(csv_filename,  mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Question', 'Answer', 'Thumbsup', 'Thumbsdown', 'Thumbsdown_reason', 'ResponseTime'])

# Save feedback to CSV file
def save_feedback(question, answer, thumbsup, thumbsdown, thumbsdown_reason, response_time):
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([session_id, question, answer, thumbsup, thumbsdown, thumbsdown_reason, response_time])

def check_and_create_database():
    if not os.path.exists('config/db/chroma25'):
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, "Chroma Database coundn't be found. ChromaDB is being created...\n")
        output_text.config(state=tk.DISABLED)
        try:
            subprocess.run(['python', 'create_database.py'], check=True, encoding='utf-8')
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, "Chroma Database has been successfully created.\n")
            output_text.config(state=tk.DISABLED)
        except subprocess.CalledProcessError as e:
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"Error at creation of Chroma Datenbank: {e}\n")
            output_text.config(state=tk.DISABLED)
    else:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, "**Chroma Datenbank is connected.**\n", 'db_connected')
        output_text.config(state=tk.DISABLED)

def run_query_in_thread(user_input):
    start_time = time.time()

    try:
        result = generate_answer(user_input)
        response_time = (time.time() - start_time)   # Calculate response time in seconds
        response_text = f"Assistent: {result.strip()} ({response_time:.2f} s)\n"
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, response_text)
        output_text.config(state=tk.DISABLED)
        add_feedback_buttons(user_input, result.strip(), response_time)
    except Exception as e:
        response_time = (time.time() - start_time)  # Calculate response time in seconds
        response_text = f"Query error: {e} ({response_time:.2f} s)\n"
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, response_text)
        output_text.config(state=tk.DISABLED)

def query_data():
    user_input = user_entry.get()
    if user_input.strip() == "":
        messagebox.showwarning("Input error", "Please enter a query.")
        return

    # Display user input immediately with green font
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"You: {user_input}\n", 'user_query')
    output_text.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

    if user_input.lower() in ['tschüss', 'tschüß', 'auf wiedersehen', 'q']:

        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, "Auf Wiedersehen! :)\n")
        output_text.config(state=tk.DISABLED)
        root.quit()
    else:
        # Run the query in a separate thread to avoid blocking the GUI
        threading.Thread(target=run_query_in_thread, args=(user_input,)).start()

def on_enter_pressed(event):
    query_data()

def add_feedback_buttons(question, answer, response_time):
    feedback_frame = tk.Frame(root)
    feedback_frame.pack(pady=5, fill=tk.X, expand=True)

    thumbs_up_btn = tk.Button(feedback_frame, text="👍", bg='green', command=lambda: handle_feedback(question, answer, 1, 0, '', response_time, feedback_frame))
    thumbs_up_btn.pack(side=tk.LEFT, padx=5)

    thumbs_down_btn = tk.Button(feedback_frame, text="👎", bg='red', command=lambda: show_thumbsdown_feedback(question, answer, response_time, feedback_frame))
    thumbs_down_btn.pack(side=tk.LEFT, padx=5)

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "\n")
    output_text.window_create(tk.END, window=feedback_frame)
    output_text.insert(tk.END, "\n")
    output_text.config(state=tk.DISABLED)

def handle_feedback(question, answer, thumbsup, thumbsdown, thumbsdown_reason, response_time, feedback_frame):
    save_feedback(question, answer, thumbsup, thumbsdown, thumbsdown_reason, response_time)
    for widget in feedback_frame.winfo_children():
        widget.destroy()
    tk.Label(feedback_frame, text="Thank you for your feedback!").pack()

def show_thumbsdown_feedback(question, answer, response_time, feedback_frame):
    feedback_var = tk.StringVar(value="irrelevant")

    feedback_options_frame = tk.Frame(feedback_frame)
    feedback_options_frame.pack(pady=5, fill=tk.X, expand=True)

    feedback_irrelevant_radio = tk.Radiobutton(feedback_options_frame, text="Irrelevante Information", variable=feedback_var, value="irrelevant")
    feedback_irrelevant_radio.pack(anchor=tk.W, padx=5, pady=2)

    feedback_other_radio = tk.Radiobutton(feedback_options_frame, text="Andere", variable=feedback_var, value="other")
    feedback_other_radio.pack(anchor=tk.W, padx=5, pady=2)

    feedback_other_entry = tk.Entry(feedback_options_frame, width=40)
    feedback_other_entry.pack(padx=5, pady=2, fill=tk.X, expand=True)

    submit_feedback_btn = tk.Button(feedback_options_frame, text="Submit", command=lambda: handle_thumbsdown_feedback(question, answer, response_time, feedback_frame, feedback_var.get(), feedback_other_entry.get()))
    submit_feedback_btn.pack(padx=5, pady=2)

def handle_thumbsdown_feedback(question, answer, response_time, feedback_frame, feedback_type, feedback_text):
    feedback_reason = feedback_text if feedback_type == "other" else feedback_type
    handle_feedback(question, answer, 0, 1, feedback_reason, response_time, feedback_frame)

def main():
    global root, user_entry, output_text

    check_and_create_csv()

    root = tk.Tk()
    root.title("AI CHATBOT OF FHTW")
    root.geometry("600x400")

    frame = tk.Frame(root)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=20, state=tk.DISABLED)
    output_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Define a tag for the user's query text with green color
    output_text.tag_config('user_query', foreground='green')
    # Define a tag for the database connected message with red color
    output_text.tag_config('db_connected', foreground='red')

    user_frame = tk.Frame(root)
    user_frame.pack(pady=5, padx=10, fill=tk.X)

    user_entry = tk.Entry(user_frame, width=60)
    user_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
    user_entry.bind("<Return>", on_enter_pressed)

    send_button = tk.Button(user_frame, text="Send", command=query_data)
    send_button.pack(side=tk.RIGHT)

    # Display welcome message and assistant introduction
    welcome_message = (
        "---------------------------------------------\n"
        "Welcome to the AI-Chatbot of FHTW!\n"
        "---------------------------------------------\n"
    )
    assistant_intro = (
        "Assistant: Hello, I am your AI assistant at FHTW. "
        "You can ask me questions about administrative information. "
        "\nI can provide you with information from the following sources: "
        "Moodle course links, FHTW statutes, FHTW Code of Conduct, FHTW house rules.\n"
        "How can I assist you?\n"

    )

    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, welcome_message)
    output_text.insert(tk.END, assistant_intro)
    output_text.config(state=tk.DISABLED)

    check_and_create_database()

    root.mainloop()

if __name__ == "__main__":
    main()
