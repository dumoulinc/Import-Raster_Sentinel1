import arcpy
import sys
import boto3
import os
from botocore.handlers import disable_signing

s3 = boto3.resource('s3')
s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
s3_client = boto3.client('s3')
bucket = 'sentinel-s1-rtc-indigo'
my_bucket = s3.Bucket(bucket)
prefixe = 'tiles/RTC/1/IW/18/T/YR/2020/'

# On stocke les chemins des fichiers dans des variables. La grille est utilisée pour
# identifier les tuiles à importer
# Le territoire est utilisé pour définir la zone d'intérêt.
grille = arcpy.GetParameterAsText(0)
territoire = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(3)
date = arcpy.GetParameterAsText(2)


# On détermine le 'Tile ID' qui permet d'identifier les tuiles à importer
def get_identity():
    arcpy.analysis.Identity(territoire, grille, output + 'identity.shp', "NO_FID", None, "NO_RELATIONSHIPS")
    identity = arcpy.SearchCursor(output + 'identity.shp')
    grid_value = ''
    for row in identity:
        grid_value = row.getValue("id")
        if grid_value == '':
            sys.exit('La grille ne couvre pas la zone d\'intérêt')
    return grid_value


def get_rasters():
    date = arcpy.GetParameterAsText(2)
    date1 = date.replace('-', '')
    identity = get_identity()
    date_loop = True
    raster_list = []
    download_list = []

    # On recherche les rasters correspondant à la date et à la tuile définie
    while date_loop == True:
        print('Création de la liste de raster qui correspondent au paramètres de recherche...')
        prefixe = os.path.join('tiles/RTC/1/IW', identity[0:2], identity[2], identity[3:], date1[:4], 'S1A_'+date1+'_' + identity +'_ASC').replace('\\', '/')
        for file in my_bucket.objects.filter(Prefix=prefixe):
            vsis3_image_path = os.path.join('/vsis3/', bucket, file.key).replace('\\', '/')
            if vsis3_image_path.endswith('.tif'):
                raster_list.append(vsis3_image_path)
                print(vsis3_image_path)

        # Si aucun raster n'est trouvé, on passe à la date suivante
        if len(raster_list) == 0:
            date1 = int(date1) + 1
            date1 = str(date1)
            print('Aucun raster trouvé pour la date ' + date)
            print('Recherche des rasters pour la date suivante...')
        else:
            date_loop = False
            print('Liste de raster créée')
            print('Nombre de raster trouvés : ' + str(len(raster_list)))

    # On télécharge les rasters dans la liste
    for raster in raster_list:
        print('Téléchargement du raster ' + raster)
        arcpy.CopyRaster_management(raster, output + raster[-13:])
        download_list.append(output + raster[-13:])

    # On clip les rasters en fonction de la zone d'intérêt
    for raster in download_list:
        print('Clip du raster ' + raster)
        arcpy.Clip_management(raster, '#', raster[:-4]+ '_clip.tif', territoire, '#', 'ClippingGeometry')
    
    #On supprime les fichiers temporaires
    arcpy.Delete_management(output + 'identity.shp')
    arcpy.Delete_management(output + 'Gamma0_VH.tif')
    arcpy.Delete_management(output + 'Gamma0_VV.tif')
    arcpy.Delete_management(output + 'ent_angle.tif')

# Lance les fonctions
get_rasters()