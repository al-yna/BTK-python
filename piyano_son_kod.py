import pygame
import os
import time
import json
import tkinter as tk
from tkinter import filedialog

# mido kütüphanesini import etmeye çalış, yoksa kullanıcıyı bilgilendir
try:
    from mido import MidiFile
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    print("Uyarı: 'mido' kütüphanesi bulunamadı. MIDI dosyası yükleme özelliği çalışmayacak.")
    print("Lütfen 'pip install mido' komutu ile kurun.")

# --- Ayarlar ve Sabitler ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650 
FPS = 60

WHITE = (255, 255, 255); BLACK = (0, 0, 0); GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230); DARK_GRAY = (100, 100, 100)
RED = (200, 0, 0); BLUE = (0, 100, 200); GREEN = (0, 150, 0)
ORANGE = (255, 140, 0); PURPLE = (128, 0, 128)
BUTTON_TEXT_COLOR = WHITE; INFO_TEXT_COLOR = DARK_GRAY

WHITE_KEY_HEIGHT = 220; BLACK_KEY_HEIGHT = 140
KEY_BORDER_THICKNESS = 1; PIANO_Y_OFFSET = 220; PIANO_X_OFFSET = 20

DISPLAY_PIANO_START_MIDI = 48  # C3
NUM_DISPLAY_KEYS = 35 
DISPLAY_PIANO_END_MIDI = DISPLAY_PIANO_START_MIDI + NUM_DISPLAY_KEYS - 1
NUM_DISPLAY_WHITE_KEYS = 20

SOUND_DIR = "sounds"; DEFAULT_INSTRUMENT = "piano"
NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

ORDERED_KEY_ASSIGNMENTS = [
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p,
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n
]

# --- Mozart Melodisi: Rondo Alla Turca (Türk Marşı) - Uzatılmış Bölüm (~20s) ---
MOZART_MELODY_EXAMPLE = [
    {'time': 0.0, 'note': 76, 'type': 'on', 'velocity': 100},  # E5
    {'time': 0.15, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 0.2, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 0.35, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 0.4, 'note': 73, 'type': 'on', 'velocity': 100},  # C#5
    {'time': 0.55, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 0.6, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 0.75, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 0.8, 'note': 76, 'type': 'on', 'velocity': 100},  # E5
    {'time': 0.95, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 1.0, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 1.15, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 1.2, 'note': 73, 'type': 'on', 'velocity': 100},  # C#5
    {'time': 1.35, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 1.4, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 1.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 1.6, 'note': 76, 'type': 'on', 'velocity': 100},  # E5
    {'time': 1.75, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 1.8, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 1.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 2.0, 'note': 73, 'type': 'on', 'velocity': 100},  # C#5
    {'time': 2.15, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 2.2, 'note': 71, 'type': 'on', 'velocity': 95},   # B4
    {'time': 2.35, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 2.4, 'note': 69, 'type': 'on', 'velocity': 100},  # A4
    {'time': 2.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 2.6, 'note': 68, 'type': 'on', 'velocity': 90},   # G#4 (Ab4)
    {'time': 2.75, 'note': 68, 'type': 'off', 'velocity': 0},
    {'time': 2.8, 'note': 69, 'type': 'on', 'velocity': 100},  # A4
    {'time': 2.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 3.0, 'note': 64, 'type': 'on', 'velocity': 90},   # E4
    {'time': 3.15, 'note': 64, 'type': 'off', 'velocity': 0},
    {'time': 3.2, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 3.35, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 3.4, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 3.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 3.6, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 3.75, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 3.8, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 3.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 4.0, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 4.15, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 4.2, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 4.35, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 4.4, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 4.55, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 4.6, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 4.75, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 4.8, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 4.95, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 5.0, 'note': 74, 'type': 'on', 'velocity': 90},
    {'time': 5.15, 'note': 74, 'type': 'off', 'velocity': 0},
    {'time': 5.2, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 5.35, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 5.4, 'note': 71, 'type': 'on', 'velocity': 95},
    {'time': 5.55, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 5.6, 'note': 69, 'type': 'on', 'velocity': 100},
    {'time': 6.2, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 6.4, 'note': 74, 'type': 'on', 'velocity': 90},
    {'time': 6.55, 'note': 74, 'type': 'off', 'velocity': 0},
    {'time': 6.6, 'note': 73, 'type': 'on', 'velocity': 90},
    {'time': 6.75, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 6.8, 'note': 71, 'type': 'on', 'velocity': 90},
    {'time': 6.95, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 7.0, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 7.15, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 7.2, 'note': 68, 'type': 'on', 'velocity': 90},
    {'time': 7.35, 'note': 68, 'type': 'off', 'velocity': 0},
    {'time': 7.4, 'note': 66, 'type': 'on', 'velocity': 90},
    {'time': 7.55, 'note': 66, 'type': 'off', 'velocity': 0},
    {'time': 7.6, 'note': 64, 'type': 'on', 'velocity': 90},
    {'time': 8.0, 'note': 64, 'type': 'off', 'velocity': 0},
    {'time': 8.2, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 8.35, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 8.4, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 8.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 8.6, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 8.75, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 8.8, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 8.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 9.0, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 9.15, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 9.2, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 9.35, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 9.4, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 9.55, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 9.6, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 9.75, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 9.8, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 9.95, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 10.0, 'note': 74, 'type': 'on', 'velocity': 90},
    {'time': 10.15, 'note': 74, 'type': 'off', 'velocity': 0},
    {'time': 10.2, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 10.35, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 10.4, 'note': 71, 'type': 'on', 'velocity': 95},
    {'time': 10.55, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 10.6, 'note': 69, 'type': 'on', 'velocity': 100},
    {'time': 11.2, 'note': 69, 'type': 'off', 'velocity': 0},
]

# --- Yardımcı Fonksiyonlar ---
def midi_to_note_name(midi_note):
    if not (0 <= midi_note <= 127): return None
    octave_num_for_name = 0
    if midi_note < 12: octave_num_for_name = -1
    elif midi_note < 24: octave_num_for_name = 0
    elif midi_note < 36: octave_num_for_name = 1
    elif midi_note < 48: octave_num_for_name = 2
    elif midi_note < 60: octave_num_for_name = 3
    elif midi_note < 72: octave_num_for_name = 4
    elif midi_note < 84: octave_num_for_name = 5
    elif midi_note < 96: octave_num_for_name = 6
    elif midi_note < 108: octave_num_for_name = 7
    elif midi_note < 120: octave_num_for_name = 8
    else: octave_num_for_name = 9
    note_index = midi_note % 12
    return f"{NOTE_NAMES[note_index]}{octave_num_for_name}"

def get_sound_path(instrument, midi_note):
    note_name = midi_to_note_name(midi_note)
    if note_name: return os.path.join(SOUND_DIR, instrument, f"{note_name}.wav")
    return None

def parse_midi_to_melody(filepath):
    if not MIDO_AVAILABLE:
        print("MIDI ayrıştırma için 'mido' kütüphanesi gerekli ama bulunamadı.")
        return None
    try:
        mid = MidiFile(filepath)
        melody = []
        current_abs_time_seconds = 0
        for msg in mid.play():
            current_abs_time_seconds += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                melody.append({'time': round(current_abs_time_seconds, 4), 'note': msg.note, 'type': 'on', 'velocity': msg.velocity})
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                melody.append({'time': round(current_abs_time_seconds, 4), 'note': msg.note, 'type': 'off', 'velocity': 0})
        print(f"MIDI dosyası '{os.path.basename(filepath)}' ayrıştırıldı, {len(melody)} nota olayı bulundu.")
        return melody
    except Exception as e:
        print(f"MIDI dosyası ('{filepath}') ayrıştırılırken hata: {e}")
        return None

# --- Sınıflar ---
class PianoKey:
    def __init__(self, midi_note, x, y, width, height, is_black, key_char=None):
        self.midi_note=midi_note; self.rect=pygame.Rect(x,y,width,height); self.is_black=is_black
        self.original_color=BLACK if is_black else WHITE; self.pressed_color=DARK_GRAY if is_black else LIGHT_GRAY
        self.current_color=self.original_color; self.key_char=key_char; self.is_pressed=False; self.sound=None
    def draw(self, surface, font_obj):
        pygame.draw.rect(surface,self.current_color,self.rect); pygame.draw.rect(surface,GRAY,self.rect,KEY_BORDER_THICKNESS)
        if self.key_char and self.rect.width > 20:
            try:
                key_name = pygame.key.name(self.key_char).upper()
                if self.key_char >= pygame.K_0 and self.key_char <= pygame.K_9: key_name = chr(self.key_char)
                text_surf = font_obj.render(key_name, True, WHITE if self.is_black else BLACK)
                text_rect = text_surf.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom-(5 if not self.is_black else 3))
                surface.blit(text_surf, text_rect)
            except Exception: pass
    def press(self,audio_manager):
        if not self.is_pressed: self.is_pressed=True; self.current_color=self.pressed_color
        if self.sound: audio_manager.play_sound_obj(self.sound)
        else: audio_manager.play_note(self.midi_note)
    def release(self):
        if self.is_pressed: self.is_pressed=False; self.current_color=self.original_color

