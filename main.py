import random


def divide_list_without_repetitions(all_pieces, n):
    result_list = []
    for i in range(n):
        result_list.append(random.choice(all_pieces))
        all_pieces.remove(result_list[i])
    return result_list


def get_the_first_piece(domino_snake, player_pieces, computer_pieces):
    player = sorted(player_pieces, key=lambda x: x[0], reverse=True)
    computer = sorted(computer_pieces, key=lambda x: x[0], reverse=True)
    if (player[0][0] + player[0][1] > computer[0][0] + computer[0][1]) or (player[0][0] + player[0][1] == computer[0][0] + computer[0][1] and player[0][0] == player[0][1]):
        domino_snake.append(player[0])
        player_pieces.remove(domino_snake[0])
        return "computer"
    elif (player[0][0] + player[0][1] < computer[0][0] + computer[0][1]) or (player[0][0] + player[0][1] == computer[0][0] + computer[0][1] and computer[0][0] == computer[0][1]):
        domino_snake.append(computer[0])
        computer_pieces.remove(domino_snake[0])
        return "player"


def is_stock_not_empty(all_pieces):
    if len(all_pieces) > 0:
        return True
    return False


def is_move_legal(move, domino_snake, pieces):
    if move == 0:
        return True
    if move > 0:
        if domino_snake[len(domino_snake) - 1][1] in pieces[abs(move) - 1]:
            return True
    if move < 0:
        if domino_snake[0][0] in pieces[abs(move) - 1]:
            return True
    return False


def orientate_piece(item):
    return item[1], item[0]


def place_a_piece(move, item, domino_snake, pieces):
    if move > 0:
        if domino_snake[len(domino_snake) - 1][1] == item[0]:
            domino_snake.append(item)
            pieces.remove(item)
        else:
            item[0], item[1] = orientate_piece(item)
            domino_snake.append(item)
            pieces.remove(item)
    elif move < 0:
        if domino_snake[0][0] == item[1]:
            domino_snake.insert(0, item)
            pieces.remove(item)
        else:
            item[0], item[1] = orientate_piece(item)
            domino_snake.insert(0, item)
            pieces.remove(item)


def make_player_move(all_pieces, domino_snake, player_pieces):
    move = 0
    while True:
        try:
            move = int(input())
            if abs(move) > len(player_pieces):
                raise ValueError
        except ValueError:
            print("Invalid input. Please try again.")
            continue
        if is_move_legal(move, domino_snake, player_pieces):
            item = player_pieces[abs(move) - 1]
            if move != 0:
                place_a_piece(move, item, domino_snake, player_pieces)
                break
            else:
                if is_stock_not_empty(all_pieces):
                    item = random.choice(all_pieces)
                    player_pieces.append(item)
                    all_pieces.remove(item)
                break
        else:
            print("Illegal move. Please try again.")
    return "computer"


# 'clever' way to choose a piece for a computer
def the_ai(pieces, snake):
    scores = [0, 0, 0, 0, 0, 0, 0]
    for item in snake:
        scores[item[0]] += 1
        scores[item[1]] += 1
    for item in pieces:
        scores[item[0]] += 1
        scores[item[1]] += 1
    result = [0] * len(pieces)
    i = 0
    for item in pieces:
        result[i] = scores[item[0]] + scores[item[1]]
        i += 1
    return result


def make_computer_move(all_pieces, domino_snake, computer_pieces):
    scores = the_ai(computer_pieces, domino_snake)
    while sum(scores) != 0:
        move = scores.index(max(scores))
        if is_move_legal(move + 1, domino_snake, computer_pieces):
            item = computer_pieces[move]
            place_a_piece(move + 1, item, domino_snake, computer_pieces)
            return "player"
        elif is_move_legal((move + 1) * -1, domino_snake, computer_pieces):
            item = computer_pieces[move]
            place_a_piece((move + 1) * -1, item, domino_snake, computer_pieces)
            return "player"
        else:
            scores[move] = 0
    if is_stock_not_empty(all_pieces):
        item = random.choice(all_pieces)
        computer_pieces.append(item)
        all_pieces.remove(item)
    return "player"


def check_conditions(all_pieces, domino_snake, player_pieces, computer_pieces):
    if len(player_pieces) == 0:
        return False, "Status: The game is over. You won!"
    elif len(computer_pieces) == 0:
        return False, "Status: The game is over. The computer won!"
    elif len(all_pieces) == 0:
        return False, "Status: The game is over. It's a draw!"
    else:
        for i in range(7):
            count = 0
            for item_ in domino_snake:
                if i in item_:
                    count += 1
            if count == 7:
                if i in domino_snake[0] and i in domino_snake[len(domino_snake) - 1]:
                    return False, "Status: The game is over. It's a draw!"
    return True, ""


def print_interface(all_pieces, domino_snake, player_pieces, computer_pieces):
    print('=' * 70)
    print('Stock size:', len(all_pieces))
    print('Computer pieces:', len(computer_pieces), end='\n\n')
    if len(domino_snake) > 6:
        print(
            f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}{domino_snake[-1]}",
            end='')
    else:
        for item in domino_snake:
            print(item, end='')
    print(end='\n\n')
    print('Your pieces:')
    for i in range(len(player_pieces)):
        print(str(i + 1) + ':' + str(player_pieces[i]))


def main():
    domino_snake = []
    all_pieces = [[i, j] for i in range(7) for j in range(i, 7)]
    player_pieces = divide_list_without_repetitions(all_pieces, 7)
    computer_pieces = divide_list_without_repetitions(all_pieces, 7)
    status = get_the_first_piece(domino_snake, player_pieces, computer_pieces)

    is_game_not_over = True
    while is_game_not_over:
        print_interface(all_pieces, domino_snake, player_pieces, computer_pieces)
        if status == "computer":
            print("\nStatus: Computer is about to make a move. Press Enter to continue...")
            input()
            status = make_computer_move(all_pieces, domino_snake, computer_pieces)
        else:
            print("\nStatus: It's your turn to make a move. Enter your command.")
            status = make_player_move(all_pieces, domino_snake, player_pieces)
        is_game_not_over, line = check_conditions(all_pieces, domino_snake, player_pieces, computer_pieces)

    print_interface(all_pieces, domino_snake, player_pieces, computer_pieces)
    print(line)


if __name__ == '__main__':
    main()
