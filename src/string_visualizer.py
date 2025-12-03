import turtle
import math
import random
import time
from itertools import combinations

# --- KONFIGURACJA ---
NUM_PINS = 32           # Liczba gwoździ na okręgu
RADIUS = 250            # Promień okręgu w pikselach
WINDOW_SIZE = 600       # Rozmiar okna
ANIMATION_SPEED = 0     # 0 = najszybciej
RESET_DELAY = 100       # Krótkie opóźnienie (w ms) po rysowaniu

# Obliczanie pozycji (x, y) dla danego numeru gwoździa
def get_pin_coords(pin_index):
    angle = (2 * math.pi * pin_index) / NUM_PINS
    x = RADIUS * math.cos(angle)
    y = RADIUS * math.sin(angle)
    return x, y

# ==========================================
# CZĘŚĆ 1: GENERATORY SEKWENCJI (Wszystkie 12+)
# Każda funkcja zwraca LISTĘ numerów gwoździ (int)
# ==========================================

def pattern_star_skip(skip=13):
    """1. Gwiazda/Wielokąt: Przeskakuje o stałą liczbę gwoździ (skip)."""
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
    """2. Krzywa Koperta: Tworzy hiperboliczną krzywą (offset to krok w lewo/prawo)."""
    sequence = []
    for i in range(NUM_PINS):
        pin_a = i
        pin_b = (NUM_PINS - 1 - i + offset) % NUM_PINS
        sequence.append(pin_a)
        sequence.append(pin_b)
    sequence.append(0)
    return sequence

def pattern_zigzag_layer(offset=12):
    """3. Zig-Zag Warstwowy: Skacze do przodu o 'offset', potem cofa się o mały krok."""
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
    """4. Mandala/Kwiat: Łączy bliski punkt z przeciwległym punktem, tworząc okrągłe wcięcie."""
    sequence = []
    half = NUM_PINS // 2
    for i in range(NUM_PINS):
        sequence.append(i)          
        sequence.append((i + half) % NUM_PINS) 
    sequence.append(0) 
    return sequence

def pattern_chaos_random():
    """5. Chaos: Losowa sekwencja odwiedzająca wszystkie gwoździe raz."""
    pins = list(range(NUM_PINS))
    random.shuffle(pins)
    pins.append(pins[0])
    return pins

def pattern_double_bounce(jump_a=11, jump_b=10):
    """6. Podwójne Odbicie: Przełącza się między dwoma różnymi 'skipami'."""
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
    """7. Styl Sierpińskiego: Używa modulo (np. 3) do wyboru następnego punktu."""
    sequence = [0]
    current = 0
    for i in range(NUM_PINS * 2): 
        current = (current + divisor) % NUM_PINS 
        sequence.append(current)
        if current == sequence[0] and i > 1:
            break
    return sequence

def pattern_offset_cardioid(multiplier=2):
    """8. Kardioida (Klasyczna): Łączy pin 'i' z pinem 'i * multiplier' (tworzy serce/nerkę)."""
    sequence = []
    for i in range(NUM_PINS):
        sequence.append(i)
        next_pin = (i * multiplier) % NUM_PINS
        sequence.append(next_pin)
    sequence.append(0)
    return sequence

def pattern_progressive_spiral(start_jump=1, step_increase=1):
    """9. Spirala Progresywna: Zwiększa 'skip' o stałą wartość w każdym kroku."""
    sequence = [0]
    current = 0
    jump = start_jump
    for i in range(NUM_PINS * 4): # Dłuższa pętla dla lepszej spirali
        current = (current + jump) % NUM_PINS
        sequence.append(current)
        jump += step_increase
        if current == sequence[0] and i > NUM_PINS:
            break
    return sequence

def pattern_inward_outward(in_step=1, out_step=15):
    """10. Dośrodkowy/Odśrodkowy: Naprzemiennie skacze do przodu o małą wartość i cofa się o dużą."""
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
    """11. Potrójna Gwiazda: Używa trzech różnych skoków cyklicznie."""
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
    """12. Pół i Ćwierć: Łączy punkty oddalone o połowę i ćwierć obwodu."""
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
    """13. Pełne Pokrycie: Rysuje linie pomiędzy wszystkimi parami pinów (bardzo gęste)."""
    sequence = []
    for i, j in combinations(range(NUM_PINS), 2):
        sequence.append(i)
        sequence.append(j)
    return sequence


# ==========================================
# CZĘŚĆ 2: KONFIGURACJA SEKWENCJI I AUTOMATYCZNE GENEROWANIE
# ==========================================

# Lista słowników do automatycznego generowania sekwencji
SEQUENCE_LIST = [
    # Format: [Nazwa, Funkcja, Lista wartości parametrów]
    
    # ["1. Star (Skip)", pattern_star_skip, [7, 13, 3]],
    # ["2. Envelope Curve", pattern_envelope_curve, [1, 5]],
    # ["3. ZigZag Layer", pattern_zigzag_layer, [12, 5]],
    # ["4. Flower Mandala", pattern_flower_mandala, [None]],
    ["5. Double Bounce", pattern_double_bounce, [(7, 15),(11,17)]], #(1+2,3+2),(1+2,5+2),(1+2,7+2),(1+2,9+2),(1+2,11+2),(1+2,13+2),(1+4,3+4),(1+4,5+4),(1+4,7+4),(1+4,9+4),(1+4,11+4),(1+4,13+4),(1+6,3+6),(1+6,5+6),(1+6,7+6),(1+6,9+6),(1+6,11+6),(1+6,13+6),(1+8,3+8),(1+8,5+8),(1+8,7+8),(1+8,9+8),(1+8,11+8),(1+8,13+8),(1+10,3+10),(1+10,5+10),(1+10,7+10),(1+10,9+10),(1+10,11+10),(1+10,13+10)]],
    # ["6. Sierpinski Style", pattern_sierpinski_style, [3, 5]],
    # ["7. Offset Cardioid", pattern_offset_cardioid, [1,2,3,4,5,6,7,8,9,10]],
    # ["8. Progressive Spiral", pattern_progressive_spiral, [(1, 2), (3, 1)]],
    # ["9. Inward Outward", pattern_inward_outward, [(2, 10)]],
    # # ["10. Triple Star", pattern_triple_star, [(3, 8), (4, 7)]],
    # ["11. Half & Quarter", pattern_half_and_quarter, [(14, 6)]],
    # ["12. Chaos Random", pattern_chaos_random, [None]],
    # ["13. Full Coverage", pattern_full_coverage, [None]]
]

