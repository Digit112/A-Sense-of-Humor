import os
import pygame as pg
import sys

pg.init()

size = width, height = (1920, 1080)
screen = pg.display.set_mode(size)

from layout import *
from classes import *

#⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
#⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⢀⠍⠙⢿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿
#⠹⣿⣿⣿⣿⣿⣿⣿⠁⠈⢀⡤⢲⣾⣗⠲⣿⣿⣿⣿⣿⣿⣟⠻
#⡀⢙⣿⣿⣿⣿⣿⣿⢀⠰⠁⢰⣾⣿⣿⡇⢀⣿⣿⣿⣿⣿⣿⡄
#⣇⢀⢀⠙⠷⣍⠛⠛⢀⢀⢀⢀⠙⠋⠉⢀⢀⢸⣿⣿⣿⣿⣿⣷
#⡙⠆⢀⣀⠤⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⣿⣿⣿⣿⣿⣿
#⣷⣖⠋⠁⢀⢀⢀⢀⢀⢀⣀⣀⣄⢀⢀⢀⢀⢸⠏⣿⣿⣿⢿⣿
#⣿⣷⡀⢀⢀⢀⢀⢀⡒⠉⠉⢀⢀⢀⢀⢀⢀⢈⣴⣿⣿⡿⢀⡿
#⣿⣿⣷⣄⢀⢀⢀⢀⠐⠄⢀⢀⢀⠈⢀⣀⣴⣿⣿⣿⡿⠁⢀⣡
#⠻⣿⣿⣿⣿⣆⠢⣤⣄⢀⢀⣀⠠⢴⣾⣿⣿⡿⢋⠟⢡⣿⣿⣿
#⢀⠘⠿⣿⣿⣿⣦⣹⣿⣀⣀⣀⣀⠘⠛⠋⠁⡀⣄⣴⣿⣿⣿⣿
#⢀⢀⢀⠈⠛⣽⣿⣿⣿⣿⣿⣿⠁⢀⢀⢀⣡⣾⣿⣿⣿⡟⣹⣿
#⢀⢀⢀⢀⢰⣿⣿⣿⣿⣿⣿⣿⣦⣤⣶⣿⡿⢛⢿⡇⠟⠰⣿⣿
#⢀⢀⢀⢀⣿⣿⣿⡿⢉⣭⢭⠏⣿⡿⢸⡏⣼⣿⢴⡇⢸⣿⣶⣿
#⢀⢀⢀⢰⣿⣿⣿⢃⣶⣶⡏⠸⠟⣱⣿⣧⣛⣣⢾⣿⣿⣿⣿⣿
#⢀⢀⢀⣾⣿⣿⣿⣾⣿⣿⠟⢻⡿⡉⣷⣬⡛⣵⣿⣿⣿⣿⣿⣿
#⢀⢀⣸⣿⣿⣿⣿⣿⣿⡿⢰⠘⣰⣇⣿⣿⣰⣿⣿⣿⣿⣿⣿⣿
#⢀⢀⠘⢿⣿⣿⣿⣿⣿⡷⢺⣿⠟⣩⣭⣽⣇⠲⠶⣿⣿⣿⣿⣿
#⢀⠐⢀⣾⣿⣿⣿⣿⠟⢐⡈⣿⣷⣶⠎⣹⡟⠟⣛⣸⣿⣿⣿⣿
#⠠⢀⣼⣿⣿⣿⣿⣯⣼⣿⣷⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿

def toggle_previewing():
	if g.previewing:
		g.previewing = False
		g.music_playing = False
		pg.mixer.music.pause()
		
	else:
		g.previewing = True
		
		if g.tmr > 0:
			g.music_playing = True
			pg.mixer.music.unpause()

def toggle_paused():
	if g.editing and not g.previewing:
		if g.paused:
			g.paused = False
		else:
			g.paused = True
		
	else:
		if g.paused:
			g.paused = False
			if g.music_playing:
				pg.mixer.music.unpause()
		else:
			g.paused = True
			if g.music_playing:
				pg.mixer.music.pause()

