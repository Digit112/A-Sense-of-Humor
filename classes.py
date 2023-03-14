import bisect
import json
import math
import pygame as pg
import random

score_text = ("Miss!", "Good!", "Perfect!")
sml_fnt = pg.font.Font("Font/OldWizard.ttf", 46)

# Width of the pane on the left in pixels. The columns for notes are evenly spaced in the remainder of the screen.
left_pane_width = 1030
scroll_columns_width = 816

# Fraction of the screen above the "perfect" line
perfect_line_height = 0.8

# Controls movement speed. Combine this with a slowed down track to slow down the song to make chart timing easier.
rate = 1

has_printed_score = False

note_w = 118
note_h = 186

note_sprs = [
	pg.transform.scale(pg.image.load("img/LEFT_ARROW_SANGUINE.png").convert_alpha(), (118,186)),
	pg.transform.scale(pg.image.load("img/UP_ARROW_CHOLERIC.png").convert_alpha(), (118,186)),
	pg.transform.scale(pg.image.load("img/DOWN_ARROW_MELANCHOLIC.png").convert_alpha(), (118,186)),
	pg.transform.scale(pg.image.load("img/RIGHT_ARROW_PHLEGMATIC.png").convert_alpha(), (118,186))
]

# Represents a note that is being drawn on the screen. pos is 1, 2, 3, or 4 and represents which kind of note this is.
class note_sprite:
	def __init__(self, pos, t, ind, g):
		# The game holding this note sprite
		self.g = g
		
		# The time this note should be hit
		self.t = t
		
		# Note vertical position in pixels. The horizontal position is calculated by the draw function to account for screen width changes.
		# Notes start above the screen so that they don't suddenly appear within the frame
		self.y = -50
		self.kind = pos
		self.note_spr = note_sprs	# Calculate the note's position
		
		self.ind = ind

	def update(self):
		time_until_hit = self.t - self.g.tmr
		self.y = perfect_line_height*self.g.screen.get_height() - time_until_hit*self.g.speed*self.g.screen.get_height()
	
	# Calculate the position of this note at the given time.
	def get_pos(self):
		time_until_hit = self.t - self.g.tmr
		return (self.g.screen.get_width() - 890 + scroll_columns_width/4 * self.kind - scroll_columns_width/8 - note_w/2, perfect_line_height*self.g.screen.get_height() - time_until_hit*self.g.speed*self.g.screen.get_height() - note_h/2 - 30)
	
	# Draws this sprite to the screen s
	def draw(self):
		x = self.g.screen.get_width() - 890 + scroll_columns_width/4 * self.kind - scroll_columns_width/8
		#if self.kind == 1:
		self.g.screen.blit(self.note_spr[self.kind-1],(x - note_w/2, self.y - note_h/2 - 30))
		#else:

# Surfaces that are spawned whenever you hit a key. Surfaces contain notices of if you got a "Perfect!" "Good!" or "Miss!"
# These are drawn at a random point near the column from which they were spawned intersecting the perfect line.
# They move up slightly and become more transparent over the course of about a second.
class hit_indicator_sprite:
	def __init__(self, x, y, s):
		self.x = x
		self.y = y
		self.s = s