class AudioManager:
    def __init__(self):
        try: pygame.mixer.init(frequency=44100,size=-16,channels=2,buffer=512); pygame.mixer.set_num_channels(64); self.mixer_ok=True
        except pygame.error as e: print(f"Mixer hatası: {e}"); self.mixer_ok=False; pygame.mixer=None
        self.sounds_cache={}; self.current_instrument=DEFAULT_INSTRUMENT; self.volume=0.7
    def load_sounds_for_keys(self, instrument_name, piano_keys_to_load):
        if not self.mixer_ok: return
        self.current_instrument=instrument_name;
        current_instrument_cache = self.sounds_cache.get(instrument_name, {})
        loaded_count=0
        for key_obj in piano_keys_to_load:
            if key_obj.midi_note not in current_instrument_cache:
                sound_path=get_sound_path(instrument_name,key_obj.midi_note)
                if sound_path and os.path.exists(sound_path):
                    try: 
                        s_inst=pygame.mixer.Sound(sound_path); s_inst.set_volume(self.volume)
                        key_obj.sound=s_inst; current_instrument_cache[key_obj.midi_note]=s_inst; loaded_count+=1
                    except pygame.error: key_obj.sound=None
                else: key_obj.sound=None
            else: key_obj.sound = current_instrument_cache[key_obj.midi_note]
        self.sounds_cache[instrument_name] = current_instrument_cache
        if loaded_count>0: print(f"{loaded_count} yeni ses '{instrument_name}' için yüklendi.")
    def play_note(self, midi_note):
        if not self.mixer_ok: return
        inst_cache=self.sounds_cache.get(self.current_instrument,{})
        if midi_note in inst_cache and inst_cache[midi_note]: inst_cache[midi_note].play(); return
        sound_path=get_sound_path(self.current_instrument,midi_note)
        if sound_path and os.path.exists(sound_path):
            try:
                s_inst=pygame.mixer.Sound(sound_path); s_inst.set_volume(self.volume); s_inst.play()
                if self.current_instrument not in self.sounds_cache: self.sounds_cache[self.current_instrument]={}
                self.sounds_cache[self.current_instrument][midi_note]=s_inst
            except pygame.error as e: print(f"Dinamik ses hatası: {sound_path} - {e}")
    def play_sound_obj(self, sound_obj):
        if not self.mixer_ok: return;
        if sound_obj: sound_obj.play()
    def set_volume(self, vol):
        if not self.mixer_ok: return
        self.volume=max(0.0,min(1.0,vol))
        for inst_cache_dict in self.sounds_cache.values():
            for sound in inst_cache_dict.values():
                if sound: sound.set_volume(self.volume)
        print(f"Ses: {self.volume:.2f}")

class MIDIManager:
    def __init__(self):
        self.input_device = None
        self.midi_available = False
        try:
            # pygame.midi modülünün varlığını kontrol et
            if hasattr(pygame, 'midi'):
                pygame.midi.init()
                self.midi_available = True
            else:
                print("Hata: Pygame kurulumunuzda 'midi' modülü bulunmuyor.")
                print("Pygame'i MIDI desteğiyle kurduğunuzdan emin olun.")
        except pygame.error as e: # Pygame'in genel hataları (örn: MIDI sistemi başlatılamadı)
            print(f"Pygame MIDI başlatılırken hata: {e}")
            print("Sisteminizde MIDI için gerekli sürücüler/kütüphaneler eksik olabilir (örn: PortMIDI).")
        except Exception as e: # Diğer beklenmedik hatalar
            print(f"MIDI sistemi başlatılırken genel bir hata oluştu: {e}")

    def print_device_info(self):
        if not self.midi_available: print("MIDI sistemi mevcut değil veya başlatılamadı."); return
        print("\nMIDI Giriş Cihazları:"); found=False
        try:
            for i in range(pygame.midi.get_count()):
                info=pygame.midi.get_device_info(i)
                if info and info[2]==1: print(f"  ID: {i}, Adı: {info[1].decode(errors='ignore')}"); found=True
            if not found: print("  Kullanılabilir MIDI giriş cihazı bulunamadı.")
            default_id=pygame.midi.get_default_input_id()
            if default_id!=-1: print(f"Varsayılan ID: {default_id}")
        except pygame.error as e:
            print(f"MIDI cihaz bilgileri alınırken Pygame hatası: {e}")
        print("-" * 30)

    def open_input_device(self, dev_id=None):
        if not self.midi_available: return False
        if self.input_device: self.close_input_device()
        try:
            actual_id=dev_id if dev_id is not None else pygame.midi.get_default_input_id()
            if actual_id!=-1:
                self.input_device=pygame.midi.Input(actual_id)
                info=pygame.midi.get_device_info(actual_id)
                if info: print(f"MIDI Açıldı: ID {actual_id} - {info[1].decode(errors='ignore')}"); return True
                self.input_device.close(); self.input_device=None; print(f"ID {actual_id} info alınamadı."); return False
            print("Uygun MIDI cihazı yok."); return False
        except pygame.error as e:
            print(f"MIDI cihazı açılırken Pygame hatası (ID: {dev_id}): {e}")
            self.input_device = None; return False
        except Exception as e: 
            print(f"MIDI açma hatası (ID: {dev_id}): {e}"); self.input_device=None; return False

    def poll_events(self):
        if not self.input_device or not self.midi_available: return []
        events=[]
        try:
            if self.input_device.poll():
                for midi_event in self.input_device.read(30):
                    d,t=midi_event; s=d[0]&0xF0; n=d[1]; v=d[2]
                    if s==0x90: events.append({'type':'midi_on' if v>0 else 'midi_off','note':n,'velocity':v,'timestamp':t})
                    elif s==0x80: events.append({'type':'midi_off','note':n,'timestamp':t})
        except pygame.error as e:
            print(f"MIDI olayları okunurken Pygame hatası: {e}")
            self.close_input_device() # Sorunlu cihazı kapat
        return events

    def close_input_device(self):
        if not self.input_device or not self.midi_available: return
        try:
            print("MIDI Kapatılıyor."); self.input_device.close(); self.input_device=None
        except pygame.error as e:
            print(f"MIDI cihazı kapatılırken Pygame hatası: {e}")
            self.input_device = None # Hata durumunda da null yap

    def quit(self):
        if not self.midi_available: return
        self.close_input_device()
        try:
            pygame.midi.quit()
        except pygame.error as e:
            print(f"Pygame MIDI sonlandırılırken hata: {e}")
        except AttributeError:
             pass # Pygame.midi hiç var olmadıysa


class Recorder:
    def __init__(self): self.is_recording=False; self.melody=[]; self.start_record_time_abs=0
    def toggle_recording(self):
        self.is_recording=not self.is_recording
        if self.is_recording: self.melody=[]; self.start_record_time_abs=time.time(); print("Kayıt Başladı.")
        else: print(f"Kayıt Durdu. {len(self.melody)} olay.")
        return self.is_recording
    def record_event(self, midi_note,event_type,velocity=64):
        if self.is_recording: self.melody.append({'time':round(time.time()-self.start_record_time_abs,4),'note':midi_note,'type':event_type,'velocity':velocity})
    def save_melody(self,filename="melody.json"):
        if not self.melody: print("Melodi yok."); return False
        try:
            with open(filename,'w') as f: json.dump(self.melody,f,indent=2)
            print(f"Kaydedildi: {filename}"); return True
        except Exception as e: print(f"Kaydetme hatası: {e}"); return False
    def load_melody(self,filename="melody.json"):
        if not os.path.exists(filename): print(f"Dosya yok: {filename}"); return False
        try:
            with open(filename,'r') as f: self.melody=json.load(f)
            print(f"Yüklendi: {filename}. {len(self.melody)} olay."); return True
        except Exception as e: print(f"Yükleme hatası ({filename}): {e}"); return False

