class Player:
    def __init__(self, health=100, happiness=50, money=100):
        self._health = health
        self._happiness = happiness
        self._money = money

    def get_health(self):
        return self._health

    def set_health(self, value):
        self._health = max(0, min(100, value)) # Health clamped between 0 and 100

    def get_happiness(self):
        return self._happiness

    def set_happiness(self, value):
        self._happiness = max(0, min(100, value)) # Happiness clamped between 0 and 100

    def get_money(self):
        return self._money

    def set_money(self, value):
        self._money = max(0, value) # Money cannot go below 0

    def display_stats(self):
        print(f"Health: {self._health}/100 | Happiness: {self._happiness}/100 | Money: ${self._money}")
