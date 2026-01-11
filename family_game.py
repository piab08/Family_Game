import random
import streamlit as st
import pandas as pd

st.title("WELCOME TO FAMILY GAME")

n = st.number_input("Enter number of players (2–4):", min_value=2, max_value=4)
player_names = []

for i in range(int(n)):
    player_names.append(st.text_input(f"Enter name for player {i+1}:"))

if st.button("Submit"):
    st.session_state.submitted = True
    st.session_state.positions = {name: 0 for name in player_names}
    icons = ['🐭', '🦁', '🐥', '🐨']
    st.session_state.player_icons = {
        player: icons[i] for i, player in enumerate(player_names)
    }
    st.session_state.activities_visible = set()
    st.success("Players added successfully!")

activities = {
    1: "Sing a song", 2: "Dance", 3: "Tell a joke", 4: "Do a funny face",
    5: "Act like an animal", 6: "Do a silly walk", 7: "Safe",
    8: "Imitate a celebrity", 9: "Do a magic trick",
    10: "Recite a tongue twister", 11: "Do a cartwheel",
    12: "Balance on one foot", 13: "Hop like a bunny",
    14: "Prank call", 15: "Clap your hands", 16: "Stomp your feet",
    17: "Spin around", 18: "Jump in place", 19: "Make a silly face",
    20: "Order pizzas", 21: "Pretend to be a superhero",
    22: "Pretend to be a pirate", 23: "Pretend to be a dinosaur",
    24: "Hop 10 times", 25: "Pretend to be a teacher",
    26: "Pretend to be a doctor", 27: "Pretend to be a firefighter",
    28: "Pretend to be a police officer", 29: "Pretend to be an astronaut",
    30: "You Win"
}

def roll_dice(name):
    dice = random.randint(1, 6)
    st.write(f"{name} rolled a {dice}")

    pos = st.session_state.positions[name] + dice

    if pos > 30:
        pos = 30 - (pos - 30)
        st.write(f"{name} bounced back to {pos}")

    st.session_state.positions[name] = pos
    st.session_state.activities_visible.add(pos)

    st.write(f"{name} is now at {pos}")

    if pos == 30:
        st.balloons()
        st.success(f"{name} WINS THE GAME!")

def fill_cell(num):
    text = str(num)

    if num in st.session_state.activities_visible:
        text += "\n" + activities[num]

    for player, pos in st.session_state.positions.items():
        if pos == num:
            text += " " + st.session_state.player_icons[player]

    return text

if st.session_state.get("submitted"):

    st.subheader("Roll the Dice")
    for name in st.session_state.positions.keys():
        if st.button(f"Roll Dice - {name}", key=f"roll_{name}"):
            roll_dice(name)

    st.subheader("Player Positions")
    for name, pos in st.session_state.positions.items():
        st.write(f"{name}: {pos}")

    st.subheader("Game Board (1 to 30)")

    board = []
    for r in range(3):
        row = list(range(r * 10 + 1, r * 10 + 11))
        if r % 2 == 1:
            row.reverse()
        board.append(row)

    numeric_df = pd.DataFrame(board[::-1])
    display_df = numeric_df.applymap(fill_cell)

    display_df = display_df.applymap(lambda x: f"{x}  ")

    def color_cell(value):
        try:
            n = int(value.split()[0])
        except:
            return ""

        if n == 30:
            return "background-color: gold"
        elif n % 2 == 0:
            return "background-color: lightblue"
        else:
            return "background-color: lightcoral"

    