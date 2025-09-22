# Branch Prediction v1
##Branch Prediction v1

A Python simulator for exploring classic branch prediction techniques. This project was built as a hands-on way to understand how CPUs guess the direction of conditional branches.

⸻

##Overview

This repository implements and compares several classic branch predictors:
	•	1-bit prediction
	•	2-bit prediction
	•	Bimodal prediction
	•	gShare prediction

Predictor implementations are written mainly from scratch for learning purposes. The original starter code is kept commented at the top of the relevant files. After learning the techniques, the logic for Bimodal and gShare was refactored into reusable functions.

⸻

##Project structure

branch-prediction-v1/
interactive_branch_prediction.py    # Main entry point (if your file is named interactive_branch_predictor.py, use that name)
learning/
1-bit-prediction.py
2-bit-prediction.py
bimodal_prediction.py
gshare_prediction.py
README.md

⸻

##Requirements
	•	Python 3.9+ (tested on 3.11)
	•	Matplotlib for plotting results

Install dependencies:
pip install matplotlib

⸻

##Running the simulator

From the project root:
python interactive_branch_prediction.py

What the program does:
	1.	Prints the source code of the selected predictor and other key information to the terminal.
	2.	Displays a Matplotlib graph showing prediction accuracy over time.

⸻

##Features
	•	Implementations of 1-bit, 2-bit, Bimodal, and gShare predictors.
	•	Interactive runner that displays predictor code and statistics in the terminal.
	•	Graphical visualization of accuracy using Matplotlib.

⸻

##Roadmap
	•	Add more advanced predictors (e.g., tournament, perceptron).
	•	Improve the CLI to allow custom trace files and predictor parameters.
	•	Export results to CSV/JSON for downstream analysis or visualization.

⸻

License

MIT License — feel free to learn from or build upon this project.
