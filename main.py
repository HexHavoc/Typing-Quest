import curses
import csv
from curses.textpad import Textbox, rectangle
import time
import random
import os
from timer import timer_mode


class TypingQuest:
    def welcome_message(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Welcome to the Ultimate Typing Test! 🎉\n",curses.color_pair(6))
        stdscr.addstr("\nSharpen your skills, improve your speed, and challenge yourself to type like a pro\n",curses.color_pair(6))
        stdscr.addstr("\n💻 How it works:\n",curses.color_pair(6))
        stdscr.addstr("\n1. You need to type your username when prompted, So we can store your results and display it on our leaderboard.\n",curses.color_pair(6))
        stdscr.addstr("\n2. You'll be presented with a passage to type.\n",curses.color_pair(6))
        stdscr.addstr("\n3. Type as accurately and as quickly as you can!\n",curses.color_pair(6))
        stdscr.addstr("\n4. Your speed and accuracy will be calculated at the end.\n",curses.color_pair(6))
        stdscr.addstr("\n5. After 5 mistakes, you must fix them before continuing.\n",curses.color_pair(6))
        stdscr.addstr("\nReady to take on the challenge? Let's get typing! 🖋️✨\n",curses.color_pair(6))
        stdscr.refresh()
        stdscr.getkey()
        
        # Get username with proper input field
        username = self.get_username(stdscr)
        self.username = username
        while(self.username == ''):
            if(self.username != ''):
                break

            stdscr.addstr(17, 15, "Can't leave the username empty(Press enter to type)",curses.color_pair(1))
            stdscr.refresh()
            stdscr.getkey()
            self.username = self.get_username(stdscr)

        self.select_typing_mode(stdscr)


    def select_typing_mode(self,stdscr):
        stdscr.clear()
        stdscr.addstr(10, 61, f"PRESS t FOR TIMER MODE AND n FOR NORMAL MODE", curses.color_pair(4)|curses.A_UNDERLINE|curses.A_BOLD)

        stdscr.addstr(23, 50, "TIMER MODE", curses.color_pair(5)|curses.A_BOLD)
        rectangle(stdscr, 20, 45, 25, 65)

        stdscr.addstr(23, 100, "NORMAL MODE", curses.color_pair(5)|curses.A_BOLD)
        rectangle(stdscr, 20, 95, 25, 115)

        stdscr.refresh()
        mode_key = stdscr.getkey()

        if(mode_key == "n"):
            self.typing_tester(stdscr)

        else:
            timer_mode(self,stdscr)

        


    def get_username(self, stdscr):
        stdscr.clear()

        input_y, input_x = 12, 15
        box_height, box_width = 1, 50
        
        rectangle(stdscr, input_y-1, input_x-1, input_y+1, input_x+box_width)
        

        stdscr.addstr(input_y-2, input_x, "Enter your username:",curses.color_pair(4))
        stdscr.refresh()
        
        win = curses.newwin(box_height, box_width-2, input_y, input_x)
        box = Textbox(win,curses.color_pair(6))
     
        stdscr.addstr(input_y+3, input_x, "Press Enter to confirm",curses.color_pair(1))
        stdscr.refresh()
        
        curses.curs_set(1)
        
        box.edit()
        
        curses.curs_set(0)

        username = box.gather().strip()

        return username

    def paragraph_loader(self):
        random_paragraph_number = random.randint(1,50)  

        with open(f"paragraphs/paragraph_{random_paragraph_number}.txt", "r") as f:
            paragraph = f.read()

        return paragraph
    

    def timer_mode_paragraph(self):
        pass

    def calculate_accuracy(self, typed_text, target_text):
        """Calculate accuracy based on correct characters vs total characters typed,
        with a much slower increase rate."""
        if not typed_text:
            return 100.0
        
        if isinstance(typed_text, list):
            typed_text = ''.join(typed_text)
        
        total_chars = len(typed_text)
        correct_chars = sum(a == b for a, b in zip(typed_text, target_text[:len(typed_text)]))
        

        raw_accuracy = (correct_chars / total_chars) * 100
        
        if raw_accuracy > 80:
     
            adjusted_accuracy = 60 + (100 - 60) * ((raw_accuracy - 80) / 20) ** 2.5
        elif raw_accuracy > 60:
       
            adjusted_accuracy = 40 + (60 - 40) * ((raw_accuracy - 60) / 20) ** 1.8
        else:
      
            adjusted_accuracy = raw_accuracy * 0.9
        
    
        return min(round(adjusted_accuracy, 2), 100.0)

    def wpm_calculator(self, start_timer, current_mistakes, total_keystrokes, stdscr):
        time_passed = max(time.time() - start_timer, 1)
        wpm = round((total_keystrokes / (time_passed / 60)) / 5)
        
        accuracy = self.calculate_accuracy(self.entered_text, self.paragraph)

        stdscr.addstr(4, 50, " " * 20)
        stdscr.addstr(4, 70, " " * 20)
        
        if current_mistakes >= 10:
            stdscr.addstr(4, 50, "Fix mistakes!", curses.color_pair(2))
            

        else:
            stdscr.addstr(4, 50, f"WPM: {wpm}", curses.color_pair(3))
            stdscr.addstr(4, 70, f"Accuracy: {accuracy}%", curses.color_pair(3))

    def typing_tester(self, stdscr):
        self.paragraph = self.paragraph_loader()
        self.entered_text = []
        self.result_rows = []
        self.total_mistakes = 0
        current_mistakes = 0
        total_keystrokes = 0 
        max_rows, max_columns = stdscr.getmaxyx()
        start_timer = time.time()
        stdscr.nodelay(True)
        start_row = 1
        stdscr.clear()

        if hasattr(self, 'username') and self.username:
            stdscr.addstr(6 , 0 , f"User: {self.username}", curses.color_pair(4)| curses.A_BOLD)

        while True:
            try:
                stdscr.addstr(1, 0, self.paragraph)
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

    def csv_writer_func(self):
        # Create results.csv if it doesn't exist with header row
        if not os.path.exists("results.csv"):
            with open("results.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='\t')
                csv_writer.writerow(["username", "wpm", "accuracy", "mistakes"])
        
        # Read existing data
        existing_data = []
        user_exists = False
        user_index = -1
        
        try:
            with open("results.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\t')
                header = next(csv_reader, None)  # Skip header row
                
                for i, row in enumerate(csv_reader):
                    if len(row) >= 4:
                        existing_data.append(row)
                        if row[0] == self.username:
                            user_exists = True
                            user_index = i
        except:
            # If there's an issue reading the file, we'll treat it as empty
            pass
        
        # Check if user exists and compare scores
        updated = False
        if user_exists:
            # Get existing scores
            existing_wpm = float(existing_data[user_index][1])
            existing_accuracy = float(existing_data[user_index][2])
            existing_mistakes = int(existing_data[user_index][3])
            
            # Compare with new scores
            improved = False
            
            # Update WPM if improved
            if self.final_wpm > existing_wpm:
                existing_data[user_index][1] = str(self.final_wpm)
                improved = True
                
            # Update accuracy if improved
            if self.final_accuracy > existing_accuracy:
                existing_data[user_index][2] = str(self.final_accuracy)
                improved = True
                
            # Update mistakes if fewer (lower is better)
            if self.total_mistakes < existing_mistakes:
                existing_data[user_index][3] = str(self.total_mistakes)
                improved = True
                
            updated = improved
        else:
            # Add new user
            existing_data.append([self.username, str(self.final_wpm), str(self.final_accuracy), str(self.total_mistakes)])
            updated = True
        
        # Write updated data back to file if any changes were made
        if updated:
            with open("results.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='\t')
                csv_writer.writerow(["username", "wpm", "accuracy", "mistakes"])  # Write header
                csv_writer.writerows(existing_data)

    def display_leaderboard(self, stdscr):
        stdscr.clear()
        
      
        leaderboard_data = []
        try:
            with open("results.csv", "r") as csv_file:
                header = next(csv.reader(csv_file, delimiter='\t'))
                csv_file.seek(0)
                
               
                csv_reader = csv.reader(csv_file, delimiter='\t')
                next(csv_reader)  
                
                for row in csv_reader:
                    if len(row) >= 4:  
                        username = row[0]
                        wpm = float(row[1])
                        accuracy = float(row[2])
                        mistakes = int(row[3])
                        leaderboard_data.append({
                            'username': username,
                            'wpm': wpm,
                            'accuracy': accuracy,
                            'mistakes': mistakes
                        })
        except Exception as e:
        
            stdscr.addstr(10, 50, f"Error loading leaderboard: {str(e)}")
            stdscr.refresh()
            stdscr.getkey()
            return
        
        # Sort the leaderboard by WPM (highest first)
        leaderboard_data.sort(key=lambda x: x['wpm'], reverse=True)
        
        # Limit to top 10 entries
        leaderboard_data = leaderboard_data[:10]
        
        stdscr.addstr(5, 73, "🏆 TOP 10 TYPING CHAMPIONS 🏆", curses.color_pair(5) | curses.A_BOLD | curses.A_UNDERLINE)
        
     
        header_y = 10
        stdscr.addstr(header_y, 40, "RANK", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(header_y, 55, "USERNAME", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(header_y, 85, "WPM", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(header_y, 105, "ACCURACY", curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(header_y, 125, "MISTAKES", curses.color_pair(4) | curses.A_BOLD)
        

        for i in range(35, 145):
            stdscr.addstr(header_y + 1, i, "━", curses.color_pair(3))
        

        for idx, entry in enumerate(leaderboard_data):
            row_y = header_y + 3 + (idx * 2)
            
            rank_color = curses.color_pair(1)  
            if idx == 0:
                rank_color = curses.color_pair(5) | curses.A_BOLD  # Gold for 1st
            elif idx == 1:
                rank_color = curses.color_pair(3) | curses.A_BOLD  # Silver for 2nd
            elif idx == 2:
                rank_color = curses.color_pair(4) | curses.A_BOLD  # Bronze for 3rd
            
    
            rank_display = f"#{idx + 1}"
            stdscr.addstr(row_y, 40, rank_display, rank_color)
            

            username = entry['username']
            if len(username) > 20:
                username = username[:17] + "..."
            stdscr.addstr(row_y, 55, username, curses.color_pair(1))
            
            # WPM
            wpm_color = curses.color_pair(1)
            if entry['wpm'] >= 70:
                wpm_color = curses.color_pair(5) | curses.A_BOLD 
            elif entry['wpm'] >= 50:
                wpm_color = curses.color_pair(3) 
            stdscr.addstr(row_y, 85, f"{entry['wpm']:.0f}", wpm_color)
            
            # Accuracy
            acc_color = curses.color_pair(1)
            if entry['accuracy'] >= 98:
                acc_color = curses.color_pair(5) | curses.A_BOLD 
            elif entry['accuracy'] >= 95:
                acc_color = curses.color_pair(3) 
            elif entry['accuracy'] < 90:
                acc_color = curses.color_pair(2) 
            stdscr.addstr(row_y, 105, f"{entry['accuracy']:.2f}%", acc_color)
            
            # Mistakes
            mistake_color = curses.color_pair(1)
            if entry['mistakes'] <= 2:
                mistake_color = curses.color_pair(5) | curses.A_BOLD 
            elif entry['mistakes'] >= 5:
                mistake_color = curses.color_pair(2) 
            stdscr.addstr(row_y, 125, str(entry['mistakes']), mistake_color)
    

        rectangle(stdscr, header_y - 2, 35, row_y + 2, 145)

        stdscr.addstr(35, 10, "PRESS ENTER TO TRY AGAIN", curses.color_pair(5))

        stdscr.addstr(35, 150, "PRESS ESC TO EXIT", curses.color_pair(5))
        
        stdscr.refresh()
        leaderboard_key = stdscr.getkey()

        if(ord(leaderboard_key) == 27):
            return 27


    def main_func(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.welcome_message(stdscr)


typer = TypingQuest()
curses.wrapper(typer.main_func)