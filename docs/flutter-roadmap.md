# Reason2Funk Flutter App Roadmap

This document summarizes the project context and planned features for the "Reason2Funk" Flutter application.

## Core App Structure
- Dark theme with orange accent `#C76E19`
- Eight primary tabs including **Studio Tools**
- Images optimized as WebP using Lanczos 2 resampling (quality 80-85%)
- `pubspec.yaml` references assets under `assets/images/Home-Page/`

## Studio Tools (In Development)
Planned subsections:
- OSC Control
- MIDI Mapping
- Visuals
- OBS Macros
- Audio Routing
- Live Stream

### Features in Progress
- Grid-based UI with custom icons
- Placeholder `MethodChannel` code for OSC
- Preset loader/saver for "Jackson's Setup" covering Pioneer DJ gear, Roland synths, and Native Instruments hardware

## Next Steps
1. **OSC Native Integration**
   - Implement Kotlin/Swift bridge code to send and receive OSC messages
   - Expose methods to Flutter via `MethodChannel`
2. **OSC Control UI**
   - Use Flutter widgets (sliders, knobs) bound to OSC emitters/listeners
   - Provide `oscurl` command-line fallback for testing
3. **Preset Manager**
   - Store mapping presets locally (e.g., `SharedPreferences` or SQLite)
   - Support import/export as JSON
4. **Monetization & Marketing**
   - Brand partnership sections (Pioneer DJ, Native Instruments, etc.)
   - Early-access content delivery via the app

*This roadmap reflects discussion from recent chat logs and provides a starting point for further development.*
