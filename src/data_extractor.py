#!/usr/bin/env python3
"""
IMDB Data Extractor

Extracts and processes large IMDB TSV.GZ files into manageable chunks for ML purposes.
Handles decompression, chunking, and data cleaning.
"""

import gzip
import pandas as pd
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IMDBDataExtractor:
    def __init__(self, raw_data_dir='data/raw', processed_data_dir='data/processed', chunks_dir='data/chunks'):
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.chunks_dir = Path(chunks_dir)
        
        # Create directories if they don't exist
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_tsv_gz(self, filename, chunk_size=100000):
        """
        Extract and process a TSV.GZ file into manageable chunks
        
        Args:
            filename (str): Name of the .tsv.gz file (without path)
            chunk_size (int): Number of rows per chunk
        """
        input_path = self.raw_data_dir / filename
        base_name = filename.replace('.tsv.gz', '')
        
        logger.info(f"Processing {filename}...")
        
        try:
            with gzip.open(input_path, 'rt', encoding='utf-8') as f:
                # Read in chunks to manage memory
                chunk_num = 0
                
                for chunk_df in pd.read_csv(f, sep='\t', chunksize=chunk_size, low_memory=False):
                    # Clean the chunk
                    cleaned_chunk = self._clean_chunk(chunk_df)
                    
                    # Save chunk
                    chunk_filename = f"{base_name}_chunk_{chunk_num:03d}.csv"
                    chunk_path = self.chunks_dir / chunk_filename
                    cleaned_chunk.to_csv(chunk_path, index=False)
                    
                    logger.info(f"Saved chunk {chunk_num}: {len(cleaned_chunk)} rows -> {chunk_filename}")
                    chunk_num += 1
                
                # Also save a sample for quick analysis
                self._create_sample(base_name, sample_size=10000)
                
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            raise
    
    def _clean_chunk(self, df):
        """Clean a data chunk by handling null values and data types"""
        # Replace IMDB null indicators with actual NaN
        df = df.replace({'\\N': pd.NA, '': pd.NA, ' ': pd.NA})
        
        # Drop rows where all values are null
        df = df.dropna(how='all')
        
        return df
    
    def _create_sample(self, base_name, sample_size=10000):
        """Create a small sample file for quick analysis"""
        chunk_files = list(self.chunks_dir.glob(f"{base_name}_chunk_*.csv"))
        
        if not chunk_files:
            return
        
        # Read first chunk and take sample
        first_chunk = pd.read_csv(chunk_files[0])
        sample_df = first_chunk.head(sample_size)
        
        sample_path = self.processed_data_dir / f"{base_name}_sample.csv"
        sample_df.to_csv(sample_path, index=False)
        logger.info(f"Created sample file: {sample_path}")
    
    def process_all_files(self, chunk_size=100000):
        """Process all TSV.GZ files in the raw data directory"""
        tsv_files = list(self.raw_data_dir.glob('*.tsv.gz'))
        
        if not tsv_files:
            logger.warning("No .tsv.gz files found in raw data directory")
            return
        
        logger.info(f"Found {len(tsv_files)} files to process")
        
        for file_path in tsv_files:
            self.extract_tsv_gz(file_path.name, chunk_size)
    
    def load_dataset(self, dataset_name, max_chunks=None):
        """
        Load a dataset from chunks
        
        Args:
            dataset_name (str): Base name of dataset (e.g., 'title.ratings')
            max_chunks (int): Maximum number of chunks to load (None for all)
        
        Returns:
            pandas.DataFrame: Combined dataset
        """
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
    
    def get_dataset_info(self):
        """Get information about available datasets and their chunks"""
        info = {}
        
        for chunk_file in self.chunks_dir.glob('*_chunk_*.csv'):
            base_name = chunk_file.name.split('_chunk_')[0]
            
            if base_name not in info:
                info[base_name] = {
                    'chunks': 0,
                    'total_rows': 0,
                    'sample_available': (self.processed_data_dir / f"{base_name}_sample.csv").exists()
                }
            
            # Count rows in this chunk
            df = pd.read_csv(chunk_file)
            info[base_name]['chunks'] += 1
            info[base_name]['total_rows'] += len(df)
        
        return info


if __name__ == "__main__":
    extractor = IMDBDataExtractor()
    
    # Process all files
    extractor.process_all_files(chunk_size=100000)
    
    # Show dataset info
    info = extractor.get_dataset_info()
    print("\nDataset Information:")
    print("-" * 50)
    for dataset, details in info.items():
        print(f"{dataset}:")
        print(f"  Chunks: {details['chunks']}")
        print(f"  Total rows: {details['total_rows']:,}")
        print(f"  Sample available: {details['sample_available']}")
        print()