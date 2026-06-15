# GIMP Clipping Mask

A Photoshop-style clipping mask plugin for **GIMP 3.x**.

## Usage

1. Have **two layers** — the **top** one will be clipped to the **bottom** one.
2. Select the **top** layer.
3. Go to `Filters → Generic → Clipping Mask` (or `Ctrl+Shift+G`).

The two layers are grouped, and the bottom layer's shape becomes the group mask.

## Installation

### Linux / macOS

1. Copy the plugin folder to GIMP's plug-ins directory:

   ```sh
   cp -r gimp-clipping-mask ~/.config/GIMP/3.2/plug-ins/
   ```

   > The exact version number (`3.2`) may vary. Check which directory exists in `~/.config/GIMP/`.

2. (Optional) Bind a keyboard shortcut via `Edit → Keyboard Shortcuts`, search for `Clipping Mask`, and assign e.g. `Ctrl+Shift+G`.

3. Restart GIMP. The plugin appears under `Filters → Generic → Clipping Mask`.

### Windows

Copy the `gimp-clipping-mask` folder to:

```
%APPDATA%\GIMP\3.2\plug-ins\
```

---

**Note:** GIMP 3 requires plugins to be inside a **directory** — loose `.py` files are not loaded.
