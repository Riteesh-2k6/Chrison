from flask import Flask, render_template, request, jsonify
from symptom_checker import get_disease_from_symptoms
from DrugInteraction import DrugInteractionChecker, get_ai_drug_interaction
from Personalised_Medication import get_personalized_medication, check_medication_safety
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import overpy
import html

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symptom-checker', methods=['GET', 'POST'])
def symptom_checker():
    if request.method == 'POST':
        symptoms = request.json.get('symptoms')
        if symptoms:
            result = get_disease_from_symptoms(symptoms)
            return jsonify({'result': result})
    return render_template('symptom_checker.html')

@app.route('/drug-interaction', methods=['GET', 'POST'])
def drug_interaction():
    if request.method == 'POST':
        try:
            drug1 = request.json.get('drug1')
            drug2 = request.json.get('drug2')
            
            if not drug1 or not drug2:
                return jsonify({
                    'error': 'Both drug names are required'
                }), 400
                
            # Initialize checker and get database results
            checker = DrugInteractionChecker()
            db_result = checker.check_interaction(drug1, drug2)
            
            # Get AI analysis from the standalone function
            ai_result = get_ai_drug_interaction(drug1, drug2)
            
            return jsonify({
                'database_result': db_result,
                'ai_result': ai_result
            })
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            print(f"Error in drug interaction check: {str(e)}")
            return jsonify({'error': 'An error occurred while checking drug interactions'}), 500
            
    return render_template('drug_interaction.html')

@app.route('/personalized-medication', methods=['GET', 'POST'])
def personalized_medication():
    if request.method == 'POST':
        data = request.json
        condition = data.get('condition')
        allergies = data.get('allergies', [])
        current_meds = data.get('current_medications', [])
        
        if condition:
            recommendations = get_personalized_medication(condition, allergies, current_meds)
            if current_meds:
                interactions = check_medication_safety(
                    [med.strip() for med in recommendations.lower().split() if med.strip()],
                    current_meds
                )
            else:
                interactions = {}
                
            return jsonify({
                'recommendations': recommendations,
                'interactions': interactions
            })
    return render_template('personalized_medication.html')

@app.route('/hospital-locator')
def hospital_locator():
    return render_template('hospital_locator.html')

