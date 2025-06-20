"""
Focused Economic Data Collection Module
Target: 30-40 high-quality countries, 1990-2023, rich indicators
"""

import pandas as pd
import numpy as np
import requests
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import our configuration
from config.data_collection_config import *

# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Setup comprehensive logging for data collection.
    
    Parameters:
    -----------
    log_level : str
        Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
    --------
    logging.Logger : Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('data_collection')
    logger.setLevel(getattr(logging, log_level))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler with detailed formatting
    log_file = LOGS_DIR / f'data_collection_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler with simple formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized - Level: {log_level}, Log file: {log_file}")
    return logger

# Initialize logger
logger = setup_logging()

# =============================================================================
# DATA VALIDATION UTILITIES
# =============================================================================

def validate_country_selection(country_list: List[str]) -> Dict[str, bool]:
    """
    Validate that selected countries are available in our focus list.
    
    Parameters:
    -----------
    country_list : List[str]
        List of country codes to validate
        
    Returns:
    --------
    Dict[str, bool] : Validation results for each country
    """
    validation_results = {}
    
    for country in country_list:
        is_valid = (
            isinstance(country, str) and
            len(country) == 3 and
            country.isupper() and
            country in FOCUS_COUNTRIES
        )
        validation_results[country] = is_valid
        
        if not is_valid:
            logger.warning(f"Country {country} not in focus list or invalid format")
    
    valid_countries = [k for k, v in validation_results.items() if v]
    logger.info(f"Validated {len(valid_countries)}/{len(country_list)} countries")
    
    return validation_results