class Piano:
    def __init__(self, x_offset, y_offset, audio_manager, white_key_w, black_key_w, black_key_h):
        self.keys = []; self.x_offset = x_offset; self.y_offset = y_offset
        self.audio_manager = audio_manager
        self.font_for_keys = pygame.font.SysFont("Arial", 12, bold=True)
        self.white_key_width = white_key_w; self.black_key_width = black_key_w
        self.black_key_height = black_key_h
        self._generate_display_keys(DISPLAY_PIANO_START_MIDI, NUM_DISPLAY_KEYS)
        if audio_manager.mixer_ok: 
            self.audio_manager.load_sounds_for_keys(DEFAULT_INSTRUMENT, self.keys)

    def _generate_display_keys(self, start_midi, num_total_keys):
        self.keys = []; current_x_white = self.x_offset; key_assignment_idx = 0 
        note_pattern_is_white = [True, False, True, False, True, True, False, True, False, True, False, True]
        print("\n--- Klavye Eşleşmeleri (Piyano Notası -> Klavye Tuşu) ---")
        temp_keys_for_layout = []
        for i in range(num_total_keys):
            midi_note = start_midi + i
            if midi_note > 127 : break
            is_black = not note_pattern_is_white[midi_note % 12]
            key_char = ORDERED_KEY_ASSIGNMENTS[key_assignment_idx] if key_assignment_idx < len(ORDERED_KEY_ASSIGNMENTS) and key_assignment_idx < num_total_keys else None
            key_obj = PianoKey(midi_note, 0, 0, 0, 0, is_black, key_char)
            temp_keys_for_layout.append(key_obj)
            if key_char:
                char_name = pygame.key.name(key_char).upper()
                if key_char >= pygame.K_0 and key_char <= pygame.K_9: char_name = chr(key_char)
                print(f"  {midi_to_note_name(midi_note)} ({'S' if is_black else 'B'}): {char_name}")
            key_assignment_idx += 1
        white_keys_for_black_placement = []
        for key_obj in temp_keys_for_layout:
            if not key_obj.is_black:
                key_obj.rect = pygame.Rect(current_x_white, self.y_offset, self.white_key_width, WHITE_KEY_HEIGHT)
                white_keys_for_black_placement.append(key_obj); self.keys.append(key_obj)
                current_x_white += self.white_key_width
        for key_obj in temp_keys_for_layout:
            if key_obj.is_black:
                found_prev_white = False
                for wk in white_keys_for_black_placement:
                    if wk.midi_note == key_obj.midi_note -1:
                         key_obj.rect = pygame.Rect(wk.rect.right - (self.black_key_width / 2), 
                                                   self.y_offset, self.black_key_width, self.black_key_height)
                         found_prev_white = True; break
                if found_prev_white: self.keys.append(key_obj)
        self.keys.sort(key=lambda k: k.midi_note)
        print("--- Eşleşmeler Son --- \n")
    def draw(self, surface):
        for key in self.keys:
            if not key.is_black: key.draw(surface, self.font_for_keys)
        for key in self.keys:
            if key.is_black: key.draw(surface, self.font_for_keys)
    def get_key_by_midi_note(self, midi_note):
        for key in self.keys:
            if key.midi_note == midi_note: return key
        return None
    def handle_mouse_press(self, pos, recorder):
        for key_type_pass in [True, False]: 
            for key in self.keys:
                if key.is_black == key_type_pass and key.rect.collidepoint(pos):
                    key.press(self.audio_manager);
                    if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'on')
                    return True
        return False
    def handle_mouse_release(self, recorder):
        for key in self.keys:
            if key.is_pressed:
                key.release();
                if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'off')
    def handle_key_event(self, pygame_key, event_type_str, recorder):
        for key in self.keys:
            if key.key_char == pygame_key:
                if event_type_str == 'on' and not key.is_pressed:
                    key.press(self.audio_manager)
                    if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'on')
                elif event_type_str == 'off' and key.is_pressed:
                    key.release()
                    if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'off')
                return True
        return False

class PlaybackHandler:
    def __init__(self,piano,audio_manager): self.piano=piano;self.audio_manager=audio_manager;self.melody_to_play=[];self.current_event_index=0;self.playback_time_elapsed=0;self.is_playing=False;self.real_start_time=0
    def start_playback(self,melody):
        if not melody: print("Çalınacak melodi yok.");return
        self.melody_to_play=sorted(melody,key=lambda x:x['time']);self.current_event_index=0;self.playback_time_elapsed=0;self.real_start_time=time.time();self.is_playing=True;print("Çalma başlatıldı.")
        for k in self.piano.keys:
            if k.is_pressed:k.release()
    def stop_playback(self):
        if not self.is_playing: return
        self.is_playing=False
        for k in self.piano.keys:
            if k.is_pressed:k.release()
    def update(self):
        if not self.is_playing or not self.melody_to_play: return
        self.playback_time_elapsed=time.time()-self.real_start_time
        while self.current_event_index<len(self.melody_to_play):
            e=self.melody_to_play[self.current_event_index]
            if self.playback_time_elapsed>=e['time']:
                key_obj=self.piano.get_key_by_midi_note(e['note'])
                if e['type']=='on':self.audio_manager.play_note(e['note']);
                if key_obj:key_obj.current_color=key_obj.pressed_color if e['type']=='on' else key_obj.original_color
                self.current_event_index+=1
            else:break
        if self.current_event_index>=len(self.melody_to_play):
            self.stop_playback()
            print("Melodi bitti.")