class Game:
	def __init__(self, fn, screen):
		self.screen = screen

		self.score = 0
		
		self.offset = 0
		
		self.note_sprites = []
		
		# Stats
		self.perfects = 0
		self.goods = 0
		self.bads = 0
		
		self.misses = 0
		
		# Number of times arrow keys were pressed
		self.key_presses = 0
		
		# State
		self.paused = False
		self.music_playing = False
		
		self.editing = False
		self.previewing = False
		
		self.placing = False
		
		self.tmr_targ = 0
		
		self.hit_indicator_sprites = []
		
		self.fn = fn
		self.load(fn)
		
		# Keeps track of which note is the next to be spawned in each column
		self.note_cursors = [0, 0, 0, 0]
		
		# The same as note_cursors, but these point to the most recently deleted notes. This is used for spawning those notes back in while editing a chart and scrolling down.
		self.back_cursors = [0, 0, 0, 0]

		# Current time in the song.
		self.tmr = -1000
		
		pg.mixer.music.play()
		if self.tmr < 0:
			pg.mixer.music.pause()

		# Amount of time before and after the note is in the perfect position within which a "perfect" and "good" score is given, in milliseconds.
		self.perfect_margin = 40
		self.good_margin = 120
		self.miss_margin = 400
		
		# Height of debug bars representing "perfect" and "good" score as a percent of the screen
		self.perfect_bar_height = int(self.speed * self.perfect_margin * self.screen.get_height() * 2)
		self.good_bar_height = int(self.speed * self.good_margin * self.screen.get_height() * 2)
		
		# Time before a note hits the perfect line that it should be spawned, based on the speed of the notes, in milliseconds.
		# Notes are spawned well before they enter the screen.
		self.spawn_ahead_time = perfect_line_height*2 / self.speed

		self.do_once = True
	
	def load(self, fn):
		fin = open(fn, "r")
		dat = json.loads(fin.read())
		fin.close()
		
		self.name = dat["name"]
		self.audio = dat["audio"]
		pg.mixer.music.load("audio/" + self.audio + ".mp3")
		
		self.time_mul = dat["time_mul"]

		self.notes = dat["notes"]
		
		# Convert according to time_mul
		for i in range(0, 4):
			for j in range(len(self.notes[i])):
				self.notes[i][j] *= self.time_mul
		
		# Scores required for each grade
		self.score_thresh = dat["score_thresh"]
		
		self.song_len = 0
		for i in range(0, 4):
			if len(self.notes[i]) > 0:
				self.song_len = max(self.song_len, self.notes[i][-1])
		
		self.song_len = self.song_len*self.time_mul + 1000
		
		# Speed measured in fraction of the screen height per millisecond so that the time it takes a note to descend from the top of the screen does not change when the window is resized
		# or when the game is played with monitors of different sizes or resolutions.
		self.speed = dat["speed"]
	
	def reset(self):
		self.score = 0
		
		self.note_cursors = [0, 0, 0, 0]
		self.back_cursors = [0, 0, 0, 0]
		
		self.note_sprites = []
		self.hit_indicator_sprites = []
		
		# State
		self.paused = False
		self.music_playing = False
		
		self.previewing = False
		
		self.placing = False
		
		# Stats
		self.perfects = 0
		self.goods = 0
		self.bads = 0
		
		self.misses = 0
		
		# Number of times arrow keys were pressed
		self.key_presses = 0
		
		pg.mixer.music.stop()
		pg.offset = 0
		
		self.tmr = -1000
		self.tmr_targ = 0
		
		pg.mixer.music.play()
		if self.tmr < 0:
			pg.mixer.music.pause()
	
	# Add a hit indicator sprite in the column given by pos with text according to score
	def add_hit_indicator(self, pos, score):
		s = sml_fnt.render(score_text[score], False, (0, 0, 0))
		s.set_alpha(200)
		
		x = self.screen.get_width() - 890 + scroll_columns_width/4 * pos - scroll_columns_width/8
		y = self.screen.get_height() * perfect_line_height
		
		x += random.randrange(-40, 40) - s.get_width()/2
		y += random.randrange(-30, 30) - s.get_height()/2
		
		self.hit_indicator_sprites.append(hit_indicator_sprite(x, y, s))
	
	# Draw all hit indicator sprites. This also makes them slightly more transparent and moves them upwards.
	def draw_hit_indicators(self):
		for s in self.hit_indicator_sprites:
			self.screen.blit(s.s, (s.x, s.y))
			s.y -= 5
			s.s.set_alpha(s.s.get_alpha()-6)
	
	# Spawns notes as needed and updates existing notes.
	def update(self, dt):
		# Get the time since the game started
		if not self.paused and not (self.editing and not self.previewing):
			if self.tmr < -1:
				if not self.paused and not self.editing or self.previewing:
					self.tmr += dt*rate
				
				if self.tmr >= 0:
					pg.mixer.music.rewind()
					pg.mixer.music.set_pos(self.tmr/1000/rate)
					
					self.offset = max(self.tmr, 0) - pg.mixer.music.get_pos()*rate
					
					# Advance cursors to the current time
					for c_i in range(0, 4):
						i = 0
						while self.note_cursors[c_i] < len(self.notes[c_i]) and self.notes[c_i][self.note_cursors[c_i]] < self.tmr:
							self.note_cursors[c_i] += 1
							
					self.music_playing = True
					pg.mixer.music.unpause()
					
			else:
				self.tmr = pg.mixer.music.get_pos()*rate + self.offset
		
