import os
import sys
import math
import struct
import wave

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def generate_ambient_track():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = os.path.join(base_dir, "music")
    os.makedirs(music_dir, exist_ok=True)
    wav_path = os.path.join(music_dir, "ambient_focus.wav")

    print(f"🎵 Synthesizing 432Hz Deep Focus Ambient Soundtrack...")
    sample_rate = 44100
    duration = 10.0 # 10 seconds reel audio loop
    num_samples = int(sample_rate * duration)

    # Frequencies for a relaxing 432Hz A-minor / Solfeggio harmony (432Hz, 216Hz, 108Hz, 528Hz)
    freqs = [108.0, 216.0, 432.0, 528.0]
    
    with wave.open(wav_path, 'w') as wav_file:
        wav_file.setnchannels(2) # Stereo
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            t = i / sample_rate
            # Fade in and fade out envelope
            envelope = math.sin(math.pi * (t / duration)) ** 2
            
            # Combine sine waves with gentle low-frequency modulation (LFO)
            lfo = 1.0 + 0.15 * math.sin(2 * math.pi * 0.2 * t)
            
            sample_val = 0
            for f in freqs:
                sample_val += math.sin(2 * math.pi * f * t) * 0.25

            # Apply envelope and volume scale
            sample_val = int(sample_val * envelope * lfo * 16384.0)
            sample_val = max(-32768, min(32767, sample_val))

            # Stereo audio data
            data = struct.pack('<hh', sample_val, sample_val)
            wav_file.writeframesraw(data)

    print(f"✅ Ambient Soundtrack created successfully at: {wav_path}")
    return wav_path

if __name__ == "__main__":
    generate_ambient_track()
