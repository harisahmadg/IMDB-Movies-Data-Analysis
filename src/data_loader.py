#!/usr/bin/env python3
"""
IMDB Data Loader

Convenient functions for loading processed IMDB data for ML analysis.
Provides easy access to chunked datasets with memory management.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import List, Optional, Dict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IMDBDataLoader:
    def __init__(self, chunks_dir='data/chunks', processed_dir='data/processed'):
        self.chunks_dir = Path(chunks_dir)
        self.processed_dir = Path(processed_dir)
    
    def load_sample(self, dataset_name: str) -> pd.DataFrame:
        """Load a small sample dataset for quick analysis"""
        sample_path = self.processed_dir / f"{dataset_name}_sample.csv"
        
        if not sample_path.exists():
            logger.warning(f"Sample file not found: {sample_path}")
            return pd.DataFrame()
        
        return pd.read_csv(sample_path)
    
    def load_chunks(self, dataset_name: str, max_chunks: Optional[int] = None) -> pd.DataFrame:
        """Load dataset from chunks with optional limit"""
        chunk_pattern = f"{dataset_name}_chunk_*.csv"
        chunk_files = sorted(list(self.chunks_dir.glob(chunk_pattern)))
        
        if not chunk_files:
            logger.warning(f"No chunks found for dataset: {dataset_name}")
            return pd.DataFrame()
        
        if max_chunks:
            chunk_files = chunk_files[:max_chunks]
        
        logger.info(f"Loading {len(chunk_files)} chunks for {dataset_name}")
        
        dataframes = []
        for chunk_file in chunk_files:
            df = pd.read_csv(chunk_file)
            dataframes.append(df)
        
        combined_df = pd.concat(dataframes, ignore_index=True)
        logger.info(f"Loaded {len(combined_df)} total rows")
        
        return combined_df
    
    def get_available_datasets(self) -> List[str]:
        """Get list of available datasets"""
        datasets = set()
        
        for chunk_file in self.chunks_dir.glob('*_chunk_*.csv'):
            dataset_name = chunk_file.name.split('_chunk_')[0]
            datasets.add(dataset_name)
        
        return sorted(list(datasets))
    
    def get_dataset_info(self) -> Dict[str, Dict]:
        """Get information about available datasets"""
        info = {}
        
        for chunk_file in self.chunks_dir.glob('*_chunk_*.csv'):
            base_name = chunk_file.name.split('_chunk_')[0]
            
            if base_name not in info:
                info[base_name] = {
                    'chunks': 0,
                    'total_rows': 0,
                    'sample_available': (self.processed_dir / f"{base_name}_sample.csv").exists()
                }
            
            # Count rows in this chunk
            try:
                df = pd.read_csv(chunk_file)
                info[base_name]['chunks'] += 1
                info[base_name]['total_rows'] += len(df)
            except Exception as e:
                logger.warning(f"Could not read chunk {chunk_file}: {e}")
        
        return info
    
    def load_for_ml(self, dataset_name: str, sample_size: Optional[int] = None, 
                    random_state: int = 42) -> pd.DataFrame:
        """
        Load dataset optimized for ML with optional sampling
        
        Args:
            dataset_name: Name of the dataset to load
            sample_size: If provided, randomly sample this many rows
            random_state: Random seed for reproducible sampling
        """
        # First try to load sample if sample_size is small
        if sample_size and sample_size <= 10000:
            sample_df = self.load_sample(dataset_name)
            if len(sample_df) >= sample_size:
                return sample_df.sample(n=sample_size, random_state=random_state)
        
        # Load full dataset or required number of chunks
        if sample_size:
            # Estimate chunks needed (assuming ~100k rows per chunk)
            estimated_chunks = max(1, (sample_size // 100000) + 1)
            df = self.load_chunks(dataset_name, max_chunks=estimated_chunks)
            
            if len(df) > sample_size:
                df = df.sample(n=sample_size, random_state=random_state)
        else:
            df = self.load_chunks(dataset_name)
        
        return df
    
    def create_merged_dataset(self, datasets: List[str], join_column: str, 
                            max_chunks_per_dataset: Optional[int] = None) -> pd.DataFrame:
        """
        Create a merged dataset from multiple datasets
        
        Args:
            datasets: List of dataset names to merge
            join_column: Column to join on (e.g., 'tconst')
            max_chunks_per_dataset: Limit chunks per dataset for memory management
        """
        if len(datasets) < 2:
            raise ValueError("Need at least 2 datasets to merge")
        
        # Load first dataset
        merged_df = self.load_chunks(datasets[0], max_chunks_per_dataset)
        logger.info(f"Base dataset {datasets[0]}: {len(merged_df)} rows")
        
        # Merge additional datasets
        for dataset_name in datasets[1:]:
            df = self.load_chunks(dataset_name, max_chunks_per_dataset)
            
            if join_column not in merged_df.columns or join_column not in df.columns:
                logger.warning(f"Join column '{join_column}' not found in {dataset_name}")
                continue
            
            logger.info(f"Merging {dataset_name}: {len(df)} rows")
            merged_df = pd.merge(merged_df, df, on=join_column, how='inner')
            logger.info(f"After merge: {len(merged_df)} rows")
        
        return merged_df

# Convenience functions for common datasets
def load_ratings(max_chunks: Optional[int] = None) -> pd.DataFrame:
    """Load title ratings dataset"""
    loader = IMDBDataLoader()
    return loader.load_chunks('title.ratings', max_chunks)

def load_basics(max_chunks: Optional[int] = None) -> pd.DataFrame:
    """Load title basics dataset"""
    loader = IMDBDataLoader()
    return loader.load_chunks('title.basics', max_chunks)

def load_names(max_chunks: Optional[int] = None) -> pd.DataFrame:
    """Load name basics dataset"""
    loader = IMDBDataLoader()
    return loader.load_chunks('name.basics', max_chunks)

def create_ml_dataset(sample_size: Optional[int] = None, random_state: int = 42) -> pd.DataFrame:
    """
    Create a ready-to-use ML dataset by merging ratings and basics
    
    Args:
        sample_size: If provided, sample this many rows
        random_state: Random seed for reproducible results
    """
    loader = IMDBDataLoader()
    
    # Load datasets with appropriate chunk limits for memory management
    max_chunks = 5 if sample_size and sample_size <= 500000 else None
    
    ratings_df = loader.load_chunks('title.ratings', max_chunks)
    basics_df = loader.load_chunks('title.basics', max_chunks)
    
    # Merge on tconst
    merged_df = pd.merge(ratings_df, basics_df, on='tconst', how='inner')
    
    # Clean data for ML
    merged_df = merged_df.replace({'\\N': pd.NA, '': pd.NA, ' ': pd.NA})
    
    # Select useful columns for ML
    ml_columns = ['averageRating', 'numVotes', 'startYear', 'runtimeMinutes', 'titleType', 'genres']
    available_columns = [col for col in ml_columns if col in merged_df.columns]
    merged_df = merged_df[['tconst'] + available_columns]
    
    # Remove rows with missing critical data
    merged_df = merged_df.dropna(subset=['averageRating', 'numVotes'])
    
    if sample_size and len(merged_df) > sample_size:
        merged_df = merged_df.sample(n=sample_size, random_state=random_state)
    
    logger.info(f"Created ML dataset with {len(merged_df)} rows and {len(merged_df.columns)} columns")
    
    return merged_df


if __name__ == "__main__":
    loader = IMDBDataLoader()
    
    # Show available datasets
    datasets = loader.get_available_datasets()
    print("Available datasets:")
    for dataset in datasets:
        print(f"  - {dataset}")
    
    print("\nDataset Information:")
    print("-" * 50)
    info = loader.get_dataset_info()
    for dataset, details in info.items():
        print(f"{dataset}:")
        print(f"  Chunks: {details['chunks']}")
        print(f"  Total rows: {details['total_rows']:,}")
        print(f"  Sample available: {details['sample_available']}")
        print()
    
    # Create a small ML dataset
    print("Creating sample ML dataset...")
    ml_df = create_ml_dataset(sample_size=10000)
    print(f"ML dataset shape: {ml_df.shape}")
    print(f"ML dataset columns: {list(ml_df.columns)}")