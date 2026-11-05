# Tokyo Street: the Sora prompt rewritten for Veo, Kling, Seedance and Runway

**Original (Sora launch prompt):** *A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, a long red dress, and black boots, and carries a black purse. She wears sunglasses and red lipstick. She walks confidently and casually. The street is damp and reflective, creating a mirror effect of the colorful lights. Many pedestrians walk about.*

All four versions describe the **same shot**, so you can compare models directly: a backward tracking shot as she walks toward the camera, then a drop to the reflections. What changes is the *dialect* each model reads best and *where* each instruction goes (prompt text vs. settings vs. negative field).

### Quick reference: where each instruction goes

| | Veo 3 / 3.1 | Kling 2.x | Seedance | Runway Gen-4 / 4.5 |
|---|---|---|---|---|
| Clip length | 8 s | 5 or 10 s | 5 or 10 s | 5 or 10 s |
| Prompt style | Cinematic prose, paragraphs | Compact: subject → action → scene → camera → light | Short literal sentences, one action per sentence, timed | Short, direct; describe motion, not appearance, when an image is attached |
| Native audio | Yes (dialogue, SFX, ambience) | Only 2.6+ with the audio toggle on | 1.5 Pro / 2.0: yes; 1.0: no | No (do sound in post) |
| Negative cues | `negativePrompt` parameter (API / Vertex) | Dedicated negative-prompt field | No field: phrase them as positives | Not supported: phrase as positives, never "no X" |
| Character lock | Reference images ("ingredients", 3.1) or first frame | Elements / image-to-video | Reference image (2.0: @image refs) | Image-to-video or References |

*Version details change quickly. Check the current model page before a paid run.*

### Shared character sheet (paste it word for word into every prompt)

> a woman in her late twenties with a sleek black bob, dark oval sunglasses, red lipstick, a cropped black leather biker jacket, a long flowing red silk slip dress, black knee-high leather boots, a small black shoulder purse

Using exactly the same wording each time is the cheapest way to keep the character consistent between models and between shots. A hairstyle is added because the original leaves it open, and models then pick a new one in every take.

---

## 1. Google Veo (Veo 3 / 3.1)

**Settings:** 16:9 · 8 s · 1080p · audio on. Text-to-video, or image-to-video from a generated hero frame.

**Prompt:**

> A cinematic medium-wide tracking shot on a 35mm lens with shallow depth of field, at night in a narrow Tokyo shopping street. A woman in her late twenties with a sleek black bob, dark oval sunglasses, red lipstick, a cropped black leather biker jacket, a long flowing red silk slip dress, black knee-high leather boots and a small black shoulder purse walks toward the camera, confident and unhurried, the hem of her dress swaying with each step.
>
> The camera dollies backward at her walking pace, keeping her centered. In the final seconds it sinks smoothly to knee height, so the wet asphalt fills the lower frame. The street is damp after rain and mirror-like: puddles reflect magenta, cyan and amber neon, plus animated billboards that loop simple glowing shapes. Dozens of pedestrians with clear umbrellas pass in both directions, soft and out of focus.
>
> Lighting: warm magenta-and-amber neon key from signs on frame left, cool cyan fill from shop windows on the right, light haze catching the glow, deep blacks, rich saturated color, subtle 35mm film grain.
>
> Timing: 0–3 s she walks through the crowd toward camera. 3–6 s she glances right at a flickering sign and a streak of neon slides across her sunglasses. 6–8 s she looks ahead with a faint half-smile as the camera lowers toward her boots splashing through a reflective puddle.
>
> Audio: dense Tokyo night ambience, the steady click of her boot heels on wet pavement, soft splashes, the electric hum and buzz of neon, overlapping pedestrian chatter, a distant train-crossing bell, faint muffled pop music from a shop doorway. No dialogue, no music score.

**Negative prompt** (the `negativePrompt` field, plain nouns without "no"):
`cartoon, anime, CGI look, daylight, dry pavement, legible text, garbled signage, warped hands, extra limbs, face morphing, flicker, subtitles, watermark`

*Why this shape:* Veo follows long, film-language prose well. It obeys timestamped beats inside its 8-second window and makes matching sound effects from the audio paragraph. Ending with "No dialogue" stops it from inventing speech.

---

## 2. Kling (2.1 / 2.5 Turbo / 2.6)

**Settings:** 16:9 · 10 s · Professional/High-quality mode · creativity ↔ relevance ≈ 0.5 · Native Audio on only if you're on 2.6+. For a stable face, run image-to-video from the hero frame.

