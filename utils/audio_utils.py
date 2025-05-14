import os
from pydub import AudioSegment


def split_audio(file_path, temp_audio_chunks_dir, max_size_mb=24):
    os.makedirs(temp_audio_chunks_dir, exist_ok=True)

    audio = AudioSegment.from_file(file_path)
    file_extension = os.path.splitext(file_path)[-1][1:]

    file_size = os.path.getsize(file_path)

    if file_size < max_size_mb * 1024 * 1024:
        print(f"Input audio-file {file_path} is smaller than {max_size_mb}MB, no need to split.")
        return [file_path]

    audio_duration_ms = len(audio)
    max_chunk_length_ms = int((max_size_mb * 1024 * 1024 / file_size) * audio_duration_ms)

    max_chunk_length_ms = int(max_chunk_length_ms * 0.9)

    chunks = []
    for i in range(0, len(audio), max_chunk_length_ms):
        chunk_path = os.path.join(temp_audio_chunks_dir, f"chunk_{i // max_chunk_length_ms}.{file_extension}")
        chunk = audio[i:i + max_chunk_length_ms]
        chunk.export(chunk_path, format=file_extension)

        chunk_size_mb = os.path.getsize(chunk_path) / (1024 * 1024)
        print(f"Created chunk {len(chunks) + 1} with size: {chunk_size_mb:.2f}MB")

        chunks.append(chunk_path)

    print(f"Split input audio-file {file_path} into {len(chunks)} chunks of max {max_size_mb}MB each")
    return chunks


def get_max_chunk_length(audio, max_size_mb=24):
    channels = audio.channels
    sample_rate = audio.frame_rate
    sample_width = audio.sample_width

    bitrate_kbps = (sample_rate * sample_width * 8 * channels) / 1000

    max_size_kb = max_size_mb * 1024
    max_length_ms = (max_size_kb * 8) / bitrate_kbps * 1000
    return int(max_length_ms)
