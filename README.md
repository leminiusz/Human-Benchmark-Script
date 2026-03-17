# Human-Benchmark-Script

Automation scripts for selected Human Benchmark tests.

The project uses screen reading (PyAutoGUI/OCR) and browser control (Selenium).

## Requirements

- Python 3.10+
- Windows
- Google Chrome

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python scripts/aim_trainer.py
python scripts/Reaction_time_test.py
python scripts/chimpanzee_test.py
python scripts/number_memory.py
python scripts/sequence_memory.py
python scripts/typing_test.py
python scripts/verbal_memory.py
python scripts/visual_memory.py
```

Press `q` to stop a script. Browser-based scripts close after `q`.

## Configuration

All coordinates, colors, delays, and limits are configured in [scripts/settings.json](scripts/settings.json).

## Script overview

- `aim_trainer.py` - clicks target circles.
- `Reaction_time_test.py` - reacts to color changes.
- `chimpanzee_test.py` - reads numbers with OCR and clicks in order.
- `number_memory.py` - reads number with OCR and types it back.
- `sequence_memory.py` - repeats highlighted sequence.
- `typing_test.py` - copies text from the page.
- `verbal_memory.py` - tracks seen/new words.
- `visual_memory.py` - handles grid pattern rounds.

## Notes

- Coordinates are screen-dependent and may require adjustment.
- OCR-based tests may need tuning in `settings.json` for different displays.
