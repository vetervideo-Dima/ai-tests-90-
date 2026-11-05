# The Spaghetti Test: "Maestra Ottavia" Edition

Five text-to-video prompts. Each one is harder than the last and tests the same things the "eating spaghetti" meme tests: hands, fork, noodle physics, chewing, and whether the face stays the same person.

## The character (use this block in every prompt)

> **Ottavia Ferrante**, a 72-year-old retired operatic mezzo-soprano. Silver hair swept up into a loose chignon, a few strands escaping at the temples. Strong Roman nose, deep laugh lines, dark brown eyes, a small mole above the left corner of her lip. Bold crimson lipstick. Wears a plum velvet shawl over a cream silk blouse, a large gold cameo brooch at the throat, and three thin gold rings on her right hand (none on the left). Theatrical, warm, expressive eyebrows.

**Setting (shared):** A tiny trattoria in the Quartieri Spagnoli, Naples. Four tables. Red-and-white checked tablecloth, a straw-wrapped Chianti bottle with a candle stub, a chipped white ceramic plate, a hand-painted Vietri tile wall behind her, a faded poster of a 1970s production of *Carmen* on the wall. Warm afternoon light from a doorway on camera left.

**Dish:** Spaghetti al pomodoro with fresh basil and grated Parmigiano. Real, long strands.

---

## Level 1 — The Still Portrait

**Prompt:**
> Static medium shot, locked-off tripod, eye level, 50mm lens. Ottavia Ferrante [character block] sits at a small table in a tiny Naples trattoria [setting block]. A full plate of spaghetti al pomodoro sits in front of her, untouched. She holds a silver fork loosely in her right hand, resting on the edge of the plate. She looks down at the plate, smiles softly, and takes one slow breath. Steam rises gently from the pasta. No other movement. Warm, soft afternoon light, shallow depth of field, 24fps, photorealistic, 5 seconds.

**What it tests:** Basic identity, hand anatomy at rest, a still object held in a hand, a plausible plate of pasta.

**Failures to watch for:**
- **Hand anatomy:** 4 or 6 fingers; fingers fused to the fork handle; rings appearing on the left hand or vanishing.
- **Fork:** wrong number of tines (2 or 5), fork bends or melts into the plate.
- **Pasta as texture:** spaghetti that looks like a flat painted pattern or a pile of worms, with no separate strands.
- **Face drift:** the mole jumps sides, the lipstick changes colour, the hair turns white-blonde or grows darker during the breath.
- **Steam:** steam that loops like a GIF or comes from the tablecloth instead of the plate.

---

## Level 2 — The First Twirl

**Prompt:**
> Static medium close-up, tripod, slightly above eye level. Ottavia Ferrante [character block] in the Naples trattoria [setting block]. She lowers her fork into the spaghetti, presses the tines against the plate, and slowly twirls three full rotations, gathering a neat nest of noodles around the fork. Loose strands lift from the plate and wrap around the tines; a few strands trail and hang. She lifts the twirled bite a few centimetres and pauses, admiring it. Her left hand rests flat on the tablecloth. Photorealistic, natural motion, 6 seconds.

**What it tests:** Fork rotation, noodles wrapping and following the fork (continuity of strands), the wrist turning.

**Failures to watch for:**
- **Noodles not attached:** the nest forms by itself, or noodles slide through the fork like smoke.
- **Fork spinning wrong:** the fork turns but the hand does not rotate, or the wrist turns 360°.
- **Strand count jumps:** the pile on the plate stays the same size while the nest grows (mass not conserved).
- **Morphing utensil:** the fork turns into a spoon, or a second fork appears.
- **Left hand:** the "resting" hand drifts, crawls, or merges into the tablecloth pattern.

---

## Level 3 — The Bite and the Chew

**Prompt:**
> Medium close-up, slow push-in on a dolly, from chest level to just below her eyes. Ottavia Ferrante [character block] in the Naples trattoria [setting block]. She lifts a twirled bite of spaghetti to her mouth, opens her mouth, and takes the bite. One long strand still hangs from her lips; she slurps it in with a small, theatrical flourish, the strand flicking slightly. She closes her mouth and chews slowly with her lips closed, jaw moving naturally, cheeks shifting, then swallows (throat moves). She dabs the corner of her lips with a white linen napkin held in her left hand. A tiny smudge of tomato sauce remains on her lip and is wiped away. Photorealistic, 8 seconds.

**What it tests:** Food entering the mouth (the classic meme failure), chewing mechanics, slurping physics, sauce on skin, the napkin as a second object.

