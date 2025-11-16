# M4A Audio Converter

A simple Python script to batch convert .m4a audio files to .mp3 or .wav format.

## Features

- Batch convert .m4a files
- Support MP3 and WAV formats
- Adjustable quality levels (high/medium/low)
- Recursive folder search
- Custom output directory
- Progress tracking

## Requirements

- Python 3.6+
- ffmpeg

### Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Basic

```bash
# Convert current directory
python convert_audio.py .

# Convert specific directory
python convert_audio.py ~/Music
```

### Options

```bash
# Convert to WAV
python convert_audio.py ~/Music --format wav

# Specify output directory
python convert_audio.py ~/Music --output ~/Output

# Recursive search
python convert_audio.py ~/Music --recursive

# Set quality (MP3 only)
python convert_audio.py ~/Music --quality high    # 320kbps
python convert_audio.py ~/Music --quality medium  # 192kbps
python convert_audio.py ~/Music --quality low     # 128kbps

# Combined options
python convert_audio.py ~/Music -f mp3 -o ./output -q high -r
```

### Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `input_dir` | - | Input directory (required) | - |
| `--format` | `-f` | Output format (mp3/wav) | mp3 |
| `--output` | `-o` | Output directory | Same as input |
| `--quality` | `-q` | Quality (high/medium/low) | high |
| `--recursive` | `-r` | Search subfolders | False |

### Help

```bash
python convert_audio.py --help
```

## Quality Settings

| Setting | Bitrate | File Size | Use Case |
|---------|---------|-----------|----------|
| high | 320kbps | Large | High-fidelity music |
| medium | 192kbps | Medium | Daily listening |
| low | 128kbps | Small | Save space/Podcasts |

## License

MIT License
