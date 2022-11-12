from PIL import Image
#Read the two images
image1 = Image.open('AlbumCovers/Glitter.jpg')
image2 = Image.open('AlbumCovers/Galapagos.jpg')
image4 = Image.open('AlbumCovers/Galapagos.jpg')
image5 = Image.open('AlbumCovers/Galapagos.jpg')

image6 = Image.open('AlbumCovers/Galapagos.jpg')
image7 = Image.open('AlbumCovers/Galapagos.jpg')
image8 = Image.open('AlbumCovers/Galapagos.jpg')

image9 = Image.open('AlbumCovers/Galapagos.jpg')
image3 = Image.open('AlbumCovers/Galapagos.jpg')

imgs = [image1,image2,image3,image4,image5,image6,image7,image8,image9]


def create_maxtrix(albums,matrix_size):
    #for now assume all images are same size
    #assuming album is Z times Z size
    album_size =  image1.size[0]

    new_image = Image.new('RGB', (matrix_size *album_size, matrix_size * album_size), (250, 250, 250))

    index = 0
    for x in range(matrix_size):
        for y in range(matrix_size):
            new_image.paste(albums[index], (album_size*x, album_size*y))
            index+=1

    new_image.save("merged_image.jpg", "JPEG")

    new_image.show()