def calculate_data_quality_score(df: pd.DataFrame, country_col: str = 'country_code') -> pd.DataFrame:
    """
    Calculate comprehensive data quality scores for countries.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with country-year data
    country_col : str
        Name of country identifier column
        
    Returns:
    --------
    pd.DataFrame : Data quality metrics by country
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    quality_metrics = []
    
    for country in df[country_col].unique():
        country_data = df[df[country_col] == country]
        
        # Basic coverage metrics
        total_years = len(country_data)
        expected_years = END_YEAR - START_YEAR + 1
        year_coverage = total_years / expected_years
        
        # Data completeness across indicators
        completeness_by_indicator = {}
        overall_completeness = 0
        
        if len(numeric_cols) > 0:
            completeness_by_indicator = (
                country_data[numeric_cols].notna().mean().to_dict()
            )
            overall_completeness = np.mean(list(completeness_by_indicator.values()))
        
        # Shock period coverage
        shock_coverage = 0
        for shock_name, shock_info in MAJOR_SHOCKS.items():
            shock_years = range(shock_info['start'], shock_info['end'] + 1)
            shock_data = country_data[country_data['year'].isin(shock_years)]
            if len(shock_data) > 0:
                shock_coverage += 1
        
        shock_coverage_rate = shock_coverage / len(MAJOR_SHOCKS)
        
        # Overall quality score (weighted average)
        quality_score = (
            0.3 * year_coverage +
            0.5 * overall_completeness +
            0.2 * shock_coverage_rate
        )
        
        quality_metrics.append({
            'country_code': country,
            'total_years': total_years,
            'year_coverage': year_coverage,
            'overall_completeness': overall_completeness,
            'shock_coverage': shock_coverage,
            'shock_coverage_rate': shock_coverage_rate,
            'quality_score': quality_score,
            'meets_criteria': (
                year_coverage >= 0.8 and
                overall_completeness >= 0.6 and
                shock_coverage >= 3
            )
        })
    
    quality_df = pd.DataFrame(quality_metrics).sort_values('quality_score', ascending=False)
    
    logger.info(f"Quality assessment complete:")
    logger.info(f"  - Countries meeting criteria: {quality_df['meets_criteria'].sum()}")
    logger.info(f"  - Average quality score: {quality_df['quality_score'].mean():.3f}")
    logger.info(f"  - Top 5 countries: {quality_df.head()['country_code'].tolist()}")
    
    return quality_df

# =============================================================================
# ENHANCED DATA COLLECTION FUNCTIONS
# =============================================================================

def collect_focused_maddison_data() -> pd.DataFrame:
    """
    Collect Maddison data with focus on our target countries and time period.
    
    Returns:
    --------
    pd.DataFrame : Processed Maddison dataset
    """
    logger.info("🌍 Starting focused Maddison data collection")
    logger.info(f"Target period: {START_YEAR}-{END_YEAR}")
    logger.info(f"Target countries: {len(FOCUS_COUNTRIES)}")
    
    try:
        # Download from Maddison Project
        maddison_url = "https://dataverse.nl/api/access/datafile/421302"
        logger.info(f"Downloading from: {maddison_url}")
        
        maddison_df = pd.read_excel(maddison_url, sheet_name='Full data')
        logger.info(f"Raw Maddison data shape: {maddison_df.shape}")
        
        # Standardize column names
        column_mapping = {
            'countrycode': 'country_code',
            'country': 'country_name',
            'year': 'year',
            'gdppc': 'gdp_per_capita',
            'pop': 'population'
        }
        
        maddison_df.columns = [column_mapping.get(col.lower(), col.lower()) for col in maddison_df.columns]
        
        # Filter to our focus
        maddison_filtered = maddison_df[
            (maddison_df['year'] >= START_YEAR) & 
            (maddison_df['year'] <= END_YEAR) &
            (maddison_df['country_code'].isin(FOCUS_COUNTRIES))
        ].copy()
        
        logger.info(f"Filtered Maddison data shape: {maddison_filtered.shape}")
        logger.info(f"Countries found: {maddison_filtered['country_code'].nunique()}")
        
        # Calculate derived variables
        maddison_filtered['gdp_total'] = (
            maddison_filtered['gdp_per_capita'] * maddison_filtered['population']
        )
        maddison_filtered['log_gdp_per_capita'] = np.log(maddison_filtered['gdp_per_capita'])
        
        # Calculate growth rates
        maddison_filtered = maddison_filtered.sort_values(['country_code', 'year'])
        maddison_filtered['gdp_growth'] = (
            maddison_filtered.groupby('country_code')['gdp_per_capita'].pct_change() * 100
        )
        maddison_filtered['population_growth_maddison'] = (
            maddison_filtered.groupby('country_code')['population'].pct_change() * 100
        )
        
        # Add shock indicators
        maddison_filtered = add_shock_indicators(maddison_filtered)
        
        logger.info("✅ Maddison data collection completed successfully")
        return maddison_filtered
        
    except Exception as e:
        logger.error(f"❌ Error in Maddison data collection: {e}")
        raise

def add_shock_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add comprehensive shock period indicators to dataframe.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with year column
        
    Returns:
    --------
    pd.DataFrame : Dataframe with shock indicators added
    """
    logger.info("🔍 Adding shock period indicators")
    
    df = df.copy()
    
    # Initialize shock columns
    df['is_shock_period'] = False
    df['shock_name'] = ''
    df['shock_type'] = ''
    df['shock_severity'] = ''
    
    for shock_name, shock_info in MAJOR_SHOCKS.items():
        # Mark shock periods
        shock_mask = (df['year'] >= shock_info['start']) & (df['year'] <= shock_info['end'])
        df.loc[shock_mask, 'is_shock_period'] = True
        df.loc[shock_mask, 'shock_name'] = shock_name
        df.loc[shock_mask, 'shock_type'] = shock_info['type']
        df.loc[shock_mask, 'shock_severity'] = shock_info['severity']
        
        # Calculate years since shock end
        post_shock_mask = df['year'] > shock_info['end']
        df.loc[post_shock_mask, f'years_since_{shock_name}'] = (
            df.loc[post_shock_mask, 'year'] - shock_info['end']
        )
        
        # Regional focus indicator
        if shock_info.get('regional_focus'):
            regional_mask = df['country_code'].isin(shock_info['regional_focus'])
            df.loc[shock_mask & regional_mask, 'is_regional_focus'] = True
    
    shock_periods = df['is_shock_period'].sum()
    logger.info(f"Added shock indicators: {shock_periods} country-year shock observations")
    
    return df