import cv2, pygame, mediapipe as mp, random, math, sys, time, os


# ---------- INIT ----------
pygame.init(); pygame.mixer.init()
W, H = 960, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("🔥 AR Fruit Ninja - Endless Lives Mode")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("arial", 32)
sfont  = pygame.font.SysFont("arial", 24)
bfont  = pygame.font.SysFont("arial", 80)


# ---------- SOUND ----------
def load_sound(path):
    try: return pygame.mixer.Sound(path)
    except: print("no sound:", path); return None


hit_snd   = load_sound("sounds/apple.mp3")
bomb_snd  = load_sound("sounds/bomb.mp3")


# ---------- HIGH SCORE ----------
HS_FILE = "high_score.txt"


def load_high_score():
    if not os.path.exists(HS_FILE): return 0
    try:
        with open(HS_FILE, "r") as f:
            return int(f.read().strip() or 0)
    except:
        return 0


def save_high_score(score):
    try:
        with open(HS_FILE, "w") as f:
            f.write(str(score))
    except:
        pass


high_score = load_high_score()


# ---------- CAMERA & MEDIAPIPE ----------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("no cam"); pygame.quit(); sys.exit()


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ---------- IMAGES ----------
BASE = 80
BOMB_BASE = 90
KNIFE_BASE = 80
HEART_SIZE = 40


def load_img(path, size):
    try:
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), size)
    except:
        print("no img:", path); return None


# fruits + slow‑motion power‑up
fruit_files = {
    "apple":      "images/apple.png",
    "grapes":     "images/grapes.png",
    "strawberry": "images/strawberry.png",
    "banana":     "images/banana.png",
    "slow":       "images/slow.png"
}
bomb_file   = "images/bomb.png"
knife_file  = "images/knife.png"
heart_file  = "images/heart.png"


base_fruits = {k: load_img(v, (BASE, BASE)) for k, v in fruit_files.items()}
base_bomb   = load_img(bomb_file, (BOMB_BASE, BOMB_BASE))
base_knife  = load_img(knife_file, (KNIFE_BASE, KNIFE_BASE))
heart_img   = load_img(heart_file, (HEART_SIZE, HEART_SIZE))


FRUIT_PTS = {"apple": 5, "grapes": 3, "strawberry": 4, "banana": 2}
BOMB_PTS  = -5


# Fixed sizes (no level scaling)
scaled_fruits = {k: v for k, v in base_fruits.items()}
scaled_bomb   = base_bomb
scaled_knife  = base_knife


# ---------- CLASSES ----------
class Fruit:
    def __init__(self, kind, slow_factor=1.0):
        self.kind = kind
        self.x = random.randint(100, W-100)
        self.y = H + 50
        base_speed = random.uniform(4, 7)  # Fixed speed
        self.base_speed = base_speed
        self.speed = base_speed * slow_factor
        self.angle = random.randint(0, 360)
        self.rot = random.choice([-5, -4, 4, 5])
        if kind == "bomb":
            self.img = scaled_bomb
            self.r = int(BOMB_BASE/2)
        else:
            self.img = scaled_fruits.get(kind)
            self.r = int(BASE/2)

    def apply_slow(self, slow_factor):
        self.speed = self.base_speed * slow_factor

    def update(self):
        self.y -= self.speed
        self.angle += self.rot

    def draw(self):
        if self.img:
            img = pygame.transform.rotate(self.img, self.angle)
            screen.blit(img, img.get_rect(center=(self.x, self.y)))
        else:
            c = (100,100,100) if self.kind=="bomb" else (255,0,0)
            pygame.draw.circle(screen, c, (int(self.x), int(self.y)), self.r)


class FX:
    def __init__(self,x,y,col,big=False):
        self.cx,self.cy=x,y; self.big=big; self.r=0
        self.sparks=[[x,y,random.uniform(-10,10),random.uniform(-10,10),
                      random.randint(20,40),col,random.randint(2,4)]
                     for _ in range(100 if big else 50)]
    def update(self):
        self.r += 12 if self.big else 6
        for s in self.sparks[:]:
            s[0]+=s[2]; s[1]+=s[3]; s[4]-=1
            if s[4]<=0: self.sparks.remove(s)
    def draw(self):
        c=(255,60,0) if self.big else (0,255,0)
        pygame.draw.circle(screen,c,(int(self.cx),int(self.cy)),
                           self.r,6 if self.big else 4)
        for x,y,_,_,life,col,size in self.sparks:
            if life>0: pygame.draw.circle(screen,col,(int(x),int(y)),size)
    def done(self): return (self.r>180 if self.big else self.r>80) and not self.sparks


class FloatScore:
    def __init__(self,x,y,text,col):
        self.x,self.y,self.t,self.c=x,y,text,col; self.life=25
    def update(self): self.y-=1.5; self.life-=1
    def draw(self):
        surf=sfont.render(self.t,True,self.c)
        screen.blit(surf,surf.get_rect(center=(int(self.x),int(self.y))))
    def done(self): return self.life<=0


# ---------- GAME STATE ----------
def reset_state():
    return dict(
        fruits=[], fxs=[], floats=[],
        score=0,
        lives=3,
        game_over=False,
        slow_until=0.0,
        next_spawn=0.0
    )


state = reset_state()
sx, sy = W//2, H//2


MODE_MENU, MODE_PLAY = 0, 1
mode = MODE_MENU


