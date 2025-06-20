"""
Focused Data Collection Configuration for Economic Shock Resilience Analysis
Focus: 1990-2023, High-Quality Countries
"""

from typing import Dict, List
from pathlib import Path

# =============================================================================
# ANALYSIS PARAMETERS - FOCUSED APPROACH
# =============================================================================

# Focused time period for better data quality
START_YEAR = 1990
END_YEAR = 2023
ANALYSIS_YEARS = END_YEAR - START_YEAR + 1

# =============================================================================
# HIGH-QUALITY COUNTRY SELECTION (30-40 countries)
# =============================================================================

# OECD countries with excellent data coverage
OECD_CORE = [
    'USA', 'GBR', 'FRA', 'DEU', 'JPN', 'CAN', 'AUS', 'ITA', 'ESP', 'NLD',
    'BEL', 'CHE', 'SWE', 'NOR', 'DNK', 'FIN', 'AUT', 'IRL', 'NZL', 'PRT'
]

# Major emerging markets with good data availability
EMERGING_MAJOR = [
    'CHN', 'IND', 'BRA', 'RUS', 'MEX', 'IDN', 'TUR', 'KOR', 'THA', 'MYS',
    'PHL', 'ZAF', 'POL', 'CZE', 'HUN', 'CHL', 'COL', 'ARG'
]

# Combined focus countries (38 total)
FOCUS_COUNTRIES = OECD_CORE + EMERGING_MAJOR

# Country groupings for analysis
COUNTRY_GROUPS = {
    'developed_oecd': OECD_CORE,
    'emerging_markets': EMERGING_MAJOR,
    'high_income': ['USA', 'GBR', 'FRA', 'DEU', 'JPN', 'CAN', 'AUS', 'CHE', 'SWE', 'NOR'],
    'upper_middle': ['CHN', 'BRA', 'RUS', 'MEX', 'TUR', 'THA', 'MYS', 'POL', 'ARG'],
    'asian_tigers': ['KOR', 'THA', 'MYS', 'PHL'],
    'european_emerging': ['POL', 'CZE', 'HUN'],
    'latin_america': ['BRA', 'MEX', 'CHL', 'COL', 'ARG']
}

# =============================================================================
# FOCUSED SHOCK PERIODS (Major shocks with good coverage)
# =============================================================================

MAJOR_SHOCKS = {
    'asian_financial_crisis_1997': {
        'start': 1997, 
        'end': 1999, 
        'type': 'financial',
        'severity': 'high',
        'regional_focus': ['THA', 'MYS', 'PHL', 'IDN', 'KOR'],
        'global_impact': True,
        'description': 'Asian financial crisis - currency and banking collapse'
    },
    'dotcom_recession_2001': {
        'start': 2001,
        'end': 2002,
        'type': 'financial',
        'severity': 'medium',
        'regional_focus': ['USA', 'GBR', 'DEU', 'JPN'],
        'global_impact': True,
        'description': 'Dot-com bubble burst and recession'
    },
    'global_financial_crisis_2008': {
        'start': 2008, 
        'end': 2010, 
        'type': 'financial',
        'severity': 'very_high',
        'regional_focus': ['USA', 'GBR', 'ESP', 'IRL', 'GRC'],
        'global_impact': True,
        'description': 'Global financial crisis - subprime and banking collapse'
    },
    'european_debt_crisis_2010': {
        'start': 2010,
        'end': 2013,
        'type': 'sovereign_debt',
        'severity': 'high',
        'regional_focus': ['ESP', 'ITA', 'PRT', 'IRL', 'GRC'],
        'global_impact': False,
        'description': 'European sovereign debt crisis'
    },
    'covid_pandemic_2020': {
        'start': 2020, 
        'end': 2022, 
        'type': 'health_economic',
        'severity': 'very_high',
        'regional_focus': [],  # Global
        'global_impact': True,
        'description': 'COVID-19 pandemic economic shock'
    }
}

# =============================================================================
# ENHANCED WORLD BANK INDICATORS
# =============================================================================

# Core economic fundamentals
CORE_ECONOMIC_INDICATORS = {
    'NY.GDP.PCAP.KD': 'gdp_per_capita_constant',
    'NY.GDP.MKTP.KD.ZG': 'gdp_growth_annual',
    'NY.GDP.PCAP.KD.ZG': 'gdp_per_capita_growth',
    'NY.GDP.MKTP.PP.KD': 'gdp_ppp_constant',
}

# Investment and savings
INVESTMENT_INDICATORS = {
    'NE.GDI.TOTL.ZS': 'gross_investment_gdp',
    'NY.GNS.ICTR.ZS': 'gross_savings_gdp',
    'NE.GDI.FPRV.ZS': 'private_investment_gdp',
    'BX.KLT.DINV.WD.GD.ZS': 'fdi_net_inflows_gdp',
}

# Trade and openness
TRADE_INDICATORS = {
    'NE.TRD.GNFS.ZS': 'trade_gdp',
    'NE.EXP.GNFS.ZS': 'exports_gdp',
    'NE.IMP.GNFS.ZS': 'imports_gdp',
    'TM.TAX.MRCH.WM.AR.ZS': 'tariff_rate_applied_weighted',
}

# Financial development
FINANCIAL_INDICATORS = {
    'FS.AST.DOMS.GD.ZS': 'domestic_credit_private_gdp',
    'FB.BNK.CAPA.ZS': 'bank_capital_assets_ratio',
    'CM.MKT.LCAP.GD.ZS': 'market_cap_gdp',
    'FR.INR.RINR': 'real_interest_rate',
}

# Government and institutions
GOVERNMENT_INDICATORS = {
    'GC.DOD.TOTL.GD.ZS': 'government_debt_gdp',
    'GC.TAX.TOTL.GD.ZS': 'tax_revenue_gdp',
    'GC.XPN.TOTL.GD.ZS': 'government_expenditure_gdp',
}

# Labor and human capital
LABOR_INDICATORS = {
    'SL.UEM.TOTL.ZS': 'unemployment_total',
    'SE.TER.ENRR': 'tertiary_education_enrollment',
    'SP.POP.GROW': 'population_growth',
    'SP.URB.TOTL.IN.ZS': 'urban_population_pct',
}

# Innovation and technology
INNOVATION_INDICATORS = {
    'GB.XPD.RSDV.GD.ZS': 'research_development_gdp',
    'IP.PAT.RESD': 'patent_applications_residents',
    'IT.NET.USER.ZS': 'internet_users_pct',
}

# Combine all indicators
WORLD_BANK_INDICATORS = {
    **CORE_ECONOMIC_INDICATORS,
    **INVESTMENT_INDICATORS,
    **TRADE_INDICATORS,
    **FINANCIAL_INDICATORS,
    **GOVERNMENT_INDICATORS,
    **LABOR_INDICATORS,
    **INNOVATION_INDICATORS
}

# =============================================================================
# DATA QUALITY REQUIREMENTS - MORE STRINGENT
# =============================================================================

MIN_DATA_COVERAGE = 0.8  # Increased from 0.7
MIN_SHOCK_COVERAGE = 4   # Must have data for at least 4 shocks
MIN_YEARS = 25           # Reduced since we're focusing on 1990-2023
MIN_COUNTRIES = 30       # Minimum viable countries for analysis

# =============================================================================
# OUTPUT CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path("data")
LOGS_DIR = Path("logs")
FIGURES_DIR = Path("figures")
REPORTS_DIR = Path("reports")

# Create directories
for directory in [OUTPUT_DIR, LOGS_DIR, FIGURES_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)
