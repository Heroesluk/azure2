from PIL import Image
#Read the two images

def create_maxtrix(albums,matrix_size):
    #for now assume all images are same size
    #assuming album is Z times Z size
    albums = [Image.open('static/images/{}'.format(i)) for i in albums]

    album_size =  albums[0].size[0]

    new_image = Image.new('RGB', (matrix_size *album_size, matrix_size * album_size), (250, 250, 250))

    index = 0
    for x in range(matrix_size):
        for y in range(matrix_size):
            new_image.paste(albums[index], (album_size*x, album_size*y))
            index+=1

    new_image.save("merged_image.jpg", "JPEG")

    new_image.show()




