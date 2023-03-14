import math
import pygame as pg
import time

# UI Layout utilities and widgets

# Widget contructor parameters:
# image_w: fn, r=ui_rect(), iw=None, ih=None, h_align=LEFT_ALIGN, v_align=TOP_ALIGN
# button_w: text, fnt, color, callback, r=ui_rect(), param=None
# label_w: txt, fnt, color, r=ui_rect(), antialias=True, gap=10, lmar=10, rmar=10, tmar=10, bmar=10, align=LEFT_ALIGN

# Event Constants
UI_BUTTON_PRESSED = 0
UI_BUTTON_HELD = 1
UI_BUTTON_RELEASED = 2

UI_KEY_PRESSED = 3
UI_KEY_HELD = 4
UI_KEY_RELEASED = 5

# Alignment Constants
LEFT_ALIGN = 0
RIGHT_ALIGN = 1

TOP_ALIGN = 2
BOTTOM_ALIGN = 3

CENTER_ALIGN = 4

# Specifies the left, right, top, and bottom anchors and relative positions of a UI rect
class ui_rect:
	def __init__(self, la=0, ra=0, ta=0, ba=0, lo=0, ro=0, to=0, bo=0):
		# Anchor position values relative to the parent bounding box values, in percent.
		self.la = la
		self.ra = ra
		self.ta = ta
		self.ba = ba
		
		# Bounding box position (left, right, top, bottom) values relative to anchors (hence the o for offset), in pixels.
		self.lo = lo
		self.ro = ro
		self.to = to
		self.bo = bo
	
	def __str__(self):
		return "%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (self.la, self.ra, self.ta, self.ba, self.lo, self.ro, self.to, self.bo)

# Specifies spacing, including margins and line spacing.
class ui_spacing:
	# Set all unspecified variables to "mar". This means you can write ui_spacing(8) instead of ui_spacing(8, 8, 8, 8, 8)
	# or ui_spacing(16, tmar=5, bmar=5) instead of ui_spacing(16, 16, 16, 5, 5)
	def __init__(self, mar=10, gap=None, lmar=None, rmar=None, tmar=None, bmar=None):
		if gap is None:
			self.gap = mar
		else:
			self.gap = gap
		
		if lmar is None:
			self.lmar = mar
		else:
			self.lmar = lmar
		
		if rmar is None:
			self.rmar = mar
		else:
			self.rmar = rmar
		
		if tmar is None:
			self.tmar = mar
		else:
			self.tmar = tmar
		
		if bmar is None:
			self.bmar = mar
		else:
			self.bmar = bmar