def toggle_options():
	pass

def toggle_editing():
	if g.editing:
		g.editing = False
		g.placing = False
		
		if g.tmr > 0:
			g.music_playing = True
			pg.mixer.music.unpause()
		
		# Unhide game overlay
		player_portrait.hidden = False
		player_name.hidden = False
		player_desc.hidden = False
		
		score_img.hidden = False
		score_label.hidden = False
		score_disp.hidden = False
		
		# Hide editor
		e_name_lbl.hidden = True
		e_name.hidden = True
		e_audio_lbl.hidden = True
		e_audio.hidden = True
		e_bpm.hidden = True
		e_bpm_lbl.hidden = True
		e_load.hidden = True
		e_save.hidden = True
		
		b_s_lbl.hidden = True
		b_s.hidden = True
		a_s_lbl.hidden = True
		a_s.hidden = True
		o_s_lbl.hidden = True
		o_s.hidden = True
		
	else:
		g.editing = True
		g.placing = False
		g.previewing = False
		
		g.music_playing = False
		pg.mixer.music.pause()
		
		g.tmr_targ = g.tmr
		
		# Hide game overlay
		player_portrait.hidden = True
		player_name.hidden = True
		player_desc.hidden = True
		
		score_img.hidden = True
		score_label.hidden = True
		score_disp.hidden = True
		
		# Unhide editor
		e_name_lbl.hidden = False
		e_name.hidden = False
		e_audio_lbl.hidden = False
		e_audio.hidden = False
		e_bpm.hidden = False
		e_bpm_lbl.hidden = False
		e_load.hidden = False
		e_save.hidden = False
		
		b_s_lbl.hidden = False
		b_s.hidden = False
		a_s_lbl.hidden = False
		a_s.hidden = False
		o_s_lbl.hidden = False
		o_s.hidden = False
		
		# Set editor fields
		e_name.set_text(g.name)
		e_audio.set_text(g.audio)
		e_bpm.set_text(str(60000 / g.time_mul))
		
		b_s.set_text(str(g.score_thresh[0]))
		a_s.set_text(str(g.score_thresh[1]))
		o_s.set_text(str(g.score_thresh[2]))
	
	game_l.cache_r()
	pause_l.cache_r()
	
	# Unpause the game.
	toggle_paused()

def quit_to_menu():
	global in_game
	
	hide_level_select()
	in_game = False

def quit():
	pg.quit()
	sys.exit()

def save_chart():
	g.name = e_name.get_text()
	
	tm_notes = [[], [], [], []]
	for i in range(4):
		for n in g.notes[i]:
			tm_notes[i].append(n / g.time_mul)
	
	dat = json.dumps({"name": g.name, "audio": g.audio, "notes": tm_notes, "time_mul": g.time_mul, "score_thresh": g.score_thresh, "speed": g.speed})
	fout = open("charts/custom/" + g.name + ".json", "w")
	fout.write(dat)
	fout.close()

def load_chart():
	g.name = e_name.get_text()
	
	g.load("charts/custom/" + g.name + ".json")
	
	e_audio.set_text(g.audio)
	
	g.reset()

def set_bpm(e_w):
	try:
		g.time_mul = 60000 / float(e_w.get_text())
	except ValueError:
		e_w.set_text(str(60000 / g.time_mul))

def set_score_thresh(e_w, i):
	try:
		g.score_thresh[i] = float(e_w.get_text())
	except ValueError:
		e_w.set_text(str(g.score_thresh[i]))

def set_name(self):
	g.name = self.get_text()

def set_audio(self):
	g.audio = self.get_text()
	
	pg.mixer.music.stop()
	pg.mixer.music.load("audio/" + g.audio + ".mp3")
	pg.mixer.music.play()
	if g.tmr < 0:
		pg.mixer.music.pause()

