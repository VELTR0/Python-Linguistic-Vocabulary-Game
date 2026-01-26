import pygame
import Vocabulary
import time
import random
from Font import SpriteFont

pygame.init()

# Sprites (werden später geladen)
selector = None
correct = None
wrong = None
Background = None

def load_sprites():
    global Background, selector, correct, wrong
    Background = pygame.image.load(r"Sprites\Backgrounds\Praise_or_Haze.png").convert_alpha()
    selector = pygame.image.load(r"Sprites\PraiseOrHaze\Selector.png").convert_alpha()
    correct = pygame.image.load(r"Sprites\PraiseOrHaze\Correcto.png").convert_alpha()
    wrong = pygame.image.load(r"Sprites\PraiseOrHaze\Wrong.png").convert_alpha()


def get_all_vocab_pairsIndian():
    """
    Sammelt alle Vokabel-Paare aus Vocabulary.py
    Erwartet mehrere dicts wie:
      { "le": "take", ... }
    """
    pairsIndian = []

    # Nimm alle dict-Variablen aus Vocabulary.py (nur die, die nicht mit _ anfangen)
    for name in dir(Vocabulary):
        # Ignoriere Python interne Attribute (die mit _ anfangen)
        if name.startswith('_'):
            continue
        value = getattr(Vocabulary, name)
        if isinstance(value, dict):
            for indian, english in value.items():
                # Nur hinzufügen, wenn beide Werte Strings sind
                if isinstance(indian, str) and isinstance(english, str):
                    pairsIndian.append((indian, english))

    # Falls doppelte Einträge existieren, ist das egal
    return pairsIndian

def build_question(vocab_pairsIndian):
    """
    Erstellt eine Frage mit 4 Auswahlmöglichkeiten.
    Standard: Indian word -> choose correct English meaning.
    """
    indian, english = random.choice(vocab_pairsIndian)

    # richtige Antwort
    correct_answer = english

    # falsche Antworten sammeln
    all_english = list({e for _, e in vocab_pairsIndian if isinstance(e, str)})
    all_english = [e for e in all_english if e != correct_answer]

    wrong_answers = random.sample(all_english, k=3)

    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    correct_index = options.index(correct_answer)


    q1 = f"{indian} means..."
    questions = [q1]
    question_text = random.choice(questions)
    return question_text, options, correct_index

def startGame(screen):
    load_sprites()
    font = SpriteFont()

    vocab_pairsIndian = get_all_vocab_pairsIndian()

    # Controls
    selected_index = 0
    answered = False
    was_correct = False
    answer_time = 0

    # Erste Frage
    question_text, options, correct_index = build_question(vocab_pairsIndian)

    game_running = True
    clock = pygame.time.Clock()

    while game_running:
        clock.tick(60)

        # Screen clear
        screen.fill((248, 40, 248))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.KEYDOWN and not answered:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % 4

                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % 4

                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    answered = True
                    was_correct = (selected_index == correct_index)
                    answer_time = time.time()

        # Neue Frage nach 1 Sekunde
        if answered and (time.time() - answer_time) > 1.0:
            selected_index = 0
            answered = False
            question_text, options, correct_index = build_question(vocab_pairsIndian)

        # ---------- BACKGROUND ZUERST ----------
        w, h = screen.get_size()
        scaledW = int(w * 0.9)
        scaledH = int(h * 0.9)
        scaledWin = pygame.transform.scale(Background, (scaledW, scaledH))
        centredB = scaledWin.get_rect(center=(w // 2, h // 2))
        screen.blit(scaledWin, centredB)

        # ---------- FRAGE (GELB) ----------
        question_surface = font.render(question_text, color=(255, 255, 0))
        question_surface = pygame.transform.scale_by(question_surface, 4.5)
        qrect = question_surface.get_rect(center=(w // 2, int(h * 0.2)))
        screen.blit(question_surface, qrect)

        # ---------- OPTIONEN (WEIß) ----------
        start_y = int(h * 0.45)
        spacing = int(h * 0.08)

        for i, opt in enumerate(options):
            option_surface = font.render(opt, color=(255, 255, 255))
            option_surface = pygame.transform.scale_by(option_surface, 3.5)

            orect = option_surface.get_rect(center=(w // 2, start_y + i * spacing))
            screen.blit(option_surface, orect)

            # Selector / Correct / Wrong nur bei ausgewählter Option
            if i == selected_index:
                if not answered:
                    arrow_img = pygame.transform.scale_by(selector, 3.75)

                else:
                    arrow_img = pygame.transform.scale_by(correct, 3.75) if was_correct else pygame.transform.scale_by(wrong, 3.75)

                arrow_rect = arrow_img.get_rect(center=(orect.left - 70, orect.centery + 10))
                screen.blit(arrow_img, arrow_rect)

        pygame.display.update()