# Stores a 9-sliced asset. This class contains the 9 sections of the image that objects can request repeated versions of via the get_repeated() method.
# When making a get_repeated() call, the cropped version of this asset will be extended if necessary to fulfill the request with a single crop() call.
# This new version is then stored for further calls.
# The slices parameter expects the (left, right, top, bottom) slices where left and right are an x value measured from the image's left and the top and bottom are a y value measured from the image's top.
class sliced_asset:
	def __init__(self, fn, slices):
		self.img = pg.image.load(fn).convert_alpha()
		
		iw = self.img.get_width()
		ih = self.img.get_height()
		
		# The widths and heights of each slice within the original sliced image
		self.srce_row_hs = [slices[2], slices[3] - slices[2], ih - slices[3]]
		self.srce_col_ws = [slices[0], slices[1] - slices[0], iw - slices[1]]
		
		self.srce_x_slices = [0, slices[0], slices[1]]
		self.srce_y_slices = [0, slices[2], slices[3]]
		
		# This class will try to extend the cached repeated image by 100 pixels each time it is extended, but is restricted to extending in multiples of the slices' sizes to simplify the algorithm
		# So round 100 pixels to the nearest multiple of the middle slice's width and height to get our new extension distance.
		self.ext_w = round(100/self.srce_col_ws[1])*self.srce_col_ws[1]
		self.ext_h = round(100/self.srce_row_hs[1])*self.srce_row_hs[1]
		
		# Create surfaces to hold the extracted images. These images are already extended to the necessary width and height.
		self.parts = [
		    [pg.Surface((self.srce_col_ws[0], self.srce_row_hs[0])), pg.Surface((self.srce_col_ws[0], self.ext_h)), pg.Surface((self.srce_col_ws[0], self.srce_row_hs[2]))],
		    [pg.Surface((self.ext_w,          self.srce_row_hs[0])), pg.Surface((self.ext_w,          self.ext_h)), pg.Surface((self.ext_w,          self.srce_row_hs[2]))],
		    [pg.Surface((self.srce_col_ws[2], self.srce_row_hs[0])), pg.Surface((self.srce_col_ws[2], self.ext_h)), pg.Surface((self.srce_col_ws[2], self.srce_row_hs[2]))],
		]
		
		# Extract the slices into separate objects. Each part now holds a copy of its slices, not repeated at all, but is large enough to hold the repetitions of its pattern up to ext_w and ext_h
		for x in range(3):
			for y in range(3):
				self.parts[x][y].blit(self.img, (0, 0), area=(self.srce_x_slices[x], self.srce_y_slices[y], self.srce_col_ws[x], self.srce_row_hs[y]))
		
		# Set the current valid crop width. This is the width and height in pixels to which the images have already been repeated and may be less than the size of the surfaces in which they are held.
		self.valid_crop_w = self.srce_col_ws[1]
		self.valid_crop_h = self.srce_row_hs[1]
		
		# Set the size of the surfaces holding the parts
		self.surf_w = self.ext_w
		self.surf_h = self.ext_h
		
		# Extend the images to the first ext_w and ext_h
		self.extend(self.ext_w, self.ext_h)
	
	# If w or h are larger than the sizes of the stored surfaces, scale them up. If w or h are smaller, the surface will not be scaled in that direction
	# Blits the old repeated pattern onto the new one.
	def expand_surface(self, w, h):
		# Round up w and h to the next highest multiple of self.ext_w and self.ext_h
		w = math.ceil(w/self.ext_w)*self.ext_w
		h = math.ceil(h/self.ext_h)*self.ext_h
		
		do_h_expand = False
		do_v_expand = False
		
		if w < self.surf_w:
			w = self.surf_w
		else:
			do_h_expand = True
		
		if h < self.surf_h:
			h = self.surf_h
		else:
			do_v_expand = True
		
		# If w is bigger than the existing top and bottom surfaces' widths, create wider surfaces and copy the existing pattern to them
		if do_h_expand:
			new_t_part = pg.Surface((w, self.srce_row_hs[0]))
			new_t_part.blit(self.parts[1][0], (0, 0))
			self.parts[1][0] = new_t_part
			
			new_b_part = pg.Surface((w, self.srce_row_hs[2]))
			new_b_part.blit(self.parts[1][2], (0, 0))
			self.parts[1][2] = new_b_part
		
		# If h is bigger than the existing left and right surfaces' heights, create taller surfaces and copy the existing pattern to them
		if do_v_expand:
			new_l_part = pg.Surface((self.srce_col_ws[0], h))
			new_l_part.blit(self.parts[0][1], (0, 0))
			self.parts[0][1] = new_l_part
			
			new_r_part = pg.Surface((self.srce_col_ws[2], h))
			new_r_part.blit(self.parts[2][1], (0, 0))
			self.parts[2][1] = new_r_part
		
		# If either are bigger, expand the middle section too
		if do_h_expand or do_v_expand:
			new_m_part = pg.Surface((w, h))
			new_m_part.blit(self.parts[1][1], (0, 0))
			self.parts[1][1] = new_m_part
		
		self.surf_w = w
		self.surf_h = h
		
		return w, h
	
	# Ensures crops can be taken from the stored images be repeating them more if necessar
	def extend(self, w, h):
		# Check to ensure the stored image is wide and tall enough to facillitate repeating the cropped pattern. If not, increase the size of the surfaces storing the repeated image.
		# This will return the new size of the surfaces, which will have been rounded up to multiples of ext_w and ext_h
		# or pulled down to the existing surface width and height if the surfaces are already of sufficient size.
		w, h = self.expand_surface(w, h)
		
		# Repeatedly duplicate the existing pattern until the size is increased as necessary.
		while self.valid_crop_w < w:
			dup_w = min(w - self.valid_crop_w, self.valid_crop_w)
			
			self.parts[1][0].blit(self.parts[1][0], (self.valid_crop_w, 0), area=(0, 0, dup_w, self.srce_row_hs[0]))
			self.parts[1][2].blit(self.parts[1][2], (self.valid_crop_w, 0), area=(0, 0, dup_w, self.srce_row_hs[2]))
			
			# Duplicate the middle piece too
			self.parts[1][1].blit(self.parts[1][1], (self.valid_crop_w, 0), area=(0, 0, dup_w, self.valid_crop_h))
			
			self.valid_crop_w += dup_w
		
		while self.valid_crop_h < h:
			dup_h = min(h - self.valid_crop_h, self.valid_crop_h)
			
			self.parts[0][1].blit(self.parts[0][1], (0, self.valid_crop_h), area=(0, 0, self.srce_col_ws[0], dup_h))
			self.parts[2][1].blit(self.parts[2][1], (0, self.valid_crop_h), area=(0, 0, self.srce_col_ws[2], dup_h))
			
			# Duplicate the middle piece too
			self.parts[1][1].blit(self.parts[1][1], (0, self.valid_crop_h), area=(0, 0, self.valid_crop_w, dup_h))
			
			self.valid_crop_h += dup_h
	
	# Retreive a crop of the cached repeated pattern. Cached patterns will be automatically expanded to fulfill the request.
	# x and y range from [0, 2] and specify which of the 9 segments should be retreived. w and h are the size of the pattern to retreive.
	# w is only used if x is 1 and h is only used if y is 1
	# Only subsurfaces are returned, which are references to the cached pattern and should not be modified
	def get_crop(self, x, y, w=0, h=0):
		self.extend(w, h)
		
		if x == 0:
			if y == 0:
				return self.parts[0][0]
			elif y == 1:
				return self.parts[0][1].subsurface((0, 0, self.srce_col_ws[0], h))
			elif y == 2:
				return self.parts[0][2]
		elif x == 1:
			if y == 0:
				return self.parts[1][0].subsurface((0, 0, w, self.srce_row_hs[0]))
			elif y == 1:
				return self.parts[1][1].subsurface((0, 0, w, h))
			elif y == 2:
				return self.parts[1][2].subsurface((0, 0, w, self.srce_row_hs[2]))
		elif x == 2:
			if y == 0:
				return self.parts[2][0]
			elif y == 1:
				return self.parts[2][1].subsurface((0, 0, self.srce_col_ws[2], h))
			elif y == 2:
				return self.parts[2][2]