**Prompt:**

> A woman in her late twenties with a sleek black bob, dark oval sunglasses, red lipstick, a cropped black leather biker jacket, a long flowing red silk slip dress, black knee-high leather boots and a small black shoulder purse walks confidently toward the camera down a rain-wet Tokyo street at night. Warm neon signs and animated billboards line both sides; the wet asphalt mirrors the colorful lights. Many pedestrians with umbrellas walk past her.
> Medium-wide full-body shot, 50mm lens look, shallow depth of field with round bokeh.
> The camera smoothly tracks backward in front of her at walking speed, steady, no shake.
> Neon practical lighting: magenta and orange glow on her face, cool blue shadows, light mist, glossy reflections on the ground.
> First she walks with a natural heel-to-toe stride and her dress sways; then she lifts a hand to adjust the purse strap on her shoulder; finally she turns her head slightly toward a bright sign and keeps walking.
> Sound: rain dripping from awnings, boot heels on wet pavement, distant traffic, crowd murmur.
> Photorealistic cinematic look, film grain.

**Negative prompt** (dedicated field):
`blurry face, deformed face, distorted body, extra fingers, foot sliding, moonwalking, clothing morphing, changing outfit, text, watermark, cartoon, low quality, overexposed`

*Why this shape:* Kling rewards a compact, ordered prompt and one clear camera move. More than one move per clip is often half-ignored. It has a real negative field, and "foot sliding" / "clothing morphing" target its usual walk-cycle artifacts. Drop the "Sound:" sentence on versions without native audio.

---

## 3. Seedance (1.0 Pro / 1.5 Pro / 2.0)

**Settings:** 16:9 · 10 s · 1080p (set resolution in the UI, not in the prompt). With 2.0, attach the hero frame as `@image1` and write "the woman from @image1".

**Prompt:**

> Night, a narrow Tokyo street after rain, full of warm neon signs and animated billboards. A woman in her late twenties with a sleek black bob, dark oval sunglasses, red lipstick, a cropped black leather biker jacket, a long flowing red silk slip dress, black knee-high leather boots and a small black shoulder purse walks toward the camera, confident and relaxed.
> Medium shot, eye level, 35mm lens, shallow depth of field.
> 0–4 s: the camera tracks backward in front of her at the same speed; pedestrians with umbrellas pass on both sides.
> 4–7 s: she turns her head to look at a glowing pink sign; its light sweeps across her sunglasses.
> 7–10 s: the camera slowly arcs to her left side as she walks past, revealing the mirror-like wet street behind her full of colorful reflections.
> Lighting: warm neon glow, cyan shop-window fill, soft haze, high contrast, realistic skin texture.
> Sound: footsteps on wet pavement, neon hum, crowd chatter, distant train.
> Sharp, stable face and hands; consistent outfit throughout; smooth natural walking; photorealistic cinematic style.

*Negative cues are written as positives (last line).* Seedance has no negative field and reads "avoid X" unreliably. Delete the "Sound:" line on 1.0, which makes video only.

*Why this shape:* Seedance follows short, literal sentences and timecoded camera instructions closely, and it handles a move that changes mid-clip (track, then arc) better than most. For a multi-shot version in one generation, add "Cut to: …" lines, a feature it supports natively.

---

## 4. Runway (Gen-4 / Gen-4 Turbo image-to-video; Gen-4.5 text-to-video)

**Settings:** 16:9 (1280×720) · 10 s. **Gen-4:** first make the hero frame (Runway Frames / References, or any image model) using the character sheet, then animate it. **Gen-4.5:** you can run the full text below as text-to-video.

**Prompt (image-to-video, describe motion, not looks):**

> The camera tracks backward smoothly at walking pace as the woman walks confidently toward it down the wet neon street. Her red dress sways with each step and her boots splash lightly through shallow puddles, sending ripples through the reflected neon. Pedestrians with umbrellas drift past in soft focus. She turns her head slightly toward a glowing sign, then faces forward again. In the last moments the camera slowly pushes in toward her face. Warm magenta and amber neon, cyan fill, light haze, anamorphic lens flares, cinematic night grade.

**Prompt (Gen-4.5 text-to-video, full description):**

