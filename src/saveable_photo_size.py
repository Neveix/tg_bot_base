from telegram import PhotoSize


class SaveablePhotoSize(PhotoSize):
    
    def from_photo_size(photo_size: PhotoSize) -> "SaveablePhotoSize":
        return SaveablePhotoSize(**photo_size.to_dict())
    def to_string(self) -> str:
        s = self
        return ",".join([s.file_id,s.file_unique_id,str(s.width),str(s.height),str(s.file_size)])
    def from_string(string: str) -> "SaveablePhotoSize":
        s = string.split(",")
        s4 = None
        if len(s) > 4:
            s4 = int(s[4])
        return SaveablePhotoSize(s[0],s[1],int(s[2]),int(s[3]),s4)