def show_level_select():
	level_select_m.hidden = False
	
	menu_m.hidden = True
	
	# Detect and add files to the level select
	songs = os.listdir(level_select_cwd)
	
	level_list_m.children = []
	
	for p in songs:
		if os.path.isdir(level_select_cwd + p):
			level_list_m.add_widget(label_w(p[:len(p)-p[::-1].find(".")-1], gui_fnt, (0, 0, 0), r=ui_rect(), draw_hitbox=(0, 0, 0), name="Level Select Directory \"" + p + "\""))
	
	for p in songs:
		if os.path.isfile(level_select_cwd + p):
			level_list_m.add_widget(label_w(p[:len(p)-p[::-1].find(".")-1], gui_fnt, (0, 0, 0), r=ui_rect(), draw_hitbox=(0, 0, 0), name="Level Select Song \"" + p + "\""))
		
def hide_level_select():
	global level_select_cwd
	
	level_select_m.hidden = True
	
	level_list_m.children = []
	
	menu_m.hidden = False
	
	level_select_cwd = "charts/SheepToaster/"

def set_selected_level(lbl):
	global selected_level
	global level_select_cwd
	
	full_path = level_select_cwd + lbl.txt
	
	# If the path without the json extension exists, it's a directory. Follow it.
	if os.path.exists(full_path):
		level_select_cwd = full_path + "/"
		show_level_select()
		
		level_back_cwd_m.set_text("Back")
	
	# Otherwise, it's a file. Set it as selected
	else:
		selected_level = lbl.txt
	
		level_load_m.set_text("Load " + selected_level)

def instantiate_game_from_selected():
	global g
	global in_game
	
	g = Game(level_select_cwd + selected_level + ".json", screen)
	in_game = True

# Removes the first folder from the cwd and reloads the level select.
def back_cwd():
	global level_select_cwd
	
	if level_select_cwd == "charts/":
		hide_level_select()
	else:
		level_select_cwd = level_select_cwd[:len(level_select_cwd) - level_select_cwd[-2::-1].find("/")-1]
		show_level_select()
		
		if level_select_cwd == "charts/":
			level_back_cwd_m.set_text("Back to Main Menu")

def begin_story():
	pass

clock = pg.time.Clock()

# Build the UI
gui_fnt = pg.font.Font("Font/OldWizard.ttf", int(18/1920*screen.get_width()))
sml_fnt = pg.font.Font("Font/OldWizard.ttf", int(46/1920*screen.get_width()))
big_fnt = pg.font.Font("Font/OldWizard.ttf", int(93/1920*screen.get_width()))
bgr_fnt = pg.font.Font("Font/OldWizard.ttf", int(110/1920*screen.get_width()))

in_game = False
level_select = False
level_select_cwd = "charts/SheepToaster/"
selected_level = "Roman Shuffle"

# Create background widget
background = image_w("img/TABLE.png", r=ui_rect(0, 1, 0, 1, 0, 0, 0, 0), name="background")

# Create main menu
main_l = layout(screen)

# Add Background
main_l.add_widget(background)

# Add Main Menu
menu_m = placeholder_w("main menu", r=ui_rect(0.5, 0.5, 0.5, 0.5, -150, 150, -250, 250), name = "menu_m", color=(0, 0, 0))
main_l.add_widget(menu_m)

# Add Main menu buttons.
story_m = button_w("Story", gui_fnt, (0, 0, 0), begin_story, r=ui_rect(0, 1, 0, 0, 20, -20, 20, 80), draw_hitbox=(0, 0, 0), name="story_m")
menu_m.add_widget(story_m)

level_select_button_m = button_w("Level Select", gui_fnt, (0, 0, 0), show_level_select, r=ui_rect(0, 1, 0, 0, 20, -20, 100, 160), draw_hitbox=(0, 0, 0), name="level_select_button_m")
menu_m.add_widget(level_select_button_m)

options_button_m = button_w("Options", gui_fnt, (0, 0, 0), show_level_select, r=ui_rect(0, 1, 0, 0, 20, -20, 180, 240), draw_hitbox=(0, 0, 0), name="level_select_button_m")
menu_m.add_widget(options_button_m)

