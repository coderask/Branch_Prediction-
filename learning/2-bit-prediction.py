'''2-bit prediction''' 

def two_bit_prediction(trace):
    # Extract unique addresses from trace to determine table size
    unique_addresses = set()
    for i in trace:
        unique_addresses.add(i[0])
    
    # Create address to index mapping
    address_to_index = {addr: idx for idx, addr in enumerate(sorted(unique_addresses))}
    
    # Initialize state table for each address (0-3: strongly not taken to strongly taken)
    states = [3] * len(unique_addresses)  # Start with strongly taken
    
    correct_predictions = 0
    total_predictions = len(trace)
    
    for i in trace:
        address = i[0]
        actual = i[1]
        
        # Map address to table index
        table_index = address_to_index[address]
        
        # Get current state for this address
        current_state = states[table_index]
        
        # Make prediction based on current state (>=2 means taken, <2 means not taken)
        predicted = 1 if current_state >= 2 else 0
        
        # Check if prediction was correct
        if predicted == actual:
            correct_predictions += 1
        
        # Update state based on actual outcome
        if actual == 1:  # Branch was taken
            if current_state < 3:
                states[table_index] += 1
        else:  # Branch was not taken
            if current_state > 0:
                states[table_index] -= 1
        
    #     print(f"Address {address}: State {current_state}, Predicted {predicted}, Actual {actual}, {'✅' if predicted == actual else '❌'}")
    
    # print(f"Accuracy: {correct_predictions}/{total_predictions}")
    return (correct_predictions, total_predictions) 
