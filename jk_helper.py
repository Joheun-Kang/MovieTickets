import sys
import pandas as pd
import numpy as np                                               

def update_empty_seats(row_seats_left, row):
    tmp = row_seats_left[row]
    row_seats_left[row] = tmp - 1
    return row_seats_left                       

def assign_seats(row, col):
    # assing seats from front
    row_id = "ABCDEFGHIJ"
    row_number = row_id[row]
    #row_number = row_id[(row+5)%10] # if you want to see from the middle
    seat_number = col + 1
    seat = row_number + str(seat_number)
    return seat