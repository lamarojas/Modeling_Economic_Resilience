"""
Test script for focused data collection approach
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from data_collection_focused import *

def test_country_validation():
    """Test country validation function."""
    print("🧪 Testing country validation...")
    
    test_countries = ['USA', 'GBR', 'XXX', 'DEU', 'invalid']
    results = validate_country_selection(test_countries)
    
    print(f"Validation results: {results}")
    valid_count = sum(results.values())
    print(f"Valid countries: {valid_count}/{len(test_countries)}")

def test_maddison_collection():
    """Test focused Maddison data collection."""
    print("\n🧪 Testing Maddison data collection...")
    
    try:
        maddison_data = collect_focused_maddison_data()
        print(f"✅ Success! Shape: {maddison_data.shape}")
        print(f"Countries: {maddison_data['country_code'].nunique()}")
        print(f"Year range: {maddison_data['year'].min()}-{maddison_data['year'].max()}")
        
        # Show data quality
        quality_df = calculate_data_quality_score(maddison_data)
        print(f"\nTop 10 countries by quality:")
        print(quality_df.head(10)[['country_code', 'quality_score', 'meets_criteria']])
        
        return maddison_data
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Running focused data collection tests...")
    
    # Run tests
    test_country_validation()
    maddison_data = test_maddison_collection()
    
    if maddison_data is not None:
        print(f"\n✅ All tests passed! Ready for next phase.")
    else:
        print(f"\n❌ Tests failed. Check logs for details.")