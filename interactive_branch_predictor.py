"""
Interactive Branch Prediction Analysis Tool
==========================================

This is the final output of my Branch Prediction project. It provides an interactive
interface to analyze branch prediction algorithms on code traces.

Features:
- Displays the code being analyzed
- Shows branch prediction accuracy over time
- Compares different prediction algorithms
- Interactive interface for future file input capability

Author: Aarnav Koushik
"""

import matplotlib.pyplot as plt
import ast
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

def display_code_being_analyzed():
    """Display the code that is being analyzed for branch prediction"""
    print("="*80)
    print("CODE BEING ANALYZED FOR BRANCH PREDICTION")
    print("="*80)
    print()
    
    # Get the code from parser.py
    code = """
def simulate_scores():
    scores = [45, 52, 63, 78, 82, 91, 100, 67, 88, 49]
    for _ in range(5):  # repeat loop to generate history
        for score in scores:
            if score >= 90:
                grade = "A"
                if score == 100:
                    comment = "Perfect!"
                else:
                    comment = "Excellent"
            elif score >= 75:
                grade = "B"
                if score >= 85:
                    comment = "Good job"
                else:
                    comment = "Well done"
            elif score >= 60:
                grade = "C"
                comment = "Needs improvement"
            else:
                grade = "F"
                if score < 50:
                    comment = "Failing badly"
                else:
                    comment = "Barely passing"
            if score % 2 == 0:
                even_comment = "Even score"
            else:
                even_comment = "Odd score"
"""
    
    print(code)
    print()
    print("This code contains multiple conditional branches (if/elif statements)")
    print("that will be analyzed by different branch prediction algorithms.")
    print()

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

def display_branch_trace_info(trace, branches_map):
    """Display information about the generated branch trace"""
    print("="*80)
    print("BRANCH TRACE INFORMATION")
    print("="*80)
    print(f"Total branch predictions: {len(trace)}")
    print(f"Unique branch addresses: {len(branches_map)}")
    print(f"Branch addresses: {sorted(branches_map.values())}")
    print()
    
    # Show first few trace entries
    print("First 10 branch predictions:")
    for i, (addr, taken) in enumerate(trace[:10]):
        print(f"  Step {i+1:2d}: Address {addr:4d} -> {'TAKEN' if taken else 'NOT TAKEN'}")
    if len(trace) > 10:
        print(f"  ... and {len(trace) - 10} more predictions")
    print()

def create_accuracy_plot(trace):
    """Create and display the accuracy plot using existing plotting functionality"""
    print("="*80)
    print("GENERATING ACCURACY ANALYSIS...")
    print("="*80)
    
    # Get accuracy history for each method
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
    
    # Create the plot
    plt.figure(figsize=(14, 10))
    
    # Plot accuracy curves with distinct colors and styles
    steps = range(1, len(trace) + 1)
    plt.plot(steps, one_bit_history, label='1-bit Prediction', linewidth=3, alpha=0.9, color='blue', linestyle='-')
    plt.plot(steps, two_bit_history, label='2-bit Prediction', linewidth=3, alpha=0.9, color='green', linestyle='-')
    plt.plot(steps, bimodal_history, label='Bimodal Prediction', linewidth=3, alpha=0.9, color='orange', linestyle='--')
    plt.plot(steps, gshare_history, label='gShare Prediction', linewidth=3, alpha=0.9, color='purple', linestyle='-')
    
    # Add horizontal line for 50% accuracy (random guessing)
    plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Random Guessing (50%)')
    
    # Customize the plot
    plt.xlabel('Branch Prediction Step', fontsize=14)
    plt.ylabel('Accuracy', fontsize=14)
    plt.title('Branch Prediction Accuracy Over Time\nInteractive Analysis Tool', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Set y-axis to show percentage
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    # Set reasonable axis limits
    plt.ylim(0, 1)
    plt.xlim(1, len(trace))
    
    # Add statistics as text
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
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
             fontsize=11)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('interactive_branch_prediction_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as 'interactive_branch_prediction_analysis.png'")
    
    plt.show()
    
    return final_accuracies

def display_final_results(final_accuracies):
    """Display the final results in a formatted table"""
    print("="*80)
    print("FINAL ACCURACY RESULTS")
    print("="*80)
    print()
    
    # Sort by accuracy (descending)
    sorted_results = sorted(final_accuracies.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Algorithm':<15} {'Accuracy':<10} {'Performance'}")
    print("-" * 50)
    
    for i, (method, acc) in enumerate(sorted_results):
        performance = "🏆 Excellent" if acc >= 0.8 else "✅ Good" if acc >= 0.6 else "⚠️  Fair" if acc >= 0.5 else "❌ Poor"
        print(f"{method:<15} {acc:>8.1%}   {performance}")
    
    print()
    best_method, best_acc = sorted_results[0]
    worst_method, worst_acc = sorted_results[-1]
    
    print(f"🏆 Best performing algorithm: {best_method} ({best_acc:.1%})")
    print(f"📊 Worst performing algorithm: {worst_method} ({worst_acc:.1%})")
    print(f"📈 Performance range: {best_acc - worst_acc:.1%}")
    print()

def show_future_capabilities():
    """Display information about future interactive capabilities"""
    print("="*80)
    print("FUTURE INTERACTIVE CAPABILITIES")
    print("="*80)
    print()
    print("🚀 This tool is designed to be extended with the following features:")
    print()
    print("1. 📁 File Input: Upload your own Python code files for analysis")
    print("2. 🔧 Custom Parameters: Adjust prediction algorithm parameters")
    print("3. 📊 Advanced Metrics: Detailed performance analysis and statistics")
    print("4. 🎯 Interactive Plotting: Zoom, pan, and explore the accuracy graphs")
    print("5. 📈 Export Results: Save analysis results in various formats")
    print("6. 🔄 Real-time Analysis: Live updates as you modify code")
    print()
    print("The current implementation uses the existing functions from:")
    print("  • parser.py - Code analysis and trace generation")
    print("  • learning/*.py - Prediction algorithms")
    print("  • plotting.py - Visualization functions")
    print()

def main():
    """Main interactive function"""
    print("🎯 INTERACTIVE BRANCH PREDICTION ANALYSIS TOOL")
    print("=" * 60)
    print()
    
    # Step 1: Display the code being analyzed
    display_code_being_analyzed()
    
    # Step 2: Generate the trace and show information
    print("Generating branch trace from the code...")
    trace, branches_map = parser.generate_branch_trace()
    display_branch_trace_info(trace, branches_map)
    
    # Step 3: Create and display the accuracy plot
    final_accuracies = create_accuracy_plot(trace)
    
    # Step 4: Display final results
    display_final_results(final_accuracies)
    
    # Step 5: Show future capabilities
    show_future_capabilities()
    
    print("="*80)
    print("ANALYSIS COMPLETE! 🎉")
    print("="*80)
    print("The interactive analysis has been completed successfully.")
    print("Check the generated plot and results above.")
    print()

if __name__ == "__main__":
    main()
