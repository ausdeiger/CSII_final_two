from PyQt6.QtWidgets import *
from votingProject_gui import *
import csv


class Booth(QMainWindow, Ui_vote_booth):
    CAND_1_NAME = 'John'
    CAND_2_NAME = 'Jane'
    CAND_1_INFO = f'{CAND_1_NAME}\'s favorite color is blue.\nHe loves the outdoors.'
    CAND_2_INFO = f'{CAND_2_NAME}\'s favorite color is yellow.\nShe has 2 dogs.'

    def __init__(self) -> None:
        """
        Sets up project
        """
        super().__init__()
        self.setupUi(self)
        self.__id = ''
        self.__signed_in_status = False
        self.__cand_selection = ''

        with open('vote_counts.txt', 'w') as file:
            row = 'This file stores voter ID\'s'
            csv.writer(file).writerow([row])

        self.label_error_message.setText('Please enter 7 digit code')
        self.progressBar_cand_1.setValue(45)
        self.progressBar_cand_2.setValue(73)
        self.label_cand_1_bar_num.setText('45')
        self.label_cand_2_bar_num.setText('73')
        self.label_cand_info_text.setText('Select a candidate to\nsee information')
        self.label_cand_1.setText(self.CAND_1_NAME)
        self.label_cand_2.setText(self.CAND_2_NAME)
        self.label_cand_1_tally.setText(self.CAND_1_NAME)
        self.label_cand_2_tally.setText(self.CAND_2_NAME)

        self.button_cand_1.setEnabled(False)
        self.button_cand_2.setEnabled(False)
        self.button_vote_submit.setEnabled(False)
        self.button_vote_again.setEnabled(False)

        self.button_validate_id.clicked.connect(self.validate_clicked)
        self.button_cand_1.clicked.connect(self.cand_one_clicked)
        self.button_cand_2.clicked.connect(self.cand_two_clicked)
        self.button_vote_submit.clicked.connect(self.submit_vote)
        self.button_vote_again.clicked.connect(self.reset)


    def reset(self) -> None:
        """
        Allows for multiple votes in a row
        """
        self.__id = ''
        self.__signed_in_status = False
        self.__cand_selection = ''
        self.label_error_message.setText('Please enter 7 digit code')
        self.label_cand_info_text.setText('Select a candidate to see information')
        self.label_cand_info.setText('Candidate Info')
        self.label_cand_1.setText(self.CAND_1_NAME)
        self.label_cand_2.setText(self.CAND_2_NAME)
        self.label_cand_1_tally.setText(self.CAND_1_NAME)
        self.label_cand_2_tally.setText(self.CAND_2_NAME)

        self.button_cand_1.setEnabled(True)
        self.button_cand_2.setEnabled(True)
        self.button_cand_1.setAutoExclusive(False)
        self.button_cand_2.setAutoExclusive(False)
        self.button_cand_1.setChecked(False)
        self.button_cand_2.setChecked(False)
        self.button_cand_1.setAutoExclusive(True)
        self.button_cand_2.setAutoExclusive(True)
        self.button_cand_1.setEnabled(False)
        self.button_cand_2.setEnabled(False)

        self.button_vote_submit.setEnabled(False)
        self.button_vote_again.setEnabled(False)
        self.button_validate_id.setEnabled(True)
        self.input_id.setText('')
        self.input_id.setEnabled(True)


    def validate_clicked(self) -> None:
        """
        Collects user ID
        """
        with open('vote_counts.txt', 'r') as vote_file:
            self.__id = self.input_id.text().strip()
            if not self.__id.isdigit() and len(str(self.__id)) > 0:
                self.label_error_message.setText('Numbers only')
            elif len(str(self.__id)) != 7 and len(str(self.__id)) > 0:
                self.label_error_message.setText('Double check: 7 digits')
            elif not self.__id:
                self.label_error_message.setText('Please enter an ID')
            elif any(line.startswith(self.__id) for line in vote_file):
                self.label_error_message.setText('This ID already voted!')
            else:
                self.label_error_message.setText('Success! Voting opened!')
                self.button_cand_1.setEnabled(True)
                self.button_cand_2.setEnabled(True)
                self.button_vote_submit.setEnabled(True)
                self.__signed_in_status = True
                self.button_validate_id.setEnabled(False)
                self.input_id.setEnabled(False)

    def cand_one_clicked(self) -> None:
        """
        Manages candidate 1 interaction
        """
        if self.__signed_in_status:
            self.label_cand_info_text.setText(self.CAND_1_INFO)
            self.__cand_selection = self.CAND_1_NAME

    def cand_two_clicked(self) -> None:
        """
        Manages candidate 2 interaction
        """
        if self.__signed_in_status:
            self.label_cand_info_text.setText(self.CAND_2_INFO)
            self.__cand_selection = self.CAND_2_NAME

    def submit_vote(self) -> None:
        """
        Submits vote
        """
        if self.__signed_in_status and self.__cand_selection:
            with open('vote_counts.txt', 'a', newline='') as vote_file:
                row = [self.__id, self.__cand_selection]
                csv.writer(vote_file).writerow(row)

            if self.__cand_selection == self.CAND_1_NAME:
                new_val = self.progressBar_cand_1.value() + 1
                self.progressBar_cand_1.setValue(new_val)
                self.label_cand_1_bar_num.setText(str(new_val))
            if self.__cand_selection == self.CAND_2_NAME:
                new_val = self.progressBar_cand_2.value() + 1
                self.progressBar_cand_2.setValue(new_val)
                self.label_cand_2_bar_num.setText(str(new_val))

            self.button_cand_1.setEnabled(False)
            self.button_cand_2.setEnabled(False)
            self.button_vote_submit.setEnabled(False)
            self.button_vote_again.setEnabled(True)
            self.label_cand_info.setText('Success!')
            self.label_cand_info_text.setText('Your vote has been counted!')