# '''Gshares efficiences only work when there are multiple branches'''


# # print("HI")
# predictions = [3] * 16

# test_trace = [
#     (0b0011, 1),
#     (0b1010, 0),
#     (0b0111, 1),
#     (0b0011, 0),
#     (0b1010, 1),
#     (0b0001, 1),
#     (0b0111, 0),
#     (0b1100, 1),
#     (0b0011, 1),
#     (0b1010, 1),
#     (0b0111, 1),
#     (0b0001, 0),
#     (0b1100, 0),
#     (0b0011, 0),
#     (0b0000, 1),
#     (0b1010, 0),
# ]

def gShare_prediction(trace):
    # Determine the maximum possible index based on unique addresses and history
    unique_addresses = set()
    for i in trace:
        unique_addresses.add(i[0])
    
    # Calculate the maximum possible index (max address XOR with max history)
    max_address = max(unique_addresses)
    max_history = 0b1111  # 4-bit history
    max_possible_index = max_address ^ max_history
    
    # Use a power-of-2 table size that can accommodate all possible XOR results
    # Find the next power of 2 that's >= max_possible_index + 1
    table_size = 1
    while table_size <= max_possible_index:
        table_size *= 2
    
    # Initialize prediction table with appropriate size
    predictions = [3] * table_size
    
    history = 0b0000 
    correct_predictions = 0

    for i in trace:
        index = i[0] ^ history #XOR the instruction address with the history 
        
        # Make prediction based on counter (>=2 means taken, <2 means not taken)
        predicted = 1 if predictions[index] >= 2 else 0
        actual = i[1]
        
        # Check if prediction was correct
        if predicted == actual:
            correct_predictions += 1
        
        # print("index", index)
        # print("adrr", bin(i[0]), "history", bin(history), "prediction", predictions[index], "actual", i[1])
        
        #update the prediction table 
        if (i[1] == 1): 
            if (predictions[index] < 3):
                predictions[index] += 1
            else:
                predictions[index] = 3
        else:
            if (predictions[index] > 0):
                predictions[index] -= 1
            else:
                predictions[index] = 0
        #update the history
        history = ((history << 1) | i[1]) & 0b1111 #mask to 4 bits

    # Print final results in the specified format
    # print(f"Accuracy: {correct_predictions} / {len(trace)}")
    # print(f"Final global history: 0b{history:04b}")
    # print(f"Final table: {predictions}")
    
    return (correct_predictions, len(trace))    
