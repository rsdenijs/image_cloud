image_cloud
===========

Simple tool to create an image cloud from the input files

Dependencies: pillow (pip install pillow)

Similar to a word cloud this creates an image cloud. 

You have two functions available, `wordcloud` and `wordcloud_gauss`. 
The first distributes the images evenly and can be set to avoid overlaps. 
The second one distributes the images in gaussian fashion around the center of the output image. 

The resulting image has a transparent background if saved in png. 

Run `wordcloud.py` for an example on how to use the functions. 

Example result for wordcloud_gauss
----------

![Alt text](https://github.com/rsdenijs/image_cloud/blob/master/cloud_gauss.png "Example")


