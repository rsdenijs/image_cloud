import random
from PIL import Image


class Rect():

    def __init__(self, left, top, right, bottom):
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom

    def separated(self, other):
        '''Returns True if the self does not intersect with other'''
        return self.right < other.left or \
            self.left > other.right or \
            self.top > other.bottom or \
            self.bottom < other.top

    def contains(self, other):
        '''Returns True if the self contains other'''
        return self.right >= other.right and \
            self.left <= other.left and \
            self.top <= other.top and \
            self.bottom >= other.bottom


def wordcloud(files, max_thumb_size, out_size, avoid_intersections=True):
    '''Generates a collage of randomly placed thumbnails.
       '''
    assert max_thumb_size[0] <= out_size[0]
    assert max_thumb_size[1] <= out_size[1]

    def gen_pos(imsize, fsize):
        '''Generates a position such that the thumbnail
         fits in the large image'''
        x_range = (0, fsize[0] - imsize[0])
        y_range = (0, fsize[1] - imsize[1])
        x = random.randint(*x_range)
        y = random.randint(*y_range)
        return x, y

    bcolor = (255, 255, 255, 0)
    out = Image.new(mode='RGBA', size=out_size, color=bcolor)
    rectangles = []
    for fl in files:
        im = Image.open(fl)
        im.thumbnail(max_thumb_size, Image.ANTIALIAS)
        w, h = im.size
        it = 0
        found_pos = False
        while not found_pos:
            x, y = gen_pos(im.size, out_size)
            rect = Rect(x, y, x + w, y + h)
            if avoid_intersections and not all(rect.separated(r) for r in rectangles):
                it += 1
                if it > 1000:
                    raise ValueError(
                        "Can not find a non-overlapping position for the image")
                continue
            rectangles.append(rect)

            found_pos = True
            out.paste(im, (x, y), im)
    return out


def wordcloud_gauss(files, max_thumb_size, out_size, variance):
    '''Generates a collage of gaussian-distributed placed thumbnails
       '''
    assert max_thumb_size[0] <= out_size[0]
    assert max_thumb_size[1] <= out_size[1]
    assert variance < out_size[0], "Decrease variance"
    assert variance < out_size[1], "Decrease"

    def gauss_pos(out_size, variance):        
        x = random.gauss(out_size[0] / 2, variance)
        y = random.gauss(out_size[1] / 2, variance)
        return x, y

    bcolor = (255, 255, 255, 0)
    out = Image.new(mode='RGBA', size=out_size, color=bcolor)
    for fl in files:
        im = Image.open(fl)
        im.thumbnail(max_thumb_size, Image.ANTIALIAS)
        w, h = im.size
        while True:
            x, y = gauss_pos(out_size, variance)
            imrect = Rect(0, 0, out_size[0], out_size[1])
            pos = Rect(
                x - w / 2 - 1, y - h / 2 - 1, x + w / 2 + 1, y + h / 2 + 1)
            if imrect.contains(pos):  # found position inside image frame
                break

        out.paste(im, (int(pos.left), int(pos.top)), im)

    return out

if __name__ == '__main__':
    import os
    files = [os.path.join('images',f) for f in os.listdir('images')]

    out = wordcloud_gauss(files,(100,100),(500,500),100)
    out.save('cloud_gauss.png')

    try:
        out = wordcloud(files,(100,100),(1200,1200),avoid_intersections=True)
        out.save('cloud.png')
    except ValueError as e:
        print("No valid placing was found for the images, try re-running or increasing the destination image size")
        pass