quit_button_m = button_w("Quit", gui_fnt, (0, 0, 0), quit, r=ui_rect(0, 1, 0, 0, 20, -20, 260, 320), draw_hitbox=(0, 0, 0), name="level_select_button_m")
menu_m.add_widget(quit_button_m)

# Add Level select.
level_select_m = placeholder_w("level_select_m", r=ui_rect(0.5, 0.5, 0.5, 0.5, -200, 200, -300, 300), name="level_select_m", color=(0, 0, 0))
main_l.add_widget(level_select_m)
level_select_m.hidden = True

# Add the list of levels
level_list_m = v_scrolling_list_w([], 50, 999, set_selected_level, r=ui_rect(0, 1, 0, 1, 0, 0, 30, -30), draw_hitbox=(0, 0, 0), name="level_list_m")
level_select_m.add_widget(level_list_m)

# Add previous directory button
level_back_cwd_m = button_w("Back", gui_fnt, (0, 0, 0), back_cwd, r=ui_rect(0, 1, 0, 0, 0, 0, 0, 30), name="level_back_cwd_m")
level_select_m.add_widget(level_back_cwd_m)

# Add load level button
level_load_m = button_w("Load Roman Shuffle", gui_fnt, (0, 0, 0), instantiate_game_from_selected, r=ui_rect(0, 1, 1, 1, 0, 0, -30, 0), name="level_load_m")
level_select_m.add_widget(level_load_m)

# Create game layout
game_l = layout(screen)

# Add Background
game_l.add_widget(background)

# Add Player card.
player_bg = image_w("img/CHARACTER_CARD_BACKGROUND.png", r=ui_rect(0, 0, 0, 0, 18, 576, 18, 1062), name="player_bg")
game_l.add_widget(player_bg)

player_portrait = image_w("img/DAKE_THE_BARD.png", r=ui_rect(0, 0, 0, 0, 40, 0, 40, 0), name="player_portrait")
player_bg.add_widget(player_portrait)

player_name = label_w("Dake (Bard)", big_fnt, (0, 0, 0), r=ui_rect(0, 1, 0, 1, 0, 0, 640, 0), name="player_name", h_align=CENTER_ALIGN)
player_bg.add_widget(player_name)

player_desc = label_w("Dake is the type of guy who eats arsenic for fun. Balance his humors so he may yet live.", sml_fnt, (0, 0, 0), r=ui_rect(0, 1, 0, 1, 0, 0, 750, 0), name="player_desc", lmar=38)
player_bg.add_widget(player_desc)

# Build Edit menu
e_name_lbl = label_w("Filename:", gui_fnt, (0, 0, 0), r=ui_rect(0, 0.5, 0, 0, 20, 0, 20, 50), name="e_name_lbl", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0)
player_bg.add_widget(e_name_lbl)
e_name_lbl.hidden = True

e_name = entry_w("", gui_fnt, (0, 0, 0), r=ui_rect(0.5, 1, 0, 0, 0, -20, 20, 50), name="e_name", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0, return_behavior=set_name)
player_bg.add_widget(e_name)
e_name.hidden = True

e_audio_lbl = label_w("Audio File:", gui_fnt, (0, 0, 0), r=ui_rect(0, 0.5, 0, 0, 20, 0, 60, 90), name="e_audio_lbl", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0)
player_bg.add_widget(e_audio_lbl)
e_audio_lbl.hidden = True

e_audio = entry_w("", gui_fnt, (0, 0, 0), r=ui_rect(0.5, 1, 0, 0, 0, -20, 60, 90), name="e_audio", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0, return_behavior=set_audio)
player_bg.add_widget(e_audio)
e_audio.hidden = True

e_bpm_lbl = label_w("BPM:", gui_fnt, (0, 0, 0), r=ui_rect(0, 0.5, 0, 0, 20, 0, 100, 130), name="e_bpm_lbl", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0)
player_bg.add_widget(e_bpm_lbl)
e_bpm_lbl.hidden = True

