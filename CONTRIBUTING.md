# Contributing to Willow Icons

## License

By submitting a pull request, you agree that your contribution will be licensed under the MIT License and included in this project under the same terms.

All contributors retain authorship of their work.

---

# Icon Design Rules

## 1. Base Shape System

![Base shape system](preview/base_shape_system.png)

All icons in Willow Icons use the same base shape system.

### Required parameters:
- Icon size: **168×168 px**
- Corner radius: **42 px**
- Canvas size: **192×192 px**
- Padding: **12 px** on each side
- Icons must be centered on the canvas

The outer silhouette must remain visually consistent across the entire icon pack.

---

## 2. Color Palette

All icons must use the official Willow color palette.

### Rules:
- Use only colors from the palette below
- Gradients are strictly prohibited
- Avoid overly saturated or neon colors
- Keep the visual style soft and balanced

| Name | Hex |
|------|------|
| Blue | `#5F97C9` |
| Dark Blue | `#3F79AD` |
| Indigo | `#6F7FC0` |
| Dark Indigo | `#4F5F9F` |
| Purple | `#8A78C8` |
| Dark Purple | `#6B58A7` |
| Red | `#D06F78` |
| Dark Red | `#B04F58` |
| Orange | `#D2945A` |
| Dark Orange | `#B0733F` |
| Yellow | `#D1C06A` |
| Dark Yellow | `#B8A64F` |
| Green | `#6FBF9A` |
| Dark Green | `#4F9B7A` |
| Teal | `#63B2A8` |
| Dark Teal | `#438F86` |
| Cyan | `#63A8C2` |
| Dark Cyan | `#428AA3` |
| Pink | `#C07FA0` |
| Dark Pink | `#9F5F7F` |
| Brown | `#9F897A` |
| Dark Brown | `#7F6B5D` |
| Gray | `#8A8F98` |
| Dark Gray | `#6B7078` |
| Black | `#32363B` |
| White | `#F4F5F7` |

---

## 3. File Formats

Only the following formats are allowed.

### Source icons
- `.svg`

Location:
```text
/icons
````

### Launcher-ready icons

* `.png`
* Resolution: `192×192 px`

Location:

```text
/app/src/main/res/drawable-nodpi
```

---

## 4. Naming Rules

All icons must follow the naming system used by the project.

### Prefixes

* `app_` — applications
* `sys_` — system icons

### Rules

* lowercase letters only
* underscores allowed
* no spaces
* no camelCase

### Examples

```text
app_telegram.svg
app_spotify.svg
sys_camera.svg
sys_settings.svg
```

---

# Launcher Support

Every newly added icon must also include launcher support entries.

---

## 1. Add PNG Export

Export the icon as:

* `192×192 px`
* PNG format

Place it in:

```text
/app/src/main/res/drawable-nodpi
```

Example:

```text
app_telegram.png
```

---

## 2. Add drawable.xml Entry

File:

```text
/app/src/main/res/xml/drawable.xml
```

Add:

```xml
<item drawable="app_youricon" />
```

---

## 3. Add appfilter.xml Entry

File:

```text
/app/src/main/res/xml/appfilter.xml
```

Add:

```xml
<item component="ComponentInfo{com.package.name/com.package.name.MainActivity}" drawable="app_youricon" />
```

---

## 4. Finding Package Names

You can obtain correct app component information directly inside Willow Icons using the built-in icon request feature.


Use that information when creating `appfilter.xml` entries.

---

# Exceptions

If your contribution does not follow one or more rules above, you must explain why.

Include:

* what rule was broken
* why it was necessary
* possible improvements or alternatives

Pull requests without explanation may be rejected.

---

# Improving the System

The Willow design system may evolve over time.

If you think a rule should be changed:

* open an issue
* explain the problem
* provide examples or suggestions

Well-reasoned improvements are welcome.