# Defines a widget. A widget has a bounding box that is cached and recalculated whenever the widgets size is changed.
# Each of the four edges have an anchor, whose position is defined as a fraction of the parent element's width (for vertical edges) or height (for horizontal edges).
# The corresponding edge of the widget's bounding box is defined as an offset from that anchor's position, in pixels.
class widget:
	def __init__(self, r=ui_rect(), draw_hitbox=None, name=""):
		# Child widgets
		self.children = []
		
		self.draw_hitbox = draw_hitbox
		
		# If True, this widget and all its children will not be recursively cached or rendered.
		self.hidden = False
		
		self.name = name
		
		# List of events this widget wants to be notified of. on_event() will be called on this object when an event in this mask has been detected,
		# sometimes only if this widget is active (If this widget is the one most recently clicked on.
		self.event_mask = []
		
		# This element's bounding box.
		self.bb = r
		
		# Cached left, right, top, and bottom values relative to the root bounding box, in pixels
		self.l = 0
		self.r = 0
		self.t = 0
		self.b = 0
		
		# Cached width and height
		self.w = 0
		self.h = 0
		
	def get_l(self):
		return self.l
	
	def get_r(self):
		return self.r
	
	def get_t(self):
		return self.t
	
	def get_b(self):
		return self.b
	
	def get_w(self):
		return self.w
	
	def get_h(self):
		return self.h
	
	# Calculate l, r, t, b, w, and h values
	def cache(self):
		self.pre_cache()
		
		pw = self.parent.get_w()
		ph = self.parent.get_h()
		
		self.l = self.parent.get_l() + pw * self.bb.la + self.bb.lo
		self.r = self.parent.get_l() + pw * self.bb.ra + self.bb.ro
		self.t = self.parent.get_t() + ph * self.bb.ta + self.bb.to
		self.b = self.parent.get_t() + ph * self.bb.ba + self.bb.bo

		self.w = self.r - self.l
		self.h = self.b - self.t
#		print(self.l, self.r, self.t, self.b, self.w, self.h)

		self.post_cache()
	
	# Called at the beginning of cache(). Inheriting classes should override this for recalculations that need to be made when the widget is moved or resized
	def pre_cache(self):
		pass
	
	# Called at the end of cache(). Inheriting classes should override this for recalculations that need to be made when the widget is moved or resized
	def post_cache(self):
		pass
	
	# Call cache on this object and all it's children, and their children, etc.
	def cache_r(self, rd):
		if not self.hidden:
			self.cache()
#			print("  "*(rd-1) + "(" + self.name + ") [[%d, %d, %d, %d], [%d, %d, %d, %d]] -> %d, %d, %d, %d" % (self.bb.la, self.bb.ra, self.bb.ta, self.bb.ba, self.bb.lo, self.bb.ro, self.bb.to, self.bb.bo, self.l, self.r, self.t, self.b))
			for c in self.children:
