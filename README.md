# A Sense of Humor

A rhythm game where you balance your patients' humors to save their lives.

Humorism  was a system of medicine detailing a supposed makeup and workings of the human body, adopted by Ancient Greek and Roman physicians and philosophers.

These humors were Blood (Sanguine), Yellow Bile (Choleric), Black Bile (Melancholic), and Phlegm (Phlegmatic). It was believed that an imbalance of these humors was what caused different diseases.

## Scoring System

When you press a key, a note is checked for within one of 3 zones specified as the margin for error in milliseconds. The lowest note found in one of these three zones is hit and your score modified. The innermost is the perfect zone. Notes hit in this zone give 20 points. The next zone is the "good" zone, these notes give 10 points. Both perfect and good notes disappear when hit. The outermost zone is the miss zone. Notes found in this (huge) zone cause 10 points to be subtracted. If no notes are found in these zones, 10 points are *subtracted* from your score and the note is not removed. If no notes are found in any of these zones, nothing happens. When a note hits the bottom of the screen, 10 points are subtracted from your score.

The margin for error for these zones are 40, 120, and 400ms. This means there is a span of 80ms (40ms before the perfect time, and 40 after) wherein any given note can be hit to get a "perfect". This is 4.8 frames.

## Track Save Files

Tracks are stored as the audio in an mp3 file, and as a JSON file containing the chart and additional info. This includes the name, time_mul, score_thresh, song_len, and speed.
name: The song's display name in-game.
author: The track's author as credited in-game
notes: An array countaining four rows each corresponding to one of the columns in-game. Each number added refers to a new note at the time specified by that number. The numbers in a given column must be in order.
time_mul: The number of milliseconds in a single unit of time. These units are what the notes are specified in.
score_thresh: The scores required to get a beta, alpha, and omega rank, respectively.
song_len: The length of the song in the same units as the notes are specified in.
speed: The fraction of the vertical height of the game window that notes descend per millisecond. If set to 0.001, notes will moved the height of the screen once per second.
