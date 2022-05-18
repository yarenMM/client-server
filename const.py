#To tackle the issue of poor passenger tracking, each passenger center-point will have a
#time to live (TTL). E.g., how many frames it is allowed to go undetected before being
#detected and considered as the same center-point again. Once the time to live for a centerpoint reaches zero,
#it is discarded by the tracking algorithm. This allows center-points to
#survive during frames where they are not detected.
TTL = 20
#a pre-defined maximum allowed distance (MAD) value, measured in pixels, 
#between two center-points. If the distance
#between point p and point q is within the MAD value, point q will be considered as the
#relocation position of point p
DISTANCE = 150 #100 125 150 
AREA = (140, 332) #l1, l2 location. "linjerna över videon för att se om personen går in eller ut"
ACC = 0.6  #accuracy, how "certain" the model need to be to determine if it is a human or not
K = 2 #'number of categories with highest score to display'
