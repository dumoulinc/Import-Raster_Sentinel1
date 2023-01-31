# Import-Raster_Sentinel1
Outil pour importer une matrice corrigée 'RTC' de Sentinel-1 en fonction d'un territoire donné.

documentation pour les données importées: https://sentinel-s1-rtc-indigo-docs.s3-us-west-2.amazonaws.com/index.html

L'outil a besoin d'un shapefile qui définit l'étendue du territoire étudié ainsi que du shapefile 'grid' (disponible dans le dossier /grid) en entrée.
On doit également entrer une date pour laquelle télécharger les matrices correspondantes. S'il n'existe aucune matrice pour la date donnée, la l'image satelitte la plus
récente à partir de cette date sera téléchargée.

![Outil](/img/4.PNG)

L'outil utilise la grille UTM fournie et le territoire à l'étude pour déterminer les matrices à télécharger

![Grille](/img/1.PNG)

![Territoire](/img/2.PNG)

L'outil exporte une matrice .tif découpée selon l'étendue du territoire à l'étude

![Output](/img/3.PNG)
