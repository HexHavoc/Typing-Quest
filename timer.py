import time
import curses
from curses.textpad import rectangle

def timer_mode(self, stdscr):
    self.paragraph = self.paragraph_loader()
    self.entered_text = []
    self.result_rows = []
    self.total_mistakes = 0
    current_mistakes = 0
    total_keystrokes = 0 
    max_rows, max_columns = stdscr.getmaxyx()
    start_row = 1
    stdscr.nodelay(True)
    stdscr.clear()
    
    # Display instructions and paragraph before starting the timer
    stdscr.addstr(1, 0, self.paragraph, curses.color_pair(6))
    
    if hasattr(self, 'username') and self.username:
        stdscr.addstr(6, 0, f"User: {self.username}", curses.color_pair(4) | curses.A_BOLD)
    
    # Clear the instruction
    stdscr.addstr(6, 70, " " * 35)
    
    for i in range(5, 0, -1):
        stdscr.addstr(6, 75, f"Starting in {i} seconds...", curses.color_pair(5) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(1)
    
    # Clear the countdown message
    stdscr.addstr(6, 70, " " * 35)
    stdscr.addstr(6, 85, "GO!", curses.color_pair(5) | curses.A_BOLD)
    stdscr.refresh()

    start_timer = time.time()
    duration = 60
    start_time = time.time()
    
    # Sleep briefly to allow the user to see "GO!" message
    time.sleep(0.5)
    
    # Clear the GO! message
    stdscr.addstr(6, 85, "    ")
    stdscr.refresh()

    while True:
        try:
            elapsed = time.time() - start_time
            remaining = max(0, duration - elapsed)
            
            # Format time as MM:SS
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            time_str = f"Time remaining: {minutes:02d}:{seconds:02d}"
            # Set color based on remaining time
            color_pair = 2 if remaining <= 10 else 1
            stdscr.attron(curses.color_pair(color_pair))

            # Display time
            stdscr.addstr(6, 150, time_str, curses.A_BOLD|curses.color_pair(5))
            
            # Refresh screen
            stdscr.refresh()
            
            # Check if timer has completed
            if remaining <= 0:
                stdscr.nodelay(False)
                stdscr.attrset(0)
                final_time = time.time() - start_timer
                self.final_wpm = round((total_keystrokes / (final_time / 60)) / 5)
                self.final_accuracy = self.calculate_accuracy(self.entered_text, self.paragraph)

                stdscr.clear()

                stdscr.addstr(10, 70, f"THE FINAL RESULTS FOR {self.username}", curses.color_pair(4)|curses.A_UNDERLINE|curses.A_BOLD)
                
                stdscr.addstr(15, 50, f"Final WPM: {self.final_wpm}", curses.color_pair(1)|curses.A_BOLD)
                stdscr.addstr(15, 70, f"Final Accuracy: {self.final_accuracy}%", curses.color_pair(1)|curses.A_BOLD)
                stdscr.addstr(15, 100, f"Total mistakes: {self.total_mistakes}", curses.color_pair(1)|curses.A_BOLD)
                rectangle(stdscr, 8, 45, 17, 120)

                stdscr.addstr(23, 5, "PRESS ESC TO QUIT", curses.color_pair(5)|curses.A_BOLD)
                rectangle(stdscr, 20, 1, 25, 25)

                stdscr.addstr(23, 70, "PRESS ENTER TO TRY AGAIN", curses.color_pair(5)|curses.A_BOLD)
                rectangle(stdscr, 20, 65, 25, 97)

                stdscr.addstr(23, 135, "PRESS l TO CHECK THE LEADERBOARD", curses.color_pair(5)|curses.A_BOLD)
                rectangle(stdscr, 20, 130, 25, 170)

                stdscr.refresh()
                prompt_key = stdscr.getkey()

                if(prompt_key == "\n"):
                    self.csv_writer_func()
                    stdscr.clear()
                    self.welcome_message(stdscr)

                elif(prompt_key == "l"):
                    stdscr.clear()
                    self.csv_writer_func()
                    exit_number = self.display_leaderboard(stdscr)

                    if(exit_number == 27):
                        stdscr.clear()
                        break

                    else:
                        stdscr.clear()  
                        self.welcome_message(stdscr)
                        break

                self.csv_writer_func()
                break
            
            stdscr.addstr(1, 0, self.paragraph, curses.color_pair(6))
            self.wpm_calculator(start_timer, current_mistakes, total_keystrokes, stdscr)

            stdscr.addstr(4, 95, " " * 20)
            
            stdscr.addstr(4, 95, f"Mistakes: {current_mistakes}/10", 
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
                    if current_mistakes < 10:
                        if len(self.entered_text) < len(self.paragraph):
                            self.entered_text.append(entered_key)
                            total_keystrokes += 1
                            if entered_key != self.paragraph[len(self.entered_text) - 1]:
                                current_mistakes += 1
                                self.total_mistakes += 1

            except TypeError:
                pass    

            if len(self.entered_text) == len(self.paragraph):
                stdscr.nodelay(False)
                stdscr.attrset(0)
                final_time = time.time() - start_timer
                self.final_wpm = round((total_keystrokes / (final_time / 60)) / 5)
                self.final_accuracy = self.calculate_accuracy(self.entered_text, self.paragraph)

                stdscr.clear()

                stdscr.addstr(10, 70, f"THE FINAL RESULTS FOR {self.username}", curses.color_pair(4)|curses.A_UNDERLINE|curses.A_BOLD)
                
                stdscr.addstr(15, 50, f"Final WPM: {self.final_wpm}", curses.color_pair(1)|curses.A_BOLD)
                stdscr.addstr(15, 70, f"Final Accuracy: {self.final_accuracy}%", curses.color_pair(1)|curses.A_BOLD)
                stdscr.addstr(15, 100, f"Total mistakes: {self.total_mistakes}", curses.color_pair(1)|curses.A_BOLD)
                rectangle(stdscr, 8, 45, 17, 120)

                stdscr.addstr(23, 5, "PRESS ESC TO QUIT", curses.color_pair(5)|curses.A_BOLD)
                rectangle(stdscr, 20, 1, 25, 25)

                stdscr.addstr(23, 70, "PRESS ENTER TO TRY AGAIN", curses.color_pair(5)|curses.A_BOLD)
                rectangle(stdscr, 20, 65, 25, 97)

                stdscr.addstr(23, 135, "PRESS l TO CHECK THE LEADERBOARD", curses.color_pair(5)|curses.A_BOLD)
                rectangle(stdscr, 20, 130, 25, 170)

                stdscr.refresh()
                prompt_key = stdscr.getkey()

                if(prompt_key == "\n"):
                    self.csv_writer_func()
                    stdscr.clear()
                    self.welcome_message(stdscr)

                elif(prompt_key == "l"):
                    stdscr.clear()
                    self.csv_writer_func()
                    exit_number = self.display_leaderboard(stdscr)

                    if(exit_number == 27):
                        stdscr.clear()
                        break

                    else:
                        stdscr.clear()  
                        self.welcome_message(stdscr)
                        break

                self.csv_writer_func()
                break
        except curses.error:
            pass