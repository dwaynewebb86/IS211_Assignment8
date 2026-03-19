import random
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

Class ComputerPlayer(HumanPlayer):
    def __init__(self, name="Computer"):
        super().__init__(name)

class Game:
    def __init__(self):
        self.die = Die()
        self.players = [Player("Player 1"), Player("Player 2")]
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

        while True:
            roll = self.die.roll()
            print(f"\n{player.name} rolled: {roll}")
            print(f"Turn total: {player.turn_score}")
            print(f"Total score: {player.score}")

            if roll == 1:
                print("Rolled a 1! No points this turn.")
                player.reset_turn()
                self.switch_player()
                break

            player.turn_score += roll

            decision = input("Roll (r) or Hold (h)? ").strip().lower()

            if decision == 'h':
                player.hold()
                print(f"{player.name} holds! Score: {player.score}")
                self.switch_player()
                break
            elif decision == 'r':
                continue
            else:
                print("Invalid — enter 'r' or 'h'")

    def game_start(self):
        print("Welcome to Pig!")
        print("First to 100 points wins.")
        while not self.game_over():
            self.play_turn()
        winner = max(self.players, key=lambda p: p.score)
        print(f"\nGame over! {winner.name} wins with {winner.score} points!")


if __name__ == "__main__":
    game = Game()
    game.game_start()