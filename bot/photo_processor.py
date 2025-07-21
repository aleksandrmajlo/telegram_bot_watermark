class PhotoProcessor:
    @staticmethod
    def get_largest_photo(photos):
        max_size = 0
        largest_file_id = None
        for photo in photos:
            if hasattr(photo, 'file_size') and photo.file_size > max_size:
                max_size = photo.file_size
                largest_file_id = photo.file_id
        return largest_file_id