#				print("  "*rd + "Caching \"" + c.name + "\" (" + str(type(c)) + ")")
				c.cache_r(rd+1)
	
	# Draw this sprite to the passed screen. This function should be overridden by inheriting classes.
	def render(self, screen):
		pass
	
	def render_hitbox(self, screen):
		pg.draw.rect(screen, self.draw_hitbox, (self.l, self.t, self.w, self.h), width=3)
		
	# Call render recursively
	def render_r(self, screen):
		if not self.hidden:
			self.render(screen)
			
			if self.draw_hitbox is not None:
				self.render_hitbox(screen)
			
			for c in self.children:
				c.render_r(screen)
	
	def add_widget(self, w):
		w.parent = self
		self.children.append(w)
	
	# Tests for collision. Only needed for widgets that the user may want to click on or make active in some way.
	def collide(self, x, y):
		return None
	
	# Call on an object to get the object among all the children of this widget that collides with the point and is drawn latest.
	def collide_r(self, x, y):
		if not self.hidden:
			if self.collide(x, y):
				ret = self
			else:
				ret = None
				
			for c in self.children:
				tmp = c.collide_r(x, y)
				if tmp is not None:
					ret = tmp
			
			return ret
	
	# Called when an event in this object's event mask is detected, sometimes only if this widget is the most recently clicked.
	# Inheriting classes needing to handle events should override this.
	def on_event(self, e):
		pass

# Loads an image and stores the surface. Scales it to w or h if either is defined, or to (w, h) if both are defined.
# The image is drawn at the size it was loaded, which may or may not align with the widget's actual bounding box.
# If fn is a list of strings, each will be opened and can be switched between with set_img()
# This widget should not be used for animated sprites.
class image_w(widget):
	def __init__(self, fn, r=ui_rect(), draw_hitbox=None, name="", iw=None, ih=None, h_align=LEFT_ALIGN, v_align=TOP_ALIGN):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.iw = iw
		self.ih = ih
		
		self.h_align = h_align
		self.v_align = v_align
		
		self.cur_img = 0
		
		self.imgs = []
		if type(fn) is str:
			self.imgs.append(pg.image.load(fn).convert_alpha())
			self.img = self.imgs[0]
		else:
			for i in fn:
				self.imgs.append(pg.image.load(i).convert_alpha())
			self.img = self.imgs[0]
		
		if iw is not None or ih is not None:
			if iw is None:
				iw = self.img.get_width()
			elif ih is None:
				ih = self.img.get_height()
			
			self.img = pg.transform.scale(self.img, (iw, ih))
			
	def render(self, screen):
		if self.h_align == CENTER_ALIGN:
			x = self.l + (self.r - self.l)/2 - self.img.get_width()/2
		elif self.h_align == RIGHT_ALIGN:
			x = self.r - self.img.get_width()
		else:
			x = self.l
		
		if self.v_align == CENTER_ALIGN:
			y = self.t + (self.b - self.t)/2 - self.img.get_height()/2
		elif self.v_align == BOTTOM_ALIGN:
			y = self.b - self.img.get_height()
		else:
			y = self.t
			
		screen.blit(self.img, (x, y))
	
	def set_img(self, i):
		self.img = self.imgs[i]
		self.cur_img = i
		
		if self.w is not None or self.h is not None:
			iw = self.iw
			ih = self.ih
			
			if self.iw is None:
				iw = self.img.get_width()
			elif self.ih is None:
				ih = self.img.get_height()
			
			self.img = pg.transform.scale(self.img, (iw, ih))
	
	def get_img(self):
		return self.cur_img

# Used to represent assets that are not yet available. This is exactly like image, except instead of specifying the image filename, You specify text to be written on the placeholder.
# If iw and ih must be specified
class placeholder_w(widget):
	def __init__(self, fn, r=ui_rect(), draw_hitbox=None, color=(0, 0, 0), name="", iw=None, ih=None, h_align=LEFT_ALIGN, v_align=TOP_ALIGN):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.iw = iw
		self.ih = ih
		
		self.h_align = h_align
		self.v_align = v_align
		
		self.fnt = pg.font.SysFont(pg.font.get_fonts()[0], 12)
		
		self.cur_img = 0
		
		self.color = color
		
		self.imgs = []
		if type(fn) is str:
			self.imgs.append(fn)
			self.img = self.imgs[0]
		else:
			for i in fn:
				self.imgs.append(i)
			self.img = self.imgs[0]
			
	def render(self, screen):
		if self.iw is None:
			iw = self.r - self.l
		else:
			iw = self.iw
		
		if self.ih is None:
			ih = self.b - self.t
		else:
			ih = self.ih
			
		if self.h_align == CENTER_ALIGN:
			x = self.l + (self.r - self.l)/2 - iw/2
		elif self.h_align == RIGHT_ALIGN:
			x = self.r - iw
		else:
			x = self.l
		
		if self.v_align == CENTER_ALIGN:
			y = self.t + (self.b - self.t)/2 - ih/2
		elif self.v_align == BOTTOM_ALIGN:
			y = self.b - ih
		else:
			y = self.t
			
		pg.draw.rect(screen, self.color, (x, y, iw, ih), width=3)
		
		tsurf = self.fnt.render(self.img, True, self.color)
		screen.blit(tsurf, (x+4, y+4))
		
	
	def set_img(self, i):
		self.img = self.imgs[i]
		self.cur_img = i
	
	def get_img(self):
		return self.cur_img