e_bpm = entry_w("", gui_fnt, (0, 0, 0), r=ui_rect(0.5, 1, 0, 0, 0, -20, 100, 130), name="e_bpm", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0, return_behavior=set_bpm)
player_bg.add_widget(e_bpm)
e_bpm.hidden = True

# Score threshholds
b_s_lbl = label_w("Score for Beta Rank:", gui_fnt, (0, 0, 0), r=ui_rect(0, 0.5, 0, 0, 20, 0, 140, 170), name="b_s_lbl", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0)
player_bg.add_widget(b_s_lbl)
b_s_lbl.hidden = True

b_s = entry_w("", gui_fnt, (0, 0, 0), r=ui_rect(0.5, 1, 0, 0, 0, -20, 140, 170), name="b_s", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0, return_behavior=set_score_thresh, params=(0,))
player_bg.add_widget(b_s)
b_s.hidden = True

a_s_lbl = label_w("Score for Alpha Rank:", gui_fnt, (0, 0, 0), r=ui_rect(0, 0.5, 0, 0, 20, 0, 180, 210), name="a_s_lbl", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0)
player_bg.add_widget(a_s_lbl)
a_s_lbl.hidden = True

a_s = entry_w("", gui_fnt, (0, 0, 0), r=ui_rect(0.5, 1, 0, 0, 0, -20, 180, 210), name="a_s", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0, return_behavior=set_score_thresh, params=(1,))
player_bg.add_widget(a_s)
a_s.hidden = True

o_s_lbl = label_w("Score for Omega Rank:", gui_fnt, (0, 0, 0), r=ui_rect(0, 0.5, 0, 0, 20, 0, 220, 250), name="o_s_lbl", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0)
player_bg.add_widget(o_s_lbl)
o_s_lbl.hidden = True

o_s = entry_w("", gui_fnt, (0, 0, 0), r=ui_rect(0.5, 1, 0, 0, 0, -20, 220, 250), name="o_s", v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0, return_behavior=set_score_thresh, params=(2,))
player_bg.add_widget(o_s)
o_s.hidden = True

# Load and Save buttons
e_load = button_w("Load", gui_fnt, (0, 0, 0), load_chart, r=ui_rect(0, 1, 1, 1, 40, -40, -170, -110), draw_hitbox=(255, 255, 255))
player_bg.add_widget(e_load)
e_load.hidden = True

e_save = button_w("Save", gui_fnt, (0, 0, 0), save_chart, r=ui_rect(0, 1, 1, 1, 40, -40, -80, -20), draw_hitbox=(255, 255, 255))
player_bg.add_widget(e_save)
e_save.hidden = True

# Add Scroll
scroll = image_w("img/SCROLL.png", r=ui_rect(1, 1, 0, 0, -962, 0, 0, 0))
game_l.add_widget(scroll)

# Add Score
mid_pane = widget(r=ui_rect(0, 1, 0, 1, 574, -935, 0, 0))
game_l.add_widget(mid_pane)

score_img = image_w(("img/RANK_GAMMA.png", "img/RANK_BETA.png", "img/RANK_ALPHA.png", "img/RANK_OMEGA.png"), r=ui_rect(0.5, 0.5, 0, 0, 0, 0, 18), iw=400, ih=400, h_align=CENTER_ALIGN)
mid_pane.add_widget(score_img)

score_label = label_w("Score", bgr_fnt, (0, 0, 0), r=ui_rect(0, 1, 1, 1, 0, 0, -600, 0), h_align=CENTER_ALIGN)
mid_pane.add_widget(score_label)

score_disp = label_w("0", bgr_fnt, (0, 0, 0), r=ui_rect(0, 1, 1, 1, 0, 0, -500, 0), h_align=CENTER_ALIGN)
mid_pane.add_widget(score_disp)

# Build Pause menu
pause_l = layout(screen)

pause_overlay = rect_w((0, 0, 0, 220), r=ui_rect(0, 1, 0, 1, 0, 0, 0, 0))
pause_l.add_widget(pause_overlay)

