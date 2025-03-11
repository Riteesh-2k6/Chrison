# Chiron Healthcare Assistant

A comprehensive healthcare assistant application that helps users find medical facilities, check symptoms, manage medications, and analyze drug interactions.

## Features

### 1. Hospital Locator 
- Find nearby hospitals and pharmacies based on your location
- View detailed information including:
  - Distance from your location
  - Contact information
  - Emergency services availability
  - Opening hours
  - Wheelchair accessibility
  - Directions via Google Maps
  - Website links (where available)

### 2. Symptom Checker 
- Input your symptoms
- Get potential diagnoses
- Receive recommendations for next steps
- AI-powered analysis using advanced medical knowledge

### 3. Drug Interaction Checker 
- Check interactions between multiple medications
- View severity levels and potential risks
- Get recommendations for medication timing
- Access both database and AI-powered analysis

### 4. Personalized Medication Management 
- Track your medications
- Get personalized dosage reminders
- View medication safety information
- Manage your medication schedule

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Chiron2.git
cd Chiron2
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
GROQ_API_KEY=your_groq_api_key
```

## Dependencies
- Flask >= 2.0.1: Web framework
- Groq >= 0.18.0: AI model integration
- Geopy >= 2.3.0: Geocoding and distance calculations
- Overpy >= 0.6: OpenStreetMap data access
- Folium >= 0.12.1: Interactive maps
- Additional dependencies listed in `requirements.txt`

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Use the navigation menu to access different features:
   - Hospital Locator: Find nearby medical facilities
   - Symptom Checker: Check your symptoms
   - Drug Interaction: Check medication interactions
   - Personalized Medication: Manage your medications

## Features in Detail

### Hospital Locator
- Enter your location and desired search radius
- View hospitals and pharmacies on an interactive map
- Click markers for detailed facility information
- Get directions to any facility
- Filter by facility type (hospital/pharmacy)

### Symptom Checker
- Enter your symptoms using natural language
- Get AI-powered analysis of potential conditions
- Receive recommendations for medical attention
- View severity levels and urgency

### Drug Interaction
- Enter two or more medications
- View potential interactions from medical database
- Get AI-enhanced analysis of interactions
- See recommendations for safe medication use

### Personalized Medication
- Add your current medications
- Set up dosage schedules
- Receive safety alerts
- Track medication history

## Security and Privacy

- No personal medical data is stored permanently
- All API communications are encrypted
- User location data is used only for immediate searches
- No tracking or analytics implemented

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenStreetMap for medical facility data
- Groq for AI capabilities
- Flask community for web framework
- All contributors and users
