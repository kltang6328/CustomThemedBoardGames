from openai import OpenAI
import json
from flask import Flask, request, render_template

app = Flask(__name__)

client = OpenAI(api_key='YOUR-API-KEY')

@app.route("/")
def index():
    return render_template("index.html")

class MonopolyGenerator:
    def generate_place(self, theme):
        theme = theme
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                        "content": "You generate 22 new Monopoly place based on the theme provided by the user. Only the name, no quotation marks. No duplicates"
                },
                {
                    "role": "user",
                    "content": theme
                } 
            ],
            temperature=0.9,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    def generate_card(self, theme):
        theme = theme
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                        "content": "You generate a new Monopoly card (community or chest) based on the theme provided by the user. Do not add Community Chest card at the beginning, only the cards details. Also do not put quotation marks at the beginning and end."
                },
                {
                    "role": "user",
                    "content": theme
                } 
            ],
            temperature=0.9,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    def generate_image(self, theme):
        theme = theme
        response = client.images.generate(
            model="dall-e-3",
            prompt="the outside monopoly box for a " + theme + " themed monopoly game",
            size="1024x1024",
            quality="standard",
            n=1,
            )
        return response.data[0].url
    def generate_board(self, theme):
        theme = theme
        response = client.images.generate(
            model="dall-e-3",
            prompt="the art on the physical monopoly board and token pieces for a " + theme + " themed monopoly game",
            size="1024x1024",
            quality="standard",
            n=1,
            )
        return response.data[0].url


class ClueGenerator:
    def generate_place(self, theme):
        theme = theme
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                        "content": "You generate clue board game spaces based on the theme provided by the user. Only the name, no quotation marks. No duplicates"
                },
                {
                    "role": "user",
                    "content": theme
                } 
            ],
            temperature=0.9,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    def generate_card(self, theme):
        theme = theme
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                        "content": "You generate a new Clue board game card based on the theme provided by the user. Donot put quotation marks at the beginning and end."
                },
                {
                    "role": "user",
                    "content": theme
                } 
            ],
            temperature=0.9,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    def generate_image(self, theme):
        theme = theme
        response = client.images.generate(
            model="dall-e-3",
            prompt="the outside clue board game box for a " + theme + " themed clue game",
            size="1024x1024",
            quality="standard",
            n=1,
            )
        return response.data[0].url
    def generate_board(self, theme):
        theme = theme
        response = client.images.generate(
            model="dall-e-3",
            prompt="the art on the physical board and token pieces for a " + theme + " themed clue game",
            size="1024x1024",
            quality="standard",
            n=1,
            )
        return response.data[0].url

class UnoGenerator:
    def generate_image(self, theme):
        theme = theme
        response = client.images.generate(
            model="dall-e-3",
            prompt="the outside uno card game box for a " + theme + " themed uno game",
            size="1024x1024",
            quality="standard",
            n=1,
            )
        return response.data[0].url
    def generate_board(self, theme):
        theme = theme
        response = client.images.generate(
            model="dall-e-3",
            prompt="the art on the physical cards for a " + theme + " themed uno game",
            size="1024x1024",
            quality="standard",
            n=1,
            )
        return response.data[0].url


@app.route('/board', methods=['POST'])
def generate_content():
    # Get the theme from the request
    theme = request.form["theme"]
    game = request.form["game"]

    if game == "mono":
        # Create Monopoly place and card generators
        mono_generator = MonopolyGenerator()

        # Generate new Monopoly places and cards based on the theme
        new_places = mono_generator.generate_place(theme)
        new_cards = [mono_generator.generate_card(theme) for _ in range(16)]
        new_image = mono_generator.generate_image(theme)
        new_board = mono_generator.generate_board(theme)

        return render_template("board.html", cards=new_cards, places_list=new_places, image=new_image, board=new_board)

    if game =="clue":
        clue_generator = ClueGenerator()

        new_places = clue_generator.generate_place(theme)
        new_cards = [clue_generator.generate_card(theme) for _ in range(16)]
        new_image = clue_generator.generate_image(theme)
        new_board = clue_generator.generate_board(theme)

        return render_template("board.html", cards=new_cards, places_list=new_places, image=new_image, board=new_board)

    if game == "uno":
        uno_generator = UnoGenerator()

        new_image = uno_generator.generate_image(theme)
        new_board = uno_generator.generate_board(theme)

        return render_template("card.html", image=new_image, board=new_board)


if __name__ == '__main__':
    app.run(debug=True)