p_menu = placeholder_w("menu.png", r=ui_rect(0.5, 0.5, 0.1, 0.9, -150, 150, 100, -100), color=(255, 255, 255))
pause_l.add_widget(p_menu)

p_resume = button_w("Resume", gui_fnt, (255, 255, 255), toggle_paused, r=ui_rect(0.1, 0.9, 0, 0.08, 0, 0, 20, 0), draw_hitbox=(255, 255, 255))
p_menu.add_widget(p_resume)

p_options = button_w("Options", gui_fnt, (255, 255, 255), toggle_options, r=ui_rect(0.1, 0.9, 0.08, 0.16, 0, 0, 20, 0), draw_hitbox=(255, 255, 255))
p_menu.add_widget(p_options)

p_edit = button_w("Edit Chart", gui_fnt, (255, 255, 255), toggle_editing, r=ui_rect(0.1, 0.9, 0.16, 0.24, 0, 0, 20, 0), draw_hitbox=(255, 255, 255))
p_menu.add_widget(p_edit)

p_hard_quit = button_w("Quit to Menu", gui_fnt, (255, 255, 255), quit_to_menu, r=ui_rect(0.1, 0.9, 0.24, 0.32, 0, 0, 20, 0), draw_hitbox=(255, 255, 255))
p_menu.add_widget(p_hard_quit)

p_soft_quit = button_w("Quit to Desktop", gui_fnt, (255, 255, 255), quit, r=ui_rect(0.1, 0.9, 0.32, 0.4, 0, 0, 20, 0), draw_hitbox=(255, 255, 255))
p_menu.add_widget(p_soft_quit)

recv_drop = pg.transform.scale(pg.image.load("img/RECEIVING_DROP.png").convert_alpha(), (118, 186))

note_mask = pg.mask.from_surface(note_sprs[0])

# Initial Cache
main_l.cache_r()
game_l.cache_r()
pause_l.cache_r()

# These two functions define separate mainloops controlling the main menu and the game. Beneath these definitions is the code that calls them depending on the state of in_game
def main_menu_cycle():
	dt = clock.tick(60)
	
	for e in pg.event.get():
		main_l.handle_event(e)
		
		if e.type == pg.QUIT:
			pg.quit()
			sys.exit()
		

	screen.fill((255,255,255))
	
	main_l.cache_r()
	main_l.render_r(screen)
	
	pg.display.flip()

