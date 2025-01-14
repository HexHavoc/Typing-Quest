import curses
import time

class TypingQuest:

    def welcome_message(self,stdscr):
        stdscr.clear()
        stdscr.addstr("Welcome to the Ultimate Typing Test! 🎉.\n")
        stdscr.addstr("\nSharpen your skills, improve your speed, and challenge yourself to type like a pro\n")
        stdscr.addstr("\n💻 How it works:\n")
        stdscr.addstr("\n1. You'll be presented with a passage to type.\n")
        stdscr.addstr("\n2. Type as accurately and as quickly as you can!.\n")
        stdscr.addstr("\n3. Your speed and accuracy will be calculated at the end.\n")
        stdscr.addstr("\nReady to take on the challenge? Let’s get typing! 🖋️✨\n")
        stdscr.refresh()
        stdscr.getkey()
        self.typing_tester(stdscr)


    
    def paragraph_loader(self):
         with open("story.txt","r") as f:
              paragraph = f.read()
         
         return paragraph
    

    def wpm_calculator(self,start_timer,stdscr):
         time_passed = max(time.time() - start_timer,1)
         wpm = round((len(self.entered_text) / (time_passed / 60)) / 5)
         stdscr.addstr(3,10,f"\nWPM {str(wpm)}",curses.color_pair(3))

    
    def typing_tester(self,stdscr):
        self.paragraph = self.paragraph_loader()
        stdscr.clear()
        self.entered_text = []
        max_rows, max_columns = stdscr.getmaxyx()
        start_timer = time.time()
        stdscr.nodelay(True)
        start_row = 1
        while True: 
            stdscr.clear()
            stdscr.addstr(1,0,self.paragraph)
            self.wpm_calculator(start_timer,stdscr)

            if(len(self.entered_text) == len(self.paragraph)):
                 stdscr.nodelay(False)
                 break

            for character_position, entered_character in enumerate(self.entered_text):

                correct_character = self.paragraph[character_position]
                display_color = curses.color_pair(1)
                if(correct_character != entered_character):
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

            if(entered_key in ["KEY_BACKSPACE",'\b',"\x7f"]):
                    if(len(self.entered_text) > 0):
                            self.entered_text.pop()
            
            elif(ord(entered_key) == 27):
                break


            else:
                if (len(self.entered_text) < (max_rows - start_row) * max_columns):
                    self.entered_text.append(entered_key)


                

    
    def main_func(self,stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        self.welcome_message(stdscr)
        


typer = TypingQuest()

curses.wrapper(typer.main_func)
        