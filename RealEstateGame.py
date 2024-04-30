# Author: Vanessa Mota-Li
# GitHub username: Vnessa19
# Date: 5/24/22
# Description: A program that contains two class RealEstateGame and Player, the program imitate a simplified version of Monopoly.

class RealEstateGame:
    """A class represents a RealEstateGame"""

    def __init__(self, players_list=None):
        """Initials a new RealEstateGame and an empty players_list"""
        self._players_list = []

    def create_spaces(self, GO_reward, list_of_rent):
        """
        Initials the game board with two parameters,
        one is GO space and its reward, the other takes a list of rents for 24 spaces
        the game board is a list of dictionary,
        space 1-24 contains nested dictionary
        """

        self._spaces_name = ["Aries Street", "Taurus Street", "Gemini Street", "Cancer Street", "Leo Street", "Virgo Street",
                       "Libra Street", "Scorpio Street", "Sagittarius Street", "Capricorn Street", "Aquarius Street",
                       "Pisces Street", "Rat Way", "Ox Way", "Tiger Way", "Rabbit Way", "Dragon Way", "Snake Way",
                       "Horse Way", "Sheep Way", "Monkey Way", "Rooster Way", "Dog Way", "Pig Way"]


        self._board = [{"GO": GO_reward}]

        index = 0
        for road in self._spaces_name:
            space_dict = {}
            rent = list_of_rent[index]
            purchasing_price = rent * 5
            space_dict = dict({road:{"Rent": rent, "Purchasing Price": purchasing_price, "Owner":None}})
            self._board.append(space_dict)
            index += 1

    # def get_board(self):
    #     """for testing"""
    #     return self._board

    def get_space_name(self, pos):
        """Return space name"""

        return self._spaces_name[pos-1]

    def create_player(self, player_name, initial_account_balance):
        """
        Creates a player object, updates the players_list
        """
        player_object = Player(player_name, initial_account_balance)
        self._players_list.append(player_object)

    def get_players_list(self):
        """Return players_list"""

        return self._players_list

    def get_player(self, player_name):
        """Return player object"""

        for player_object in self._players_list:
            if player_object.get_name() == player_name:
                return player_object

    def get_player_account_balance(self, player_name):
        """
        Takes as a parameter the name of the player and returns the player's account balance
        by using Player's get_balance method.
        """

        return self.get_player(player_name).get_balance()

    def get_player_current_position(self, player_name):
        """
        Takes as a parameter the name of the player and returns the player's current position on the board as an integer
        by using Player's get_pos method.
        """

        return self.get_player(player_name).get_pos()

    def buy_space(self, player_name):
        """
        Takes as parameters the name of the player, and checks if the player can buy the current space
        """

        player_object = self.get_player(player_name)
        pos = player_object.get_pos()
        space_name = self.get_space_name(pos)

        # GO cannot be bought
        if pos == 0:
            return False

        # Check whether the space is owned by other players
        if self._board[pos][space_name]['Owner'] is not None:
            return False

        # Check whether player has enough money to buy the space
        if player_object.get_balance() < self._board[pos][space_name]['Purchasing Price']:
            return False

        # If they do, deduct the purchasing price from player's account
        player_object.deduct_balance(self._board[pos][space_name]['Purchasing Price'])
        # Set space's owner as player's name
        self._board[pos][space_name]['Owner'] = player_name
        # Update player's spaces_own_list
        player_object.add_spaces_owned(pos)
        return True

    def move_player(self, player_name, steps_to_move):

        # Check player’s account balance, if it is zero or below, return immediately.
        if self.get_player_account_balance(player_name) <= 0:
            return

        # If player passes GO(player’s current position + steps_to_move > 25), change player’s account balance by adding GO_reward.
        new_pos = self.get_player_current_position(player_name) + steps_to_move
        if new_pos > 24:
            new_pos -= 25
            self.get_player(player_name).add_balance(self._board[0]['GO'])
        self.get_player(player_name).change_pos(new_pos)

        # Return if new position is 0(lands on GO)
        if new_pos == 0:
            return

        # Check if player’s current pos’s space is owned by other player,
        player_object = self.get_player(player_name)
        pos = player_object.get_pos()
        space_name = self.get_space_name(pos)
        if self._board[pos][space_name]['Owner'] != None and player_name:
            # if yes, deduct the space’s rent from player,
            player_object.deduct_balance(self._board[pos][space_name]['Rent'])
            # and increase the same amount for owner.
            owner_object = self.get_player(self._board[pos][space_name]['Owner'])
            owner_object.add_balance((self._board[pos][space_name]['Rent']))

        #Check player’s account balance
        if self.get_player_account_balance(player_name) <= 0:
            # if it is less and equal to 0, player has lost the game, change each space player owns owner to None.
            for pos in player_object.get_spaces_owned():
                space_name = self.get_space_name(pos)
                self._board[pos][space_name]['Owner'] = None
            # And empty player’s spaces_own list.
            player_object.empty_spaces_owned()

    # def show_spaces_own(self, player_name):
    #     """for testing"""
    #     player_object = self.get_player(player_name)
    #     ls = player_object.get_spaces_owned()
    #     return ls

    def check_game_over(self):
        """
        Return winning player’s name when all players except one have current account balance of 0.
        Return an empty string when there is no winner.
        “””"""

        winner = ""
        players = []
        for player_object in self._players_list:
            if player_object.get_balance() > 0:
                players.append(player_object.get_name())

        if len(players) == 1:
            winner = players[0]

        return winner


class Player:
    """A class represents a player"""

    def __init__(self, player_name, initial_account_balance, space_owned=None):
        """
        Initial a Player object with their name, initial account balance, current position set as 0, and their space_owned list
        """

        self._name = player_name
        self._balance = initial_account_balance
        self._spaces_owned = []
        self._pos = 0

    def get_name(self):
        """Return name"""

        return self._name

    def get_balance(self):
        """
        Returns account balance
        """

        return self._balance

    def add_balance(self, amount):
        """Adds account balance with amount"""

        self._balance += amount

    def deduct_balance(self, amount):
        """Subtract account balance with amount"""

        self._balance -= amount

    def get_pos(self):
        """Return pos"""

        return self._pos

    def change_pos(self, new_pos):
        """Modifies and return player pos"""

        self._pos = new_pos

    def get_spaces_owned(self):
        """Return spaces_owned list"""

        return self._spaces_owned

    def add_spaces_owned(self, pos):
        """Modify spaces_owned list"""

        self._spaces_owned.append(pos)

    def empty_spaces_owned(self):
        """Empty spaces_own list"""

        self._spaces_owned = []










