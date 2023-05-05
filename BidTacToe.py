import pygame
from random import randint


# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (600, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Bid Tac Toe')

# Board size
board_size = 300  # Size of the board (in pixels)
board_pos = ((window.get_width() - board_size) // 2,
             (window.get_height() - board_size) // 2)
cell_size = board_size // 3  # Size of each cell (in pixels)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define bid stacks
BID_STACK = [100, 100]
bidding_now = True

# Set up bid arrows
bid_value = [0, 0]
arrow_rect_x = pygame.Rect(25, 100, 50, 50)
arrow_up_rect_x = pygame.Rect(arrow_rect_x.centerx - 10, arrow_rect_x.y + 5, 20, 20)
arrow_down_rect_x = pygame.Rect(arrow_rect_x.centerx - 10, arrow_rect_x.bottom - 25, 20, 20)
arrow_rect_x2 = pygame.Rect(80, 100, 50, 50)
arrow_up_rect_x2 = pygame.Rect(arrow_rect_x2.centerx - 10, arrow_rect_x2.y + 5, 20, 20)
arrow_down_rect_x2 = pygame.Rect(arrow_rect_x2.centerx - 10, arrow_rect_x2.bottom - 25, 20, 20)
arrow_rect_o = pygame.Rect(425, 100, 50, 50)
arrow_up_rect_o = pygame.Rect(arrow_rect_o.centerx - 10, arrow_rect_o.y + 5, 20, 20)
arrow_down_rect_o = pygame.Rect(arrow_rect_o.centerx - 10, arrow_rect_o.bottom - 25, 20, 20)
bid_rect = pygame.Rect(25, 160, 100, 50)
circle_player_x = pygame.Rect(25, 15, 150, 50)
circle_player_o = pygame.Rect(400, 15, 150, 50)
# TODO: Bid arrow for +-10

# Define the game board
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]


# Define game logic
def handle_move(row, col, player):
    global bidding_now
    if board[row][col] is None:
        board[row][col] = player
        bidding_now = True
        return True
    else:
        return False


def check_winner():
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # Check for tie
    if all(all(row) for row in board):
        return 'tie'


