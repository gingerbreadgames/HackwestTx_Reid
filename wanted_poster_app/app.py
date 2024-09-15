import os
import random
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'wanted_poster_output'

# Sepia filter function
def apply_sepia(image):
    width, height = image.size
    pixels = image.load()
    
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            tr = min(tr, 255)
            tg = min(tg, 255)
            tb = min(tb, 255)
            pixels[px, py] = (tr, tg, tb)

    return image

# Remove background function
def remove_background(image):
    image = image.convert("RGBA")
    datas = image.getdata()

    new_data = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    return image

# Generate random crime and bounty
crimes = [
    "Public Intoxication", "Horse Theft", "Bank Robbery", "Stagecoach Hijacking", 
    "Gunfight in the Saloon", "Claim Jumping", "Train Robbery", "Rustling Cattle", 
    "Duel at High Noon", "Card Sharking", "Trespassing on Ranch Land", "Moonshine Smuggling",
    "Assault with a Six-Shooter", "Disturbing the Peace", "Bounty Hunting Without a License", 
    "Stagecoach Sabotage", "Illegal Gold Panning", "Smuggling Contraband Whiskey", 
    "Snake Oil Salesman", "Fleeing a Posse", "Wagon Train Sabotage", "Dynamiting a Mine", 
    "Riverboat Gambling Fraud", "Highway Robbery", "Shooting Up the Sheriff's Office", 
    "Impersonating a Lawman", "Raiding an Outlaw Hideout", "Vigilante Justice", 
    "Bar Brawling", "Breaking Horses Without a Permit", "Kidnapping a Rancher's Daughter", 
    "Running a Speakeasy", "Stealing Stagecoach Strongbox", "Counterfeiting Gold Coins", 
    "Destroying Telegraph Lines", "Burning Down a Sawmill", "Fencing Stolen Livestock", 
    "Poisoning the Water Hole", "Ambushing a Wagon Train", "Attempting to Blow Up the Train Bridge", 
    "Robbing a General Store"
]
def random_crime():
    return random.choice(crimes)

bounties = [
    "$25", "$50", "$75", "$100", "$150", "$200", "$250", "$300", "$350", "$400", "$450", "$500", 
    "$600", "$750", "$800", "$900", "$1,000", "$1,250", "$1,500", "$2,000", "$2,500", "$3,000", 
    "$3,500", "$4,000", "$5,000", "$6,000", "$7,500", "$10,000", "$12,500", "$15,000", "$20,000", 
    "$25,000", "$30,000", "$35,000", "$40,000", "$50,000", "$60,000", "$75,000", "$100,000", "$150,000"
]
def random_bounty():
    return random.choice(bounties)

# Main route for form and processing image
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]

        if file.filename == "":
            return "No file selected", 400

        if file:
            img1 = Image.open(file)

            # Apply sepia filter and remove background
            img1 = apply_sepia(img1)
            img1 = remove_background(img1)

            # Open background wanted poster image
            wanted_img = Image.open("Static/wanted_background.jpg")

            # Resize the background
            new_bg_height = int(img1.height * 2.5)
            new_bg_width = int(img1.width * 2)
            wanted_img = wanted_img.resize((new_bg_width, new_bg_height))

            # Draw text on wanted poster
            draw = ImageDraw.Draw(wanted_img)
            font1 = ImageFont.truetype("Static/fonts/Dkwildbunch-66eA.otf", 80)
            font2 = ImageFont.truetype("Static/fonts/Dkwildbunch-66eA.otf", 50)
            text1 = "WANTED!"
            text2 = random_crime()
            text3 = random_bounty()
            text_color = (0, 0, 0)  

            x_center = new_bg_width // 2

            draw.text((x_center, 400), text1, fill=text_color, font=font1, anchor="mm")
            draw.text((x_center, 500), text2, fill=text_color, font=font2, anchor="mm")
            draw.text((x_center, 550), text3, fill=text_color, font=font2, anchor="mm")

            # Paste the processed image onto the wanted poster
            img_x_center = (new_bg_width - img1.width) // 2
            wanted_img.paste(img1, (img_x_center, 100), img1)

            # Save the output
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "wanted_poster.png")
            wanted_img.save(output_path)

            # Return the generated wanted poster image
            return send_file(output_path, as_attachment=True)

    return render_template("test.html")

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)