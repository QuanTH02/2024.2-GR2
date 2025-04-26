import os
from pathlib import Path
from typing import List, Dict, Any
import json

def load_dataset(dataset_name: str) -> List[Dict[str, Any]]:
    """
    Load dataset from the specified name.
    
    Args:
        dataset_name: Name of the dataset to load
        
    Returns:
        List of code examples with their metadata
    """
    dataset_path = Path('data/datasets') / f'{dataset_name}.json'
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset {dataset_name} not found at {dataset_path}")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    return dataset

def save_dataset(dataset: List[Dict[str, Any]], dataset_name: str):
    """
    Save dataset to file.
    
    Args:
        dataset: List of code examples with their metadata
        dataset_name: Name to save the dataset as
    """
    dataset_path = Path('data/datasets') / f'{dataset_name}.json'
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dataset_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2) 