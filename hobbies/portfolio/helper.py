from django.conf import settings
from random import choice, seed
from os import listdir
from .popomodels import POPOImage
from os import path

class Helper:
    colors = [
        '#3273dc',
        'orange',
        'purple',
        'blueviolet',
        'coral',
        'crimson',
        'deepskyblue',
        'indigo'
    ]
    
    def choose_css_color(self):
        seed()
        return choice(self.colors)

    def select_static_file(self, image_category):
        seed()
        folder = 'images/'
        if (image_category.lower() == 'primary'):
            folder += 'Primary/'
        elif (image_category.lower() == 'food'):
            folder += 'Food/'
        elif (image_category.lower() == 'programming'):
            folder += 'Programming/'
        elif (image_category.lower() == 'other'):
            folder += 'Other/'
        else:
            raise ValueError("image_category must be Primary, Food, Programming, or Other")

        # This only works becuase there is only one entry in STATICFILES_DIRS. I don't love it but I need to move on
        # collectstatic adds extra files to the '/staticfiles' dir which do not exist in localhost (And might not in prod?)
        # so I've just decided to reference the files as they exist in '/static'
        image = folder + choice(listdir(settings.STATICFILES_DIRS[0] + '/' + folder))
        return self.create_popo_image(image)
    
    def create_popo_image(self, image):
        alt_text = path.splitext(path.basename(image))[0]
        return POPOImage(image, alt_text)