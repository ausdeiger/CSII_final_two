from PyQt6.QtWidgets import QApplication

from votingProject_logic import Booth


def main():
    application = QApplication([])
    window = Booth()
    window.show()
    application.exec()




if __name__ == '__main__':
    main()