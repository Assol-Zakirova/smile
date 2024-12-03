import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_empty_board():
    return [['*' for _ in range(7)] for _ in range(7)]

def display_board(board):
    print("    0   1   2   3   4   5   6")
    for i, row in enumerate(board):
        print(f"{chr(65 + i)}  {'   '.join(row)}")

def place_ship(board, length):
    placed = False
    while not placed:
        direction = random.choice(['horizontal', 'vertical'])
        row = random.randint(0, 6)
        col = random.randint(0, 6)

        ship_coords = []
        for i in range(length):
            r = row + i if direction == 'vertical' else row
            c = col + i if direction == 'horizontal' else col
            if 0 <= r < 7 and 0 <= c < 7 and board[r][c] == '*':
                ship_coords.append((r, c))
            else:
                break

        if len(ship_coords) == length:
            # Ensure ships don't touch, even by corner
            if check_surrounding(board, ship_coords):
                for r, c in ship_coords:
                    board[r][c] = 'S'
                placed = True

    return ship_coords

def check_surrounding(board, ship_coords):
    """Check surrounding cells to ensure ships don't touch, even diagonally."""
    for r, c in ship_coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 7 and 0 <= nc < 7 and board[nr][nc] == 'S':
                    return False
    return True

def setup_ships():
    board = create_empty_board()
    ships = []
    ships.append(place_ship(board, 3))  # 1 ship of length 3
    for _ in range(2):
        ships.append(place_ship(board, 2))  # 2 ships of length 2
    for _ in range(4):
        ships.append(place_ship(board, 1))  # 4 ships of length 1
    return board, ships

def validate_input(user_input):
    if len(user_input) != 2:
        return None
    row, col = user_input[0].upper(), user_input[1]
    if row < 'A' or row > 'G' or not col.isdigit() or not (0 <= int(col) <= 6):
        return None
    return ord(row) - 65, int(col)

def is_sunk(board, ship):
    return all(board[r][c] == 'h' for r, c in ship)

def mark_sunk(board, ship):
    for r, c in ship:
        board[r][c] = 's'

def check_victory(ships, board):
    return all(all(board[r][c] == 's' for r, c in ship) for ship in ships)

def play_game():
    name = input("Enter your name: ")
    clear_screen()
    player_board = create_empty_board()
    computer_board, ships = setup_ships()
    shots = 0

    while not check_victory(ships, player_board):
        clear_screen()
        print(f"{name}'s Game Board:")
        display_board(player_board)

        user_input = input("Enter your shot (e.g., A3): ")
        coords = validate_input(user_input)
        if not coords:
            print("Invalid input. Try again.")
            continue

        row, col = coords
        if player_board[row][col] != '*':
            print("You already shot there. Try again.")
            continue

        shots += 1
        if computer_board[row][col] == 'S':
            player_board[row][col] = 'h'
            computer_board[row][col] = 'h'
            for ship in ships:
                if (row, col) in ship and is_sunk(computer_board, ship):
                    mark_sunk(player_board, ship)
                    mark_sunk(computer_board, ship)
                    print("Ship sunk!")
        else:
            player_board[row][col] = 'm'

        if check_victory(ships, player_board):
            clear_screen()
            print(f"Congratulations {name}! You won in {shots} shots!")
            break

    replay = input("Do you want to play again? (yes/no): ").strip().lower()
    if replay == 'yes':
        play_game()
    else:
        print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