**Failures to watch for:**
- **Food clipping:** pasta goes *through* the cheek or chin, or disappears before reaching the lips.
- **Fork in the face:** the fork merges with the teeth or the lips.
- **Chewing:** mouth stays open while "chewing"; jaw moves sideways like a cow; chewing continues with nothing in the mouth; teeth multiply.
- **Slurp:** the strand gets longer instead of shorter, or snaps back onto the plate.
- **Sauce:** the smudge appears and disappears randomly, or the napkin wipes and the red stays.
- **Identity under deformation:** when the mouth opens wide, the face becomes a different (younger) woman; the mole vanishes.

---

## Level 4 — Conversation Between Bites

**Prompt:**
> Medium two-shot with a slow lateral dolly from left to right, revealing the waiter. Ottavia Ferrante [character block] in the Naples trattoria [setting block] is mid-meal, half the plate eaten. A waiter enters frame on the right: **Gennaro**, a stocky man in his 40s, black waistcoat, white shirt, rolled sleeves, thick dark moustache, white apron. He pours red wine from the Chianti bottle into her glass. While she twirls spaghetti with her right hand, she turns her head toward him and says something, gesturing with the fork, a strand of spaghetti dangling from it and swinging with the motion. Gennaro laughs. She brings the bite to her mouth and eats it. Photorealistic, 10 seconds.

**What it tests:** Two people, two sets of hands, liquid pour, noodles swinging on a moving fork (pendulum physics), head turn with identity kept.

**Failures to watch for:**
- **Identity swap / blend:** Ottavia picks up Gennaro's moustache or he gets her silver hair; faces merge during the head turn.
- **Hand count:** a third arm appears; the bottle hand belongs to nobody; hands swap owners.
- **Wine:** the pour goes through the glass, the level does not rise, or the wine is a solid red rod.
- **Swinging strand:** the dangling noodle is rigid like wire, or floats against gravity, or stays still while the fork waves.
- **Plate continuity:** the plate refills between shots, or the half-eaten pasta becomes a full plate again.
- **Background:** the *Carmen* poster changes text, the tiles change pattern during the dolly (parallax errors).

---

## Level 5 — The Aria at the Table (Full Chaos)

**Prompt:**
> Handheld camera, documentary style, slight natural shake, moving freely around the table from a three-quarter front angle to a close-up and back. Ottavia Ferrante [character block] in the crowded tiny Naples trattoria [setting block], with Gennaro the waiter [waiter block] standing by the table. She twirls a big forkful of spaghetti vigorously, sauce flicking off the strands and splashing small red dots onto the checked tablecloth and onto her cream blouse. She bursts into a deep, full-bellied laugh, head thrown back, and then talks to Gennaro with clear, lip-synced speech:
>
> **Ottavia (Italian, warm, theatrical):** *"Gennaro! Questo sugo… è meglio della Scala!"*
> **Gennaro (laughing):** *"Signora, lei lo dice ogni settimana!"*
>
> Mid-line she takes the bite, chews with her mouth closed for a beat, then keeps talking after swallowing, gesturing with the fork. A strand slips off and slaps against her chin, leaving sauce; she laughs again and wipes it with her thumb. Background diners turn to look. Ambient sound: clinking plates, a Neapolitan song on a radio. Photorealistic, 15 seconds, 24fps, with synced audio.

**What it tests:** Everything at once: camera motion, fast fork action, sauce particles, a strong facial expression (laughing), real lip-sync in Italian, speaking around food, two characters, crowd background, and identity over 15 seconds.

**Failures to watch for:**
- **Lip-sync:** mouth shapes do not match the Italian words; she "talks" while her mouth is full with no muffling; Gennaro's line comes from Ottavia's mouth.
- **Laugh deformation:** when her head goes back, the jaw unhinges, the teeth become a white bar, or the face turns into a different person when she comes back.
- **Sauce splashes:** droplets fly *upward* or freeze mid-air; stains appear before the splash; stains vanish a second later; the blouse changes colour instead of getting spotted.
- **Chin slap:** the strand passes through the chin; the sauce mark does not stay; the thumb has two nails.
- **Handheld drift:** the camera shake makes the table geometry shift, the plate slides, the Chianti bottle duplicates or the trattoria grows from 4 tables to 20.
- **Identity over time:** by second 12 the chignon has come loose, the rings have moved to the other hand, or she looks 20 years younger.
- **Background diners:** they look at her with melted, mirror-copied faces, or all have the same face.

---

## Quick Scoring Sheet

| Level | Main test | Pass if… |
|---|---|---|
| 1 | Static hand + fork + pasta | 5 fingers, 4 tines, real strands, same face for 5 s |
| 2 | Twirl physics | Noodles follow the fork, plate pile shrinks |
| 3 | Bite + chew | Pasta enters the mouth, closed-mouth chewing, no clipping |
| 4 | Two people + pour + swinging noodle | No identity blend, wine fills, strand swings with gravity |
| 5 | Handheld + laugh + lip-sync + splashes | Words match the mouth, sauce stays, Ottavia is still Ottavia at second 15 |
