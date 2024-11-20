import pandas as pd
import geopy.distance
import json
from geopy.geocoders import Nominatim

# Load hospital data
hospitalPath = r'data/hospitalData.csv'
hospitalDF = pd.read_csv(hospitalPath)

# Load patient data
patientPath = r'data/individual_form.json'
with open(patientPath, 'r') as file:
    patientData = json.load(file)


# Extract patient's coordinates from their address
def getPatientCoords(patient):
    try:
        address = f"{patient['Address']}, {patient['City']}, {patient['State']}"
        geolocator = Nominatim(user_agent="hospital_recommender")
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError(f"Could not geocode the address: {address}")
    except Exception as e:
        print(f"Error geocoding patient address: {e}")
        return None

# Calculate the distance between two geocoordinates
def calculateDis(pCoords, hCoords):
    return geopy.distance.distance(pCoords, hCoords).miles

# Update hospital data with the calculated distance from the patient's address
def updateData(hospital_df, patient_coords):
    if patient_coords is None:
        return hospital_df  
    hospital_df['Distance'] = hospital_df.apply(
        lambda row: calculateDis(
            patient_coords, (row['LATITUDE'], row['LONGITUDE'])), axis=1)
    return hospital_df

# Function to get the hospital recommendation for a specific patient
def recommendedHospitals(patient, hospital_df, max_distance):
    preferred_type = patient.get('Type of Care')
    insurance = patient.get('Insurance Provider') 
    name = patient.get('First Name')
    #Display patient preferences
    print(f"{name}'s Preferences: Type - {preferred_type}, Insurance - {insurance}")
    
    # Normalize inputs for consistency
    if preferred_type:
        preferred_type = preferred_type.lower()
        print(f"{name} prefers: {preferred_type} hospital")
    
    if insurance:
        insurance = insurance.lower()
        print(f"{name} has insurance provider: {insurance}")
    
    patient_coords = getPatientCoords(patient)
    hospital_df = updateData(hospital_df, patient_coords)
    
    if patient_coords is None:
        print("Error: Could not get coordinates for patient. Please check their address.")
        return None
    
    # Filter hospitals that are within the specified distance
    print(f"Total hospitals: {len(hospital_df)}")
    newH_DF = hospital_df[hospital_df['Distance'] <= max_distance]
    print(f"Hospitals within {max_distance} miles: {len(newH_DF)}")
    
    # Filter by preferred type
    if preferred_type:
        newH_DF = newH_DF.copy()
        newH_DF['TYPE_normalized'] = newH_DF['TYPE'].str.lower()
        newH_DF = newH_DF[newH_DF['TYPE_normalized'].str.contains(preferred_type, na=False)]
        print(f"Hospitals after type filter: {len(newH_DF)}")
    
    # Filter by insurance
    if insurance:
        newH_DF = newH_DF.copy()
        newH_DF['INSURANCE_normalized'] = newH_DF['INSURANCE'].str.lower()
        newH_DF = newH_DF[
            newH_DF['INSURANCE_normalized'].apply(lambda x: insurance in x if isinstance(x, str) else False)
        ]
        print(f"Hospitals after insurance filter: {len(newH_DF)}")
    
    # Check if any hospitals match after filtering
    if newH_DF.empty:
        print(f"No hospitals found within {max_distance} miles that match the preferred type or insurance.")
        return None
    
    # Display hospital details
    print(f"\nRecommended Hospital(s) and their details within {max_distance} miles:")
    print(newH_DF[['NAME', 'TYPE', 'COUNTY', 'INSURANCE', 'Distance']])
    
    recommended_hospitals = newH_DF['NAME'].tolist()
    return recommended_hospitals


