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

    
    def typing_tester(self,stdscr):
        stdscr.clear()
        test_string = "Hello this is the demo string for the typing test program."
        entered_text = []
        stdscr.addstr(test_string)

        while True:  
            stdscr.clear()
            stdscr.addstr(test_string)


            for entered_character in entered_text:
                stdscr.addstr(entered_character,curses.color_pair(1))


            stdscr.refresh()

            entered_key = stdscr.getkey()

            if(entered_key in ["KEY_BACKSPACE",'\b',"\x7f"]):
                    if(len(entered_text) > 0):
                            entered_text.pop()
            
            elif(ord(entered_key) == 27):
                break

            else:
                entered_text.append(entered_key)

                

    
    def main_func(self,stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.welcome_message(stdscr)
        


typer = TypingQuest()

curses.wrapper(typer.main_func)
        