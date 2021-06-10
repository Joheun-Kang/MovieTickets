import sys
import numpy as np
import unittest
import pandas as pd
from jk_helper import update_empty_seats, assign_seats 

# basic reservation information
def read_reservation(infile):
    try:
        df = pd.read_csv(infile, sep=" ", header=None)
        return len(df)
    except pandas.errors.EmptyDataError:
        print("Sorry, We don't have any reservation at this time")
        exit(0)


class read_res_request(object):     

    def __init__(self, n, infile):
        self.n = n
        self.infile = infile

    def read(self, infile):
        df = pd.read_csv(infile, sep=" ", header=None)
        self.group_id = df.loc[self.n, 0]                                 
        self.num_reservations = df.loc[self.n, 1]  
        if self.num_reservations <= 0:
            print("Invalid Reservation please try again")
            exit(0)
        return self.group_id, self.num_reservations

class type1(object):

    def __init__(self, group_id, num_reservations):
        self.group_id = group_id
        self.num_reservations = num_reservations

    def type1_allot(self):
        for i in range(nrows):
            for j in range(cols):
                if seats[i][j] == 1.0:
                    seats[i][j] = 0.0
                    seat_id[i][j] = self.group_id
                    update_empty_seats(row_seats_left, i)
                    seat = assign_seats(i, j)
                    return seat # DONE

class type2(object):

    def __init__(self, group_id, num_reservations):
        self.group_id = group_id
        self.num_reservations = num_reservations

    #conditions 
    def group_empty_row(self):
        for i in range(nrows):
            if row_seats_left[i] >= self.num_reservations:                
                return i

    def group_seat_check(self):
        row = self.group_empty_row()
        temp = []
        for j in range(cols):    
            if seats[row][j] == 1:
                temp.append(j)
        return temp, row

    def seats_in_one_row(self):
        for i in range(nrows):
            if row_seats_left[i] >= self.num_reservations:
                return True
            
    def type2_allot(self):
        temp, row = self.group_seat_check() 
        #print('temp %s row %d' %(temp,row))
        alloted_seats = []
        seat_allocated = []
        #print('is seat updates?',seats) 
        for i in range(self.num_reservations):
            col = temp[i]
            seat_allocated.append(col)
            seats[row][col] = 0
            seat_id[row][col] = self.group_id
            update_empty_seats(row_seats_left, row)
            seat = assign_seats(row, col)
            alloted_seats.append(seat) 
        return alloted_seats

class type3(object):

    def __init__(self, group_id, num_reservations):
        self.group_id = group_id
        self.num_reservations = num_reservations

    def type3_allot(self):
        no_of_rows = self.num_reservations // no_avail_seats
        remaining_seats = self.num_reservations % no_avail_seats
        grouptwoObj = type2(self.group_id, cols)
        for i in range(no_of_rows):
            grouptwoObj.type2_allot()
        grouptwoObjnew = type2(self.group_id, remaining_seats)
        grouptwoObjnew.type2_allot()


# writing files to output.txt file        
def write_file(outfile, group_id, assignments):
    with open(outfile, 'a') as out:
        if isinstance(assignments, list):
            out.write(group_id + " " + ','.join(assignments))
            out.write("\n")
        else:
            out.write(group_id + " " + assignments)
            out.write("\n")

           
def seat_allocator(group_id, num_reservations):
    
    reserved_seats = []
    
    type1Obj = type1(group_id, num_reservations)
    type2Obj = type2(group_id, num_reservations)
    type3Obj = type3(group_id, num_reservations)
    
    #print('here emp_seat_row',row_seats_left) # need to be [5,5,5,5,5,5,5,5,5,5]
    print('sum(row_seats_left)',sum(row_seats_left))
    if sum(row_seats_left) and sum(row_seats_left) >= num_reservations:
        
        # case1: num_reservations == 1 
        if num_reservations == 1:
            seat = type1Obj.type1_allot()
            reserved_seats.append(seat)
           
            
            
        # case2: num_reservations < no.of seats in a row 
        elif num_reservations > 1 and num_reservations <= no_avail_seats:
            flag = type2Obj.seats_in_one_row()
            
            if sum(row_seats_left) > num_reservations and flag:
                reserved_seats = type2Obj.type2_allot()
                

            elif sum(row_seats_left) >= num_reservations:
                for res in range(num_reservations):
                    seat = type1Obj.type1_allot()
                    reserved_seats.append(seat)
                    
                    
        # case3: num_reservations > no.of seats in a row
        elif num_reservations > no_avail_seats:
            if sum(row_seats_left) > num_reservations:
                type3Obj.type3_allot()
            elif sum(row_seats_left) == num_reservations:
                for res in range(num_reservations):
                    seat = type1Obj.type1_allot()
                    reserved_seats.append(seat)
                    
        
        write_file(outfile, group_id, reserved_seats)                        
    
    elif sum(row_seats_left) == 0:
        write_file(outfile, group_id, "The theater is fully booked")
        
    elif sum(row_seats_left) and sum(row_seats_left) < num_reservations:
    	write_file(outfile, group_id, "Insufficient Seats! we have only  " + str(sum(row_seats_left)))
        # continue
    else:
        print("System Error")
        exit(0)
    
    return reserved_seats





 
def __main__(infile):

	total_reservations = read_reservation(infile) # how many groups made reservation
	reserved_total = 0  # initialize reservation
	for n in range(total_reservations):
		readBookingObj = read_res_request(n, infile)
		group_id, no_of_reservations = readBookingObj.read(infile)
		reserved_seats = seat_allocator(group_id, no_of_reservations)
		reserved_total = reserved_total + (len(reserved_seats))
	return reserved_total



#----
cols = 20
nrows = 10
buffer_ = 3
no_avail_seats = cols//(buffer_+1)


# Each row, only 5 people can be seated 
row_seats_left = [5,5,5,5,5,5,5,5,5,5] # -> change to row_seats_left


# keep only this columns
even_row_avail_col = [1,5,9,13,17]
odd_row_avail_col = [2,6,10,14,18]


#create seats
seats = np.zeros(shape=(nrows, cols))
for row in range(nrows):
    if row%2 == 0: # even row
        for col in even_row_avail_col:
            seats[row][col] = 1
    else:
        for col in odd_row_avail_col:
            seats[row][col] = 1

# create seats_id
seat_id = np.array(seats, dtype=object)
for row in range(len(seat_id)):
	for col in range(len(seat_id[0])):
		if seat_id[row][col] == 0.0:
			seat_id[row][col] = "-"

# print('new seats',seats)
# print('new_seat_id',seat_id)
#----

# print(seats)
# print(seat_id)

if __name__ == '__main__':
    try:
        #database = sys.argv[1]
        infile = sys.argv[1]
        outfile = sys.argv[2]  
        
        
        #__main__(database, infile)
        __main__(infile)
        
               
        print("#######################   SCREEN  #######################")
    
        for i in range(nrows):
            rows = seat_id[i]
            print (rows)

        print("#######################  BACK  #######################")
           
    except IndexError:
        print ('Invalied .txt input file or output file')
        sys.exit()