class Game:
    def __init__(self):
        pygame.init()
        self.dynamic_white_key_width = (SCREEN_WIDTH - 2 * PIANO_X_OFFSET) / NUM_DISPLAY_WHITE_KEYS
        self.dynamic_black_key_width = self.dynamic_white_key_width * 0.62 
        self.dynamic_black_key_height = WHITE_KEY_HEIGHT * 0.65
        print(f"Beyaz Tuş Genişliği ({NUM_DISPLAY_KEYS}-tuş piyano): {self.dynamic_white_key_width:.2f}px")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Python Piyano - {NUM_DISPLAY_KEYS} Tuş ({midi_to_note_name(DISPLAY_PIANO_START_MIDI)}-{midi_to_note_name(DISPLAY_PIANO_END_MIDI)})")
        self.clock = pygame.time.Clock(); self.ui_font = pygame.font.SysFont("Verdana", 16)
        self.title_font = pygame.font.SysFont("Verdana", 24, bold=True)
        
        self.audio_manager = AudioManager()
        self.piano = Piano(PIANO_X_OFFSET, PIANO_Y_OFFSET, self.audio_manager, 
                           self.dynamic_white_key_width, self.dynamic_black_key_width, self.dynamic_black_key_height)
        self.midi_manager = MIDIManager(); self.recorder = Recorder()
        self.playback_handler = PlaybackHandler(self.piano, self.audio_manager)
        self.running = True; self.active_midi_device_name = "Yok"
        self._setup_ui_elements()
        self.root_tk = None 

    def _setup_ui_elements(self):
        btn_h=35; btn_w=200; p=10; y_start=60
        x_col1=SCREEN_WIDTH-btn_w-p
        self.record_button_rect=pygame.Rect(x_col1,y_start,btn_w,btn_h)
        self.play_button_rect=pygame.Rect(x_col1,y_start+(btn_h+p),btn_w,btn_h)
        self.save_button_rect=pygame.Rect(x_col1,y_start+2*(btn_h+p),btn_w,btn_h)
        self.load_button_rect=pygame.Rect(x_col1,y_start+3*(btn_h+p),btn_w,btn_h)
        self.mozart_button_rect = pygame.Rect(x_col1, y_start + 4*(btn_h + p), btn_w, btn_h)
        # Nikah Masası butonu kaldırıldı, MIDI Yükle onun yerine geldi
        self.load_midi_button_rect = pygame.Rect(x_col1, y_start + 5*(btn_h + p), btn_w, btn_h)


        x_col0=p; btn_w0=220
        self.midi_open_button_rect=pygame.Rect(x_col0,y_start,btn_w0,btn_h)
        vol_btn_w=(btn_w0-p)//2
        self.volume_up_rect=pygame.Rect(x_col0,y_start+(btn_h+p),vol_btn_w,btn_h)
        self.volume_down_rect=pygame.Rect(x_col0+vol_btn_w+p,y_start+(btn_h+p),vol_btn_w,btn_h)
        
    def run(self):
        if self.midi_manager.open_input_device():
            dev_id=pygame.midi.get_default_input_id()
            if dev_id!=-1:
                info=pygame.midi.get_device_info(dev_id)
                if info: self.active_midi_device_name=info[1].decode(errors='ignore').split(" ",1)[0][:15]
        while self.running:
            self.clock.tick(FPS)
            self._handle_events();self._process_midi();self._update_playback();self._render()
        self._cleanup()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: self.running=False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                pos=event.pos
                if self.record_button_rect.collidepoint(pos): self.recorder.toggle_recording();self.playback_handler.stop_playback()
                elif self.play_button_rect.collidepoint(pos) and not self.recorder.is_recording and self.recorder.melody: self.playback_handler.start_playback(self.recorder.melody)
                elif self.mozart_button_rect.collidepoint(pos) and not self.recorder.is_recording:
                    print("Mozart - Rondo Alla Turca çalınıyor...")
                    self.playback_handler.start_playback(MOZART_MELODY_EXAMPLE)
                # Nikah Masası butonu için elif kaldırıldı
                elif self.load_midi_button_rect.collidepoint(pos) and not self.recorder.is_recording:
                    self._load_and_play_midi_file()
                elif self.save_button_rect.collidepoint(pos) and not self.recorder.is_recording: self.recorder.save_melody()
                elif self.load_button_rect.collidepoint(pos) and not self.recorder.is_recording:
                    if self.recorder.load_melody(): self.playback_handler.stop_playback()
                elif self.midi_open_button_rect.collidepoint(pos): self._handle_midi_device_selection()
                elif self.volume_up_rect.collidepoint(pos): self.audio_manager.set_volume(self.audio_manager.volume+0.05)
                elif self.volume_down_rect.collidepoint(pos): self.audio_manager.set_volume(self.audio_manager.volume-0.05)
                else: self.piano.handle_mouse_press(pos,self.recorder)
            
            if event.type==pygame.MOUSEBUTTONUP and event.button==1: self.piano.handle_mouse_release(self.recorder)
            
            if event.type==pygame.KEYDOWN:
                self.piano.handle_key_event(event.key,'on',self.recorder)
                if event.key==pygame.K_SPACE: self.recorder.toggle_recording();self.playback_handler.stop_playback()
                elif event.key==pygame.K_UP: self.audio_manager.set_volume(self.audio_manager.volume+0.05)
                elif event.key==pygame.K_DOWN: self.audio_manager.set_volume(self.audio_manager.volume-0.05)

            if event.type==pygame.KEYUP: 
                self.piano.handle_key_event(event.key,'off',self.recorder)

    def _load_and_play_midi_file(self):
        if not MIDO_AVAILABLE:
            print("MIDI dosyası yüklemek için 'mido' kütüphanesi kurulu olmalı.")
            return
        try:
            if self.root_tk is None: 
                self.root_tk = tk.Tk()
            self.root_tk.withdraw() # Ana Tkinter penceresini gizle
            
            filepath = filedialog.askopenfilename(
                parent=self.root_tk, # Dosya diyalogunun ana penceresi
                title="MIDI Dosyası Seç (.mid)",
                filetypes=(("MIDI dosyaları", "*.mid *.midi"), ("Tüm dosyalar", "*.*"))
            )
            # self.root_tk.deiconify() # İsteğe bağlı: Diyalog sonrası root'u tekrar görünür yap (genelde gerekmez)
        except Exception as e:
            print(f"Dosya seçme penceresi hatası: {e}")
            filepath = None

        if filepath:
            print(f"Seçilen MIDI dosyası: {filepath}")
            # Kullanıcıya MP3 değil, MIDI seçmesi gerektiğini hatırlat (dosya tipi filtresine rağmen)
            if not (filepath.lower().endswith(".mid") or filepath.lower().endswith(".midi")):
                print("Hata: Lütfen geçerli bir MIDI dosyası (.mid veya .midi) seçin.")
                return

            parsed_melody = parse_midi_to_melody(filepath)
            if parsed_melody:
                self.playback_handler.stop_playback()
                self.playback_handler.start_playback(parsed_melody)
            else:
                print("MIDI dosyası ayrıştırılamadı veya boş.")
        else:
            print("MIDI dosyası seçilmedi.")


    def _handle_midi_device_selection(self):
        self.midi_manager.print_device_info()
        try:
            pygame.display.iconify(); dev_id_str=input("MIDI ID: ")
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            if dev_id_str.strip():
                dev_id=int(dev_id_str)
                if self.midi_manager.open_input_device(dev_id):
                    info=pygame.midi.get_device_info(dev_id)
                    if info: self.active_midi_device_name=info[1].decode(errors='ignore').split(" ",1)[0][:15]
                else: self.active_midi_device_name="Yok (Hata)"
            else: self.midi_manager.close_input_device();self.active_midi_device_name="Yok"
        except ValueError: print("Geçersiz ID.")
        except Exception as e: print(f"MIDI seçimi hatası: {e}");self.active_midi_device_name="Yok (Hata)"
    
    def _process_midi(self):
        midi_events=self.midi_manager.poll_events()
        for event in midi_events:
            key_on_screen=self.piano.get_key_by_midi_note(event['note'])
            if event['type']=='midi_on':
                self.audio_manager.play_note(event['note'])
                if key_on_screen: key_on_screen.press(self.audio_manager)
                if self.recorder and self.recorder.is_recording : self.recorder.record_event(event['note'],'on',event['velocity'])
            elif event['type']=='midi_off':
                if key_on_screen: key_on_screen.release()
                if self.recorder and self.recorder.is_recording: self.recorder.record_event(event['note'],'off')
    
    def _update_playback(self):
        if self.playback_handler.is_playing: self.playback_handler.update()
    
    def _draw_button(self, rect, text, base_clr, hi_clr=None, state=False, text_clr=BUTTON_TEXT_COLOR):
        final_clr = hi_clr if state and hi_clr else base_clr
        pygame.draw.rect(self.screen,final_clr,rect,border_radius=6)
        pygame.draw.rect(self.screen,DARK_GRAY,rect,2,border_radius=6)
        txt_s=self.ui_font.render(text,True,text_clr)
        self.screen.blit(txt_s,txt_s.get_rect(center=rect.center))

    def _render(self):
        self.screen.fill(LIGHT_GRAY)
        start_note_name = midi_to_note_name(DISPLAY_PIANO_START_MIDI)
        end_note_name = midi_to_note_name(DISPLAY_PIANO_END_MIDI)
        title_text = f"Python Piyano - {NUM_DISPLAY_KEYS} Tuş ({start_note_name} - {end_note_name})"
        title_s=self.title_font.render(title_text,True,DARK_GRAY)
        self.screen.blit(title_s,(self.screen.get_width()//2-title_s.get_width()//2,15))
        
        self.piano.draw(self.screen)
        self._draw_button(self.record_button_rect,'Kaydediliyor...' if self.recorder.is_recording else 'Kayıt Başlat/Durdur',BLUE,RED,self.recorder.is_recording)
        self._draw_button(self.play_button_rect,'Çalınıyor...' if self.playback_handler.is_playing else 'Melodiyi Çal',GREEN,DARK_GRAY,self.playback_handler.is_playing or not self.recorder.melody)
        self._draw_button(self.mozart_button_rect, "Mozart Çal", ORANGE, DARK_GRAY, self.playback_handler.is_playing and self.playback_handler.melody_to_play == MOZART_MELODY_EXAMPLE)
        # Nikah Masası butonu çizimi kaldırıldı
        self._draw_button(self.load_midi_button_rect, "MIDI Yükle & Çal", PURPLE, DARK_GRAY, self.playback_handler.is_playing and self.playback_handler.melody_to_play not in [MOZART_MELODY_EXAMPLE, self.recorder.melody])
        self._draw_button(self.save_button_rect,"Kaydet (.json)",BLUE)
        self._draw_button(self.load_button_rect,"Yükle (.json)",BLUE)
        self._draw_button(self.midi_open_button_rect,f"MIDI: {self.active_midi_device_name}",DARK_GRAY,text_clr=(WHITE if self.active_midi_device_name!="Yok" else GRAY))
        self._draw_button(self.volume_up_rect,"Ses +",GREEN)
        self._draw_button(self.volume_down_rect,"Ses -",RED)
        status_y=self.screen.get_height()-30
        status_txt1=f"Enstrüman: {self.audio_manager.current_instrument} | Ses: {int(self.audio_manager.volume*100)}%"
        self.screen.blit(self.ui_font.render(status_txt1,True,BLACK),(20,status_y))
        if self.recorder.is_recording:
            rec_dur=time.time()-self.recorder.start_record_time_abs
            self.screen.blit(self.ui_font.render(f"Kayıt: {rec_dur:.1f}s",True,RED),(SCREEN_WIDTH//2-50,status_y))
        pygame.display.flip()
    
    def _cleanup(self):
        print("Uygulama kapatılıyor...");
        if self.root_tk:
            try:
                self.root_tk.quit()
                self.root_tk.destroy()
            except tk.TclError: pass # Pencere zaten yoksa
            except Exception as e: print(f"Tkinter kapatılırken hata: {e}")
        self.midi_manager.quit();pygame.quit()

if __name__ == '__main__':
    if not os.path.exists(SOUND_DIR): os.makedirs(SOUND_DIR); print(f"'{SOUND_DIR}' oluşturuldu.")
    def_instr_dir = os.path.join(SOUND_DIR, DEFAULT_INSTRUMENT)
    if not os.path.exists(def_instr_dir):
        os.makedirs(def_instr_dir); print(f"'{def_instr_dir}' oluşturuldu.")
        print(f"Lütfen .wav piyano ses dosyalarınızı bu klasöre ekleyin.")
        print(f"Bu piyano {midi_to_note_name(DISPLAY_PIANO_START_MIDI)} - {midi_to_note_name(DISPLAY_PIANO_END_MIDI)} aralığını gösterir.")
    game = Game(); game.run()

import pygame
import os
import time
import json
import tkinter as tk
from tkinter import filedialog

# mido kütüphanesini import etmeye çalış, yoksa kullanıcıyı bilgilendir
try:
    from mido import MidiFile
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    print("Uyarı: 'mido' kütüphanesi bulunamadı. MIDI dosyası yükleme özelliği çalışmayacak.")
    print("Lütfen 'pip install mido' komutu ile kurun.")

# --- Ayarlar ve Sabitler ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650 
FPS = 60

WHITE = (255, 255, 255); BLACK = (0, 0, 0); GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230); DARK_GRAY = (100, 100, 100)
RED = (200, 0, 0); BLUE = (0, 100, 200); GREEN = (0, 150, 0)
ORANGE = (255, 140, 0); PURPLE = (128, 0, 128)
BUTTON_TEXT_COLOR = WHITE; INFO_TEXT_COLOR = DARK_GRAY

WHITE_KEY_HEIGHT = 220; BLACK_KEY_HEIGHT = 140
KEY_BORDER_THICKNESS = 1; PIANO_Y_OFFSET = 220; PIANO_X_OFFSET = 20

DISPLAY_PIANO_START_MIDI = 48  # C3
NUM_DISPLAY_KEYS = 35 
DISPLAY_PIANO_END_MIDI = DISPLAY_PIANO_START_MIDI + NUM_DISPLAY_KEYS - 1
NUM_DISPLAY_WHITE_KEYS = 20

SOUND_DIR = "sounds"; DEFAULT_INSTRUMENT = "piano"
NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

ORDERED_KEY_ASSIGNMENTS = [
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p,
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n
]

# --- Mozart Melodisi: Rondo Alla Turca (Türk Marşı) - Uzatılmış Bölüm (~20s) ---
MOZART_MELODY_EXAMPLE = [
    {'time': 0.0, 'note': 76, 'type': 'on', 'velocity': 100},  # E5
    {'time': 0.15, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 0.2, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 0.35, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 0.4, 'note': 73, 'type': 'on', 'velocity': 100},  # C#5
    {'time': 0.55, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 0.6, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 0.75, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 0.8, 'note': 76, 'type': 'on', 'velocity': 100},  # E5
    {'time': 0.95, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 1.0, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 1.15, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 1.2, 'note': 73, 'type': 'on', 'velocity': 100},  # C#5
    {'time': 1.35, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 1.4, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 1.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 1.6, 'note': 76, 'type': 'on', 'velocity': 100},  # E5
    {'time': 1.75, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 1.8, 'note': 69, 'type': 'on', 'velocity': 90},   # A4
    {'time': 1.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 2.0, 'note': 73, 'type': 'on', 'velocity': 100},  # C#5
    {'time': 2.15, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 2.2, 'note': 71, 'type': 'on', 'velocity': 95},   # B4
    {'time': 2.35, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 2.4, 'note': 69, 'type': 'on', 'velocity': 100},  # A4
    {'time': 2.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 2.6, 'note': 68, 'type': 'on', 'velocity': 90},   # G#4 (Ab4)
    {'time': 2.75, 'note': 68, 'type': 'off', 'velocity': 0},
    {'time': 2.8, 'note': 69, 'type': 'on', 'velocity': 100},  # A4
    {'time': 2.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 3.0, 'note': 64, 'type': 'on', 'velocity': 90},   # E4
    {'time': 3.15, 'note': 64, 'type': 'off', 'velocity': 0},
    {'time': 3.2, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 3.35, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 3.4, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 3.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 3.6, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 3.75, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 3.8, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 3.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 4.0, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 4.15, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 4.2, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 4.35, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 4.4, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 4.55, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 4.6, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 4.75, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 4.8, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 4.95, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 5.0, 'note': 74, 'type': 'on', 'velocity': 90},
    {'time': 5.15, 'note': 74, 'type': 'off', 'velocity': 0},
    {'time': 5.2, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 5.35, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 5.4, 'note': 71, 'type': 'on', 'velocity': 95},
    {'time': 5.55, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 5.6, 'note': 69, 'type': 'on', 'velocity': 100},
    {'time': 6.2, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 6.4, 'note': 74, 'type': 'on', 'velocity': 90},
    {'time': 6.55, 'note': 74, 'type': 'off', 'velocity': 0},
    {'time': 6.6, 'note': 73, 'type': 'on', 'velocity': 90},
    {'time': 6.75, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 6.8, 'note': 71, 'type': 'on', 'velocity': 90},
    {'time': 6.95, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 7.0, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 7.15, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 7.2, 'note': 68, 'type': 'on', 'velocity': 90},
    {'time': 7.35, 'note': 68, 'type': 'off', 'velocity': 0},
    {'time': 7.4, 'note': 66, 'type': 'on', 'velocity': 90},
    {'time': 7.55, 'note': 66, 'type': 'off', 'velocity': 0},
    {'time': 7.6, 'note': 64, 'type': 'on', 'velocity': 90},
    {'time': 8.0, 'note': 64, 'type': 'off', 'velocity': 0},
    {'time': 8.2, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 8.35, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 8.4, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 8.55, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 8.6, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 8.75, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 8.8, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 8.95, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 9.0, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 9.15, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 9.2, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 9.35, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 9.4, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 9.55, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 9.6, 'note': 69, 'type': 'on', 'velocity': 90},
    {'time': 9.75, 'note': 69, 'type': 'off', 'velocity': 0},
    {'time': 9.8, 'note': 76, 'type': 'on', 'velocity': 100},
    {'time': 9.95, 'note': 76, 'type': 'off', 'velocity': 0},
    {'time': 10.0, 'note': 74, 'type': 'on', 'velocity': 90},
    {'time': 10.15, 'note': 74, 'type': 'off', 'velocity': 0},
    {'time': 10.2, 'note': 73, 'type': 'on', 'velocity': 100},
    {'time': 10.35, 'note': 73, 'type': 'off', 'velocity': 0},
    {'time': 10.4, 'note': 71, 'type': 'on', 'velocity': 95},
    {'time': 10.55, 'note': 71, 'type': 'off', 'velocity': 0},
    {'time': 10.6, 'note': 69, 'type': 'on', 'velocity': 100},
    {'time': 11.2, 'note': 69, 'type': 'off', 'velocity': 0},
]

# --- Yardımcı Fonksiyonlar ---
def midi_to_note_name(midi_note):
    if not (0 <= midi_note <= 127): return None
    octave_num_for_name = 0
    if midi_note < 12: octave_num_for_name = -1
    elif midi_note < 24: octave_num_for_name = 0
    elif midi_note < 36: octave_num_for_name = 1
    elif midi_note < 48: octave_num_for_name = 2
    elif midi_note < 60: octave_num_for_name = 3
    elif midi_note < 72: octave_num_for_name = 4
    elif midi_note < 84: octave_num_for_name = 5
    elif midi_note < 96: octave_num_for_name = 6
    elif midi_note < 108: octave_num_for_name = 7
    elif midi_note < 120: octave_num_for_name = 8
    else: octave_num_for_name = 9
    note_index = midi_note % 12
    return f"{NOTE_NAMES[note_index]}{octave_num_for_name}"

def get_sound_path(instrument, midi_note):
    note_name = midi_to_note_name(midi_note)
    if note_name: return os.path.join(SOUND_DIR, instrument, f"{note_name}.wav")
    return None

def parse_midi_to_melody(filepath):
    if not MIDO_AVAILABLE:
        print("MIDI ayrıştırma için 'mido' kütüphanesi gerekli ama bulunamadı.")
        return None
    try:
        mid = MidiFile(filepath)
        melody = []
        current_abs_time_seconds = 0
        for msg in mid.play():
            current_abs_time_seconds += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                melody.append({'time': round(current_abs_time_seconds, 4), 'note': msg.note, 'type': 'on', 'velocity': msg.velocity})
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                melody.append({'time': round(current_abs_time_seconds, 4), 'note': msg.note, 'type': 'off', 'velocity': 0})
        print(f"MIDI dosyası '{os.path.basename(filepath)}' ayrıştırıldı, {len(melody)} nota olayı bulundu.")
        return melody
    except Exception as e:
        print(f"MIDI dosyası ('{filepath}') ayrıştırılırken hata: {e}")
        return None

# --- Sınıflar ---
class PianoKey:
    def __init__(self, midi_note, x, y, width, height, is_black, key_char=None):
        self.midi_note=midi_note; self.rect=pygame.Rect(x,y,width,height); self.is_black=is_black
        self.original_color=BLACK if is_black else WHITE; self.pressed_color=DARK_GRAY if is_black else LIGHT_GRAY
        self.current_color=self.original_color; self.key_char=key_char; self.is_pressed=False; self.sound=None
    def draw(self, surface, font_obj):
        pygame.draw.rect(surface,self.current_color,self.rect); pygame.draw.rect(surface,GRAY,self.rect,KEY_BORDER_THICKNESS)
        if self.key_char and self.rect.width > 20:
            try:
                key_name = pygame.key.name(self.key_char).upper()
                if self.key_char >= pygame.K_0 and self.key_char <= pygame.K_9: key_name = chr(self.key_char)
                text_surf = font_obj.render(key_name, True, WHITE if self.is_black else BLACK)
                text_rect = text_surf.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom-(5 if not self.is_black else 3))
                surface.blit(text_surf, text_rect)
            except Exception: pass
    def press(self,audio_manager):
        if not self.is_pressed: self.is_pressed=True; self.current_color=self.pressed_color
        if self.sound: audio_manager.play_sound_obj(self.sound)
        else: audio_manager.play_note(self.midi_note)
    def release(self):
        if self.is_pressed: self.is_pressed=False; self.current_color=self.original_color

class AudioManager:
    def __init__(self):
        try: pygame.mixer.init(frequency=44100,size=-16,channels=2,buffer=512); pygame.mixer.set_num_channels(64); self.mixer_ok=True
        except pygame.error as e: print(f"Mixer hatası: {e}"); self.mixer_ok=False; pygame.mixer=None
        self.sounds_cache={}; self.current_instrument=DEFAULT_INSTRUMENT; self.volume=0.7
    def load_sounds_for_keys(self, instrument_name, piano_keys_to_load):
        if not self.mixer_ok: return
        self.current_instrument=instrument_name;
        current_instrument_cache = self.sounds_cache.get(instrument_name, {})
        loaded_count=0
        for key_obj in piano_keys_to_load:
            if key_obj.midi_note not in current_instrument_cache:
                sound_path=get_sound_path(instrument_name,key_obj.midi_note)
                if sound_path and os.path.exists(sound_path):
                    try: 
                        s_inst=pygame.mixer.Sound(sound_path); s_inst.set_volume(self.volume)
                        key_obj.sound=s_inst; current_instrument_cache[key_obj.midi_note]=s_inst; loaded_count+=1
                    except pygame.error: key_obj.sound=None
                else: key_obj.sound=None
            else: key_obj.sound = current_instrument_cache[key_obj.midi_note]
        self.sounds_cache[instrument_name] = current_instrument_cache
        if loaded_count>0: print(f"{loaded_count} yeni ses '{instrument_name}' için yüklendi.")
    def play_note(self, midi_note):
        if not self.mixer_ok: return
        inst_cache=self.sounds_cache.get(self.current_instrument,{})
        if midi_note in inst_cache and inst_cache[midi_note]: inst_cache[midi_note].play(); return
        sound_path=get_sound_path(self.current_instrument,midi_note)
        if sound_path and os.path.exists(sound_path):
            try:
                s_inst=pygame.mixer.Sound(sound_path); s_inst.set_volume(self.volume); s_inst.play()
                if self.current_instrument not in self.sounds_cache: self.sounds_cache[self.current_instrument]={}
                self.sounds_cache[self.current_instrument][midi_note]=s_inst
            except pygame.error as e: print(f"Dinamik ses hatası: {sound_path} - {e}")
    def play_sound_obj(self, sound_obj):
        if not self.mixer_ok: return;
        if sound_obj: sound_obj.play()
    def set_volume(self, vol):
        if not self.mixer_ok: return
        self.volume=max(0.0,min(1.0,vol))
        for inst_cache_dict in self.sounds_cache.values():
            for sound in inst_cache_dict.values():
                if sound: sound.set_volume(self.volume)
        print(f"Ses: {self.volume:.2f}")

class MIDIManager:
    def __init__(self):
        self.input_device = None
        self.midi_available = False
        try:
            # pygame.midi modülünün varlığını kontrol et
            if hasattr(pygame, 'midi'):
                pygame.midi.init()
                self.midi_available = True
            else:
                print("Hata: Pygame kurulumunuzda 'midi' modülü bulunmuyor.")
                print("Pygame'i MIDI desteğiyle kurduğunuzdan emin olun.")
        except pygame.error as e: # Pygame'in genel hataları (örn: MIDI sistemi başlatılamadı)
            print(f"Pygame MIDI başlatılırken hata: {e}")
            print("Sisteminizde MIDI için gerekli sürücüler/kütüphaneler eksik olabilir (örn: PortMIDI).")
        except Exception as e: # Diğer beklenmedik hatalar
            print(f"MIDI sistemi başlatılırken genel bir hata oluştu: {e}")

    def print_device_info(self):
        if not self.midi_available: print("MIDI sistemi mevcut değil veya başlatılamadı."); return
        print("\nMIDI Giriş Cihazları:"); found=False
        try:
            for i in range(pygame.midi.get_count()):
                info=pygame.midi.get_device_info(i)
                if info and info[2]==1: print(f"  ID: {i}, Adı: {info[1].decode(errors='ignore')}"); found=True
            if not found: print("  Kullanılabilir MIDI giriş cihazı bulunamadı.")
            default_id=pygame.midi.get_default_input_id()
            if default_id!=-1: print(f"Varsayılan ID: {default_id}")
        except pygame.error as e:
            print(f"MIDI cihaz bilgileri alınırken Pygame hatası: {e}")
        print("-" * 30)

    def open_input_device(self, dev_id=None):
        if not self.midi_available: return False
        if self.input_device: self.close_input_device()
        try:
            actual_id=dev_id if dev_id is not None else pygame.midi.get_default_input_id()
            if actual_id!=-1:
                self.input_device=pygame.midi.Input(actual_id)
                info=pygame.midi.get_device_info(actual_id)
                if info: print(f"MIDI Açıldı: ID {actual_id} - {info[1].decode(errors='ignore')}"); return True
                self.input_device.close(); self.input_device=None; print(f"ID {actual_id} info alınamadı."); return False
            print("Uygun MIDI cihazı yok."); return False
        except pygame.error as e:
            print(f"MIDI cihazı açılırken Pygame hatası (ID: {dev_id}): {e}")
            self.input_device = None; return False
        except Exception as e: 
            print(f"MIDI açma hatası (ID: {dev_id}): {e}"); self.input_device=None; return False

    def poll_events(self):
        if not self.input_device or not self.midi_available: return []
        events=[]
        try:
            if self.input_device.poll():
                for midi_event in self.input_device.read(30):
                    d,t=midi_event; s=d[0]&0xF0; n=d[1]; v=d[2]
                    if s==0x90: events.append({'type':'midi_on' if v>0 else 'midi_off','note':n,'velocity':v,'timestamp':t})
                    elif s==0x80: events.append({'type':'midi_off','note':n,'timestamp':t})
        except pygame.error as e:
            print(f"MIDI olayları okunurken Pygame hatası: {e}")
            self.close_input_device() # Sorunlu cihazı kapat
        return events

    def close_input_device(self):
        if not self.input_device or not self.midi_available: return
        try:
            print("MIDI Kapatılıyor."); self.input_device.close(); self.input_device=None
        except pygame.error as e:
            print(f"MIDI cihazı kapatılırken Pygame hatası: {e}")
            self.input_device = None # Hata durumunda da null yap

    def quit(self):
        if not self.midi_available: return
        self.close_input_device()
        try:
            pygame.midi.quit()
        except pygame.error as e:
            print(f"Pygame MIDI sonlandırılırken hata: {e}")
        except AttributeError:
             pass # Pygame.midi hiç var olmadıysa


class Recorder:
    def __init__(self): self.is_recording=False; self.melody=[]; self.start_record_time_abs=0
    def toggle_recording(self):
        self.is_recording=not self.is_recording
        if self.is_recording: self.melody=[]; self.start_record_time_abs=time.time(); print("Kayıt Başladı.")
        else: print(f"Kayıt Durdu. {len(self.melody)} olay.")
        return self.is_recording
    def record_event(self, midi_note,event_type,velocity=64):
        if self.is_recording: self.melody.append({'time':round(time.time()-self.start_record_time_abs,4),'note':midi_note,'type':event_type,'velocity':velocity})
    def save_melody(self,filename="melody.json"):
        if not self.melody: print("Melodi yok."); return False
        try:
            with open(filename,'w') as f: json.dump(self.melody,f,indent=2)
            print(f"Kaydedildi: {filename}"); return True
        except Exception as e: print(f"Kaydetme hatası: {e}"); return False
    def load_melody(self,filename="melody.json"):
        if not os.path.exists(filename): print(f"Dosya yok: {filename}"); return False
        try:
            with open(filename,'r') as f: self.melody=json.load(f)
            print(f"Yüklendi: {filename}. {len(self.melody)} olay."); return True
        except Exception as e: print(f"Yükleme hatası ({filename}): {e}"); return False

class Piano:
    def __init__(self, x_offset, y_offset, audio_manager, white_key_w, black_key_w, black_key_h):
        self.keys = []; self.x_offset = x_offset; self.y_offset = y_offset
        self.audio_manager = audio_manager
        self.font_for_keys = pygame.font.SysFont("Arial", 12, bold=True)
        self.white_key_width = white_key_w; self.black_key_width = black_key_w
        self.black_key_height = black_key_h
        self._generate_display_keys(DISPLAY_PIANO_START_MIDI, NUM_DISPLAY_KEYS)
        if audio_manager.mixer_ok: 
            self.audio_manager.load_sounds_for_keys(DEFAULT_INSTRUMENT, self.keys)

    def _generate_display_keys(self, start_midi, num_total_keys):
        self.keys = []; current_x_white = self.x_offset; key_assignment_idx = 0 
        note_pattern_is_white = [True, False, True, False, True, True, False, True, False, True, False, True]
        print("\n--- Klavye Eşleşmeleri (Piyano Notası -> Klavye Tuşu) ---")
        temp_keys_for_layout = []
        for i in range(num_total_keys):
            midi_note = start_midi + i
            if midi_note > 127 : break
            is_black = not note_pattern_is_white[midi_note % 12]
            key_char = ORDERED_KEY_ASSIGNMENTS[key_assignment_idx] if key_assignment_idx < len(ORDERED_KEY_ASSIGNMENTS) and key_assignment_idx < num_total_keys else None
            key_obj = PianoKey(midi_note, 0, 0, 0, 0, is_black, key_char)
            temp_keys_for_layout.append(key_obj)
            if key_char:
                char_name = pygame.key.name(key_char).upper()
                if key_char >= pygame.K_0 and key_char <= pygame.K_9: char_name = chr(key_char)
                print(f"  {midi_to_note_name(midi_note)} ({'S' if is_black else 'B'}): {char_name}")
            key_assignment_idx += 1
        white_keys_for_black_placement = []
        for key_obj in temp_keys_for_layout:
            if not key_obj.is_black:
                key_obj.rect = pygame.Rect(current_x_white, self.y_offset, self.white_key_width, WHITE_KEY_HEIGHT)
                white_keys_for_black_placement.append(key_obj); self.keys.append(key_obj)
                current_x_white += self.white_key_width
        for key_obj in temp_keys_for_layout:
            if key_obj.is_black:
                found_prev_white = False
                for wk in white_keys_for_black_placement:
                    if wk.midi_note == key_obj.midi_note -1:
                         key_obj.rect = pygame.Rect(wk.rect.right - (self.black_key_width / 2), 
                                                   self.y_offset, self.black_key_width, self.black_key_height)
                         found_prev_white = True; break
                if found_prev_white: self.keys.append(key_obj)
        self.keys.sort(key=lambda k: k.midi_note)
        print("--- Eşleşmeler Son --- \n")
    def draw(self, surface):
        for key in self.keys:
            if not key.is_black: key.draw(surface, self.font_for_keys)
        for key in self.keys:
            if key.is_black: key.draw(surface, self.font_for_keys)
    def get_key_by_midi_note(self, midi_note):
        for key in self.keys:
            if key.midi_note == midi_note: return key
        return None
    def handle_mouse_press(self, pos, recorder):
        for key_type_pass in [True, False]: 
            for key in self.keys:
                if key.is_black == key_type_pass and key.rect.collidepoint(pos):
                    key.press(self.audio_manager);
                    if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'on')
                    return True
        return False
    def handle_mouse_release(self, recorder):
        for key in self.keys:
            if key.is_pressed:
                key.release();
                if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'off')
    def handle_key_event(self, pygame_key, event_type_str, recorder):
        for key in self.keys:
            if key.key_char == pygame_key:
                if event_type_str == 'on' and not key.is_pressed:
                    key.press(self.audio_manager)
                    if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'on')
                elif event_type_str == 'off' and key.is_pressed:
                    key.release()
                    if recorder and recorder.is_recording: recorder.record_event(key.midi_note, 'off')
                return True
        return False

