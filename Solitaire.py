import cards  # required !!!

#############################################
#   solitare game
#   diff functions to use for different uses like validating movements and different cards 
#       differnet functions having different moves
#       each functio purpose to solitare game
#
#   main function getting different options avaiable 
#       prompting user if they won or lost or if they didnt do somethig right
#################################################



RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    deck = cards.Deck()  # Create a deck of cards
    deck.shuffle()  # Shuffle the deck

    # Initialize the tableau with four columns, each containing one card
    tableau = []
    foundation = []  # Initialize an empty foundation

    # Deal four more cards to the tableau, one to each column
    for _ in range(4):
        tableau.append([deck.deal()])

    stock = deck  # The remaining cards form the stock

    return (stock, tableau, foundation)
    
def deal_to_tableau(tableau, stock):
    
    # for loop for differnet suits
    for i in range(4):
        if not stock.is_empty():
            tableau[i].append(stock.deal())
            
            # break if 
        else:
            break

           
def validate_move_to_foundation(tableau, from_col):
    
    # Empty column always False
    if len(tableau[from_col]) == 0:
        print(f"Error, empty column: {from_col}")
        return False

    move_card = tableau[from_col][-1]
    
    # Ace always False
    if move_card.value() == 1:
        print(f"\nError, cannot move {move_card}.")
        return False
    
    # Loop through every column
    for col in tableau:
        
        # Check if empty column
        if len(col) == 0:
            continue
        
        cur_card = col[-1]
        
        # Check if current card
        if cur_card == move_card:
            continue
        
        # Check if same suit
        if cur_card.suit() != move_card.suit():
            continue
        
        # Check if ace
        if cur_card.value() == 1:
            return True
        
        # Check if higher value
        if cur_card.value() > move_card.value():
            return True

    print(f"Error, cannot move {move_card}.")
    return False

    
def move_to_foundation(tableau, foundation, from_col):
    
    # if loop to make sure if it right, move if so
    if validate_move_to_foundation(tableau, from_col):
        card = tableau[from_col].pop()
        foundation.append(card)


def validate_move_within_tableau(tableau, from_col, to_col):
    # if loop to see if it less than or more than equal to
    if not (0 <= from_col < 4 and 0 <= to_col < 4):
        print("\nError, column index out of range.")
        return False
    elif len(tableau[from_col]) == 0:
        print("\nError, no card in column:", from_col)
        return False
    elif len(tableau[to_col]) > 0 and (tableau[to_col][-1].get_suit() != tableau[from_col][-1].get_suit() or
            tableau[to_col][-1].get_value() != tableau[from_col][-1].get_value() + 1):
        print("\nError, target column is not valid:", to_col)
        return False
    elif to_col == from_col:
        print("\nError, cannot move a card to its own column:", to_col)
        return False
    elif len(tableau[to_col]) > 0:
        print("\nError, target column is not empty:", to_col)
        return False
    else:
        return True


def move_within_tableau(tableau, from_col, to_col):
    # check if the move is valid
    if tableau[from_col] and (not tableau[to_col] or tableau[from_col][-1] < tableau[to_col][-1]):
        # move the card
        tableau[to_col].append(tableau[from_col].pop())

        
def check_for_win(tableau, stock):
    # Check if the stock is empty
    if stock:
        return False
    
    # Loop through each column
    for col in tableau:
        # Loop through each card
        for card in col:
            if card.value() != 1:
                return False

    return True


def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    
    '''
    '''
    while True:
        option = input("\nInput an option (DFTRHQ): ")
        if option.upper() == 'D':
            return ['D']
        elif option.upper() == 'R':
            return ['R']
        elif option.upper() == 'H':
            return ['H']
        elif option.upper() == 'Q':
            return ['Q']
        elif option[0].upper() == 'F':
            try:
                col = int(option.split()[1])
                if col < 1 or col > 4:
                    raise ValueError
                return ["F", col-1]
            except ValueError:
                print("Error in option:".format())
                return []
        elif option[0].upper() == 'T':
            try:
                cols = list(map(int, option.split()[1:]))
                if len(cols) != 2 or cols[0] < 1 or cols[0] > 4 or cols[1] < 1 or cols[1] > 4 or cols[0] == cols[1]:
                    raise ValueError
                updated_cols = []
                for col in cols:
                    updated_cols.append(col-1)
                return ["T"] + updated_cols
            except ValueError:
                print("\nError in option: {}".format())
                return []
        else:
            print("\nError in option: {}".format())
            return []


        
def main():
    print(RULES)  # Display the game rules
    
    stock, tableau, foundation = init_game()  # Initialize the game
    
    while True:
        display(stock, tableau, foundation)  # Display the game state
        
        option = get_option()  # Get user input
        
        if option == ['D']:
            deal_to_tableau(tableau, stock)
        elif option[0] == 'F':
            move_to_foundation(tableau, foundation, option[1])
        elif option[0] == 'T':
            move_from_col, move_to_col = option[1], option[2]
            if validate_move_within_tableau(tableau, move_from_col, move_to_col):
                move_within_tableau(tableau, move_from_col, move_to_col)
        elif option == ['R']:
            stock, tableau, foundation = init_game()
        elif option == ['H']:
            print(MENU)
        elif option == ['Q']:
            print("You have quit the game.")
            break
        else:
            print("Invalid option. Please try again.")
        
        if check_for_win(tableau, stock):
            display(stock, tableau, foundation)
            print("Congratulations! You have won the game.")
            break

# Entry point of the program
if __name__ == '__main__':
    main()
