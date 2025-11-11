from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

MAZE = [
    ['#','#','#','#','#','#','#','#','#','S','#','#','#','#','#','#','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','#',' ','#'],
    ['#',' ','#','#','#','#',' ','#','#','#','#',' ','#',' ','#',' ',' ',' ','#'],
    ['#',' ','#',' ','#',' ',' ','#',' ',' ',' ',' ','#',' ','#','#','#','#','#'],
    ['#',' ',' ',' ','#',' ','#','#','#','#','#','#','#',' ',' ',' ',' ',' ','#'],
    ['#','#','#','#','#',' ',' ',' ',' ','#',' ',' ',' ',' ','#','#','#',' ','#'],
    ['#',' ',' ',' ',' ',' ','#','#',' ',' ',' ','#','#','#','#',' ',' ',' ','#'],
    ['#','#','#',' ','#','#','#','#','#','#','#','#',' ',' ',' ',' ','#',' ','#'],
    ['#',' ','#',' ','#',' ',' ',' ',' ',' ',' ',' ',' ','#','#',' ','#','#','#'],
    ['#',' ','#',' ','#',' ','#','#','#',' ','#',' ','#','#','#',' ','#',' ','#'],
    ['#',' ','#',' ',' ',' ','#',' ','#',' ','#',' ','#',' ',' ',' ','#',' ','#'],
    ['#',' ','#',' ','#',' ','#',' ','#','#','#',' ','#','#','#',' ',' ',' ','#'],
    ['#',' ',' ',' ','#',' ','#',' ',' ',' ','#',' ',' ',' ',' ',' ','#',' ','#'],
    ['#','#','#',' ','#',' ','#',' ','#','#','#','#','#','#','#','#','#',' ','#'],
    ['#',' ',' ',' ','#',' ',' ',' ','#',' ',' ','#',' ','#','#',' ','#',' ','#'],
    ['#',' ','#','#','#','#','#',' ','#','#',' ','#',' ','#','#',' ','#','#','#'],
    ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','#'],
    ['#',' ','#',' ','#','#','#','#','#',' ','#',' ','#',' ',' ',' ','#',' ','#'],
    ['#',' ','#',' ',' ',' ',' ',' ','#',' ','#',' ','#',' ','#',' ','#',' ','#'],
    ['#','#','#','#','#','#','#','#','#','F','#','#','#','#','#','#','#','#','#']
]

def find_symbol(maze, symbol):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == symbol:
                return (r, c)
    return None

def is_open(maze, r, c):
    if r < 0 or c < 0 or r >= len(maze) or c >= len(maze[0]):
        return False
    return maze[r][c] != '#'

def available_directions(maze, r, c):
    directions = []
    if is_open(maze, r - 1, c): directions.append("up")
    if is_open(maze, r + 1, c): directions.append("down")
    if is_open(maze, r, c - 1): directions.append("left")
    if is_open(maze, r, c + 1): directions.append("right")
    return directions

# Global position (reset per call)
player_pos = list(find_symbol(MAZE, 'S'))

@app.route("/voice", methods=["POST"])
def voice():
    """Start of a new call"""
    start = find_symbol(MAZE, 'S')
    player_pos[0], player_pos[1] = start

    resp = VoiceResponse()
    resp.say(
        "Welcome to the Maze Challenge. "
        "Use the number pad to move: eight for up, two for down, four for left, and six for right. "
        "At any time, press nine to restart from the beginning.",
        voice="alice", language="en-GB"
    )

    gather = Gather(num_digits=1, action="/move", method="POST", timeout=10)
    gather.say("Press a direction to begin.", voice="alice", language="en-GB")
    resp.append(gather)

    resp.say("No input received. Goodbye.", voice="alice")
    resp.hangup()
    return Response(str(resp), mimetype="text/xml")


@app.route("/move", methods=["POST"])
def move():
    """Handle keypad movement"""
    digits = request.form.get('Digits')
    resp = VoiceResponse()

    if not digits:
        resp.say("No input detected. Try again.", voice="alice")
        return gather_prompt(resp)

    key = digits.strip()
    dr, dc = 0, 0

    if key == '8': dr, dc = -1, 0
    elif key == '2': dr, dc = 1, 0
    elif key == '4': dr, dc = 0, -1
    elif key == '6': dr, dc = 0, 1
    elif key == '9':
        start = find_symbol(MAZE, 'S')
        player_pos[0], player_pos[1] = start
        resp.say("Maze restarted. You're back at the start.", voice="alice")
        return gather_prompt(resp)
    else:
        resp.say("Invalid key. Use eight, two, four, six, or nine to restart.", voice="alice")
        return gather_prompt(resp)

    r, c = player_pos
    nr, nc = r + dr, c + dc

    # wall or out of bounds
    if nr < 0 or nc < 0 or nr >= len(MAZE) or nc >= len(MAZE[0]) or MAZE[nr][nc] == '#':
        directions = available_directions(MAZE, r, c)
        dir_text = ", ".join(directions)
        resp.say(f"You hit a wall. You can go {dir_text}.", voice="alice", language="en-GB")
        return gather_prompt(resp)

    # successful move
    player_pos[0], player_pos[1] = nr, nc

    if MAZE[nr][nc] == 'F':
        resp.say("Congratulations! You reached the finish!", voice="alice", language="en-GB")
        resp.hangup()
        return Response(str(resp), mimetype="text/xml")

    # Silent move — no feedback unless a wall is hit
    return gather_prompt(resp)


def gather_prompt(resp):
    """Prompt the user for their next move"""
    gather = Gather(num_digits=1, action="/move", method="POST", timeout=10)
    gather.say("Press eight for up, two for down, four for left, six for right, or nine to restart.", voice="alice", language="en-GB")
    resp.append(gather)
    resp.say("No input received. Goodbye.", voice="alice")
    resp.hangup()
    return Response(str(resp), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


# Example solve path:
# 8 = DOWN
# 2 = UP
# 4 = LEFT
# 6 = RIGHT 
#
# 8444884888448888668888668866888