class PlaybackHandler:
    def __init__(self,piano,audio_manager): self.piano=piano;self.audio_manager=audio_manager;self.melody_to_play=[];self.current_event_index=0;self.playback_time_elapsed=0;self.is_playing=False;self.real_start_time=0
    def start_playback(self,melody):
        if not melody: print("Çalınacak melodi yok.");return
        self.melody_to_play=sorted(melody,key=lambda x:x['time']);self.current_event_index=0;self.playback_time_elapsed=0;self.real_start_time=time.time();self.is_playing=True;print("Çalma başlatıldı.")
        for k in self.piano.keys:
            if k.is_pressed:k.release()
    def stop_playback(self):
        if not self.is_playing: return
        self.is_playing=False
        for k in self.piano.keys:
            if k.is_pressed:k.release()
    def update(self):
        if not self.is_playing or not self.melody_to_play: return
        self.playback_time_elapsed=time.time()-self.real_start_time
        while self.current_event_index<len(self.melody_to_play):
            e=self.melody_to_play[self.current_event_index]
            if self.playback_time_elapsed>=e['time']:
                key_obj=self.piano.get_key_by_midi_note(e['note'])
                if e['type']=='on':self.audio_manager.play_note(e['note']);
                if key_obj:key_obj.current_color=key_obj.pressed_color if e['type']=='on' else key_obj.original_color
                self.current_event_index+=1
            else:break
        if self.current_event_index>=len(self.melody_to_play):
            self.stop_playback()
            print("Melodi bitti.")