def game_cycle():
	dt = clock.tick(60)
	
	for e in pg.event.get():
		game_l.handle_event(e)
		pause_l.handle_event(e)
		
		if e.type == pg.QUIT:
			pg.quit()
			sys.exit()
		
		elif e.type == pg.WINDOWRESIZED:
			game_l.cache_r()
			pause_l.cache_r()
		
		elif e.type == pg.MOUSEBUTTONDOWN:
			if g.editing:
				if e.button == 2:
					toggle_previewing()
				
				elif e.button == 3:
					for n_i in range(len(g.note_sprites)):
						n = g.note_sprites[n_i]
						
						x, y = n.get_pos()
						
						x = int(e.pos[0] - x)
						y = int(e.pos[1] - y)
						
						if x < 0 or x >= note_mask.get_size()[0] or y < 0 or y >= note_mask.get_size()[1]:
							continue
						
						if note_mask.get_at((x, y)):
							del g.notes[n.kind-1][n.ind]
							del g.note_sprites[n_i]
							break
				
				elif e.button == 1:
					for n_i in range(len(g.note_sprites)):
						n = g.note_sprites[n_i]
						
						x, y = n.get_pos()
						
						x = int(e.pos[0] - x)
						y = int(e.pos[1] - y)
						
						if x < 0 or x >= note_mask.get_size()[0] or y < 0 or y >= note_mask.get_size()[1]:
							continue
						
						if note_mask.get_at((x, y)):
							del g.notes[n.kind-1][n.ind]
							del g.note_sprites[n_i]
							break
					
					g.placing = True
				
				elif e.button == 4:
					if pg.key.get_mods() & pg.KMOD_SHIFT:
						diff = g.time_mul * 2**round(math.log2(800 / g.time_mul))
					else:
						diff = g.time_mul * 2**round(math.log2(200 / g.time_mul))
					
					g.tmr_targ = round((g.tmr + diff) / diff) * diff
					g.delete_old_notes(False)
				
				elif e.button == 5:
					if pg.key.get_mods() & pg.KMOD_SHIFT:
						diff = g.time_mul * 2**round(math.log2(800 / g.time_mul))
					else:
						diff = g.time_mul * 2**round(math.log2(200 / g.time_mul))
					
					g.tmr_targ = round((g.tmr - diff) / diff) * diff
					g.delete_new_notes()
					
					# Spawn notes below the screen
					for i in range(0, 4):
						while True:
							if g.back_cursors[i] < len(g.notes[i]) and g.tmr - g.notes[i][g.back_cursors[i]] < 2000:
								g.note_sprites.insert(0, note_sprite(i+1, g.notes[i][g.back_cursors[i]], g.back_cursors[i], g))
								if g.back_cursors[i] == 0:
									break
								else:
									g.back_cursors[i] -= 1
							else:
								break
		
		elif e.type == pg.MOUSEBUTTONUP:
			if g.placing and not g.paused:
				g.placing = False
				
				x, y = e.pos
				
				c = math.ceil((x - (screen.get_width() - 890)) / scroll_columns_width * 4)
				
				if c >= 1 and c <= 4:
					t = (screen.get_height() * 0.8 - y) / screen.get_height() / g.speed + g.tmr
					
					if pg.key.get_mods() & pg.KMOD_SHIFT:
						t = round(t / (g.time_mul/4)) * (g.time_mul/4)
					
					if t >= 0:
						# Find where in the notes list this should be inserted.
						ind = bisect.bisect(g.notes[c-1], t)
						g.notes[c-1].insert(ind, t)
						
						# Find where in the note_sprites list this should be inserted.
						spr_ind = bisect.bisect_left(g.note_sprites, ind, key=lambda a: a.ind)
						
						if spr_ind < len(g.note_sprites):
							for i in g.note_sprites[spr_ind:]:
								i.ind += 1
						
						g.note_sprites.insert(spr_ind, note_sprite(c, t, ind, g))
						
						g.note_cursors[c-1] += 1
		
		elif e.type == pg.KEYDOWN:
			key_pos = 0
			
			if e.key == pg.K_l:
				if rate == 0.5:
					rate = 1
				else:
					rate = 0.5
			
			if e.key == pg.K_ESCAPE:
				toggle_paused()
			
			if not g.paused and not g.editing or g.previewing:
				if e.key == pg.K_RETURN:
					if g.editing:
						g.set_time(-1000, False, True)
					else:
						g.set_time(-1000, True, True)
				
				elif e.key == pg.K_LEFT:
					key_pos = 1
				elif e.key == pg.K_UP:
					key_pos = 2
				elif e.key == pg.K_DOWN:
					key_pos = 3
				elif e.key == pg.K_RIGHT:
					key_pos = 4
					
				if key_pos != 0:
					g.key_presses += 1
					
					# For all notes on the board in the appropriate column, check their time against the game timer.
					# The lowest note found is hit
					note_hit = None
					score_for_note = 0
					for n_i in range(len(g.note_sprites)):
						n = g.note_sprites[n_i]
						if n.kind == key_pos:
							if abs(n.t - g.tmr) < g.perfect_margin:
								note_hit = n_i
								score_for_note = 2
								break
								
							elif abs(n.t - g.tmr) < g.good_margin:
								note_hit = n_i
								score_for_note = 1
								break
					
					if note_hit is not None:
						note_hit_spr = g.note_sprites[note_hit]
						
						# Score
						g.add_hit_indicator(key_pos, score_for_note)
						if score_for_note == 1:
							g.goods += 1
							g.score += 10
					
							if note_hit_spr.ind > g.back_cursors[note_hit_spr.kind-1]:
								g.back_cursors[note_hit_spr.kind-1] = n.ind
							
							del g.note_sprites[note_hit]
						else:
							g.perfects += 1
							g.score += 20
							g.back_cursors[g.note_sprites[note_hit].kind-1] = n.ind
					
							if note_hit_spr.ind > g.back_cursors[note_hit_spr.kind-1]:
								g.back_cursors[note_hit_spr.kind-1] = n.ind
							
							del g.note_sprites[note_hit]
	
	# Detect if a note has passed below the screen
	g.delete_old_notes()
	
	# Delete fully transparent hit indicators
	i = 0
	while i < len(g.hit_indicator_sprites): # do NOT delete this while loop! It completes in linear time ALWAYS and does not slow down the game!
		if g.hit_indicator_sprites[i].s.get_alpha() == 0:
			del g.hit_indicator_sprites[i]
		else:
			i += 1
	
	if g.is_done() and not has_printed_score:
		print("perfects: %d" % g.perfects)
		print("goods: %d" % g.goods)
		print("bads: %d" % g.bads)
		print("misses: %d" % g.misses)
		print("keypresses: %d" % g.key_presses)
		has_printed_score = True
	
