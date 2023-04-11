class PollModel:
    def __init__(self):
        self.questions = []
        self.polls = []

    def add_question(self, question):
        self.questions.append(question)

    def add_poll(self, poll):
        self.polls.append(poll)

    def remove_question(self, index):
        self.questions.pop(index)

    def remove_poll(self, index):
        self.polls.pop(index)
