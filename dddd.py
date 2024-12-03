def print_leaderboard():
    with open("leaderboard.txt") as file:
        player_list = []

        for line in file:
            data = line.rstrip()
            name, shots = data.split(';')
            player_list.append((int(shots), name))

        player_list = sorted(player_list)
        print('BEST PLAYERS:')
        for player in player_list:
            print(player[1], '-', player[0])
        file.close()
