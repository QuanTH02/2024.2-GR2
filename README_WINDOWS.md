# CodeAttack - Windows Setup Guide

This guide will help you set up and run CodeAttack on Windows.

## Prerequisites

- Python 3.7 or higher
- Git
- Windows 10/11

## Quick Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd CodeAttack
```

### 2. Create virtual environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run setup script
```bash
python setup_windows.py
```

## Manual Setup

If you prefer manual setup:

### 1. Install PyTorch
```bash
# For CPU only
pip install torch torchvision torchaudio

# For CUDA (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Install other dependencies
```bash
pip install transformers datasets pandas numpy tqdm pyyaml scikit-learn tree-sitter sentence-transformers
```

### 3. Create directories
```bash
mkdir output data checkpoints
mkdir output\translation output\summarize output\refinement
mkdir data\code_translation data\code_summarization data\code_refinement
mkdir checkpoints\code_translation checkpoints\code_summarization checkpoints\code_refinement
```

## Running CodeAttack

### Basic Usage
```bash
python codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname test_run --theta 0.4
```

### Parameters Explained

- `--attack_model`: Model used for attack (codebert, bertattack, textfooler)
- `--victim_model`: Model to be attacked (codet5, codebert, graphcodebert, plbart, roberta)
- `--task`: Task type (translation, summarize, refinement)
- `--lang`: Language pair (java_cs, cs_java, java_small, etc.)
- `--use_ast`: Use AST constraint (0/1)
- `--use_dfg`: Use DFG constraint (0/1)
- `--out_dirname`: Output directory name
- `--theta`: Percentage of tokens to attack (0.0-1.0)

### Example Commands

#### Code Translation
```bash
python codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname java_cs_test --theta 0.4
```

#### Code Summarization
```bash
python codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang java --use_ast 0 --use_dfg 0 --out_dirname java_summary_test --theta 0.4
```

## Important Notes

### 1. Model Checkpoints
The system expects pre-trained model checkpoints in the `checkpoints/` directory. You need to:
- Download the required model checkpoints
- Place them in the appropriate subdirectories
- Update the paths in `configs/config_data.yaml` if needed

### 2. Data Files
The system expects data files in the `data/` directory. You need to:
- Prepare your dataset files
- Place them in the appropriate subdirectories
- Update the paths in `configs/config_data.yaml` if needed

### 3. GPU Usage
- The code automatically detects if CUDA is available
- If no GPU is available, it will run on CPU (slower but functional)
- For better performance, use a machine with NVIDIA GPU

### 4. Tree-sitter
- Tree-sitter is used for GraphCodeBERT functionality
- The setup script will handle the basic setup
- For full functionality, you may need to build tree-sitter libraries

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'textfooler'**
   - The textfooler module is optional
   - You can still use codebert and bertattack models

2. **FileNotFoundError: [Errno 2] No such file or directory**
   - Make sure you've run `setup_windows.py`
   - Check that all directories exist

3. **CUDA out of memory**
   - Reduce batch_size in config files
   - Use smaller models
   - Run on CPU if GPU memory is insufficient

4. **Model checkpoint not found**
   - Download the required model checkpoints
   - Update paths in config files
   - Use pre-trained models from Hugging Face

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed
2. Verify that directories exist
3. Check the console output for specific error messages
4. Ensure you have sufficient disk space and memory

## Performance Tips

1. **Use GPU**: Install CUDA version of PyTorch for better performance
2. **Reduce batch size**: If you encounter memory issues
3. **Use smaller models**: For faster execution
4. **Disable constraints**: Set `--use_ast 0 --use_dfg 0` for faster execution

## Limitations on Windows

1. **Tree-sitter**: Some advanced features may not work without proper tree-sitter setup
2. **External scripts**: Some functionality has been replaced with Python equivalents
3. **Performance**: May be slower than Linux due to Windows overhead

## Support

For issues specific to this Windows port, please check the troubleshooting section above. For general CodeAttack issues, refer to the original repository documentation. 