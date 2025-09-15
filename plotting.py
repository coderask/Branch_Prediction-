"""
Plotting script to display accuracy over time for each branch prediction method.
This script tracks the accuracy of each prediction method as it processes the trace step by step.
"""

import matplotlib.pyplot as plt
import numpy as np
import parser
from learning import gShare_prediction
import learning.Bimodal_prediction as bimodal_prediction
import importlib.util
import sys

# Import 1-bit prediction
spec1 = importlib.util.spec_from_file_location("one_bit_prediction", "learning/1-bit-prediction.py")
one_bit_prediction = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(one_bit_prediction)

# Import 2-bit prediction  
spec2 = importlib.util.spec_from_file_location("two_bit_prediction", "learning/2-bit-prediction.py")
two_bit_prediction = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(two_bit_prediction)

def get_accuracy_over_time(trace, prediction_function):
    """Get accuracy over time by calling the prediction function on progressively larger subsets"""
    accuracy_history = []
    
    for i in range(1, len(trace) + 1):
        # Get subset of trace up to current point
        current_trace = trace[:i]
        
        # Call the prediction function on this subset
        correct, total = prediction_function(current_trace)
        
        # Calculate accuracy
        accuracy = correct / total if total > 0 else 0
        accuracy_history.append(accuracy)
    
    return accuracy_history

def plot_accuracy_over_time():
    """Create a plot showing accuracy over time for all prediction methods"""
    # Generate the trace data
    trace, branches_map = parser.generate_branch_trace()
    
    print(f"Processing {len(trace)} branch predictions...")
    print(f"Number of unique branch addresses: {len(branches_map)}")
    
    # Get accuracy history for each method using your original functions
    print("Running 1-bit prediction...")
    one_bit_history = get_accuracy_over_time(trace, one_bit_prediction.one_bit_prediction)
    print(f"  1-bit final accuracy: {one_bit_history[-1]:.1%}")
    
    print("Running 2-bit prediction...")
    two_bit_history = get_accuracy_over_time(trace, two_bit_prediction.two_bit_prediction)
    print(f"  2-bit final accuracy: {two_bit_history[-1]:.1%}")
    
    print("Running bimodal prediction...")
    bimodal_history = get_accuracy_over_time(trace, bimodal_prediction.bimodal_prediction)
    print(f"  Bimodal final accuracy: {bimodal_history[-1]:.1%}")
    
    print("Running gShare prediction...")
    gshare_history = get_accuracy_over_time(trace, gShare_prediction.gShare_prediction)
    print(f"  gShare final accuracy: {gshare_history[-1]:.1%}")
    
    # Check if 1-bit and bimodal are identical
    if one_bit_history == bimodal_history:
        print("  WARNING: 1-bit and Bimodal predictions are identical!")
    else:
        print("  1-bit and Bimodal predictions are different.")
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot accuracy curves with distinct colors and styles
    steps = range(1, len(trace) + 1)
    plt.plot(steps, one_bit_history, label='1-bit Prediction', linewidth=3, alpha=0.9, color='blue', linestyle='-')
    plt.plot(steps, two_bit_history, label='2-bit Prediction', linewidth=3, alpha=0.9, color='green', linestyle='-')
    plt.plot(steps, bimodal_history, label='Bimodal Prediction', linewidth=3, alpha=0.9, color='orange', linestyle='--')
    plt.plot(steps, gshare_history, label='gShare Prediction', linewidth=3, alpha=0.9, color='purple', linestyle='-')
    
    # Add horizontal line for 50% accuracy (random guessing)
    plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Random Guessing (50%)')
    
    # Customize the plot
    plt.xlabel('Branch Prediction Step', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.title('Branch Prediction Accuracy Over Time', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Set y-axis to show percentage
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Set reasonable axis limits
    plt.ylim(0, 1)
    plt.xlim(1, len(trace))
    
    # Add some statistics as text
    final_accuracies = {
        '1-bit': one_bit_history[-1],
        '2-bit': two_bit_history[-1],
        'Bimodal': bimodal_history[-1],
        'gShare': gshare_history[-1]
    }
    
    best_method = max(final_accuracies, key=final_accuracies.get)
    worst_method = min(final_accuracies, key=final_accuracies.get)
    
    stats_text = f"Final Accuracies:\n"
    for method, acc in sorted(final_accuracies.items(), key=lambda x: x[1], reverse=True):
        stats_text += f"{method}: {acc:.1%}\n"
    stats_text += f"\nBest: {best_method} ({final_accuracies[best_method]:.1%})\n"
    stats_text += f"Worst: {worst_method} ({final_accuracies[worst_method]:.1%})"
    
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             fontsize=9)
    
    plt.tight_layout()
    
    # Save the plot to a file
    plt.savefig('branch_prediction_accuracy.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'branch_prediction_accuracy.png'")
    
    plt.show()
    
    # Print final results
    print("\n" + "="*50)
    print("FINAL ACCURACY RESULTS")
    print("="*50)
    for method, acc in sorted(final_accuracies.items(), key=lambda x: x[1], reverse=True):
        print(f"{method:12}: {acc:.1%}")
    
    return final_accuracies

if __name__ == "__main__":
    # Run the plotting function
    final_accuracies = plot_accuracy_over_time()
