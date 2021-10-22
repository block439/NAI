"""
    Zmierz się ze sztuczną intelignecją w szachach :)
    Zasady gry w szachy: https://pl.wikipedia.org/wiki/Zasady_gry_w_szachy
    W celu dokonania ruchu użyj notacji algebraicznej wpisując do konsoli swój ruch.
    Na przykład: ruch pionkiem z pola a2 na pole a3 będzie wyglądać następująco a2a3.

    W celu możliwości uruchomienia gry należy pobrać i zainstalować bibliotekę easyAi i chess.
    W konsoli użyj komendy 'pip install -r /path/to/requirements.txt' pozwoli na automatyczną instalację potrzebnych bibliotek

    Autorzy: Mieszko Dziadowiec, Aleksander Reiter
"""
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import chess
import chess.engine
import time
engine = chess.engine.SimpleEngine.popen_uci('D:\\pobrane\\stockfish.exe')
class ChessGame(TwoPlayerGame):
    def __init__(self, players=None):
        self.board = chess.Board()
        self.players = players
        self.current_player = 1
        self.start_time = time.time()
    def possible_moves(self):
        return list(self.board.legal_moves)
    def make_move(self, move):
        self.board.push(move)
    def unmake_move(self, move):
        self.board.pop()
    def win(self):
        return self.board.is_variant_win()
    def is_over(self):
        return self.board.is_game_over()
    def show(self):
        print(f'Time of execution: {time.time() - self.start_time} seconds')
        print(self.board)
        outcome = self.board.outcome()
        if outcome is not None:
            print(f'Termination: {outcome.termination.name}, result: {outcome.result()}')
        self.start_time = time.time()
        info = engine.analyse(self.board, chess.engine.Limit(depth=10))
        print("Score:", info["score"])
        moves = list(self.board.legal_moves)
        print(f'Probably best move: {info["pv"][0]}')
        print(moves)
    def scoring(self):
        if self.board.is_checkmate():
            return -100000
        info = engine.analyse(self.board, chess.engine.Limit(depth=20))
        multiplier = 1
        kara = 0
        #if self.current_player == 1:
        #    multiplier = 0.3
        #    #kara = randrange(100, 8000)
        try:
            return info["score"].relative.cp * multiplier - kara
        except:
            return (20000 - 2000 * info["score"].relative.moves) * multiplier - kara
# Start a match (and store the history of moves when it ends)
ai = Negamax(1, win_score=100000)
ai2 = Negamax(1)
#game = ChessGame( [ AI_Player(ai), Human_Player() ] )
game = ChessGame( [ Human_Player(), AI_Player(ai) ] )
history = game.play()