> Cinematic medium-wide tracking shot, 40mm anamorphic look with oval bokeh, at night on a rain-soaked Tokyo street lined with warm neon and animated signage. A woman in her late twenties with a sleek black bob, dark oval sunglasses, red lipstick, a cropped black leather biker jacket, a long flowing red silk slip dress, black knee-high leather boots and a small black shoulder purse walks confidently toward the camera as it tracks backward. The wet street mirrors the lights; pedestrians with umbrellas pass in soft focus. She glances at a glowing sign, then looks ahead; the camera slowly pushes in toward her face. Moody high-contrast neon lighting, cinematic color grade.

**Negative cues, Runway-style:** none in the prompt. Runway's guidance says negative phrasing isn't supported and can *add* the unwanted element. Keep quality in the positive wording ("smoothly", "soft focus", "steady"), and re-roll or lower motion intensity if limbs warp.

**Ambience/audio (do it in post, not in the prompt):** layered rain-city bed, close heel clicks timed to her steps, neon buzz, crowd walla, a distant train bell. Runway's own audio tools or any DAW will work.

*Why this shape:* Gen-4 takes appearance from the input image and the prompt only directs motion. Repeating the outfit in the text adds nothing and can cause drift. Short subject-plus-motion sentences beat long lists of keywords.

---

## Sequel: 6-shot storyboard, "After Midnight"

**Story:** Later that night she leaves the neon avenue, steps into a lantern alley, and finds the city answering her in red.
**Continuity rules:** same character sheet in every shot. Whenever she crosses the frame sideways, she moves **left → right** (screen direction). Shot 2 (seen from behind) and shot 6 (straight at the camera) move along the lens axis instead. Rain gets steadier with each shot. Palette: magenta/cyan neon, then warm lantern amber, then all red. Total running time is about 44 s, made from 8–10 s generations trimmed in the edit.
**Workflow:** generate one hero still, use it as the reference/first frame for every shot, and end each clip on a frame that can start the next one.

1. **Shot 1, "Scramble" (6 s, Kling or Veo).** Extreme wide, high angle from a second-floor window, 24mm, static, locked-off. The walk signal chimes and a flood of umbrellas pours across a giant scramble crossing. Her red dress is the only warm spot in the crowd as she cuts diagonally left → right. Rain thickens and the billboards loop glowing abstract shapes. *Audio: crossing chime melody, rain on hundreds of umbrellas, crowd footsteps.* **Cut on her exiting frame right.**

2. **Shot 2, "Turn-off" (7 s, Seedance).** Medium shot from behind, 35mm, the camera follows at shoulder height. She leaves the avenue and ducks under a low awning into a narrow alley of tiny bars with red paper lanterns. Smoke from a yakitori grill drifts through the lantern light, and the neon fades behind her. *Audio: the avenue noise muffles, grill sizzle, muffled laughter, rain drumming on tin awnings.* **Match cut: a lantern's red glow → a red reflection in a puddle.**

3. **Shot 3, "Reflection" (7 s, Veo).** Low-angle close-up on a puddle, 85mm, static, focus on the water. Her boot steps in from frame left; ripples spread through the reflection of lanterns and her face in sunglasses. As the water settles, the reflection shows the same alley **empty, with every lantern lit red**, while the real alley above still has people in it. *Audio: one drip, then the world's sound drops to a low hum.* **Hard cut, sound returns.**

4. **Shot 4, "The Counter" (8 s, Kling image-to-video).** Medium close-up, 50mm, slow push-in. She slides open a wooden door, sits at a six-seat counter, and for the first time takes off her sunglasses: calm dark eyes. The bartender's hands set down a highball glass, and neon through the rain-streaked window paints her face pink and blue. *Audio: jazz vinyl crackle, ice settling, rain on glass.* *(Keep the sunglasses in her hand or on the counter so the prop stays continuous.)*

5. **Shot 5, "The Signal" (6 s, Veo).** Extreme close-up, 100mm macro, static. Condensation runs down the glass, and in its curved reflection the street signs outside **pulse in sync, one by one turning red**. Rack focus from the glass to her eyes as she looks up toward the window. *Audio: neon buzz rising in pitch, a low bass note entering.* *(This replaces a phone screen. Readable UI text is still where every model fails most often.)*

6. **Shot 6, "Into the Red" (10 s, Runway Gen-4.5 or Veo).** Wide, 24mm, crane up. She steps out of the alley back onto the main avenue and puts her sunglasses back on. Every neon sign and billboard switches in a wave to the same deep red as her dress, and the wet street becomes a red mirror. She walks straight toward the camera as it rises over the umbrellas and above the rooftops, revealing a whole district glowing red under the rain. *Audio: bass swell, rain, the hum of the city returning, cut to silence on black.* **End card.**
