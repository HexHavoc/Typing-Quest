import curses

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

    
    def typing_tester(self,stdscr):
        self.paragraph = self.paragraph_loader()
        stdscr.clear()
        entered_text = []
        max_rows, max_columns = stdscr.getmaxyx()
        start_row = 1
        while True:  
            stdscr.clear()
            stdscr.addstr(1,0,self.paragraph)

            for character_position, entered_character in enumerate(entered_text):
                current_row = start_row + (character_position // max_columns)
                current_column = character_position % max_columns 
                if current_row < max_rows:
                    stdscr.addstr(current_row, current_column, entered_character, curses.color_pair(1))


            stdscr.refresh()

            entered_key = stdscr.getkey()

            if(entered_key in ["KEY_BACKSPACE",'\b',"\x7f"]):
                    if(len(entered_text) > 0):
                            entered_text.pop()
            
            elif(ord(entered_key) == 27):
                break


            else:
                if (len(entered_text) < (max_rows - start_row) * max_columns and len(entered_text) < len(self.paragraph)):
                    entered_text.append(entered_key)

                

    
    def main_func(self,stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.welcome_message(stdscr)
        


typer = TypingQuest()

curses.wrapper(typer.main_func)
        