# ==========================================
# CZĘŚĆ 3: WIZUALIZACJA (TURTLE)
# ==========================================

# Flaga używana do blokowania programu
WAIT_FOR_KEY_PRESS = False

def handle_key_press():
    """Funkcja obsługi klawisza, która odblokowuje pętlę"""
    global WAIT_FOR_KEY_PRESS
    WAIT_FOR_KEY_PRESS = False
    
def setup_turtle():
    screen = turtle.Screen()
    screen.setup(WINDOW_SIZE, WINDOW_SIZE)
    screen.bgcolor("black")
    screen.title("String Art Sequence Generator")
    
    # Żółw do linii (Rysownik)
    t_line = turtle.Turtle()
    t_line.speed(ANIMATION_SPEED)
    t_line.hideturtle()
    
    # Żółw do tekstu (Etykieta)
    t_text = turtle.Turtle()
    t_text.speed(0)
    t_text.hideturtle()
    t_text.penup()
    t_text.goto(0, RADIUS + 30)
    
    # Ustawienie nasłuchiwania na klawisz dla pauzy
    screen.listen()
    # Dowolne naciśnięcie klawisza (np. spacji) wywoła handle_key_press
    screen.onkey(handle_key_press, 'space') 
    screen.onkey(handle_key_press, 'Return') 
    
    return t_line, t_text, screen

def draw_pins(t):
    """Rysuje gwoździe na okręgu"""
    t.penup()
    t.color("red")
    for i in range(NUM_PINS):
        x, y = get_pin_coords(i)
        t.goto(x, y)
        t.dot(5) 

def draw_sequence(t, sequence, color="cyan"):
    """Rysuje linie na podstawie listy numerów gwoździ"""
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
    """Wyświetla nazwę aktualnej sekwencji i komunikat o oczekiwaniu"""
    t_text.clear()
    param_str = f"Parametry: {params}" if params is not None else "Domyślne"
    wait_msg = " [NACIŚNIJ SPACJĘ/ENTER]" if wait else ""
    t_text.color("white")
    t_text.write(f"{name} ({param_str}){wait_msg}", align="center", font=("Arial", 14, "bold"))

def main():
    global WAIT_FOR_KEY_PRESS
    t_line, t_text, screen = setup_turtle()
    
    # Rysowanie stałych gwoździ
    draw_pins(t_line)
    
    # Wyłącz animację dla szybkiego rysowania
    screen.tracer(0) 
    
    first_run = True

    for seq_data in SEQUENCE_LIST:
        name, func, params_list = seq_data
        
        for param in params_list:
            
            # 1. BLOKADA OCZEKIWANIA (po pierwszym wzorze)
            if not first_run:
                WAIT_FOR_KEY_PRESS = True
                display_sequence_name(t_text, name, param_display, wait=True)
                screen.update() # Rysuje komunikat
                
                # Czekaj w pętli, aż flaga WAIT_FOR_KEY_PRESS zostanie zmieniona przez handle_key_press()
                while WAIT_FOR_KEY_PRESS:
                    # To pozwala okienkowi Tkinter obsłużyć zdarzenia (jak naciśnięcie klawisza)
                    screen.update() 
                    time.sleep(0.01) # Małe opóźnienie dla wydajności
            
            # 2. GENEROWANIE PARAMETRÓW
            if param is None:
                seq = func()
                param_display = "Domyślne"
            elif isinstance(param, tuple):
                seq = func(*param)
                param_display = str(param)
            else:
                seq = func(param)
                param_display = str(param)
            
            # 3. CZYSZCZENIE I RYSOWANIE
            
            # Użyjemy .resetsize() aby zapobiec bugom z clear, 
            # choć .clear() powinien działać poprawnie, jeśli okno nie jest zamknięte.
            t_line.clear() 
            
            # Resetowanie stanu prędkości i pióra po clear
            t_line.speed(ANIMATION_SPEED) 
            t_line.penup()
            
            draw_pins(t_line) 
            
            # Aktualizuj etykietę bez komunikatu "KLIKNIJ"
            display_sequence_name(t_text, name, param_display, wait=True) 
            
            # Rysowanie sekwencji
            draw_sequence(t_line, seq, color="#00FFFF") 
            
            # Ręczne odświeżenie ekranu, żeby wzór pojawił się natychmiast
            screen.update() 
            
            # Oznaczenie, że pierwszy wzór został już narysowany
            first_run = False 
            
            # Wypisanie sekwencji w konsoli
            print(f"--- {name} ({param_display}) ---")
            print(f"Długość sekwencji: {len(seq)} ruchów")
            print(f"Sekwencja: {seq}") 
            
    print("\nKoniec wszystkich sekwencji. Kliknij w okno, aby zamknąć.")
    screen.exitonclick()

if __name__ == "__main__":
    main()