# Represents a button. Buttons add events to the pygame queue when their bounding box is clicked.
class button_w(widget):
	def __init__(self, text, fnt, color, callback, r=ui_rect(), draw_hitbox=None, name="", params=()):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.text = text
		self.callback = callback
		
		self.params = params
		
		self.event_mask = [pg.MOUSEBUTTONDOWN]
		
		# Create the text of this button
		self.add_widget(label_w(text, fnt, color, ui_rect(0, 1, 0, 1, 0, 0, 0, 0), h_align=CENTER_ALIGN, v_align=CENTER_ALIGN, lmar=0, rmar=0, tmar=0, bmar=0))
	
	def collide(self, x, y):
		if x <= self.r and x >= self.l and y >= self.t and y <= self.b:
			return self
	
	def on_event(self, e):
		self.callback(*self.params)
	
	def set_text(self, t):
		self.children[0].set_text(t)

# Represents a text box. Text will be wrapped automatically and rendered in the bounding box if possible.
class label_w(widget):
	def __init__(self, txt, fnt, color, r=ui_rect(), draw_hitbox=None, name="", antialias=True, gap=10, lmar=10, rmar=10, tmar=10, bmar=10, h_align=LEFT_ALIGN, v_align=TOP_ALIGN):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.txt = txt
		self.fnt = fnt
		self.color = color
		self.antialias = antialias
		
		self.gap = gap
		self.lmar = lmar
		self.rmar = rmar
		self.tmar = tmar
		self.bmar = bmar
		
		self.h_align = h_align
		self.v_align = v_align
		
		# Records the indexes of characters immediately following a split.
		self.splits = [0]
		
		# Index of the first character not renderable within the space. Equal to the length of the text if all of it is shown.
		self.max_cur = 0
		
		# Cached, rendered lines of text.
		self.lines = []
	
	def post_cache(self):
		h_space = self.get_w() - self.lmar - self.rmar
		v_space = self.get_h() - self.tmar - self.bmar
		
		txt = self.txt
		
		self.lines = []
		self.splits = [0]
		
		self.max_cur = len(txt)
		
		# While there is enough vertical space for another line...
		while self.fnt.get_height() < v_space:
			# Check if the remaining text can fit on this line. If so, render it and return. We still have to loop over the remaining characters to check for newlines.
			if self.fnt.size(txt)[0]-5 < h_space:
				has_found_newline = False
				
				for c_i in range(len(txt)):
					c = txt[c_i]
					if c == "\n":
						has_found_newline = True
						self.lines.append(self.fnt.render(txt[:c_i], self.antialias, self.color))
						txt = txt[c_i+1:]
						self.splits.append(c_i+1)
						v_space -= self.fnt.get_height() + self.gap
						break
				
				# Print the rest of the text, if needed, and return.
				if not has_found_newline:
					if len(txt) > 0:
						self.lines.append(self.fnt.render(txt, self.antialias, self.color))
					return
				else:
					continue
			
			# Otherwise, fit as much as possible into the space.
			last_space = -1
			s_len = 0
			for c_i in range(len(txt)):
				c = txt[c_i]
				
				s_len += self.fnt.metrics(c)[0][4]
				
				if c == " ":
					last_space = c_i
				
				# If this character is a newline, split here.
				if c == "\n":
					self.lines.append(self.fnt.render(txt[:c_i], self.antialias, self.color))
					txt = txt[c_i+1:]
					self.splits.append(c_i+1)
					v_space -= self.fnt.get_height() + self.gap
					break
				
				# If this much text is too much...
				elif s_len > h_space:
					# If there has been no whitespace on this line, split the line right here.
					if last_space == -1:
						self.lines.append(self.fnt.render(txt[:c_i], self.antialias, self.color))
						txt = txt[c_i:]
						self.splits.append(c_i)
						v_space -= self.fnt.get_height() + self.gap
						break
						
					# Otherwise, split at the last whitespace.
					else:
						self.lines.append(self.fnt.render(txt[:last_space], self.antialias, self.color))
						txt = txt[last_space+1:]
						self.splits.append(last_space+1)
						v_space -= self.fnt.get_height() + self.gap
						break
		
		self.max_cur = self.splits[-1] - 1
		del self.splits[-1]
	
	def render(self, screen):
		lines_height = len(self.lines) * (self.gap + self.fnt.get_height()) - self.gap
		
		# Set top_pix to the y-value of the top of the first line.
		if self.v_align == CENTER_ALIGN:
			top_pix = self.t + self.tmar + ((self.b - self.bmar) - (self.t + self.tmar)) / 2 - lines_height/2
			
		elif self.v_align == BOTTOM_ALIGN:
			top_pix = self.b - self.bmar - lines_height
			
		else:
			top_pix = self.t + self.tmar
		
		if self.h_align == LEFT_ALIGN:
			for l in self.lines:
				screen.blit(l, (self.l + self.lmar, top_pix))
				top_pix += self.fnt.get_height() + self.gap
				
		elif self.h_align == CENTER_ALIGN:
			for l in self.lines:
				screen.blit(l, (self.l + self.lmar + ((self.r - self.rmar) - (self.l + self.lmar)) / 2 - l.get_width()/2, top_pix))
				top_pix += self.fnt.get_height() + self.gap
		
		elif self.h_align == RIGHT_ALIGN:
			for l in self.lines:
				screen.blit(l, (self.r - self.rmar - l.get_width(), top_pix))
				top_pix += self.fnt.get_height() + self.gap
	
	# Returns the index of the character clicked on for the purposes of setting cursor position. x and y provided in window coordinates.
	def get_pos(self, x, y):
		lines_height = len(self.lines) * (self.gap + self.fnt.get_height()) - self.gap
		
		# Set top_pix to the y-value of the top of the first line.
		if self.v_align == CENTER_ALIGN:
			top_pix = self.t + self.tmar + ((self.b - self.bmar) - (self.t + self.tmar)) / 2 - lines_height/2
			
		elif self.v_align == BOTTOM_ALIGN:
			top_pix = self.b - self.bmar - lines_height
			
		else:
			top_pix = self.t + self.tmar
		
		# If the cursor is above the first line, or there is no text, return the first character.
		if y < top_pix or self.txt == "":
			return 0
		
		for l_i in range(len(self.lines)):
			l = self.lines[l_i]
			
			s = self.splits[l_i]
			e = self.splits[l_i+1] if l_i+1 < len(self.splits) else len(self.txt)
			
			t = self.txt[s:e]
			
			# If the cursor is below this line, continue to the next
			top_pix += l.get_height() + self.gap
			if y > top_pix:
				continue
			
			# If the cursor is left or right of this line, return the start or end character on this line.
			if self.h_align == LEFT_ALIGN:
				t_l = self.l + self.lmar
			elif self.h_align == CENTER_ALIGN:
				t_l = self.l + self.lmar + ((self.r - self.rmar) - (self.l + self.lmar)) / 2 - l.get_width()/2
			elif self.h_align == RIGHT_ALIGN:
				t_l = self.r - self.rmar - l.get_width()
				
			if x < t_l:
				return self.splits[l_i]
			
			t_r = t_l + l.get_width()
			if x > t_r:
				return self.splits[l_i+1] if l_i+1 < len(self.splits) else len(self.txt)
			
			for c_i in range(len(t)):
				c = t[c_i]
				
				t_l += self.fnt.metrics(c)[0][4]
				
				if x < t_l:
					return c_i + self.splits[l_i]
		
		return 0
	
	def set_text(self, s):
		self.txt = s
		self.cache()
	
