import curses

class TypingQuest:

    def __init__(self):
        pass

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
        stdscr.refresh()
        stdscr.getkey()


    
    def main_func(self,stdscr):
        self.welcome_message(stdscr)


typer = TypingQuest()

curses.wrapper(typer.main_func)
        