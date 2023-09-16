import glob
import string


initial_state = [0,0,1,0,1,1,0,1,1,0,1]
tap_sequence_1 = [0,6]
tap_sequences_2 = [0,9]
tap_sequence_3 = [0,9,10,12]
feedback= 0
feedbacks=[]
def LFSR(initial_state):
    for i in range(2000):#pow(2, len(initial_state)) 
        
        global feedback
        first_bit = initial_state[0]
        for j in range(len(tap_sequence_1)):
           if j == 0:
                
               
               feedback= initial_state[tap_sequence_1[j]]
             
           else:
               
               feedback  =  feedback ^  initial_state[tap_sequence_1[j]]

        initial_state.pop()
        feedbacks.append(feedback)
        print("This time feedback is : ", feedback)
        initial_state= [feedback, *initial_state]


def initial_tapSequence_populator():
    tap_sequence = int(input("Enter the number of tap sequences "))
    global tap_sequences
    for k in range(tap_sequence):
        tap_sequences.append(int(input("Enter the sequence " + str(k) + " bit in tap sequence  : ")))
    
    print(tap_sequences)



def initial_state_populator(size_of_register):
    for i in range(1,size_of_register+1):
        initial_state.append(int(input("Enter the "+ str(i) + " bit of Register " )))
def start():
    size_of_register = int(input("Enter the size")) 
    initial_state_populator(size_of_register)
    initial_tapSequence_populator()
    LFSR(initial_state)
start()






    
    
        

   