@app.route('/hospital-locator', methods=['POST'])
def find_hospitals():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'})
        
        print(f"Received request data: {data}")
        
        address = data.get('address')
        if not address:
            return jsonify({'error': 'Please provide an address'})
            
        radius = int(data.get('radius', 5000))
        if radius < 1000 or radius > 10000:
            radius = 5000

        print(f"Searching for: {address} with radius {radius}m")

        try:
            # Initialize geocoder with a longer timeout and user agent
            geolocator = Nominatim(
                user_agent="chiron_healthcare_assistant",
                timeout=10
            )
            
            # Get user's location with more specific parameters
            location = geolocator.geocode(
                address,
                exactly_one=True,
                language="en",
                country_codes="in"  # Limit to India
            )
            
            if not location:
                return jsonify({'error': 'Could not find the specified location. Please try a more specific address in India.'})
            
            print(f"Found location: {location.address} at {location.latitude}, {location.longitude}")
            
            user_location = (location.latitude, location.longitude)
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            return jsonify({'error': 'Failed to find the location. Please try a more specific address.'})
        
        try:
            # Get medical facilities using a simpler query
            api = overpy.Overpass()
            
            # Split the query into two parts to avoid timeout
            # First query: Hospitals
            hospital_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="hospital"](around:{radius},{user_location[0]},{user_location[1]});
              way["amenity"="hospital"](around:{radius},{user_location[0]},{user_location[1]});
            );
            out body;
            >;
            out skel qt;
            """
            
            # Second query: Pharmacies
            pharmacy_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="pharmacy"](around:{radius},{user_location[0]},{user_location[1]});
              way["amenity"="pharmacy"](around:{radius},{user_location[0]},{user_location[1]});
            );
            out body;
            >;
            out skel qt;
            """
            
            print("Querying hospitals...")
            hospital_result = api.query(hospital_query)
            print(f"Found {len(hospital_result.nodes)} hospital nodes and {len(hospital_result.ways)} hospital ways")
            
            print("Querying pharmacies...")
            pharmacy_result = api.query(pharmacy_query)
            print(f"Found {len(pharmacy_result.nodes)} pharmacy nodes and {len(pharmacy_result.ways)} pharmacy ways")
            
            facilities = []
            hospitals_count = 0
            pharmacies_count = 0
            
            # Process hospital nodes
            for node in hospital_result.nodes:
                name = node.tags.get('name', 'Hospital')
                facility_coords = (node.lat, node.lon)
                distance = round(geodesic(user_location, facility_coords).kilometers, 2)
                
                details = {
                    'phone': node.tags.get('phone', 'Not available'),
                    'emergency': node.tags.get('emergency', 'Unknown'),
                    'healthcare': node.tags.get('healthcare', 'General'),
                    'opening_hours': node.tags.get('opening_hours', 'Not specified'),
                    'website': node.tags.get('website', ''),
                    'wheelchair': node.tags.get('wheelchair', 'Unknown'),
                    'address': node.tags.get('addr:full', node.tags.get('addr:street', 'Address not available'))
                }
                
                facility = {
                    'type': 'hospital',
                    'name': html.escape(name),
                    'lat': float(node.lat),
                    'lon': float(node.lon),
                    'distance': distance,
                    'details': details,
                    'directions_url': f"https://www.google.com/maps/dir/?api=1&origin={user_location[0]},{user_location[1]}&destination={node.lat},{node.lon}&travelmode=driving"
                }
                facilities.append(facility)
                hospitals_count += 1
            
            # Process pharmacy nodes
            for node in pharmacy_result.nodes:
                name = node.tags.get('name', 'Pharmacy')
                facility_coords = (node.lat, node.lon)
                distance = round(geodesic(user_location, facility_coords).kilometers, 2)
                
                details = {
                    'phone': node.tags.get('phone', 'Not available'),
                    'opening_hours': node.tags.get('opening_hours', 'Not specified'),
                    'website': node.tags.get('website', ''),
                    'wheelchair': node.tags.get('wheelchair', 'Unknown'),
                    'address': node.tags.get('addr:full', node.tags.get('addr:street', 'Address not available'))
                }
                
                facility = {
                    'type': 'pharmacy',
                    'name': html.escape(name),
                    'lat': float(node.lat),
                    'lon': float(node.lon),
                    'distance': distance,
                    'details': details,
                    'directions_url': f"https://www.google.com/maps/dir/?api=1&origin={user_location[0]},{user_location[1]}&destination={node.lat},{node.lon}&travelmode=driving"
                }
                facilities.append(facility)
                pharmacies_count += 1
            
            # Sort facilities by distance
            facilities.sort(key=lambda x: x['distance'])
            
            response_data = {
                'user_location': {
                    'lat': float(user_location[0]),
                    'lon': float(user_location[1]),
                    'address': location.address
                },
                'facilities': facilities,
                'stats': {
                    'hospitals': hospitals_count,
                    'pharmacies': pharmacies_count
                }
            }
            
            print(f"Found {hospitals_count} hospitals and {pharmacies_count} pharmacies")
            return jsonify(response_data)
            
        except overpy.exception.OverpassTooManyRequests:
            print("Overpass API rate limit exceeded")
            return jsonify({'error': 'Too many requests. Please try again later.'})
        except overpy.exception.OverpassGatewayTimeout:
            print("Overpass API timeout")
            return jsonify({'error': 'The search took too long. Please try with a smaller radius.'})
        except Exception as e:
            print(f"Overpass API error: {str(e)}")
            return jsonify({'error': 'Failed to fetch medical facilities. Please try again.'})
            
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({'error': f'Invalid input: {str(e)}'})
    except Exception as e:
        print(f"Error in find_hospitals: {str(e)}")
        return jsonify({'error': 'An error occurred while searching for medical facilities. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)
