# CodeAttack: Code-Based Adversarial Attacks for Pre-trained Programming Language Models

This project implements the paper "CodeAttack: Code-Based Adversarial Attacks for Pre-trained Programming Language Models" (AAAI 2023). It provides a framework for generating adversarial examples for code-based models.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/codeattack.git
cd codeattack
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

To run the attack on a dataset:

```bash
python main.py --dataset_name your_dataset --model_name Salesforce/codet5-base
```

### Command Line Arguments

- `--model_name`: Name of the pre-trained model to use (default: 'Salesforce/codet5-base')
- `--dataset_name`: Name of the dataset to use (required)
- `--max_perturbations`: Maximum number of perturbations allowed (default: 0.4)
- `--similarity_threshold`: Minimum similarity threshold for adversarial examples (default: 0.5)
- `--output_dir`: Directory to save results (default: 'results')

### Example

```bash
python main.py --dataset_name code_search --model_name Salesforce/codet5-base --max_perturbations 0.3 --similarity_threshold 0.6
```

## Project Structure

```
codeattack/
├── data/
│   ├── datasets/     # Dataset files
│   └── models/       # Saved models
├── src/
│   ├── attacks/      # Attack implementations
│   ├── evaluation/   # Evaluation metrics
│   └── utils/        # Utility functions
├── results/          # Attack results
├── tests/            # Test files
├── main.py           # Main script
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Features

- Multiple attack methods:
  - Token substitution
  - Token insertion
  - Token deletion
  - Token reordering
- Comprehensive evaluation metrics:
  - Performance drop
  - Success rate
  - Code similarity
  - Average perturbations
- Support for various pre-trained models
- Easy to extend with new attack methods

## Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{codeattack2023,
  title={CodeAttack: Code-Based Adversarial Attacks for Pre-trained Programming Language Models},
  author={Your Name and Co-authors},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  year={2023}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 