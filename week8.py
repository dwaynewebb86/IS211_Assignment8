import random
import argparse
import time
random.seed(0)


class Die:
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class HumanPlayer:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_score = 0

    def hold(self):
        self.score += self.turn_score
        self.turn_score = 0

    def reset_turn(self):
        self.turn_score = 0

    def take_turn(self, die):
        while True:
            roll = die.roll()
            print(f"\n{self.name} rolled: {roll}")
        
        if roll == 1:
            print("Rolling a 1 gives you no points.")
            self.reset_turn()
            return False
        
        self.turn_score += roll
        print(f"Turn total: {self.turn_score}")
        print(f"Total score: {self.score}")
        
        
        while True:
            decision = input("Roll (r) or Hold (h)? ").strip().lower()
            if decision == 'h':
                self.hold()
                print(f"{self.name} hold Score: {self.score}")
                return True
            elif decision == 'r':
                break   
            else:
                print("Invalid — enter 'r' or 'h'")


class ComputerPlayer(HumanPlayer):
    def __init__(self, name="Computer"):
        super().__init__(name)

    def take_turn(self, die):
        hold_at = min(25, 100 - self.score)
        while self.turn_score < hold_at:
            roll = die.roll()
            print(f"\n{self.name} rolled: {roll}")
            if roll == 1:
                print(f"{self.name} rolled a 1! No points.")
                self.reset_turn()
                return False
            self.turn_score += roll
            print(f"{self.name} turn total: {self.turn_score}")
        print(f"{self.name} holds at {self.turn_score}")
        self.hold()
        return True


class PlayerFactory:
    def create(self, player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)


class Game:
    def __init__(self, players):
        self.die = Die()
        self.players = players
        self.current_player_index = 0

    def current_player(self):
        return self.players[self.current_player_index]

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def game_over(self):
        return any(player.score >= 100 for player in self.players)

    def play_turn(self):
        player = self.current_player()
        player.reset_turn()
        player.take_turn(self.die)
        self.switch_player()

    def game_start(self):
        print("Welcome to Pig!")
        print("First to 100 points wins.")
        while not self.game_over():
            self.play_turn()
        winner = max(self.players, key=lambda p: p.score)
        print(f"\nGame over! {winner.name} wins with {winner.score} points!")


class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.monotonic()

    def time_up(self):
        return time.monotonic() - self.start_time >= 60

    def game_over(self):
        return self.game.game_over() or self.time_up()

    def play_turn(self):
        self.game.play_turn()

    def game_start(self):
        print("Welcome to Pig! (Timed - 60 seconds)")
        print("First to 100 points wins or most points after 60 seconds!")
        while not self.game_over():
            self.play_turn()
            if self.time_up():
                print("\nTime is up!")
                break
        winner = max(self.game.players, key=lambda p: p.score)
        print(f"\nGame over! {winner.name} wins with {winner.score} points!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', choices=['human', 'computer'], default='human')
    parser.add_argument('--player2', choices=['human', 'computer'], default='human')
    parser.add_argument('--timed', action='store_true')
    args = parser.parse_args()

    factory = PlayerFactory()
    players = [
        factory.create(args.player1, "Player 1"),
        factory.create(args.player2, "Player 2")
    ]

    game = Game(players)

    if args.timed:
        game = TimedGameProxy(game)

    game.game_start()