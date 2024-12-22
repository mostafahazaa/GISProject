import arcpy


arcpy.env.overwriteOutput=True
positions = r"E:\projects_4th\GIS\Data\ne_10m_populated_places.shp"
countries = r"E:\projects_4th\GIS\Data\ne_10m_admin_0_countries.shp"
output_path= r"E:\projects_4th\GIS\Output"

cities_selcted = "cities_selcted"
country_selected = "country_selected"



list_of_countres=["Russia","Australia"]

arcpy.MakeFeatureLayer_management(positions,cities_selcted)

for country in list_of_countres :
    print (country)
    arcpy.MakeFeatureLayer_management(countries,country_selected,""" "NAME" = '{}'   """.format(country))
    arcpy.SelectLayerByLocation_management(cities_selcted,'WITHIN',country_selected)
    arcpy.FeatureClassToFeatureClass_conversion(cities_selcted,output_path,"The_Cities_of_ {}".format(country))