#		print(self.tmr)
		
		# Loop over the notes under the cursor. If they are about to appear on screen, spawn them and advance the cursor.
		for c_i in range(4):
			c = self.notes[c_i]
			while self.note_cursors[c_i] < len(self.notes[c_i]) and c[self.note_cursors[c_i]] - self.spawn_ahead_time < self.tmr:
				self.note_sprites.append(note_sprite(c_i+1, self.notes[c_i][self.note_cursors[c_i]], self.note_cursors[c_i], self))
				self.note_cursors[c_i] += 1
			
		# Update note sprites
		for n in self.note_sprites:
			n.update()
	
	def set_time(self, t, do_reload, autoplay):
		self.tmr = t
		
		self.note_cursors = [0, 0, 0, 0]
		while len(self.note_sprites) > 0:
			del self.note_sprites[0]
		
		if self.tmr < 0:
			self.music_playing = False
			if pg.mixer.music.get_busy():
				pg.mixer.music.pause()
		else:
			if autoplay:
				self.music_playing = True
				if not pg.mixer.music.get_busy():
					pg.mixer.music.unpause()
				
			pg.mixer.music.rewind()
			pg.mixer.music.set_pos(t/1000/rate)
				
		self.offset = max(t, 0) - pg.mixer.music.get_pos()*rate
		
		# Advance cursors to the current time
		for c_i in range(0, 4):
			i = 0
			while self.note_cursors[c_i] < len(self.notes[c_i]) and self.notes[c_i][self.note_cursors[c_i]] < t:
				self.note_cursors[c_i] += 1
		
		if do_reload:
			self.load(self.fn)
	
	def is_done(self):
		return self.tmr > self.song_len
	
	def cache_grade(self):
		self.grade = 0
		for i in range(2, -1, -1):
			if self.score_thresh[i] <= self.score:
				self.grade = i+1
				break

	def draw_notes(self):
		for n in self.note_sprites:
			n.draw()
	
	def delete_old_notes(self, do_score=True):
		n_i = 0
		while n_i < len(self.note_sprites):
			n = self.note_sprites[n_i]
			
			if n.y > self.screen.get_height() + note_h/2 + 200:
				if do_score:
					self.misses += 1
					self.score = max(0, self.score - 10)
				
				if n.ind > self.back_cursors[n.kind-1]:
					self.back_cursors[n.kind-1] = n.ind
				
				del self.note_sprites[n_i]
			else:
				n_i += 1
	
	def delete_new_notes(self):
		n_i = 0
		while n_i < len(self.note_sprites):
			n = self.note_sprites[n_i]
			
			if n.ind < self.note_cursors[n.kind-1]:
				self.note_cursors[n.kind-1] = n.ind
				
			del self.note_sprites[n_i]
			
			n.y < -200
	
	# Convert a time to a y value on the screen based on the gamer's current timer. If you pass the tmr's current value to this function, you will get the y-vlue of the perfect line back.
	def t2y(self, t):
		time_until_hit = t - self.tmr
		return perfect_line_height*self.screen.get_height() - time_until_hit*self.speed*self.screen.get_height()
	
	# Convert the given y value to it's corresponding time in the song depending on the state of the timer
	def y2t(self, y):
		return (perfect_line_height*self.screen.get_height() - y) / (self.speed*self.screen.get_height()) + self.tmr
	
	# Return the x-value of the midline of the associated column
	def c2x(self, c):
		return self.screen.get_width() - 890 + scroll_columns_width/4 * c - scroll_columns_width/8