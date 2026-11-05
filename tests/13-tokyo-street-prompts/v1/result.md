# Tokyo Street: the Sora prompt rewritten for four video models

**Original (Sora):** *A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, a long red dress, and black boots, and carries a black purse. She wears sunglasses and red lipstick. She walks confidently and casually. The street is damp and reflective, creating a mirror effect of the colorful lights. Many pedestrians walk about.*

The four versions below keep the same scene but are written the way each model reads prompts best.

---

## 1. Google Veo (Veo 3 / 3.1)

Veo responds well to cinematic prose with clear camera language, and it generates audio natively, so the soundscape is part of the prompt.

**Prompt:**

> Medium-wide tracking shot, 35mm lens, shallow depth of field. A stylish woman in her late twenties walks toward the camera down a narrow Tokyo street at night, filled with warm glowing neon and animated city signage in Japanese. She wears a black leather jacket, a long flowing red dress, black knee-high boots, and carries a small black purse on her shoulder. She wears dark sunglasses and red lipstick. She walks confidently and casually, with a relaxed stride, the hem of her dress swaying with each step.
>
> The camera dollies backward slowly at her walking pace, keeping her centered, then gently drifts down to knee height to reveal the wet asphalt. The street is damp after rain and mirror-like, reflecting pink, cyan and amber neon in rippling puddles. Many pedestrians with umbrellas walk past in both directions, slightly out of focus.
>
> Lighting: warm neon key light from signs on camera left, cool blue fill from shop windows, soft haze in the air catching the light, high contrast, rich saturated colors, filmic grain.
>
> Motion beats: (0–3s) she walks toward camera through the crowd; (3–6s) she glances at an animated sign to her right, a neon reflection slides across her sunglasses; (6–8s) she looks back ahead with a faint smile, camera lowers toward the reflective street.
>
> Audio: city ambience of a busy Tokyo night, distant train announcement, light chatter of pedestrians, footsteps on wet pavement, the hum and buzz of neon signs, faint J-pop from a shop doorway. No dialogue.
>
> Negative prompt: cartoon, anime style, distorted face, extra limbs, warped hands, text artifacts, flickering, low resolution, daylight, dry street.

---

## 2. Kling (Kling 2.x)

Kling works best with a compact, structured prompt — subject, action, scene, camera, lighting — plus a separate negative prompt field. Camera movement is best kept to a single clear move.

**Prompt:**

> A stylish woman walks confidently down a Tokyo street at night. She wears a black leather jacket, long red dress, black boots, sunglasses and red lipstick, carrying a black purse. Warm glowing neon signs and animated billboards line the street. The wet asphalt reflects colorful lights like a mirror. Many pedestrians walk around her.
>
> Shot type: full body, medium-wide shot.
> Lens: 50mm, f/1.8, cinematic bokeh.
> Camera move: smooth tracking shot moving backward in front of her (dolly out), steady.
> Lighting: neon practicals, warm magenta and orange glow, cool blue shadows, reflections on the wet ground, light mist.
> Motion beats: natural walking cycle with confident hip sway; her hair moves slightly; she adjusts her purse strap; pedestrians cross behind her.
> Ambience/audio: busy night street, rain drips, footsteps, distant traffic and city chatter.
> Style: photorealistic, cinematic, 4K, film look.
>
> **Negative prompt:** blurry, deformed face, distorted body, extra fingers, unnatural walking, sliding feet, morphing clothes, text, watermark, low quality, cartoon.

Settings tip: Professional mode, 10 seconds, 16:9, relevance (CFG) around 0.5.

---

## 3. Seedance (ByteDance Seedance 1.0)

Seedance follows precise action and camera instructions very literally and supports multiple shots in one prompt. Keep sentences simple and put camera instructions in clear terms.

**Prompt:**

