# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:23:49 2022

@author: mohaa
"""

import numpy as np
import random 
import math 

col_number = 7
row_number = 6

def board_creation():
    board = np.zeros((6,7))
    return board

def piece_drop(board, r, c, dropped):
    board[r][c] = dropped 

def is_valid(board, col):
	return board[row_number-1][col] == 0

def next_row(board, col):
    for i in range(row_number):
        if board[i][col] == 0:
            return i
        

def print_board(board):
    print(np.flip(board, 0))    
    
def win(board, dropped):
    for i in range(7): # Vertical Win
        for j in range(3):
            if board[j][i] == dropped and board[j+1][i] == dropped and board[j+2][i] == dropped and board[j+3][i] == dropped:                                                                             
                return True
            
    for i in range(4): # Horizontal Win
        for j in range(6):
            if board[j][i] == dropped and board[j][i+1] == dropped and board[j][i+2] == dropped and board[j][i+3] == dropped:
                return True

    for i in range(4): # Left Diagonal Win
        for j in range(3,6):
            if board[j][i] == dropped and board[j-1][i+1] == dropped and board[j-2][i+2] == dropped and board[j-3][i+3] == dropped:
                return True
            
    for i in range(4): # Right Diagonal Win
        for j in range(3):
            if board[j][i] == dropped and board[j+1][i+1] == dropped and board[j+2][i+2] == dropped and board[j+3][i+3] == dropped:
                return True


def score(board, dropped):
    total_score = 0
    center = [int(i) for i in list(board[:, 3])] # put priority on middle column
    center_count = center.count(dropped)
    total_score += center_count*6
    
    for c in range(col_number): # Vertical score    
        col_score = [int(i) for i in list(board[:,c])]
        for j in range(row_number-3):
            col_count = col_score[j:j+4]           
            total_score += evaluate(col_count, dropped) 
    
    for i in range(row_number): # Horizonal score
        row_score = [int(j) for j in list(board[i,:])]
        for c in range(col_number-3):
            row_count = row_score[c:c+4]          
            total_score += evaluate(row_count, dropped)    
                
                
    for r in range(row_number - 3): # Left Diagonal score
        for c in range(col_number -3):
            left_count = [board[r+3-i][c+i] for i in range(4)]   
            total_score += evaluate(left_count, dropped) 
            
    
    for r in range(row_number - 3): # Right Diagonal score
        for c in range(col_number -3):
            right_count = [board[r+i][c+i] for i in range(4)]
            total_score += evaluate(right_count, dropped)    
    
    
    return total_score


def evaluate(distance, dropped):
    this_score = 0 # initialize
    opp = 1 # opponent is human 
    if dropped == 1:
       opp = 2 # oponnent is AI
       
    if distance.count(dropped) == 4: # 4 in a row
        this_score += 1000
    elif distance.count(dropped) == 3 and distance.count(0) == 1: # 3 in a row
        this_score += 50
    elif distance.count(dropped) == 2 and distance.count(0) == 2: # 2 in a row
        this_score += 20
    
    if distance.count(opp) == 3 and distance.count(0) == 1: # opponent has 3 in a row
        this_score -= 40
        
    if distance.count(opp) == 2 and distance.count(0) == 1: # opponent has 2 in a row
        this_score -= 10
        
    return this_score
       
   
       
       
       
       
def get_valid(board):
	valid_locations = []
	for col in range(col_number):
		if is_valid(board, col):
			valid_locations.append(col)
	return valid_locations
    
        
def best_move(board, dropped):
    valid_locations = get_valid(board)
    top_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = next_row(board, col)
        temp_board = board.copy()
        piece_drop(temp_board, row, col, dropped)
        current_score = score(temp_board, dropped)
        if current_score > top_score:
            top_score = current_score
            best_col = col

    return best_col

def terminal(board):
    return win(board, 1) or win(board, 2) or len(get_valid(board)) == 0


def minimax(board, depth, alpha, beta, maxplayer):
    valid_locations = get_valid(board)
    terminal_node = terminal(board)
    if depth == 0 or terminal_node:
        if terminal_node:
            if win(board, 2):
                return (None, 99999999) # AI wins
            elif win(board, 1): 
                return (None, -99999999) # human wins           
            else: # game ends
                return (None, 0)
        else: # Depth is 0
            return (None, score(board, 2))
    if maxplayer: # Maximize AI
        current_score = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = next_row(board, col)
            temp = board.copy()
            piece_drop(temp, row, col, 2)
            new_score = minimax(temp, depth-1, alpha, beta, False)[1] # [1] to only return current score
            if new_score > current_score: # Get the Max 
                current_score = new_score
                best_col = col 
            alpha = max(alpha, current_score)
            if alpha >= beta:  # ignore irrelevent branches
                break
        return best_col, current_score
    else: 
        current_score = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = next_row(board, col)
            temp = board.copy()
            piece_drop(temp, row, col, 1)
            new_score = minimax(temp, depth -1, alpha, beta, True)[1] # [1] to only return current score
            if new_score < current_score: # Get the Min 
                current_score = new_score
                best_col = col
            beta = min(beta, current_score)
            if alpha >= beta:
                break
        return best_col, current_score
    
    
   
board = board_creation()
print_board(board)
end = False
a = -math.inf # initializing alpha
b = math.inf # initializing beta

player = random.randint(0,1) # randomize who goes first

while not end:
    
    if player == 0: # human opponent
        col = int(input("Player 1 choose your move [0-6]"))
        if is_valid(board, col):            
            row = next_row(board, col)
            piece_drop(board, row, col, 1)           
            if win(board, 1):
                print('Player 1 won')
                end = True
            player += 1
            player = player % 2
            print_board(board)

            
    if player == 1 and not end: # AI 
        col, minimax_score = minimax(board, 5, a, b, True)
        print('AI chose column: ', col)
        print('AI score: ', minimax_score)
        if is_valid(board, col):
            row = next_row(board, col)
            piece_drop(board, row, col, 2)
            if win(board, 2):
                print('AI won')
                end = True
            print_board(board)  
            player += 1
            player = player % 2
    