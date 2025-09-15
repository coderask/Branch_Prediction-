#history table  
# hTable = [0] * 4 #start with not taken 



# #GPT generated addresses & results 
# # 4 unique branch addresses
# branch_addresses = [
#     0b0001, 0b0010, 0b0011, 0b0100
# ]

# # Simulate 30 executions by repeating these addresses in some order
# executed_addresses = [
#     0b0001, 0b0010, 0b0011, 0b0100, 0b0001, 0b0010, 0b0011, 0b0100,
#     0b0001, 0b0010, 0b0011, 0b0100, 0b0001, 0b0010, 0b0011, 0b0100,
#     0b0001, 0b0010, 0b0011, 0b0100, 0b0001, 0b0010, 0b0011, 0b0100,
#     0b0001, 0b0010, 0b0011, 0b0100, 0b0001, 0b0010
# ]

# # Corresponding actual outcomes (1 = taken, 0 = not taken)
# executed_results = [
#     1,0,1,1, 1,1,1,0, 0,0,1,1, 1,0,0,0, 1,1,1,0, 0,0,1,1, 1,1,0,0, 1,0
# ]

# pTotal = 0
# rTotal = len(executed_results)
# for address, result in zip(executed_addresses,executed_results):
#     prediction = hTable[address-1]
#     print("prediction:", prediction, " actual: ", result)
#     if prediction == result:
#         print("jignator")
#         pTotal+=1   
#     if result:
#         hTable[address-1] = 1
#     else:
#         hTable[address-1] = 0


# print("accuracy:" , pTotal/rTotal)
    
# print(pTotal, rTotal)



def bimodal_prediction(trace):
    # Extract unique addresses from trace to determine table size
    unique_addresses = set()
    for i in trace:
        unique_addresses.add(i[0])
    
    # Create address to index mapping
    address_to_index = {addr: idx for idx, addr in enumerate(sorted(unique_addresses))}
    
    # Initialize history table with appropriate size
    hTable = [0] * len(unique_addresses)
    
    pTotal = 0
    rTotal = len(trace)
    
    for i in trace:
        address = i[0]  # Keep address as original value from trace
        result = i[1]
        # print("HTABLE", hTable)
        # print("ADDRESS", address)
        
        # Map address to table index
        table_index = address_to_index[address]
        prediction = hTable[table_index]
        
        if prediction == result:
            pTotal += 1   
        if result:
            hTable[table_index] = 1
        else:
            hTable[table_index] = 0
    
    return(pTotal, rTotal)