class entry_w(widget):
	def __init__(self, txt, fnt, color, r=ui_rect(), draw_hitbox=None, name="", bg=(255, 255, 255), antialias=True, gap=10, lmar=10, rmar=10, tmar=10, bmar=10, h_align=LEFT_ALIGN, v_align=TOP_ALIGN, return_behavior=None, params=()):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.bg = bg
		
		self.params = params
		
		# Create the text of this button
		self.add_widget(label_w(txt, fnt, color, ui_rect(0, 1, 0, 1, 0, 0, 0, 0), h_align=h_align, v_align=v_align, lmar=lmar, rmar=rmar, tmar=tmar, bmar=bmar))
		
		# If this is None, hitting enter will insert a newline. Otherwise, it will be called with the entry widget as its parameter.
		self.return_behavior = return_behavior
		
		self.event_mask = [pg.KEYDOWN, pg.MOUSEBUTTONDOWN]
		
		self.cur = len(txt)
	
	def collide(self, x, y):
		if x <= self.r and x >= self.l and y >= self.t and y <= self.b:
			return self
	
	def on_event(self, e):
		lbl = self.children[0]
		
		if e.type == pg.KEYDOWN:
			if e.key == pg.K_BACKSPACE:
				if self.cur > 0:
					lbl.txt = lbl.txt[:self.cur-1] + lbl.txt[self.cur:]
					self.cur -= 1
			
			elif e.key == pg.K_DELETE:
				lbl.txt = lbl.txt[:self.cur] + lbl.txt[self.cur+1:]
			
			elif e.key == pg.K_END:
				self.cur = len(lbl.txt)
			
			elif e.key == pg.K_HOME:
				self.cur = 0
			
			elif e.key == pg.K_RETURN:
				if self.return_behavior is None:
					lbl.txt = lbl.txt[:self.cur] + "\n" + lbl.txt[self.cur:]
					self.cur += 1
				else:
					self.return_behavior(self, *self.params)
			
			elif e.key == pg.K_LEFT:
				self.cur -= 1
			
			elif e.key == pg.K_RIGHT:
				self.cur += 1
			
			elif lbl.max_cur == len(lbl.txt) or len(lbl.txt) == 0:
				lbl.txt = lbl.txt[:self.cur] + e.unicode + lbl.txt[self.cur:]
				self.cur += 1
			
			lbl.cache()
		
		elif e.type == pg.MOUSEBUTTONDOWN:
			self.cur = lbl.get_pos(*e.pos)
	
	def render(self, screen):
		pg.draw.rect(screen, self.bg, (self.l, self.t, self.w, self.h))
	
	def set_text(self, s):
		self.children[0].set_text(s)
	
	def get_text(self):
		return self.children[0].txt

