from player import Player
import time

def main():
    player = Player()
    day = 1
    running = True

    print("Welcome to the Text Life Simulator!")
    print("Try to survive and thrive!")

    while running:
        print(f"\n--- Day {day} ---")
        player.display_stats()

        if player.get_health() <= 0:
            print("Your health dropped to 0. Game Over!")
            running = False
            break
        if player.get_happiness() <= 0:
            print("Your happiness dropped to 0. Game Over!")
            running = False
            break
        if player.get_money() <= 0 and day > 1: # Give a grace period on day 1
            print("You ran out of money. Game Over!")
            running = False
            break

        print("\nWhat would you like to do?")
        print("1. Work (Earn money, lose happiness/health)")
        print("2. Rest (Regain health, lose money/happiness)")
        print("3. Socialize (Gain happiness, lose money)")
        print("4. Check Stats")
        print("5. Quit Game")

        choice = input("Enter your choice: ")

        if choice == '1':
            player.set_money(player.get_money() + 50)
            player.set_happiness(player.get_happiness() - 15)
            player.set_health(player.get_health() - 10)
            print("You worked hard and earned some money!")
        elif choice == '2':
            player.set_health(player.get_health() + 20)
            player.set_money(player.get_money() - 10)
            player.set_happiness(player.get_happiness() - 5)
            print("You rested and feel a bit better.")
        elif choice == '3':
            player.set_happiness(player.get_happiness() + 25)
            player.set_money(player.get_money() - 20)
            player.set_health(player.get_health() - 5)
            print("You socialized and feel happier!")
        elif choice == '4':
            player.display_stats()
        elif choice == '5':
            print("Quitting game. Goodbye!")
            running = False
        else:
            print("Invalid choice. Please try again.")

        if running: # Only advance day if game is still running
            day += 1
            # Apply passive daily changes
            player.set_health(player.get_health() - 2)
            player.set_happiness(player.get_happiness() - 3)
            player.set_money(player.get_money() - 5)
            time.sleep(1) # Pause for a moment to read output

    print(f"\nGame Over. You survived {day - 1} days.")

if __name__ == "__main__":
    main()
