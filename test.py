from PIL import Image, ImageDraw, ImageFont



'''
NOTE:
1. We can use "loop=" for loading bars to only go once
'''



def create_mastery_gif(m1_image, m2_image, m3_image, m1_text, m2_text, m3_text, save_location):
    step = 10

    # 308, 560
    images = []

    first_image = [0, 0]
    first_words = [350, 280]

    second_image = [0, -560]
    second_words = [350, -560 + 280]

    third_image = [0, -560 * 2]
    third_words = [350, (-560 * 2) + 280]

    first_image_2 = [0, -560 * 3]
    first_words_2 = [350, (-560 * 3) + 280]


    for rotation in range(3):
        for stationary in range(0, 150):
            im = Image.new('RGB', (308 * 4, 560), (0, 0, 0))
            im2 = Image.open(m1_image)
            im.paste(im2, (0,first_image[1]))
            im3 = Image.open(m2_image)
            im.paste(im3, (0,second_image[1]))
            im4 = Image.open(m3_image)
            im.paste(im4, (0, third_image[1]))
            im5 = Image.open(m1_image)
            im.paste(im5, (0, first_image_2[1]))

            image_editable = ImageDraw.Draw(im)
            font = ImageFont.truetype("CONSOLAB.TTF", size=50)
            image_editable.text((first_words[0], first_words[1]), m1_text, fill=(255, 255, 255), font=font)
            image_editable.text((second_words[0], second_words[1]), m2_text, fill=(255, 255, 255), font=font)
            image_editable.text((third_words[0], third_words[1]), m3_text, fill=(255, 255, 255), font=font)
            image_editable.text((first_words_2[0], first_words_2[1]), m1_text, fill=(255, 255, 255), font=font)
            images.append(im)


        # Move to next image
        for movement in range (0, 560, step):
            im = Image.new('RGB', (308 * 4, 560), (0, 0, 0))
            im2 = Image.open(m1_image)
            im.paste(im2, (0,first_image[1]))
            im3 = Image.open(m2_image)
            im.paste(im3, (0,second_image[1]))
            im4 = Image.open(m3_image)
            im.paste(im4, (0, third_image[1]))
            im5 = Image.open(m1_image)
            im.paste(im5, (0, first_image_2[1]))

            image_editable = ImageDraw.Draw(im)
            font = ImageFont.truetype("CONSOLAB.TTF", size=50)
            image_editable.text((first_words[0], first_words[1]), m1_text, fill=(255, 255, 255), font=font)
            image_editable.text((second_words[0], second_words[1]), m2_text, fill=(255, 255, 255), font=font)
            image_editable.text((third_words[0], third_words[1]), m3_text, fill=(255, 255, 255), font=font)
            image_editable.text((first_words_2[0], first_words_2[1]), m1_text, fill=(255, 255, 255), font=font)
            images.append(im)



            first_image[1] += step
            second_image [1] += step
            third_image[1] += step
            first_image_2[1] += step


            first_words[1] += step
            second_words[1] += step
            third_words[1] += step
            first_words_2[1] += step



    images[0].save(save_location,
                save_all=True, append_images=images[1:], optimize=True, duration=20, loop=0)








create_mastery_gif('loading_images/Yone_19.png', 'loading_images/Velkoz_0.png', 'loading_images/Akali_9.png', "one", "two", "three", 'temp.gif')


'''
f = Image.open('temp.gif')
f.info['duration'] = 40
f.save('temp.gif', save_all=True)
'''