class rect_w(widget):
	def __init__(self, color, r=ui_rect, draw_hitbox=None, name=""):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.color = color
	
	def post_cache(self):
		self.block = pg.Surface((self.w, self.h)).convert_alpha()
		self.block.fill(self.color)
	
	def render(self, screen):
		screen.blit(self.block, (self.l, self.t))

# A list of items, only some of which may be visible. Scrolling moves the list up or down.
# "Options" should be an iterable of widgets that may have children. Use widget.clone() to create copies of a template that you can then modify to produce the list.
# These widgets will be displayed option_height pixels below the previous one by modifying their ta, ba, to, and bo values.
# Their ui_rect is entirely controlled by the parent object. spacing should be controlled by the spacing object passed to the constructor.
# It is important that the child widgets don't have colliders (widget.collide() isn't overridden). Otherwise the clicked event won't go to the list itself and your callback won't be called.
class v_scrolling_list_w(widget):
	def __init__(self, options, option_height, num_options_shown, callback, r=ui_rect, draw_hitbox=None, name="", spacing=ui_spacing()):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.s = spacing
		
		self.callback = callback
		
		self.option_height = option_height
		self.num_options_shown = num_options_shown
		
		self.cur = 0
		
		self.event_mask = [pg.MOUSEBUTTONDOWN]
		
		for w in options:
			self.add_widget(w)
			w.bb.la = 0
			w.bb.ra = 1
			w.bb.ta = 0
			w.bb.ba = 0
			w.bb.lo = self.s.lmar
			w.bb.ro = -self.s.rmar
	
	def post_cache(self):
		for w in self.children:
			w.bb.la = 0
			w.bb.ra = 1
			w.bb.ta = 0
			w.bb.ba = 0
			w.bb.lo = self.s.lmar
			w.bb.ro = -self.s.rmar
		
		top_pix = self.s.tmar
		
		first_unshown = min(len(self.children), self.cur + self.num_options_shown)
		
		for w_i in range(0, self.cur):
			self.children[w_i].hidden = True
		
		for w_i in range(self.cur, first_unshown):
			w = self.children[w_i]
			
			w.bb.to = top_pix
			top_pix += self.option_height
			w.bb.bo = top_pix
			top_pix += self.s.gap
			
			w.hidden = False
		
		for w_i in range(first_unshown, len(self.children)):
			self.children[w_i].hidden = True
	
	def on_event(self, e):
		if e.button == 1:
			x,y = e.pos
			first_unshown = min(len(self.children), self.cur + self.num_options_shown)
			
			for w_i in range(self.cur, first_unshown):
				w = self.children[w_i]
				
				if x > w.l and x < w.r and y > w.t and y < w.b:
					self.callback(w)
					break
		
		elif e.button == 5:
			if self.cur + self.num_options_shown < len(self.children):
				self.cur += 1
				self.cache()
		
		elif e.button == 4:
			if self.cur > 0:
				self.cur -= 1
				self.cache()
	
	def collide(self, x, y):
		if x <= self.r and x >= self.l and y >= self.t and y <= self.b:
			return self

