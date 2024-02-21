from PIL import Image, ImageDraw, ImageFont
import data_dragon_functions as dd


GH_BG_COLOUR = (22, 27, 34, 0) #(24, 28, 36)



'''
THIS FUNCTION REQUIRES THAT AT LEAST THREE CHAMPIONS HAVE BEEN PLAYED BY A PLAYER.
While this is a pretty good assumption, there should ideally be a way to handle
if a player has only ever played one champion.
'''
def create_mastery_gif(m1_image, m2_image, m3_image, m1_text, m2_text, m3_text, save_location):
    step = 10
    text_off_set = 250
    total_width = int(308 * 3.5)
    background_colour = GH_BG_COLOUR
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
            im = Image.new('RGBA', (total_width, 560), background_colour)
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
            im = Image.new('RGBA', (total_width, 560), background_colour)
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
                save_all=True, append_images=images[1:], optimize=True, duration=20, loop=0, disposal=2)


def create_extra_info(list_of_messages, save_location):
    images = []
    background_colour = GH_BG_COLOUR
    width = 30 * 50
    for message in list_of_messages:
        im = Image.new('RGBA', (width , 50), background_colour)
        image_editable = ImageDraw.Draw(im)
        font = ImageFont.truetype("CONSOLAB.TTF", size=50)
        image_editable.text((0, 0), message, fill=(255, 255, 255), font=font)
        images.append(im)


    images[0].save(save_location,
                save_all=True, append_images=images[1:], optimize=True, duration=4000, loop=0, disposal=2)


def create_animated_loading_bar(champ_image, champ, percentage, save_location):
    bars = int((percentage / 100) * 25)
    out = "|"
    for x in range(25):
        out = out + "-"
    out = out + "|"

    current_pos = 1



    images = []
    background_colour = GH_BG_COLOUR
    width = 120 * 30
    start_loading_bar = len(f" {champ}".ljust(dd.get_longest_name() + 4, " ")) * 70

    for bar in range(bars):
        im = Image.new('RGBA', (width , 120), background_colour)

        # CHAMPION ICON
        im2 = Image.open(champ_image)
        im.paste(im2, (0, 0))



        image_editable = ImageDraw.Draw(im)
        font = ImageFont.truetype("CONSOLAB.TTF", size=120)

        # Champion name
        image_editable.text((200, 0), f"{champ}", fill=(255, 255, 255), font=font)

        # Add the loading bar
        image_editable.text((start_loading_bar, 0), out, fill=(255, 255, 255), font=font)

        # Add the percentage
        image_editable.text((start_loading_bar + (120 * 15), 0), f"{round(percentage, 2): .2f}%", fill=(255, 255, 255), font=font)

        images.append(im)

        out = out[:current_pos] + "█" + out[current_pos + 1:]
        current_pos += 1


    images[0].save(save_location,
                save_all=True, append_images=images[1:], optimize=True, duration=50, disposal=2)

   

