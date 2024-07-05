# 🍏 SmartBite

SmartBite is an AI tool that identifies food dishes in photos, providing details about ingredients, allergens, macronutrients, and calories. Improve your health and well-being with conscious and balanced eating. 🍽️🌿

<div align="center">
    <img src="https://github.com/sergiolms/smartbite/assets/86774052/897885e8-efca-400e-a679-73b6ab3f828b" alt="SmartBite Showcase gif" />
    <br/>
    <i>If your prefer it, <a href="https://github.com/sergiolms/smartbite/assets/86774052/36561ee5-0d07-437d-bf9c-9ebc00980083" target="_blank">here</a> is the video</i>
</div>

## ✨ Live Demo ✨

Try it now at the [GitHub Pages of this repository][5] or at [Hugging Face site][6].

<!-- TODO: añadir el artículo de Medium aquí una vez se publique -->

## 🚀 The Project

It was created as a result of a final project for [AI Saturdays 🤖 ALICANTE][1], with the idea of developing an AI-based tool that recognizes a food dish in a photograph and identifies its ingredients, allergens, macronutrients, and calories (approximate per portion/grams) for that dish.

### 👥 Social Impact
It could help improve people's health and well-being. By helping them be aware of what they eat, it can help prevent diseases related to obesity and diabetes. Additionally, it aims to promote a balanced and sustainable diet by informing about the importance of proper nutrition.

### 🧑🏻‍🍳 Authors

<table align="center" style="font-size:14px">
    <tbody>
        <tr>
            <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
                <a href="https://github.com/sergiolms">
                    <img src="https://avatars.githubusercontent.com/u/86774052?v=4" width="100" height="auto" alt="Sergio L. Maciá Sempere"/>
                    <br />
                    <sub><b>Sergio Maciá</b></sub>
                </a>
            </td>
            <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
                <a href="https://github.com/Javier-Macia">
                    <img src="https://avatars.githubusercontent.com/u/72144607?v=4" width="100" height="auto" alt="Javier Maciá Sempere"/>
                    <br />
                    <sub><b>Javier Maciá</b></sub>
                </a>
            </td>
            <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
                <a href="https://github.com/adl23-ua">
                    <img src="https://avatars.githubusercontent.com/u/123936715?v=4" width="100" height="auto" alt="Antonio Díaz-Parreño Lajara"/>
                    <br />
                    <sub><b>Antonio Díaz-Parreño</b></sub>
                </a>
            </td>
        </tr>
    </tbody>
</table>

## 🧠 About the Model

- It was trained using the InceptionV3 model from the Keras library of Tensorflow.
- Currently, the model has an approximate accuracy rate of 84% and a loss of 0.9252.
- In the `model` folder, you can find a [more detailed document](model/README-en.md) about the model evaluation (scoring).
- It was trained with 101 dishes that can be seen [here](datasource/meta/labels.txt).

## 🌿 Getting Started

In the [`google-collab`](google-collab) folder, you can find a couple of Notebooks to train and use the model for making predictions. In the notebooks, you'll find the code divided into blocks and explained step by step.

If you prefer to run it on your machine, follow the instructions in the [Requirements](#️-requirements) section.

### ⚙️ Requirements

If you run the Google Collab notebooks, no installation on your machine is necessary. 
You will find instructions about the project dependencies in the notebook itself.

If you decide to download the project and run it on your machine, you will need:
- Python, to run the scripts. 
    - Python v3.12.3 was used for development. You can install it [here][2]
- Tensorflow v2.16.1, to run the model.
- [Gradio][3], to generate a web interface from where to upload images.
- [Git LFS][4], since the model weighs more than 100MB, it is necessary to handle large files in git.

## 🏋🏻‍♂️ Train the Model

If you want to train or fine-tune the model using the same project configuration, in the [`scripts`](scripts) folder you have the Python scripts used both to train the model and to use it for making predictions.

## ☝️🤓 Dataset

The dataset used is called Food101. You can find more information in [`datasource/images`](datasource/images/README.md)

[1]:https://saturdays.ai/alicante/
[2]:https://www.python.org/downloads/release/python-3123/
[3]:https://github.com/gradio-app/gradio
[4]:https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage
[5]:https://sergiolms.github.io/smartbite/
[6]:https://huggingface.co/spaces/sergiolms/smartbite