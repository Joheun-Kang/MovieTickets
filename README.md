# Movie Ticket Reservation System 
## Joheun Kang 




# How it works 
This movie ticket reservation system will read the input file that contains group name (R####) and number of seats that customers need. Then, it will give us an output file that shows the group names  with the assigned seats.

Input: .txt file (group_name, #seats)
Output: .txt file (group_name_assign, seats)

# Assumption
In this system, we will have some assumptions to run the program. The assumption can always be changed depending on the preference of programmers. 

## Here are some assumptions. 

We assume that 
- All seats are empty at first
- This reservation system is "first come first"
- Group of People want to be seated from the back (las rows) (If not, we can fill up the rows from middle) 
- Group of people wanted to be seated in the same row.

# Code explanation

First, we initialize two matrices called "seats" and "seat_id". 
"seats" is the binary matrix and 0 indicates "not available seats" because of the 3 buffers requirement, and 1s are available seats.
"seat_id" is the matrix with 1 and "-", and 1 will be replaced to group names. 

Since we have the two requirements, 3 buffers and 1 row buffer, we create "even_row_avail_col" and "odd_row_avail_col". In that way, this system would satisfy those two requirements with maximum capacity. 


Then, we need to the create an indicator for the available seats for each row ("row_seats_left").
this will help us to track the available seats in each row.


### read_reservation(in-file)
- simply read input file. If the file is empty, that means there is ZERO reservation :(
- If the file is not empty, we take total_reservations (total number of groups)

### read_res_request(n,infile)
- using the total number of reservation, we read the input file line by line and get "group_id" and "number of reservations" that the group requests.

### seat_allocator(group_id, number of reservation)

If the available seats left, and it's more than the number of reservation, we can assign them some seats.
However,  if there is zero seats left or available seats are less than the number of reservations, we can't. 


If not the second case, there are three possible ways to do it.

1. type1: Number of reservation  = 1. 
in this case, we simply go through from the back of the row, and if there is an available seat, we can assign the seat. 

2. type2: Number of reservations >1 and number of reservation <= a single row (20)
in this case, we first need to check if there is a row that has available seats more than the reservations because people prefer to be seated in the same row. 
Then, 
if the available seats are more than number of reservations and there is the available row that the group can fit in the same row, 
we assign the seats and update the available seats. 

else if the available seats are more than or equal to the number of reservations, that means the group cannot fit to the same row, then we assign them from the seats that are available in the previous rows. 

3.type3: Number of reservation > row length
in this case, 
if there are available more than re number of reservations, we try to fit the group in a same row as much as possible.
However, if the available seats is exactly same as the number of reservation, they will be assign to the any available seats.


# Future Work
To make better reservation system (more realistic), we can take customers preference.
For example, we may give them a choice such as (front, middle, back), and apply that to the system.




Thank you!