> A stylish woman in a black leather jacket, long red dress, black boots, sunglasses and red lipstick, carrying a black purse, walks confidently and casually down a Tokyo street at night. The street is full of warm neon lights and animated signs. The ground is wet and reflects the colorful lights like a mirror. Many pedestrians walk around.
>
> Shot type: medium shot, eye level.
> Lens: 35mm, cinematic depth of field.
> Camera move: the camera tracks backward in front of her, then slowly orbits to her side as she passes a bright sign.
> Lighting: warm neon glow, colorful reflections, soft haze, night atmosphere, high contrast.
> Motion beats: she walks forward steadily; she turns her head slightly to look at a sign; she continues walking past the camera.
> Ambience/audio: Tokyo street noise, footsteps on wet pavement, distant music.
> Style: realistic, cinematic, 1080p.
>
> Avoid: blurry faces, distorted hands, extra people merging, flickering lights, cartoonish look.

---

## 4. Runway (Gen-4 / Gen-4 Turbo)

Runway prefers clear, direct descriptions of what happens in the shot. It reacts well to camera terminology and to a short sequence of actions. Gen-4 is strongest in image-to-video, so generate a reference frame first if possible.

**Prompt:**

> Cinematic tracking shot. A stylish woman walks down a rain-soaked Tokyo street at night. Black leather jacket, long red dress, black boots, black purse, sunglasses, red lipstick. She walks confidently and casually toward the camera.
>
> Shot type: medium-wide, eye level.
> Lens: 40mm anamorphic, oval bokeh, subtle lens flares from neon.
> Camera move: handheld-steady backward tracking, slow push-in at the end on her face.
> Lighting: warm glowing neon and animated signage, mirror reflections in the wet street, moody contrast, cinematic color grade.
> Motion beats: she walks through the crowd; neon reflections ripple in a puddle as she steps through it; she tilts her head slightly and keeps walking.
> Ambience/audio: (for sound design in post) rain-soaked city hum, footsteps, distant traffic, crowd chatter.
> Pedestrians walk about in the background.
>
> Negative cues: no distortion, no extra limbs, no blurry face, no cartoon style, no text.

---

## Sequel: 6-shot storyboard — "After Midnight"

The same woman continues her night. Same wardrobe (black leather jacket, long red dress, black boots, black purse, sunglasses, red lipstick), same rainy neon Tokyo.

1. **Shot 1 — Crossing.** Wide high-angle shot, 24mm, static camera from above a scramble crosswalk. The light turns green and hundreds of pedestrians flood the crossing; the woman's red dress stands out in the crowd as she crosses diagonally. Rain begins to fall again. *Audio: crossing signal chime, rain, crowd footsteps.*

2. **Shot 2 — The Alley.** Medium shot, 35mm, slow tracking from behind as she turns off the main street into a narrow alley of tiny bars with paper lanterns (Omoide Yokocho style). Steam rises from a yakitori grill; red lanterns glow. *Audio: sizzling grill, muffled laughter, rain on awnings.*

3. **Shot 3 — The Reflection.** Close-up, 85mm, low angle on a puddle. Her boots step into frame; the puddle reflects her face and the lanterns above. As the ripples settle, the reflection shows something else: the same street, but empty. *Audio: single water drip, the city sound drops away.*

4. **Shot 4 — The Bar.** Medium close-up, 50mm, slow push-in. She slides open a wooden door and sits at a small counter. She takes off her sunglasses for the first time, revealing her eyes. The bartender places a glass in front of her; neon from outside paints her face pink and blue. *Audio: jazz record crackle, ice clinking.*

5. **Shot 5 — The Signal.** Extreme close-up, 100mm macro, static. Her phone on the counter lights up with a message; reflected in the glass, the animated signs outside begin to flicker in sync. She looks up toward the window. *Audio: phone vibration, neon buzz rising.*

6. **Shot 6 — Into the Light.** Wide shot, 24mm, crane up. She steps out of the alley back onto the main street. All the neon signs glitch and switch to the same color — deep red — matching her dress. She puts her sunglasses back on and walks into the glow as the camera rises above the rooftops of the city. *Audio: bass swell, rain, fade to city hum.*
