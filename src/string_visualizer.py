import turtle
import math
import random
import time
from itertools import combinations

# --- CONFIGURATION ---
NUM_PINS = 32           # Number of nails on the ring
RADIUS = 250            # Radius of the ring in pixels
WINDOW_SIZE = 600       # Size of the window
ANIMATION_SPEED = 0     # 0 = fastest
RESET_DELAY = 100       # Short delay (in ms) after drawing

# Calculate position (x, y) for a given nail number
def get_pin_coords(pin_index):
    angle = (2 * math.pi * pin_index) / NUM_PINS
    x = RADIUS * math.cos(angle)
    y = RADIUS * math.sin(angle)
    return x, y

# ==========================================
# PART 1: SEQUENCE GENERATORS (All 12+)
# Each function returns a LIST of nail numbers (int)
# ==========================================

def pattern_star_skip(skip=13):
    """1. Star/Polygon: Skips a constant number of nails (skip)."""
    sequence = [0]
    current = 0
    for _ in range(NUM_PINS * 2): 
        current = (current + skip) % NUM_PINS
        if current == sequence[0]:
            sequence.append(current)
            break
        sequence.append(current)
    return sequence

def pattern_envelope_curve(offset=1):
    """2. Envelope Curve: Creates a hyperbolic curve (offset is the step left/right)."""
    sequence = []
    for i in range(NUM_PINS):
        pin_a = i
        pin_b = (NUM_PINS - 1 - i + offset) % NUM_PINS
        sequence.append(pin_a)
        sequence.append(pin_b)
    sequence.append(0)
    return sequence

def pattern_zigzag_layer(offset=12):
    """3. Layered Zig-Zag: Jumps forward by 'offset', then moves back a small step."""
    sequence = [0]
    current = 0
    for i in range(NUM_PINS * 2): 
        forward = (current + offset) % NUM_PINS
        sequence.append(forward)
        current = (current + 1) % NUM_PINS
        sequence.append(current)
        if current == 0 and i > NUM_PINS / 2:
            break
    return sequence

def pattern_flower_mandala():
    """4. Mandala/Flower: Connects a near point with an opposite point, creating a circular indentation."""
    sequence = []
    half = NUM_PINS // 2
    for i in range(NUM_PINS):
        sequence.append(i)          
        sequence.append((i + half) % NUM_PINS) 
    sequence.append(0) 
    return sequence

def pattern_chaos_random():
    """5. Chaos: Random sequence visiting all nails once."""
    pins = list(range(NUM_PINS))
    random.shuffle(pins)
    pins.append(pins[0])
    return pins

def pattern_double_bounce(jump_a=11, jump_b=10):
    """6. Double Bounce: Switches between two different 'skips'."""
    sequence = [0]
    current = 0
    for i in range(NUM_PINS * 2): 
        if i % 2 == 0:
            current = (current + jump_a) % NUM_PINS
        else:
            current = (current + jump_b) % NUM_PINS
        sequence.append(current)
        if current == sequence[0] and i > 1:
            break
    return sequence

def pattern_sierpinski_style(divisor=3):
    """7. Sierpinski Style: Uses modulo (e.g., 3) to choose the next point."""
    sequence = [0]
    current = 0
    for i in range(NUM_PINS * 2): 
        current = (current + divisor) % NUM_PINS 
        sequence.append(current)
        if current == sequence[0] and i > 1:
            break
    return sequence

def pattern_offset_cardioid(multiplier=2):
    """8. Cardioid (Classic): Connects pin 'i' to pin 'i * multiplier' (creates a heart/kidney shape)."""
    sequence = []
    for i in range(NUM_PINS):
        sequence.append(i)
        next_pin = (i * multiplier) % NUM_PINS
        sequence.append(next_pin)
    sequence.append(0)
    return sequence

def pattern_progressive_spiral(start_jump=1, step_increase=1):
    """9. Progressive Spiral: Increases 'skip' by a constant value each step."""
    sequence = [0]
    current = 0
    jump = start_jump
    for i in range(NUM_PINS * 4): # Longer loop for a better spiral
        current = (current + jump) % NUM_PINS
        sequence.append(current)
        jump += step_increase
        if current == sequence[0] and i > NUM_PINS:
            break
    return sequence

def pattern_inward_outward(in_step=1, out_step=15):
    """10. Inward/Outward: Alternates jumping forward by a small value and back by a large one."""
    sequence = [0]
    current = 0
    for i in range(NUM_PINS * 2):
        if i % 2 == 0:
            current = (current + in_step) % NUM_PINS
        else:
            current = (current + out_step) % NUM_PINS
        sequence.append(current)
        if current == sequence[0] and i > 1:
            break
    return sequence

def pattern_triple_star(skip_1=3, skip_2=8):
    """11. Triple Star: Uses three different jumps cyclically."""
    sequence = [0]
    current = 0
    skips = [skip_1, skip_2, skip_1 + skip_2]
    
    for i in range(NUM_PINS * 3):
        jump = skips[i % 3]
        current = (current + jump) % NUM_PINS
        sequence.append(current)
        if current == sequence[0] and i > 2:
            break
    return sequence

def pattern_half_and_quarter(skip_half=16, skip_quarter=8):
    """12. Half & Quarter: Connects points separated by half and quarter of the circumference."""
    sequence = [0]
    current = 0
    skips = [skip_half, skip_quarter]
    
    for i in range(NUM_PINS * 2):
        jump = skips[i % 2]
        current = (current + jump) % NUM_PINS
        sequence.append(current)
        if current == sequence[0] and i > 1:
            break
    return sequence
    
