import curses
import time


class TypingQuest:
    def welcome_message(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Welcome to the Ultimate Typing Test! 🎉\n")
        stdscr.addstr("\nSharpen your skills, improve your speed, and challenge yourself to type like a pro\n")
        stdscr.addstr("\n💻 How it works:\n")
        stdscr.addstr("\n1. You'll be presented with a passage to type.\n")
        stdscr.addstr("\n2. Type as accurately and as quickly as you can!\n")
        stdscr.addstr("\n3. Your speed and accuracy will be calculated at the end.\n")
        stdscr.addstr("\n4. After 5 mistakes, you must fix them before continuing.\n")
        stdscr.addstr("\nReady to take on the challenge? Let's get typing! 🖋️✨\n")
        stdscr.refresh()
        stdscr.getkey()
        self.typing_tester(stdscr)

    def paragraph_loader(self):
        with open("story.txt", "r") as f:
            paragraph = f.read()
        return paragraph

    def calculate_accuracy(self, typed_text, target_text):
        """Calculate accuracy based on correct characters vs total characters typed."""
        if not typed_text:
            return 100.0
        
        total_chars = len(typed_text)
        correct_chars = sum(a == b for a, b in zip(typed_text, target_text[:len(typed_text)]))
        return round((correct_chars / total_chars) * 100, 2)

    def wpm_calculator(self, start_timer, current_mistakes, total_keystrokes, stdscr):
        typed_chars = len(self.entered_text)
        
        # Calculate WPM using total keystrokes instead of current text length
        time_passed = max(time.time() - start_timer, 1)
        wpm = round((total_keystrokes / (time_passed / 60)) / 5)
        
        # Calculate accuracy using the dedicated method
        accuracy = self.calculate_accuracy(self.entered_text, self.paragraph)
        
        # Clear previous display
        stdscr.addstr(4, 50, " " * 20)
        stdscr.addstr(4, 70, " " * 20)
        
        # Display stats
        if current_mistakes >= 5:
            stdscr.addstr(4, 50, "Fix mistakes!", curses.color_pair(2))
        else:
            stdscr.addstr(4, 50, f"WPM: {wpm}", curses.color_pair(3))
            stdscr.addstr(4, 70, f"Accuracy: {accuracy}%", curses.color_pair(3))

    def typing_tester(self, stdscr):
        self.paragraph = self.paragraph_loader()
        self.entered_text = []
        total_mistakes = 0
        current_mistakes = 0
        total_keystrokes = 0  # Track total valid keystrokes
        max_rows, max_columns = stdscr.getmaxyx()
        start_timer = time.time()
        stdscr.nodelay(True)
        start_row = 1
        stdscr.clear()

        while True:
            try:
                stdscr.addstr(1, 0, self.paragraph)
                self.wpm_calculator(start_timer, current_mistakes, total_keystrokes, stdscr)
                
                stdscr.addstr(4, 95, f"Mistakes: {current_mistakes}/5", 
                            curses.color_pair(2) if current_mistakes > 0 else curses.color_pair(1))

                for character_position, entered_character in enumerate(self.entered_text):
                    correct_character = self.paragraph[character_position]
                    display_color = curses.color_pair(1)
                    
                    if correct_character != entered_character:
                        display_color = curses.color_pair(2)    
                        
                    current_row = start_row + (character_position // max_columns)
                    current_column = character_position % max_columns
                    
                    if current_row < max_rows:
                        stdscr.addstr(current_row, current_column, entered_character, display_color)
                
                stdscr.refresh()

                try:
                    entered_key = stdscr.getkey()
                except:
                    continue

                try:
                    if entered_key in ["KEY_BACKSPACE", '\b', "\x7f"]:
                        if len(self.entered_text) > 0:
                            if self.paragraph[len(self.entered_text) - 1] != self.entered_text[-1]:
                                current_mistakes = max(0, current_mistakes - 1)
                            self.entered_text.pop()

                    elif entered_key == "\n":
                        pass

                    elif ord(entered_key) == 27:
                        break
                    else:
                        if current_mistakes < 5:
                            if len(self.entered_text) < len(self.paragraph):
                                self.entered_text.append(entered_key)
                                total_keystrokes += 1  # Increment keystrokes for valid characters
                                # Check if the newly typed character is a mistake
                                if entered_key != self.paragraph[len(self.entered_text) - 1]:
                                    current_mistakes += 1
                                    total_mistakes += 1

                except TypeError:
                    pass

                if len(self.entered_text) == len(self.paragraph):
                    stdscr.nodelay(False)
                    # Calculate final WPM using total keystrokes
                    final_time = time.time() - start_timer
                    final_wpm = round((total_keystrokes / (final_time / 60)) / 5)
                    final_accuracy = self.calculate_accuracy(self.entered_text, self.paragraph)
                    
                    stdscr.addstr(6, 50, f"Final WPM: {final_wpm}", curses.color_pair(3))
                    stdscr.addstr(6, 70, f"Final Accuracy: {final_accuracy}%", curses.color_pair(3))
                    stdscr.addstr(6, 100, f"Total mistakes: {total_mistakes}", curses.color_pair(3))
                    stdscr.refresh()
                    stdscr.getkey()
                    break

            except curses.error:
                pass

    def main_func(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.welcome_message(stdscr)


typer = TypingQuest()
curses.wrapper(typer.main_func)