import os
import sys
import math
import struct
import wave

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_simple_music():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = os.path.join(base_dir, "music")
    os.makedirs(music_dir, exist_ok=True)
    wav_path = os.path.join(music_dir, "simple_mindset_music.wav")

    print(f"🎵 Synthesizing Simple & Soft Mindset Music...")
    sample_rate = 44100
    duration = 12.0 # 12-second soft reel audio loop
    num_samples = int(sample_rate * duration)

    # Soft, minimal piano-like chord progression (Cmaj7 -> Am7 -> Fmaj7 -> G)
    notes = [
        # Note frequencies in Hz (C4, E4, G4, B4, A3, C4, E4, G4, F3, A3, C4, E4, G3, B3, D4, F4)
        [261.63, 329.63, 392.00, 493.88], # Cmaj7
        [220.00, 261.63, 329.63, 392.00], # Am7
        [174.61, 220.00, 261.63, 329.63], # Fmaj7
        [196.00, 246.94, 293.66, 349.23]  # G7
    ]

    chord_duration = duration / len(notes)

    with wave.open(wav_path, 'w') as wav_file:
        wav_file.setnchannels(2) # Stereo
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate
            chord_idx = int(t / chord_duration) % len(notes)
            current_chord = notes[chord_idx]
            
            # Fade envelope inside chord
            t_in_chord = t % chord_duration
            envelope = math.exp(-1.5 * t_in_chord) * math.sin(math.pi * (t / duration)) ** 2
            
            sample_val = 0
            for note_freq in current_chord:
                # Soft sine harmonics with slight decay for a gentle piano feel
                sample_val += math.sin(2 * math.pi * note_freq * t) * 0.25
                sample_val += math.sin(2 * math.pi * note_freq * 2 * t) * 0.05 # gentle overtone

            # Volume scaling
            sample_val = int(sample_val * envelope * 14000.0)
            sample_val = max(-32768, min(32767, sample_val))

            # Write stereo frames
            data = struct.pack('<hh', sample_val, sample_val)
            wav_file.writeframesraw(data)

    print(f"✅ Simple Mindset Music created successfully at: {wav_path}")
    return wav_path

if __name__ == "__main__":
    generate_simple_music()