def pattern_full_coverage():
    """13. Full Coverage: Draws lines between all pairs of pins (very dense)."""
    sequence = []
    for i, j in combinations(range(NUM_PINS), 2):
        sequence.append(i)
        sequence.append(j)
    return sequence


# ==========================================
# PART 2: SEQUENCE CONFIGURATION AND AUTO-GENERATION
# ==========================================

# List of dictionaries for automatic sequence generation
SEQUENCE_LIST = [
    # Format: [Name, Function, List of parameter values]
    
    ["1. Star (Skip)", pattern_star_skip, [7, 13, 3]],
    ["2. Envelope Curve", pattern_envelope_curve, [1, 5]],
    ["3. ZigZag Layer", pattern_zigzag_layer, [12, 5]],
    ["4. Flower Mandala", pattern_flower_mandala, [None]],
    ["5. Double Bounce", pattern_double_bounce, [(7, 15),(11,17)]],
    ["6. Sierpinski Style", pattern_sierpinski_style, [3, 5]],
    ["7. Offset Cardioid", pattern_offset_cardioid, [1,2,3,4,5,6,7,8,9,10]],
    ["8. Progressive Spiral", pattern_progressive_spiral, [(1, 2), (3, 1)]],
    ["9. Inward Outward", pattern_inward_outward, [(2, 10)]],
    ["10. Triple Star", pattern_triple_star, [(3, 8), (4, 7)]],
    ["11. Half & Quarter", pattern_half_and_quarter, [(14, 6)]],
    ["12. Chaos Random", pattern_chaos_random, [None]],
    ["13. Full Coverage", pattern_full_coverage, [None]]
]

# ==========================================
# PART 3: VISUALIZATION (TURTLE)
# ==========================================

# Flag used to block the program
WAIT_FOR_KEY_PRESS = False

def handle_key_press():
    """Key handler function that unlocks the loop"""
    global WAIT_FOR_KEY_PRESS
    WAIT_FOR_KEY_PRESS = False
    
def setup_turtle():
    screen = turtle.Screen()
    screen.setup(WINDOW_SIZE, WINDOW_SIZE)
    screen.bgcolor("black")
    screen.title("String Art Sequence Generator")
    
    # Turtle for lines (Drawer)
    t_line = turtle.Turtle()
    t_line.speed(ANIMATION_SPEED)
    t_line.hideturtle()
    
    # Turtle for text (Label)
    t_text = turtle.Turtle()
    t_text.speed(0)
    t_text.hideturtle()
    t_text.penup()
    t_text.goto(0, RADIUS + 30)
    
    # Set up key listener for pause
    screen.listen()
    # Any key press (e.g., space) will call handle_key_press
    screen.onkey(handle_key_press, 'space') 
    screen.onkey(handle_key_press, 'Return') 
    
    return t_line, t_text, screen

def draw_pins(t):
    """Draws nails on the circle"""
    t.penup()
    t.color("red")
    for i in range(NUM_PINS):
        x, y = get_pin_coords(i)
        t.goto(x, y)
        t.dot(5) 

def draw_sequence(t, sequence, color="cyan"):
    """Draws lines based on the list of nail numbers"""
    if not sequence: return

    t.color(color)
    t.pensize(1)
    
    sx, sy = get_pin_coords(sequence[0])
    t.penup()
    t.goto(sx, sy)
    t.pendown()
    
    for pin in sequence[1:]:
        x, y = get_pin_coords(pin)
        t.goto(x, y)

def display_sequence_name(t_text, name, params, wait=False):
    """Displays the name of the current sequence and the waiting message"""
    t_text.clear()
    param_str = f"Params: {params}" if params is not None else "Default"
    wait_msg = " [PRESS SPACE/ENTER]" if wait else ""
    t_text.color("white")
    t_text.write(f"{name} ({param_str}){wait_msg}", align="center", font=("Arial", 14, "bold"))

def main():
    global WAIT_FOR_KEY_PRESS
    t_line, t_text, screen = setup_turtle()
    
    # Draw static nails once at the start
    draw_pins(t_line)
    
    # Turn off animation for instant drawing
    screen.tracer(0) 
    
    for seq_data in SEQUENCE_LIST:
        name, func, params_list = seq_data
        
        for param in params_list:
            if param is None:
                param_display = "Default"
            else:
                param_display = str(param)

            # Generate the actual sequence points
            if param is None:
                seq = func()
            elif isinstance(param, tuple):
                seq = func(*param)
            else:
                seq = func(param)
            
            # 2. DRAWING
            t_line.clear() 
            t_line.penup()
            draw_pins(t_line) 
            
            # Update label to show what is currently being drawn
            display_sequence_name(t_text, name, param_display, wait=False) 
            
            # Draw the lines
            draw_sequence(t_line, seq, color="#00FFFF") 
            
            # Print to console immediately
            print(f"--- {name} ({param_display}) ---")
            print(f"Sequence length: {len(seq)} moves")
            print(f"Sequence: {seq}") 

            # Refresh screen to show the finished pattern
            screen.update() 
            
            # 3. WAIT FOR USER (Pause after drawing is done)
            WAIT_FOR_KEY_PRESS = True
            # Update text to show the "Press Space" prompt
            display_sequence_name(t_text, name, param_display, wait=True)
            screen.update()
            
            while WAIT_FOR_KEY_PRESS:
                screen.update() 
                time.sleep(0.01) 
            
    print("\nEnd of all sequences. Click in the window to close.")
    screen.exitonclick()
if __name__ == "__main__":
    main()