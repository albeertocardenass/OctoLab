import sys
import os


if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

from ui.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
