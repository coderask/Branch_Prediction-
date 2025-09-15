'''1-bit prediction algorithm'''

def one_bit_prediction(trace):
    # Extract unique addresses from trace to determine table size
    unique_addresses = set()
    for i in trace:
        unique_addresses.add(i[0])
    
    # Create address to index mapping
    address_to_index = {addr: idx for idx, addr in enumerate(sorted(unique_addresses))}
    
    # Initialize last prediction table for each address (0 = not taken, 1 = taken)
    last_predictions = [0] * len(unique_addresses)  # Start with not taken
    
    correct_predictions = 0
    total_predictions = len(trace)
    
    for i in trace:
        address = i[0]
        actual = i[1]
        
        # Map address to table index
        table_index = address_to_index[address]
        
        # Get current prediction for this address
        current_prediction = last_predictions[table_index]
        
        # Make prediction (1-bit: just use the last outcome for this address)
        predicted = current_prediction
        
        # Check if prediction was correct
        if predicted == actual:
            correct_predictions += 1
        
        # Update the last prediction for this address
        last_predictions[table_index] = actual
        
    #     print(f"Address {address}: Predicted {predicted}, Actual {actual}, {'✅' if predicted == actual else '❌'}")
    
    # print(f"Accuracy: {correct_predictions}/{total_predictions}")
    return (correct_predictions, total_predictions)
