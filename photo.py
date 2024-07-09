class Photo:
    
    def __init__(self, photo_id, histogram, link) -> None:
        self.photo_id = photo_id
        self.histogram = histogram
        self.link = link

    #Не хранить фотографию нигде. 