# Draw the game board
def draw_board():
    window.fill(WHITE)

    board_margin = 200  # Amount of margin around the board

    # Draw the board lines
    for i in range(1, 3):
        pygame.draw.line(window, BLACK, (board_pos[0] + i * cell_size, board_pos[1]),
                         (board_pos[0] + i * cell_size, board_pos[1] + board_size), 10)
        pygame.draw.line(window, BLACK, (board_pos[0], board_pos[1] + i * cell_size),
                         (board_pos[0] + board_size, board_pos[1] + i * cell_size), 10)

    # Draw text on the left and right sides of the board
    font = pygame.font.SysFont(None, 50)
    text1 = font.render("Player X", True, BLACK)
    text2 = font.render("Player O", True, BLACK)
    window.blit(text1, (board_pos[0] - text1.get_width() - board_margin,
                        board_pos[1] + board_size // 2 - text1.get_height() // 2))
    window.blit(text2, (board_pos[0] + board_size + board_margin,
                        board_pos[1] + board_size // 2 - text2.get_height() // 2))

    # Draw pieces
    for row in range(3):
        for col in range(3):
            if board[row][col] is not None:
                draw_piece(row, col)

    # Draw text on the left and right sides of the board
    font = pygame.font.SysFont(None, 50)
    text1 = font.render("Player X", True, BLACK)
    text2 = font.render("Player O", True, BLACK)
    window.blit(text1, (25, 25))
    window.blit(text2, (400, 25))
    text1 = font.render("Stack: " + str(BID_STACK[0]), True, BLACK)
    text2 = font.render("Stack: " + str(BID_STACK[1]), True, BLACK)
    window.blit(text1, (25, 65))
    window.blit(text2, (400, 65))
    text1 = font.render("BID", True, BLACK)
    window.blit(text1, (45, 170))

    # Draw bid arrows and bid value
    pygame.draw.rect(window, BLACK, arrow_rect_x, 2)
    pygame.draw.polygon(window, BLACK, [(arrow_up_rect_x.centerx, arrow_up_rect_x.y),
                                        (arrow_up_rect_x.x, arrow_up_rect_x.bottom),
                                        (arrow_up_rect_x.right, arrow_up_rect_x.bottom)], 2)
    pygame.draw.polygon(window, BLACK, [(arrow_down_rect_x.centerx, arrow_down_rect_x.bottom),
                                        (arrow_down_rect_x.x, arrow_down_rect_x.y),
                                        (arrow_down_rect_x.right, arrow_down_rect_x.y)], 2)
    pygame.draw.rect(window, BLACK, arrow_rect_x2, 2)
    pygame.draw.polygon(window, BLACK, [(arrow_up_rect_x2.centerx, arrow_up_rect_x2.y),
                                        (arrow_up_rect_x2.x, arrow_up_rect_x2.bottom),
                                        (arrow_up_rect_x2.right, arrow_up_rect_x2.bottom)], 2)
    pygame.draw.polygon(window, BLACK, [(arrow_down_rect_x2.centerx, arrow_down_rect_x2.bottom),
                                        (arrow_down_rect_x2.x, arrow_down_rect_x2.y),
                                        (arrow_down_rect_x2.right, arrow_down_rect_x2.y)], 2)
    number_text = font.render(str(bid_value[0]), True, BLACK)
    window.blit(number_text, (arrow_rect_x2.right + 20, arrow_rect_x2.centery - number_text.get_height() // 2))
    pygame.draw.rect(window, BLACK, arrow_rect_o, 2)
    pygame.draw.polygon(window, BLACK, [(arrow_up_rect_o.centerx, arrow_up_rect_o.y),
                                        (arrow_up_rect_o.x, arrow_up_rect_o.bottom),
                                        (arrow_up_rect_o.right, arrow_up_rect_o.bottom)], 2)
    pygame.draw.polygon(window, BLACK, [(arrow_down_rect_o.centerx, arrow_down_rect_o.bottom),
                                        (arrow_down_rect_o.x, arrow_down_rect_o.y),
                                        (arrow_down_rect_o.right, arrow_down_rect_o.y)], 2)
    number_text = font.render(str(bid_value[1]), True, BLACK)
    window.blit(number_text, (arrow_rect_o.right + 20, arrow_rect_o.centery - number_text.get_height() // 2))
    pygame.draw.rect(window, BLACK, bid_rect, 2)

    if bidding_now is False:
        if current_player == 'X':
            pygame.draw.rect(window, GREEN, circle_player_x, 2)
        else:
            pygame.draw.rect(window, GREEN, circle_player_o, 2)


# Draw a piece on the board
def draw_piece(row, col):
    # Calculate the center of the cell
    center_x = col * cell_size + cell_size // 2 + board_pos[0]
    center_y = row * cell_size + cell_size // 2 + board_pos[1]

    # Draw an X or O depending on the value of the cell
    if board[row][col] == "X":
        pygame.draw.line(window, (255, 0, 0), (center_x - cell_size // 3, center_y - cell_size // 3),
                         (center_x + cell_size // 3, center_y + cell_size // 3), 5)
        pygame.draw.line(window, (255, 0, 0), (center_x + cell_size // 3, center_y - cell_size // 3),
                         (center_x - cell_size // 3, center_y + cell_size // 3), 5)
    elif board[row][col] == "O":
        pygame.draw.circle(window, (0, 0, 255), (center_x, center_y), cell_size // 3, 5)


# Handle user input
def handle_input(player):
    global current_player, bidding_now
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bidding_now is True:
                # Check for bid click
                if arrow_up_rect_x.collidepoint(event.pos):
                    bid_value[0] += 10
                elif arrow_down_rect_x.collidepoint(event.pos):
                    bid_value[0] -= 10
                elif arrow_up_rect_x2.collidepoint(event.pos):
                    bid_value[0] += 1
                elif arrow_down_rect_x2.collidepoint(event.pos):
                    bid_value[0] -= 1
                elif arrow_up_rect_o.collidepoint(event.pos):
                    bid_value[1] += 1
                elif arrow_down_rect_o.collidepoint(event.pos):
                    bid_value[1] -= 1
                elif bid_rect.collidepoint(event.pos):
                    bidding_now = False
                    bid_value[1] = get_ai_bid()
                    if bid_value[0] > bid_value[1]:
                        current_player = 'X'
                        BID_STACK[0] -= bid_value[0]
                        BID_STACK[1] += bid_value[0]
                    elif bid_value[0] < bid_value[1]:
                        current_player = 'O'
                        BID_STACK[0] += bid_value[1]
                        BID_STACK[1] -= bid_value[1]
                    else:
                        bidding_now = True
            else:
                # Get the coordinates of the mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Determine which cell the mouse click corresponds to
                row = (mouse_y - board_pos[1]) // cell_size
                col = (mouse_x - board_pos[0]) // cell_size

                # Correct of border clicks
                row = max(0, min(2, row))
                col = max(0, min(2, col))

                if handle_move(row, col, player):
                    return True
        return False


# Get AI's bid
def get_ai_bid():
    # TODO: If a win is possible, go all in
    return randint(1, min(BID_STACK[1], BID_STACK[0]+1))


# Check for a winner
def check_game_over():
    winner = check_winner()

    # Draw pieces - necessary to draw the last piece
    for row in range(3):
        for col in range(3):
            if board[row][col] is not None:
                draw_piece(row, col)

    if winner is not None:
        font = pygame.font.SysFont(None, 100)
        if winner == 'tie':
            text = font.render("Tie!", True, BLACK)
        else:
            text = font.render(f"{winner} wins!", True, BLACK)
        window.blit(text, (150, 250))
        pygame.display.update()
        pygame.time.wait(2000)
        return True
    return False


# Reset the game
def reset_game():
    global board, current_player, BID_STACK
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    current_player = 'X'
    BID_STACK = [100, 100]


# Main game loop
current_player = 'X'
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw the board and pieces
    draw_board()

    # Handle player input
    if handle_input(current_player):
        # Check for a winner
        if check_game_over():
            reset_game()

    pygame.display.update()

