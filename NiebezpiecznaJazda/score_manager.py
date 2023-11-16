import pandas as pd
import pathlib


class ScoreManager:
    def __init__(self):
        self.filename = pathlib.Path('scores.csv')
        self.columns = ['Nickname', 'Score']
        self.scores = pd.DataFrame(columns=self.columns)

    def save_score(self, nickname, score):
        new_score = pd.DataFrame([[nickname, score]], columns=self.columns)
        self.scores = pd.concat([self.scores, new_score], ignore_index=True)
        self.scores = self.scores.sort_values(by='Score', ascending=False)
        self.scores.to_csv(self.filename, index=False)

    def load_scores(self):
        if self.filename.is_file():
            self.scores = pd.read_csv(self.filename)
        else:
            self.scores = pd.DataFrame(columns=self.columns)
