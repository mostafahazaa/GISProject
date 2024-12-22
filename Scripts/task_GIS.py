import arcpy
import re


def print_airports_with_ramp(workspace, feature_class):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = workspace

    fields = ["name", "location", "wikipedia"]

    with arcpy.da.SearchCursor(feature_class, fields) as cursor:
        for airport in cursor:
            airport_name = airport[0]
            location = airport[1]
            wikipedia = airport[2]

            if location.lower() == 'ramp':
                print("Name:", airport_name)
                print("Location:", location)
                print("Wikipedia:", wikipedia)
                print("-" * 50)  # Adding some fun dashes!


def create_shapefiles_for_arabic_cities(positions, countries, output_path):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"E:\projects_4th\GIS"

    # List of Arabic countries
    arabic_countries = ["Algeria", "Bahrain", "Comoros", "Djibouti", "Egypt", "Iraq",
                        "Jordan", "Kuwait", "Lebanon", "Libya", "Mauritania", "Morocco",
                        "Oman", "Palestine", "Qatar", "Saudi Arabia", "Somalia", "Sudan",
                        "Syria", "Tunisia", "United Arab Emirates", "Yemen"]


    arcpy.MakeFeatureLayer_management(positions, "cities_selected")

    for country in arabic_countries:
        print(country)


        arcpy.MakeFeatureLayer_management(countries, "country_selected", """ "NAME" = '{}' """.format(country))


        arcpy.SelectLayerByLocation_management("cities_selected", "WITHIN", "country_selected")


        arcpy.FeatureClassToFeatureClass_conversion("cities_selected", output_path, "The_Cities_of_{}".format(country))

        print("Shapefile for cities of {} has been created successfully!".format(country))

def extract_urban_areas(urban_areas_fc, countries_fc, output_folder):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_folder  # Set workspace to the output folder

    # Define invalid characters for Windows filenames
    invalid_chars = r'<>:"/\|?*'

    # Create a feature layer for urban areas with the condition "area_sqkm" > 50
    arcpy.MakeFeatureLayer_management(urban_areas_fc, "urban_areas_layer", """ "area_sqkm" > 50 """)
    counter = 0
    # Iterate over the countries
    with arcpy.da.SearchCursor(countries_fc, ["FID", "REGION_UN", "SOVEREIGNT"]) as cursor:
        for row in cursor:
            country_fid = row[0]
            region_un = row[1]
            country_name = row[2]

            # Check if the country is in Africa
            if region_un == "Africa":
                # Create a feature layer for the current country
                arcpy.MakeFeatureLayer_management(countries_fc, "country_layer", """ "FID" = {} """.format(country_fid))

                # Select urban areas within the current country
                arcpy.SelectLayerByLocation_management("urban_areas_layer", "WITHIN", "country_layer")

                # Get the country name and sanitize it
                country_name = country_name.strip()  # Remove leading and trailing whitespaces
                # Replace invalid characters with underscores
                country_name = ''.join(c if c.isalnum() or c in ['_', ' '] else '_' for c in country_name if c not in invalid_chars)
                # Remove all characters that are not alphanumeric or whitespace
                country_name = re.sub(r'\W+', '', country_name)

                # Construct the output filename
                output_name = "UrbanAreas_in_{}_FID{}".format(country_name, country_fid)
                arcpy.FeatureClassToFeatureClass_conversion("urban_areas_layer", output_folder, output_name)
                counter += 1
                print("Created shapefile for Urban Areas in", region_un)

        print("Total Urban Areas extracted in Africa:", counter)




# Define workspace and feature class

workspace = r"E:\projects_4th\GIS\Data"
airport = r"E:\projects_4th\GIS\Data\project_dataset\Datasets\ne_10m_airports.shp"
positions = r"E:\projects_4th\GIS\Data\ne_10m_populated_places.shp"
urban = r"E:\projects_4th\GIS\Data\project_dataset\Datasets\ne_10m_urban_areas.shp"
countries = r"E:\projects_4th\GIS\Data\ne_10m_admin_0_countries.shp"
output_path = r"E:\projects_4th\GIS\Output"



# Call the function
print_airports_with_ramp(workspace, airport)
#create_shapefiles_for_arabic_cities(positions, countries, output_path)
#extract_urban_areas(urban,countries,output_path)