# ---------- MAIN LOOP ----------
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Smoother 60 FPS

    for e in pygame.event.get():
        if e.type == pygame.QUIT: running=False
        if e.type == pygame.KEYDOWN:
            if mode == MODE_MENU and e.key == pygame.K_SPACE:
                mode = MODE_PLAY; state = reset_state()
            elif mode == MODE_PLAY and state["game_over"] and e.key == pygame.K_r:
                state = reset_state()

    if mode == MODE_MENU:
        screen.fill((0,0,0))
        title = bfont.render("AR Fruit Ninja", True, (255,215,0))
        screen.blit(title, title.get_rect(center=(W//2, H//2-80)))
        hs = font.render(f"High Score: {high_score}", True, (255,255,255))
        screen.blit(hs, hs.get_rect(center=(W//2, H//2)))
        lives_text = font.render("3 LIVES - Slice until you lose all!", True, (0,255,0))
        screen.blit(lives_text, lives_text.get_rect(center=(W//2, H//2+60)))
        info = sfont.render("Press SPACE to start", True, (0,255,0))
        screen.blit(info, info.get_rect(center=(W//2, H//2+100)))
        pygame.display.flip()
        continue

    # ---------- CAMERA ----------
    ret, frame = cap.read()
    if not ret: continue
    frame = cv2.flip(frame,1); frame = cv2.resize(frame,(W,H))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    tx, ty = sx, sy
    if res.multi_hand_landmarks:
        tip = res.multi_hand_landmarks[0].landmark[8]
        tx, ty = int(tip.x*W), int(tip.y*H)-5
    sx += int((tx-sx)*0.35); sy += int((ty-sy)*0.35)

    screen.blit(pygame.surfarray.make_surface(rgb.swapaxes(0,1)), (0,0))

    now = time.time()
    slow_factor = 0.4 if now < state["slow_until"] else 1.0

    # ---------- SPAWN (ENDLESS) ----------
    if not state["game_over"]:
        spawn_interval = 1.0  # Fixed spawn every 1 second
        bomb_chance = 0.15
        slow_chance = 0.05

        if now >= state["next_spawn"]:
            state["next_spawn"] = now + spawn_interval
            r = random.random()
            if r < slow_chance:
                kind = "slow"
            else:
                r2 = random.random()
                kinds = list(FRUIT_PTS.keys())
                kind = "bomb" if r2 < bomb_chance else random.choice(kinds)
            state["fruits"].append(Fruit(kind, slow_factor))

    # ---------- UPDATE FRUITS ----------
    for f in state["fruits"][:]:
        f.apply_slow(slow_factor)
        f.update(); f.draw()

        if math.hypot(sx-f.x, sy-f.y) < f.r and not state["game_over"]:
            if f.kind == "bomb":
                state["score"] += BOMB_PTS
                state["lives"] -= 1
                if bomb_snd: bomb_snd.play()
                state["fxs"].append(FX(f.x,f.y,(255,0,0),big=True))  # Big red bomb explosion
                if state["lives"] <= 0:  # GAME ENDS ONLY HERE
                    state["game_over"] = True
            elif f.kind == "slow":
                state["slow_until"] = now + 5
                state["fxs"].append(FX(f.x,f.y,(0,255,255)))
                state["floats"].append(FloatScore(sx+30, sy-30, "SLOW", (0,255,255)))
                if hit_snd: hit_snd.play()
            else:
                pts = FRUIT_PTS[f.kind]
                state["score"] += pts
                if hit_snd: hit_snd.play()
                state["fxs"].append(FX(f.x,f.y,(0,255,0)))
                state["floats"].append(FloatScore(sx+30, sy-30, f"+{pts}", (0,255,0)))
            state["fruits"].remove(f)

        elif f.y < -60:
            state["fruits"].remove(f)

    # ---------- EFFECTS ----------
    for fx in state["fxs"][:]:
        fx.update(); fx.draw()
        if fx.done(): state["fxs"].remove(fx)

    for fs in state["floats"][:]:
        fs.update(); fs.draw()
        if fs.done(): state["floats"].remove(fs)

    # ---------- KNIFE + SCORE ----------
    pygame.draw.circle(screen,(200,255,0),(sx,sy),32,4)
    if scaled_knife:
        screen.blit(scaled_knife, scaled_knife.get_rect(center=(sx,sy)))
    score_text = sfont.render(str(state["score"]),True,(255,255,255))
    screen.blit(score_text, score_text.get_rect(center=(sx,sy)))

    # ---------- TOP INFO ----------
    screen.blit(font.render(f"Score: {state['score']}",True,(255,255,255)),(20,20))
    screen.blit(font.render(f"Lives: {state['lives']}",True,(255,0,0)),(20,60))
    screen.blit(font.render(f"High: {high_score}",True,(255,255,0)),(20,100))

    # lives as hearts
    if heart_img:
        for i in range(state["lives"]):
            screen.blit(heart_img, (W- (i+1)*(HEART_SIZE+5) - 10, 20))

    # slow status
    if slow_factor < 1.0:
        txt = sfont.render("SLOW MO!",True,(0,255,255))
        screen.blit(txt,(W-120,60))

    # ---------- GAME OVER ----------
    if state["game_over"]:
        if state["score"] > high_score:
            high_score = state["score"]
            save_high_score(high_score)
        overlay = pygame.Surface((W,H)); overlay.set_alpha(180); overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))
        msg = bfont.render("GAME OVER",True,(255,50,50))
        screen.blit(msg, msg.get_rect(center=(W//2,H//2-40)))
        final_score = font.render(f"Final: {state['score']}",True,(255,255,255))
        screen.blit(final_score, final_score.get_rect(center=(W//2,H//2)))
        restart = font.render("Press R to restart",True,(0,255,0))
        screen.blit(restart, restart.get_rect(center=(W//2,H//2+60)))

    pygame.display.flip()

cap.release(); pygame.quit(); sys.exit()
