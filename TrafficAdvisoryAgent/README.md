# AI Traffic Advisory Agent

Real-time traffic advisory system with intelligent route recommendations for New York City. Built with Streamlit, featuring interactive maps, congestion prediction, and environmental impact analysis.

## Features

- **25 NYC Locations** - Comprehensive coverage including Manhattan, Brooklyn, Queens, and major airports
- **Interactive Map** - Street-level route visualization with OpenStreetMap integration
- **Real-time Insights** - Traffic patterns, congestion analysis, and sustainability metrics
- **Priority-based Routing** - 4 traffic levels × 3 priority categories (Time, Cost, Environment)
- **Time-based Analysis** - Select any time to see predicted traffic conditions
- **Environmental Impact** - CO₂ emission calculations and fuel consumption estimates

## Quick Start

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/TrafficAdvisoryAgent.git
cd TrafficAdvisoryAgent
pip install -r requirements.txt

```
Run the application:
```bash
streamlit run traffic_app_optimized.py
```

The app will open at http://localhost:8501

Requirements
Python 3.8+
Streamlit 1.28+
Plotly 5.17+
Pandas 2.0+
NumPy 1.24+
Full dependencies in requirements.txt

How to Use
Select locations - Choose from 25 NYC locations (Times Square, Central Park, JFK Airport, etc.)
Choose priority - Pick time efficiency, cost savings, or environmental impact
Set traffic level - Select expected congestion (Low, Medium, High, Critical)
Pick time - Choose when you plan to travel
Get recommendations - View optimized routes with detailed insights

```bash
TrafficAdvisoryAgent/
├── traffic_app_optimized.py  # Main Streamlit application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker containerization
├── deploy.sh                  # IBM Cloud deployment script
├── manifest.yml               # Cloud Foundry config
├── IBM_CLOUD_DEPLOYMENT.md    # Deployment guide
├── PROJECT_PROMPT.md          # Technical documentation
└── data/                      # Data storage
```

#Key Technologies
- Frontend: Streamlit with custom CSS styling
- Maps: Plotly scatter_mapbox with OpenStreetMap tiles
- Data Processing: Pandas, NumPy for optimized performance
- Deployment: Docker, IBM Cloud Code Engine ready

#Performance
- Load Time: 2-3 seconds
- Dataset: 128 optimized traffic records
- Map: 800px height, 20-waypoint routing
- Caching: Singleton pattern for performance optimization