class Game:
    def __init__(self):
        pygame.init()
        self.dynamic_white_key_width = (SCREEN_WIDTH - 2 * PIANO_X_OFFSET) / NUM_DISPLAY_WHITE_KEYS
        self.dynamic_black_key_width = self.dynamic_white_key_width * 0.62 
        self.dynamic_black_key_height = WHITE_KEY_HEIGHT * 0.65
        print(f"Beyaz Tuş Genişliği ({NUM_DISPLAY_KEYS}-tuş piyano): {self.dynamic_white_key_width:.2f}px")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Python Piyano - {NUM_DISPLAY_KEYS} Tuş ({midi_to_note_name(DISPLAY_PIANO_START_MIDI)}-{midi_to_note_name(DISPLAY_PIANO_END_MIDI)})")
        self.clock = pygame.time.Clock(); self.ui_font = pygame.font.SysFont("Verdana", 16)
        self.title_font = pygame.font.SysFont("Verdana", 24, bold=True)
        
        self.audio_manager = AudioManager()
        self.piano = Piano(PIANO_X_OFFSET, PIANO_Y_OFFSET, self.audio_manager, 
                           self.dynamic_white_key_width, self.dynamic_black_key_width, self.dynamic_black_key_height)
        self.midi_manager = MIDIManager(); self.recorder = Recorder()
        self.playback_handler = PlaybackHandler(self.piano, self.audio_manager)
        self.running = True; self.active_midi_device_name = "Yok"
        self._setup_ui_elements()
        self.root_tk = None 

    def _setup_ui_elements(self):
        btn_h=35; btn_w=200; p=10; y_start=60
        x_col1=SCREEN_WIDTH-btn_w-p
        self.record_button_rect=pygame.Rect(x_col1,y_start,btn_w,btn_h)
        self.play_button_rect=pygame.Rect(x_col1,y_start+(btn_h+p),btn_w,btn_h)
        self.save_button_rect=pygame.Rect(x_col1,y_start+2*(btn_h+p),btn_w,btn_h)
        self.load_button_rect=pygame.Rect(x_col1,y_start+3*(btn_h+p),btn_w,btn_h)
        self.mozart_button_rect = pygame.Rect(x_col1, y_start + 4*(btn_h + p), btn_w, btn_h)
        # Nikah Masası butonu kaldırıldı, MIDI Yükle onun yerine geldi
        self.load_midi_button_rect = pygame.Rect(x_col1, y_start + 5*(btn_h + p), btn_w, btn_h)


        x_col0=p; btn_w0=220
        self.midi_open_button_rect=pygame.Rect(x_col0,y_start,btn_w0,btn_h)
        vol_btn_w=(btn_w0-p)//2
        self.volume_up_rect=pygame.Rect(x_col0,y_start+(btn_h+p),vol_btn_w,btn_h)
        self.volume_down_rect=pygame.Rect(x_col0+vol_btn_w+p,y_start+(btn_h+p),vol_btn_w,btn_h)
        
    def run(self):
        if self.midi_manager.open_input_device():
            dev_id=pygame.midi.get_default_input_id()
            if dev_id!=-1:
                info=pygame.midi.get_device_info(dev_id)
                if info: self.active_midi_device_name=info[1].decode(errors='ignore').split(" ",1)[0][:15]
        while self.running:
            self.clock.tick(FPS)
            self._handle_events();self._process_midi();self._update_playback();self._render()
        self._cleanup()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: self.running=False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                pos=event.pos
                if self.record_button_rect.collidepoint(pos): self.recorder.toggle_recording();self.playback_handler.stop_playback()
                elif self.play_button_rect.collidepoint(pos) and not self.recorder.is_recording and self.recorder.melody: self.playback_handler.start_playback(self.recorder.melody)
                elif self.mozart_button_rect.collidepoint(pos) and not self.recorder.is_recording:
                    print("Mozart - Rondo Alla Turca çalınıyor...")
                    self.playback_handler.start_playback(MOZART_MELODY_EXAMPLE)
                # Nikah Masası butonu için elif kaldırıldı
                elif self.load_midi_button_rect.collidepoint(pos) and not self.recorder.is_recording:
                    self._load_and_play_midi_file()
                elif self.save_button_rect.collidepoint(pos) and not self.recorder.is_recording: self.recorder.save_melody()
                elif self.load_button_rect.collidepoint(pos) and not self.recorder.is_recording:
                    if self.recorder.load_melody(): self.playback_handler.stop_playback()
                elif self.midi_open_button_rect.collidepoint(pos): self._handle_midi_device_selection()
                elif self.volume_up_rect.collidepoint(pos): self.audio_manager.set_volume(self.audio_manager.volume+0.05)
                elif self.volume_down_rect.collidepoint(pos): self.audio_manager.set_volume(self.audio_manager.volume-0.05)
                else: self.piano.handle_mouse_press(pos,self.recorder)
            
            if event.type==pygame.MOUSEBUTTONUP and event.button==1: self.piano.handle_mouse_release(self.recorder)
            
            if event.type==pygame.KEYDOWN:
                self.piano.handle_key_event(event.key,'on',self.recorder)
                if event.key==pygame.K_SPACE: self.recorder.toggle_recording();self.playback_handler.stop_playback()
                elif event.key==pygame.K_UP: self.audio_manager.set_volume(self.audio_manager.volume+0.05)
                elif event.key==pygame.K_DOWN: self.audio_manager.set_volume(self.audio_manager.volume-0.05)

            if event.type==pygame.KEYUP: 
                self.piano.handle_key_event(event.key,'off',self.recorder)

    def _load_and_play_midi_file(self):
        if not MIDO_AVAILABLE:
            print("MIDI dosyası yüklemek için 'mido' kütüphanesi kurulu olmalı.")
            return
        try:
            if self.root_tk is None: 
                self.root_tk = tk.Tk()
            self.root_tk.withdraw() # Ana Tkinter penceresini gizle
            
            filepath = filedialog.askopenfilename(
                parent=self.root_tk, # Dosya diyalogunun ana penceresi
                title="MIDI Dosyası Seç (.mid)",
                filetypes=(("MIDI dosyaları", "*.mid *.midi"), ("Tüm dosyalar", "*.*"))
            )
            # self.root_tk.deiconify() # İsteğe bağlı: Diyalog sonrası root'u tekrar görünür yap (genelde gerekmez)
        except Exception as e:
            print(f"Dosya seçme penceresi hatası: {e}")
            filepath = None

        if filepath:
            print(f"Seçilen MIDI dosyası: {filepath}")
            # Kullanıcıya MP3 değil, MIDI seçmesi gerektiğini hatırlat (dosya tipi filtresine rağmen)
            if not (filepath.lower().endswith(".mid") or filepath.lower().endswith(".midi")):
                print("Hata: Lütfen geçerli bir MIDI dosyası (.mid veya .midi) seçin.")
                return

            parsed_melody = parse_midi_to_melody(filepath)
            if parsed_melody:
                self.playback_handler.stop_playback()
                self.playback_handler.start_playback(parsed_melody)
            else:
                print("MIDI dosyası ayrıştırılamadı veya boş.")
        else:
            print("MIDI dosyası seçilmedi.")


    def _handle_midi_device_selection(self):
        self.midi_manager.print_device_info()
        try:
            pygame.display.iconify(); dev_id_str=input("MIDI ID: ")
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            if dev_id_str.strip():
                dev_id=int(dev_id_str)
                if self.midi_manager.open_input_device(dev_id):
                    info=pygame.midi.get_device_info(dev_id)
                    if info: self.active_midi_device_name=info[1].decode(errors='ignore').split(" ",1)[0][:15]
                else: self.active_midi_device_name="Yok (Hata)"
            else: self.midi_manager.close_input_device();self.active_midi_device_name="Yok"
        except ValueError: print("Geçersiz ID.")
        except Exception as e: print(f"MIDI seçimi hatası: {e}");self.active_midi_device_name="Yok (Hata)"
    
    def _process_midi(self):
        midi_events=self.midi_manager.poll_events()
        for event in midi_events:
            key_on_screen=self.piano.get_key_by_midi_note(event['note'])
            if event['type']=='midi_on':
                self.audio_manager.play_note(event['note'])
                if key_on_screen: key_on_screen.press(self.audio_manager)
                if self.recorder and self.recorder.is_recording : self.recorder.record_event(event['note'],'on',event['velocity'])
            elif event['type']=='midi_off':
                if key_on_screen: key_on_screen.release()
                if self.recorder and self.recorder.is_recording: self.recorder.record_event(event['note'],'off')
    
    def _update_playback(self):
        if self.playback_handler.is_playing: self.playback_handler.update()
    
    def _draw_button(self, rect, text, base_clr, hi_clr=None, state=False, text_clr=BUTTON_TEXT_COLOR):
        final_clr = hi_clr if state and hi_clr else base_clr
        pygame.draw.rect(self.screen,final_clr,rect,border_radius=6)
        pygame.draw.rect(self.screen,DARK_GRAY,rect,2,border_radius=6)
        txt_s=self.ui_font.render(text,True,text_clr)
        self.screen.blit(txt_s,txt_s.get_rect(center=rect.center))

    def _render(self):
        self.screen.fill(LIGHT_GRAY)
        start_note_name = midi_to_note_name(DISPLAY_PIANO_START_MIDI)
        end_note_name = midi_to_note_name(DISPLAY_PIANO_END_MIDI)
        title_text = f"Python Piyano - {NUM_DISPLAY_KEYS} Tuş ({start_note_name} - {end_note_name})"
        title_s=self.title_font.render(title_text,True,DARK_GRAY)
        self.screen.blit(title_s,(self.screen.get_width()//2-title_s.get_width()//2,15))
        
        self.piano.draw(self.screen)
        self._draw_button(self.record_button_rect,'Kaydediliyor...' if self.recorder.is_recording else 'Kayıt Başlat/Durdur',BLUE,RED,self.recorder.is_recording)
        self._draw_button(self.play_button_rect,'Çalınıyor...' if self.playback_handler.is_playing else 'Melodiyi Çal',GREEN,DARK_GRAY,self.playback_handler.is_playing or not self.recorder.melody)
        self._draw_button(self.mozart_button_rect, "Mozart Çal", ORANGE, DARK_GRAY, self.playback_handler.is_playing and self.playback_handler.melody_to_play == MOZART_MELODY_EXAMPLE)
        # Nikah Masası butonu çizimi kaldırıldı
        self._draw_button(self.load_midi_button_rect, "MIDI Yükle & Çal", PURPLE, DARK_GRAY, self.playback_handler.is_playing and self.playback_handler.melody_to_play not in [MOZART_MELODY_EXAMPLE, self.recorder.melody])
        self._draw_button(self.save_button_rect,"Kaydet (.json)",BLUE)
        self._draw_button(self.load_button_rect,"Yükle (.json)",BLUE)
        self._draw_button(self.midi_open_button_rect,f"MIDI: {self.active_midi_device_name}",DARK_GRAY,text_clr=(WHITE if self.active_midi_device_name!="Yok" else GRAY))
        self._draw_button(self.volume_up_rect,"Ses +",GREEN)
        self._draw_button(self.volume_down_rect,"Ses -",RED)
        status_y=self.screen.get_height()-30
        status_txt1=f"Enstrüman: {self.audio_manager.current_instrument} | Ses: {int(self.audio_manager.volume*100)}%"
        self.screen.blit(self.ui_font.render(status_txt1,True,BLACK),(20,status_y))
        if self.recorder.is_recording:
            rec_dur=time.time()-self.recorder.start_record_time_abs
            self.screen.blit(self.ui_font.render(f"Kayıt: {rec_dur:.1f}s",True,RED),(SCREEN_WIDTH//2-50,status_y))
        pygame.display.flip()
    
    def _cleanup(self):
        print("Uygulama kapatılıyor...");
        if self.root_tk:
            try:
                self.root_tk.quit()
                self.root_tk.destroy()
            except tk.TclError: pass # Pencere zaten yoksa
            except Exception as e: print(f"Tkinter kapatılırken hata: {e}")
        self.midi_manager.quit();pygame.quit()

if __name__ == '__main__':
    if not os.path.exists(SOUND_DIR): os.makedirs(SOUND_DIR); print(f"'{SOUND_DIR}' oluşturuldu.")
    def_instr_dir = os.path.join(SOUND_DIR, DEFAULT_INSTRUMENT)
    if not os.path.exists(def_instr_dir):
        os.makedirs(def_instr_dir); print(f"'{def_instr_dir}' oluşturuldu.")
        print(f"Lütfen .wav piyano ses dosyalarınızı bu klasöre ekleyin.")
        print(f"Bu piyano {midi_to_note_name(DISPLAY_PIANO_START_MIDI)} - {midi_to_note_name(DISPLAY_PIANO_END_MIDI)} aralığını gösterir.")
    game = Game(); game.run()