#	print("pa: %d, mp: %d, ed: %d, pv: %d, pl: %d, tmr: %d, trg: %d, off: %d" % (g.paused, g.music_playing, g.editing, g.previewing, g.placing, g.tmr, g.tmr_targ, g.offset))
	
	# Lerp towards the correct time.
	if g.editing and not g.previewing:
		g.set_time((g.tmr_targ - g.tmr) * 0.4 + g.tmr, False, False)
	
	g.update(dt)
	
	# Get current grade
	g.cache_grade()
	score_img.set_img(g.grade)
	
	score_disp.set_text(str(g.score))
	score_disp.cache()

	screen.fill((255,255,255))
	
	game_l.render_r(screen)

	# Draw receiving drops
	for i in range(1, 5):
		x = screen.get_width() - 890 + scroll_columns_width/4 * i - scroll_columns_width/8
		screen.blit(recv_drop, (x-note_w/2, perfect_line_height*screen.get_height() - note_h/2 - 30))
		
	g.draw_notes()
	
	# Draw timestamps in edit mode
	if g.editing:
		t = math.ceil(g.y2t(0) / g.time_mul)
		
		for t in range(t, t-40, -1):
			y = g.t2y(t * g.time_mul)
			
			if y > screen.get_height():
				break
			
			tsurf = sml_fnt.render(str(t), True, (0, 0, 0), (248, 212, 141))
			screen.blit(tsurf, (screen.get_width() - 950 - tsurf.get_width(), y - tsurf.get_height()/2))
	
	# Render note previews
	if g.placing:
		x, y = pg.mouse.get_pos()
		
		c = math.ceil((x - (screen.get_width() - 890)) / scroll_columns_width * 4)
		
		if c >= 1 and c <= 4:
			t = (screen.get_height() * 0.8 - y) / screen.get_height() / g.speed + g.tmr
			
			if pg.key.get_mods() & pg.KMOD_SHIFT:
				t = round(t / (g.time_mul/4)) * (g.time_mul/4)
			
			time_until_hit = t - g.tmr
			screen.blit(note_sprs[c-1], (screen.get_width() - 890 + scroll_columns_width/4 * c - scroll_columns_width/8 - note_w/2, perfect_line_height*screen.get_height() - time_until_hit*g.speed*screen.get_height() - note_h/2 - 30))
	
	g.draw_hit_indicators()
	
	# If paused, show the pause menu.
	if g.paused:
		pause_l.hidden = False
		pause_l.render_r(screen)
	else:
		pause_l.hidden = True
	
	pg.draw.line(screen, (0, 0, 0), (0, 900), (0, 900))

	pg.display.flip()

while True:
	if in_game:
		game_cycle()
	else:
		main_menu_cycle()