# A 9-sliced image. The image is segmented into 9 rectangles by four lines, 2 vertical and 2 horizontal.
# These lines are specified in the constructor for the sliced_asset object passed in the sliced parameter
class sliced_image_w(widget):
	def __init__(self, sliced, r=ui_rect, draw_hitbox=None, name=""):
		widget.__init__(self, r, draw_hitbox, name)
		
		self.sliced = sliced
		
		self.final = None
	
	def post_cache(self):
		s = time.time()
		
		self.final = pg.Surface((self.w, self.h)).convert_alpha()
		
		# These are the values that the sliced lines correspond to in the display's global coordinates.
		l_slice = self.sliced.srce_x_slices[1]
		r_slice = self.w - self.sliced.srce_col_ws[2]
		t_slice = self.sliced.srce_y_slices[1]
		b_slice = self.h - self.sliced.srce_row_hs[2]
		
		mid_slice_w = r_slice - l_slice
		mid_slice_h = b_slice - t_slice
		
		# Draw corners
		self.final.blit(self.sliced.get_crop(0, 0), (0, 0))
		self.final.blit(self.sliced.get_crop(2, 0), (r_slice, 0))
		self.final.blit(self.sliced.get_crop(0, 2), (0, b_slice))
		self.final.blit(self.sliced.get_crop(2, 2), (r_slice, b_slice))
		
		# Draw edges
		self.final.blit(self.sliced.get_crop(0, 1, h=mid_slice_h), (0, t_slice))
		self.final.blit(self.sliced.get_crop(2, 1, h=mid_slice_h), (r_slice, t_slice))
		self.final.blit(self.sliced.get_crop(1, 0, w=mid_slice_w), (l_slice, 0))
		self.final.blit(self.sliced.get_crop(1, 2, w=mid_slice_w), (l_slice, b_slice))
		
		# Draw middle
		self.final.blit(self.sliced.get_crop(1, 1, w=mid_slice_w, h=mid_slice_h), (l_slice, t_slice))
		
		print(time.time() - s)
	
	def render(self, screen):
		screen.blit(self.final, (self.l, self.t))

class layout:
	def __init__(self, screen):
		self.screen = screen
		self.children = []
		
		self.hidden = False
		
		self.event_mask = []
		
		# The most recently clicked element.
		self.active = self
	
	def get_l(self):
		return 0
	
	def get_r(self):
		return self.screen.get_width()
	
	def get_t(self):
		return 0
	
	def get_b(self):
		return self.screen.get_height()
		
	def get_w(self):
		return self.screen.get_width()
	
	def get_h(self):
		return self.screen.get_height()
	
	def cache_r(self):
		if not self.hidden:
			for c in self.children:
#				print("Caching \"" + c.name + "\" (" + str(type(c)) + ")")
				c.cache_r(1)
	
	def resize_r(self):
		if not self.hidden:
			for c in children:
				c.resize_r()
	
	# Render the GUI to the specified screen
	def render_r(self, screen):
		if not self.hidden:
			for c in self.children:
				c.render_r(screen)
	
	def add_widget(self, w):
		w.parent = self
		self.children.append(w)
	
	# Should be called on each event in the pygame queue once per tick so that layout can respond to pygame events.
	def handle_event(self, e):
		if not self.hidden:
			# Handle clicks. Locate the widget that was clicked, notify it
			if e.type == pg.MOUSEBUTTONDOWN:
				col = None
				for c in self.children:
					tmp = c.collide_r(e.pos[0], e.pos[1])
					if tmp is not None:
						col = tmp
				
				if col is not None:
					# Set the clicked widget to active
					self.active = col
					
					# If the clicked object has UI_BUTTON_PRESSED in its event mask, call its handler.
					if pg.MOUSEBUTTONDOWN in col.event_mask:
						col.on_event(e)
				
				else:
					self.active = self
			
			if e.type == pg.KEYDOWN:
				if pg.KEYDOWN in self.active.event_mask:
					self.active.on_event(e)
		