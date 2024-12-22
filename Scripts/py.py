import arcpy

def create_shapefiles_for_urban_areas(input_feature_class, countries, output_workspace):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = output_workspace

    # List the fields available in the input feature class
    fields = [field.name for field in arcpy.ListFields(input_feature_class)]

    # Check if the necessary fields are present in the feature class
    if "FID" in fields and "area_sqkm" in fields:
        
        # Create a search cursor for the countries feature class
        with arcpy.da.SearchCursor(countries, ["FID", "ADMIN"]) as country_cursor:
            for country_row in country_cursor:
                country_fid = country_row[0]
                country_name = country_row[1]

                # Create a feature layer for the current country
                arcpy.MakeFeatureLayer_management(countries, "country_layer", """ "FID" = {} """.format(country_fid))

                # Select urban areas within the current country
                arcpy.SelectLayerByLocation_management(input_feature_class, "WITHIN", "country_layer")

                # Create a feature layer for the selected urban areas
                arcpy.MakeFeatureLayer_management(input_feature_class, "urban_area_layer", """ "area_sqkm" > 50 """)

                # Copy the selected urban areas to a new shapefile
                output_name = "UrbanAreas_in_{}_FID{}".format(country_name.replace(" ", "_"), country_fid)
                arcpy.FeatureClassToFeatureClass_conversion("urban_area_layer", output_workspace, output_name)

                print("Shapefile {output_name} has been created successfully!")
    else:
        print("The required fields are not present in the input feature class.")

# Input feature class containing urban areas data
input_feature_class = r"E:\projects_4th\GIS\Data\project_dataset\Datasets\ne_10m_urban_areas.shp"  # Update with your input shapefile path

# Countries shapefile
countries = r"E:\projects_4th\GIS\Data\ne_10m_admin_0_countries.shp"

# Output workspace to save the new shapefiles
output_workspace = r"E:\projects_4th\GIS\Output"  # Update with your output workspace path

# Call the function
create_shapefiles_for_urban_areas(input_feature_class, countries, output_workspace)
