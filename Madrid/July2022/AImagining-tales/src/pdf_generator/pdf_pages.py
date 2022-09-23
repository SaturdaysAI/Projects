import os
import numpy as np
from fpdf import FPDF

W_A4 = 200
H_A4 = 297


def add_borders_style_up(pdf):
    pdf.rect(5.0, 10.0, 200.0, 268.0)
    pdf.rect(8.0, 13.0, 194.0, 262.0)

    pdf.set_xy(6.0, 11.0)
    pdf.image('upleft.PNG', link='', type='', w=1586 / 80, h=1920 / 80)  # TODO generar imagenes upleft etc
    pdf.set_xy(183.0, 11.0)
    pdf.image('upright.PNG', link='', type='', w=1586 / 80, h=1920 / 80)
    return pdf


def add_borders_style_down(pdf):
    # pdf.ln(253)
    pdf.set_xy(6.0, 252.0)
    pdf.image('downleft.PNG', link='', type='', w=1586 / 80, h=1920 / 80)
    pdf.set_xy(183.0, 252.0)
    pdf.image('downright.PNG', link='', type='', w=1586 / 80, h=1920 / 80)
    return pdf


def create_cover(page_config, image_path):
    # Create PDF
    pdf = FPDF('P', 'mm', 'A4')  # A4 is 210mm by 297mm

    pdf.add_page()
    pdf.set_margins(5, 0, 5)  # parametrizar 5,0,5

    pdf = add_borders_style_up(pdf)

    title_tale = page_config['pdf_style']['text']
    font = page_config['pdf_style']['font']
    title_size = page_config['pdf_style']['text_size']

    w_image = page_config['pdf_style']['w_image']
    h_image = page_config['pdf_style']['h_image']

    # get image or pass by param

    print("Building page...")
    pdf.set_font(font, 'B', title_size)
    pdf.ln(60)

    pdf.multi_cell(W_A4, 10, title_tale, border=0, align='C')

    pdf.image(image_path, x=((W_A4 - w_image) / 2), y=140, w=w_image, h=h_image)

    pdf = add_borders_style_down(pdf)

    return pdf


def create_middle_page(pdf, page_config, image_path):
    pdf.add_page()
    pdf.set_margins(5, 0, 5)  # parametrizar 5,0,5

    pdf = add_borders_style_up(pdf)

    text = page_config['pdf_style']['text']
    font = page_config['pdf_style']['font']
    size = page_config['pdf_style']['text_size']

    w_image = page_config['pdf_style']['w_image']
    h_image = page_config['pdf_style']['h_image']

    # Preprocess text 

    texts = text.split('\n\n')
    if len(texts) == 1:
        text_before = texts[0]
        text_after = " "
    else:
        index_middle = int(np.ceil(len(texts)/2))
        text_before = '\n'.join(texts[:index_middle])
        text_after = '\n'.join(texts[index_middle:])

    print("Building page...")
    pdf.set_font(font, '', size)

    pdf.ln(10)
    pdf.cell(15)
    pdf.multi_cell(W_A4 - 10 - 15, 5, text_before, 0, 'J')

    pdf.image(image_path, x=((W_A4 - w_image) / 2), y=pdf.get_y() + 8, w=w_image, h=h_image)

    pdf.ln(pdf.get_y() + 8)
    pdf.cell(15)
    pdf.multi_cell(W_A4 - 10 - 15, 5, text_after, 0, 'J')

    pdf = add_borders_style_down(pdf)

    return pdf


def create_up_page(pdf, page_config, image_path):
    pdf.add_page()
    pdf.set_margins(5, 0, 5)  # parametrizar 5,0,5

    pdf = add_borders_style_up(pdf)

    text = page_config['pdf_style']['text']
    font = page_config['pdf_style']['font']
    size = page_config['pdf_style']['text_size']

    w_image = page_config['pdf_style']['w_image']
    h_image = page_config['pdf_style']['h_image']

    # Preprocess text 
    texts = text.split('\n\n')
    if len(texts) == 1:
        texts = texts[0]
    else:
        texts = '\n'.join(texts)

    print("Building page...")
    pdf.ln(20)
    pdf.image(image_path, x=((W_A4 - w_image) / 2), y=30, w=w_image, h=h_image)

    pdf.set_font(font, '', size)

    pdf.ln(pdf.get_y() + 10)
    pdf.cell(15)
    pdf.multi_cell(W_A4 - 10 - 15, 5, texts, 0, 'J')

    pdf = add_borders_style_down(pdf)

    return pdf


def create_down_page(pdf, page_config, image_path):
    pdf.add_page()
    pdf.set_margins(5, 0, 5)  # parametrizar 5,0,5

    pdf = add_borders_style_up(pdf)

    text = page_config['pdf_style']['text']
    font = page_config['pdf_style']['font']
    size = page_config['pdf_style']['text_size']

    w_image = page_config['pdf_style']['w_image']
    h_image = page_config['pdf_style']['h_image']

    # Preprocess text
    texts = text.split('\n\n')
    if len(texts) == 1:
        texts = texts[0]
    else:
        texts = '\n'.join(texts)

    print("Building page...")
    pdf.set_font(font, '', size)

    pdf.ln(10)
    pdf.cell(15)
    pdf.multi_cell(W_A4 - 10 - 15, 5, texts, 0, 'J')

    pdf.image(image_path, x=((W_A4 - w_image) / 2), y=pdf.get_y() + 8, w=w_image, h=h_image)

    pdf = add_borders_style_down(pdf)

    return pdf
