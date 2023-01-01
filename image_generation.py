from PIL import Image, ImageDraw, ImageFont







'''
THIS FUNCTION REQUIRES THAT AT LEAST THREE CHAMPIONS HAVE BEEN PLAYED BY A PLAYER.
While this is a pretty good assumption, there should ideally be a way to handle
if a player has only ever played one champion.
'''
def create_mastery_gif(m1_image, m2_image, m3_image, m1_text, m2_text, m3_text, save_location):
    step = 10
    text_off_set = 250
    total_width = int(308 * 3.5)
    background_colour = (24, 28, 36)
    # 308, 560
    images = []

    first_image = [0, 0]
    first_words = [350, text_off_set]

    second_image = [0, -560]
    second_words = [350, -560 + text_off_set]

    third_image = [0, -560 * 2]
    third_words = [350, (-560 * 2) + text_off_set]

    first_image_2 = [0, -560 * 3]
    first_words_2 = [350, (-560 * 3) + text_off_set]


    for rotation in range(3):
        for stationary in range(0, 150):
            im = Image.new('RGB', (total_width, 560), background_colour)
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
            im = Image.new('RGB', (total_width, 560), background_colour)
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

