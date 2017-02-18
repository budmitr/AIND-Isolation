def score_moves(game, player, opponent_scaling_factor=1):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_moves = float(len(game.get_legal_moves(player)))
    opponent_moves = float(len(game.get_legal_moves(game.get_opponent(player))))

    score = player_moves - opponent_scaling_factor * opponent_moves
    return score


def score_center(game, player, opponent_scaling_factor=1):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    def evaluate_location(location, width, height):
        dy = abs(height // 2 - location[0])
        dx = abs(width // 2 - location[1])
        return dx + dy

    gw, gh = game.width, game.height
    max_dist = evaluate_location((0, 0), gw, gh)  # ensure that more is better
    player_score = float(max_dist - evaluate_location(game.get_player_location(player), gw, gh))
    opponent_score = float(max_dist - evaluate_location(game.get_player_location(game.get_opponent(player)), gw, gh))

    score = player_score - opponent_scaling_factor * opponent_score
    return score


def score_freecells(game, player, opponent_scaling_factor=1):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    def evaluate_location(location, width, height, radius=2):
        top = max(0, location[0] - radius)
        bot = min(width, location[0] + radius)
        left = max(0, location[1] - radius)
        right = min(height, location[1] + radius)

        free_spaces = game.get_blank_spaces()
        free_spaces_radius = []
        for fs in free_spaces:
            if (top <= fs[0] <= bot) and (left <= fs[1] <= right):
                free_spaces_radius.append(fs)

        return len(free_spaces_radius)

    gw, gh = game.width, game.height
    player_score = float(evaluate_location(game.get_player_location(player), gw, gh))
    opponent_score = float(evaluate_location(game.get_player_location(game.get_opponent(player)), gw, gh))

    score = player_score - opponent_scaling_factor * opponent_score
    return score


def score_moves_center(game, player, opponent_scaling_factor=1):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    move_score = score_moves(game, player, opponent_scaling_factor)
    center_score = score_center(game, player, opponent_scaling_factor)
    score = move_score + center_score
    return score


def score_moves_freecells(game, player, opponent_scaling_factor=1):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    move_score = score_moves(game, player, opponent_scaling_factor)
    cell_score = score_freecells(game, player, opponent_scaling_factor)
    score = move_score + cell_score
    return score


def score_moves_center_freecells(game, player, opponent_scaling_factor=1):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    move_score = score_moves(game, player, opponent_scaling_factor)
    cell_score = score_freecells(game, player, opponent_scaling_factor)
    center_score = score_center(game, player, opponent_scaling_factor)
    score = move_score + cell_score + center_score
    return score


def scale(fn, factor):
    return lambda game, player: fn(game, player, factor)
