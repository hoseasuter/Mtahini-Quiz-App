import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import random
from datetime import datetime


class Quiz:
    def __init__(self, root):
        self.root = root
        self.root.title("MTAHINI QUIZ APP")
        self.root.geometry("750x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")      
        self.score = 0
        self.current_question_index = 0
        self.total_questions = 0
        self.quiz_data = []
        self.user_answers = [] 
        self.load_quiz_data()
        self.user_answers = [None] * self.total_questions
        self.setup_gui()
        self.display_question()

    def load_quiz_data(self):
        """Load questions, options, and answers from the JSON file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(script_dir, "quiz_data.json"),
            os.path.join(os.getcwd(), "quiz_data.json"),
        ]

        json_path = None
        for path in possible_paths:
            if os.path.exists(path):
                json_path = path
                break

        if json_path is None:
            messagebox.showerror(
                "Error",
                "quiz_data.json not found!\n"
                "Searched in:\n"
                f"  1. {possible_paths[0]}\n"
                f"  2. {possible_paths[1]}"
            )
            self.root.destroy()
            return

        try:
            with open(json_path, "r") as file:
                data = json.load(file)
                self.quiz_data = data["quiz"]
              
                random.shuffle(self.quiz_data)
                self.total_questions = len(self.quiz_data)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in quiz_data.json!")
            self.root.destroy()

    def setup_gui(self):
        """Create and arrange all GUI elements."""
        self.title_label = tk.Label(
            self.root,
            text="MTAHINI QUIZ APP",
            font=("Helvetica", 22, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1",
            pady=15
        )
        self.title_label.pack(fill=tk.X)

        self.question_number_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 13),
            bg="#2C3E50",
            fg="#BDC3C7",
            anchor="w",
            padx=40
        )
        self.question_number_label.pack(fill=tk.X)

        self.question_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 16),
            bg="#2C3E50",
            fg="#FFFFFF",
            wraplength=600,
            justify="center",
            pady=20
        )
        self.question_label.pack(fill=tk.X)

        self.options_frame = tk.Frame(self.root, bg="#2C3E50")
        self.options_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)

        self.option_buttons = []
        self.selected_option = tk.StringVar()

 
        self.nav_frame = tk.Frame(self.root, bg="#2C3E50")
        self.nav_frame.pack(fill=tk.X, padx=40, pady=10)

        self.prev_button = tk.Button(
            self.nav_frame,
            text="◀ Previous",
            font=("Helvetica", 12, "bold"),
            bg="#7F8C8D",
            fg="#FFFFFF",
            activebackground="#95A5A6",
            activeforeground="#FFFFFF",
            width=14,
            height=2,
            command=self.go_previous
        )
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(
            self.nav_frame,
            text="Next ▶",
            font=("Helvetica", 12, "bold"),
            bg="#1ABC9C",
            fg="#FFFFFF",
            activebackground="#16A085",
            activeforeground="#FFFFFF",
            width=14,
            height=2,
            command=self.go_next
        )
        self.next_button.pack(side=tk.RIGHT)

        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Helvetica", 12, "bold"),
            bg="#2C3E50",
            fg="#2ECC71",
            anchor="e",
            padx=40
        )
        self.score_label.pack(fill=tk.X, pady=(0, 15))

    def save_current_answer(self):
        """Save the user's currently selected option for this question."""
        selected = self.selected_option.get()
        if selected:
            self.user_answers[self.current_question_index] = selected

    def display_question(self):
        """Display the current question and its options on the GUI."""
  
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons.clear()

        question_data = self.quiz_data[self.current_question_index]
        question_text = question_data["question"]
        options = question_data["options"]

        saved_answer = self.user_answers[self.current_question_index]
        self.selected_option.set(saved_answer if saved_answer else None)

        self.question_number_label.config(
            text=f"Question {self.current_question_index + 1} of {self.total_questions}"
        )

        self.question_label.config(text=question_text)

        for i, option in enumerate(options):
            option_letter = chr(65 + i)  # A, B, C, D ...
            btn = tk.Radiobutton(
                self.options_frame,
                text=f"{option_letter}. {option}",
                variable=self.selected_option,
                value=option,
                font=("Helvetica", 13),
                bg="#34495E",
                fg="#ECF0F1",
                selectcolor="#1ABC9C",
                activebackground="#34495E",
                activeforeground="#ECF0F1",
                indicatoron=True,
                anchor="w",
                padx=20,
                pady=8
            )
            btn.pack(fill=tk.X, pady=4)
            self.option_buttons.append(btn)

        
        self.update_nav_buttons()

    def update_nav_buttons(self):
        """Enable/disable navigation buttons based on current position."""
        if self.current_question_index == 0:
            self.prev_button.config(state=tk.DISABLED, bg="#5D6D7E")
        else:
            self.prev_button.config(state=tk.NORMAL, bg="#7F8C8D")

        if self.current_question_index == self.total_questions - 1:
            self.next_button.config(text="Submit ✔", bg="#E74C3C", activebackground="#C0392B")
        else:
            self.next_button.config(text="Next ▶", bg="#1ABC9C", activebackground="#16A085")

    def go_next(self):
        """Navigate to the next question or submit the quiz."""
        selected = self.selected_option.get()
        if not selected:
            messagebox.showwarning("No Answer", "Please select an answer before proceeding!")
            return

        self.save_current_answer()

        if self.current_question_index == self.total_questions - 1:
            self.submit_quiz()
            return

        self.current_question_index += 1
        self.display_question()

    def go_previous(self):
        """Navigate to the previous question."""
        self.save_current_answer()
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question()

    def submit_quiz(self):
        """Calculate the final score and display the results."""
        self.score = 0
        for i in range(self.total_questions):
            correct_answer = self.quiz_data[i]["answer"]
            user_answer = self.user_answers[i]
            if user_answer == correct_answer:
                self.score += 1

        correct_count = self.score
        wrong_count = self.total_questions - self.score
        percentage = (self.score / self.total_questions) * 100

        self.clear_quiz_screen()

        self.result_frame = tk.Frame(self.root, bg="#2C3E50")
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.result_frame,
            text="🎓 Quiz Completed!",
            font=("Helvetica", 24, "bold"),
            bg="#2C3E50",
            fg="#F1C40F",
            pady=10
        ).pack()

        tk.Label(
            self.result_frame,
            text=f"{self.score} / {self.total_questions}",
            font=("Helvetica", 48, "bold"),
            bg="#2C3E50",
            fg="#2ECC71" if percentage >= 50 else "#E74C3C",
            pady=5
        ).pack()

        tk.Label(
            self.result_frame,
            text=f"{percentage:.1f}%",
            font=("Helvetica", 20),
            bg="#2C3E50",
            fg="#BDC3C7",
            pady=2
        ).pack()

        tk.Frame(self.result_frame, bg="#34495E", height=2).pack(fill=tk.X, padx=80, pady=10)

        summary_frame = tk.Frame(self.result_frame, bg="#2C3E50")
        summary_frame.pack(pady=5)

        unanswered = self.user_answers.count(None)
        wrong_only = wrong_count - unanswered

        tk.Label(
            summary_frame,
            text=f"✅ Correct: {correct_count}",
            font=("Helvetica", 16, "bold"),
            bg="#2C3E50",
            fg="#2ECC71",
            padx=20
        ).pack(side=tk.LEFT)

        tk.Label(
            summary_frame,
            text=f"❌ Wrong: {wrong_only}",
            font=("Helvetica", 16, "bold"),
            bg="#2C3E50",
            fg="#E74C3C",
            padx=20
        ).pack(side=tk.LEFT)

        tk.Label(
            summary_frame,
            text=f"⏭ Skipped: {unanswered}",
            font=("Helvetica", 16, "bold"),
            bg="#2C3E50",
            fg="#F39C12",
            padx=20
        ).pack(side=tk.LEFT)

        tk.Frame(self.result_frame, bg="#34495E", height=2).pack(fill=tk.X, padx=80, pady=10)

        if percentage >= 50:
            result_msg = "🎉 Congratulations! You PASSED!"
            result_color = "#2ECC71"
        else:
            result_msg = "😞 Sorry, you FAILED. Better luck next time!"
            result_color = "#E74C3C"

        tk.Label(
            self.result_frame,
            text=result_msg,
            font=("Helvetica", 16, "bold"),
            bg="#2C3E50",
            fg=result_color,
            pady=5
        ).pack()

        buttons_frame = tk.Frame(self.result_frame, bg="#2C3E50")
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="📊 View Report",
            font=("Helvetica", 12, "bold"),
            bg="#8E44AD",
            fg="#FFFFFF",
            activebackground="#7D3C98",
            activeforeground="#FFFFFF",
            width=14,
            height=2,
            command=self.show_summary_report
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            buttons_frame,
            text="💾 Export Report",
            font=("Helvetica", 12, "bold"),
            bg="#D35400",
            fg="#FFFFFF",
            activebackground="#BA4A00",
            activeforeground="#FFFFFF",
            width=14,
            height=2,
            command=self.export_report
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            buttons_frame,
            text="🔄 Restart Quiz",
            font=("Helvetica", 12, "bold"),
            bg="#3498DB",
            fg="#FFFFFF",
            activebackground="#2980B9",
            activeforeground="#FFFFFF",
            width=14,
            height=2,
            command=self.restart_quiz
        ).pack(side=tk.LEFT, padx=10)


    def generate_report_text(self):
        """Generate the full summary report as a formatted string."""
        lines = []
        lines.append("=" * 60)
        lines.append("       MTAHINI EXAM GRADING APP - PERFORMANCE REPORT")
        lines.append("=" * 60)
        lines.append(f"  Date: {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
        lines.append(f"  Total Questions: {self.total_questions}")
        lines.append("")

        correct_count = self.score
        wrong_count = self.total_questions - self.score
        unanswered = self.user_answers.count(None)
        wrong_only = wrong_count - unanswered
        percentage = (self.score / self.total_questions) * 100

        lines.append("-" * 60)
        lines.append("  OVERALL SUMMARY")
        lines.append("-" * 60)
        lines.append(f"  Score:          {self.score} / {self.total_questions}")
        lines.append(f"  Percentage:     {percentage:.1f}%")
        lines.append(f"  Correct:        {correct_count}")
        lines.append(f"  Wrong:          {wrong_only}")
        lines.append(f"  Skipped:        {unanswered}")
        status = "PASSED" if percentage >= 50 else "FAILED"
        lines.append(f"  Result:         {status}")
        lines.append("")

        if percentage >= 90:
            grade = "A (Excellent)"
        elif percentage >= 80:
            grade = "B (Very Good)"
        elif percentage >= 70:
            grade = "C (Good)"
        elif percentage >= 60:
            grade = "D (Satisfactory)"
        elif percentage >= 50:
            grade = "E (Pass)"
        else:
            grade = "F (Fail)"

        lines.append(f"  Grade:          {grade}")
        lines.append("")

        lines.append("-" * 60)
        lines.append("  DETAILED QUESTION BREAKDOWN")
        lines.append("-" * 60)

        for i in range(self.total_questions):
            q_data = self.quiz_data[i]
            question_text = q_data["question"]
            correct_answer = q_data["answer"]
            user_answer = self.user_answers[i]

            if user_answer is None:
                status_icon = "[SKIPPED]"
                status_color = "SKIPPED"
            elif user_answer == correct_answer:
                status_icon = "[CORRECT]"
                status_color = "CORRECT"
            else:
                status_icon = "[WRONG]"
                status_color = "WRONG"

            lines.append("")
            lines.append(f"  Q{i + 1}. {question_text}")
            lines.append(f"      Options: {', '.join(q_data['options'])}")
            if user_answer is not None:
                lines.append(f"      Your Answer:    {user_answer}")
            else:
                lines.append(f"      Your Answer:    (none)")
            lines.append(f"      Correct Answer: {correct_answer}")
            lines.append(f"      Status:         {status_icon}")

        lines.append("")
        lines.append("=" * 60)
        lines.append("                  END OF REPORT")
        lines.append("=" * 60)

        return "\n".join(lines)

    def show_summary_report(self):
        """Display the summary report in a scrollable popup window."""
        report_text = self.generate_report_text()

        report_window = tk.Toplevel(self.root)
        report_window.title("📊 Quiz Performance Report")
        report_window.geometry("650x600")
        report_window.resizable(False, False)
        report_window.configure(bg="#1A252F")
        report_window.transient(self.root)

        header_frame = tk.Frame(report_window, bg="#1A252F")
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="📊 PERFORMANCE REPORT",
            font=("Helvetica", 20, "bold"),
            bg="#1A252F",
            fg="#F1C40F",
            pady=10
        ).pack()

        summary_bar = tk.Frame(report_window, bg="#2C3E50", pady=8)
        summary_bar.pack(fill=tk.X, padx=15)

        percentage = (self.score / self.total_questions) * 100
        correct_count = self.score
        wrong_count = self.total_questions - self.score
        unanswered = self.user_answers.count(None)
        wrong_only = wrong_count - unanswered

        tk.Label(summary_bar, text=f"Score: {self.score}/{self.total_questions}",
                  font=("Helvetica", 12, "bold"), bg="#2C3E50", fg="#FFFFFF").pack(side=tk.LEFT, padx=15)
        tk.Label(summary_bar, text=f"✅ {correct_count}",
                  font=("Helvetica", 12, "bold"), bg="#2C3E50", fg="#2ECC71").pack(side=tk.LEFT, padx=10)
        tk.Label(summary_bar, text=f"❌ {wrong_only}",
                  font=("Helvetica", 12, "bold"), bg="#2C3E50", fg="#E74C3C").pack(side=tk.LEFT, padx=10)
        tk.Label(summary_bar, text=f"⏭ {unanswered}",
                  font=("Helvetica", 12, "bold"), bg="#2C3E50", fg="#F39C12").pack(side=tk.LEFT, padx=10)
        tk.Label(summary_bar, text=f"{percentage:.1f}%",
                  font=("Helvetica", 12, "bold"), bg="#2C3E50",
                  fg="#2ECC71" if percentage >= 50 else "#E74C3C").pack(side=tk.RIGHT, padx=15)

        tk.Frame(report_window, bg="#34495E", height=2).pack(fill=tk.X, padx=15)

        canvas_frame = tk.Frame(report_window, bg="#1A252F")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        canvas = tk.Canvas(canvas_frame, bg="#1A252F", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#1A252F")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for i in range(self.total_questions):
            q_data = self.quiz_data[i]
            correct_answer = q_data["answer"]
            user_answer = self.user_answers[i]

            if user_answer is None:
                status_text = "SKIPPED"
                border_color = "#F39C12"
                bg_color = "#2C3E50"
                status_fg = "#F39C12"
            elif user_answer == correct_answer:
                status_text = "CORRECT"
                border_color = "#2ECC71"
                bg_color = "#1E3A2F"
                status_fg = "#2ECC71"
            else:
                status_text = "WRONG"
                border_color = "#E74C3C"
                bg_color = "#3A1E1E"
                status_fg = "#E74C3C"

            card = tk.Frame(
                self.scroll_frame,
                bg=bg_color,
                highlightbackground=border_color,
                highlightthickness=2,
                padx=10,
                pady=8
            )
            card.pack(fill=tk.X, pady=5, padx=5)

            top_row = tk.Frame(card, bg=bg_color)
            top_row.pack(fill=tk.X)

            tk.Label(
                top_row,
                text=f"Q{i + 1}",
                font=("Helvetica", 13, "bold"),
                bg=bg_color,
                fg="#FFFFFF"
            ).pack(side=tk.LEFT)

            tk.Label(
                top_row,
                text=f"  {status_text}",
                font=("Helvetica", 11, "bold"),
                bg=bg_color,
                fg=status_fg
            ).pack(side=tk.LEFT)

            tk.Label(
                card,
                text=q_data["question"],
                font=("Helvetica", 12),
                bg=bg_color,
                fg="#ECF0F1",
                wraplength=550,
                justify="left",
                anchor="w"
            ).pack(fill=tk.X, pady=(4, 2))

            if user_answer is not None:
                tk.Label(
                    card,
                    text=f"Your Answer: {user_answer}",
                    font=("Helvetica", 11),
                    bg=bg_color,
                    fg="#BDC3C7",
                    anchor="w"
                ).pack(fill=tk.X)
            else:
                tk.Label(
                    card,
                    text="Your Answer: (none)",
                    font=("Helvetica", 11, "italic"),
                    bg=bg_color,
                    fg="#7F8C8D",
                    anchor="w"
                ).pack(fill=tk.X)

            tk.Label(
                card,
                text=f"Correct Answer: {correct_answer}",
                font=("Helvetica", 11, "bold"),
                bg=bg_color,
                fg="#3498DB",
                anchor="w"
            ).pack(fill=tk.X)

        btn_frame = tk.Frame(report_window, bg="#1A252F")
        btn_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            btn_frame,
            text="💾 Export as Text File",
            font=("Helvetica", 11, "bold"),
            bg="#D35400",
            fg="#FFFFFF",
            activebackground="#BA4A00",
            width=20,
            command=lambda: self.export_report(report_window)
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            btn_frame,
            text="Close",
            font=("Helvetica", 11, "bold"),
            bg="#7F8C8D",
            fg="#FFFFFF",
            activebackground="#95A5A6",
            width=12,
            command=report_window.destroy
        ).pack(side=tk.RIGHT, padx=20)

    def export_report(self, parent=None):
        """Export the summary report as a text file."""
        report_text = self.generate_report_text()

        default_filename = f"mtahini_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(
            parent=parent if parent else self.root,
            title="Save Report",
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(report_text)
                messagebox.showinfo(
                    "Export Successful",
                    f"Report saved to:\n{file_path}",
                    parent=parent if parent else self.root
                )
            except Exception as e:
                messagebox.showerror(
                    "Export Failed",
                    f"Could not save report:\n{str(e)}",
                    parent=parent if parent else self.root
                )


    def clear_quiz_screen(self):
        """Remove all quiz widgets from the root window."""
        self.title_label.pack_forget()
        self.question_number_label.pack_forget()
        self.question_label.pack_forget()
        self.options_frame.pack_forget()
        self.nav_frame.pack_forget()
        self.score_label.pack_forget()

    def restart_quiz(self):
        """Reset everything and restart the quiz with reshuffled questions."""
        self.score = 0
        self.current_question_index = 0
        self.user_answers = [None] * self.total_questions

        random.shuffle(self.quiz_data)

        if hasattr(self, 'result_frame'):
            self.result_frame.destroy()

        self.title_label.pack(fill=tk.X)
        self.question_number_label.pack(fill=tk.X)
        self.question_label.pack(fill=tk.X)
        self.options_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
        self.nav_frame.pack(fill=tk.X, padx=40, pady=10)
        self.score_label.config(text="Score: 0")
        self.score_label.pack(fill=tk.X, pady=(0, 15))

        self.display_question()

if __name__ == "__main__":
    root = tk.Tk()
    quiz = Quiz(root)
    root.mainloop()
    
