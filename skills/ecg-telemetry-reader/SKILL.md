---
name: ecg-telemetry-reader
description: Helps read and interpret photos of ECG/EKG tracings (rhythm strips, 12-lead printouts) and bedside patient monitor or telemetry screens. Extracts vital signs, calibration, rhythm and waveform findings into a structured summary, and flags potentially critical findings for urgent escalation. Use when the user shares or describes a photo of an ECG, rhythm strip, 12-lead printout, monitor, or telemetry display and asks to read, transcribe, interpret, or check it.
---

# ECG & Telemetry Photo Reader

This skill helps you read a photo of an ECG/EKG tracing or a bedside monitor /
telemetry screen and turn it into a clear, structured summary: vital signs,
rhythm characteristics, and notable waveform findings.

## ⚠️ Safety notice (always follow)

- This is a **reading/transcription and educational aid**, not a diagnostic
  tool. It does **not** replace interpretation by a qualified clinician
  (physician, cardiologist, nurse) who has the full clinical picture.
- **Always end your response with a disclaimer** stating that the analysis is
  informational, may contain errors due to image quality, and must be
  confirmed by a qualified healthcare professional with access to the patient
  and their history.
- If the tracing or vitals show signs that could indicate a
  life-threatening situation (see "Red flags" below), **say so clearly and
  first**, and recommend immediate evaluation by clinical staff or emergency
  services (e.g., 911 / 112) — do not bury this at the end of a long report.
- Be mindful of patient privacy: if the photo shows a name, MRN, date of
  birth, or other identifying information, do not repeat or highlight it
  unless the user specifically asks you to transcribe it, and avoid storing
  or echoing it unnecessarily.
- Respond in the same language the user used (e.g., Spanish if they wrote in
  Spanish).

## When to use this skill

Use this skill when the user shares a photo (or describes one in detail) of:

- An ECG/EKG rhythm strip or 12-lead printout
- A bedside patient monitor showing waveforms and vitals
- A central station / telemetry display
- A wearable or portable ECG device readout

and asks things like "what does this ECG show?", "can you read these vitals?",
"is this rhythm normal?", "transcribe this monitor", or "does this look
concerning?".

## Step 1 — Assess image quality and classify the image

Before analyzing, check:

- Is the image sharp enough to read numbers and waveform shapes? Watch for
  glare, blur, cropping, or low resolution.
- If it's unreadable, say what's unclear and ask for a retake: closer, better
  lit, no glare, with the full strip/screen and any calibration marks or lead
  labels visible.

Classify what you're looking at:

1. **Single-lead rhythm strip** — one continuous waveform, often with a
   calibration pulse.
2. **12-lead ECG printout** — a grid of leads labeled I, II, III, aVR, aVL,
   aVF, V1–V6, usually with a rhythm strip along the bottom.
3. **Bedside monitor / telemetry screen** — numeric vitals (HR, BP, SpO2, RR,
   temp, etc.) plus one or more live waveforms.
4. **Trend / central station view** — graphs of vitals over time, possibly
   multiple patients.

## Step 2 — Read calibration and scale (ECG tracings)

If visible, note:

- **Paper/sweep speed** — typically 25 mm/s (each small box = 0.04 s, each
  large box = 0.2 s). Some strips use 50 mm/s — check for a printed value.
- **Gain/calibration pulse** — typically 10 mm/mV (a small rectangular pulse
  at the start of the tracing). Note if it looks like 5 mm/mV (half-standard)
  or 20 mm/mV (double-standard), as this changes amplitude interpretation.
- If no calibration marks are visible, state that intervals/amplitudes are
  estimates based on assumed standard settings (25 mm/s, 10 mm/mV).

## Step 3 — Analyze the ECG waveform

For a rhythm strip or 12-lead, work through:

- **Rate**: Read a printed HR if shown. Otherwise estimate from the strip —
  e.g., 300 / (number of large boxes between R waves), or count QRS
  complexes in a 6-second strip and multiply by 10.
- **Rhythm regularity**: Regular, regularly irregular, or irregularly
  irregular (R-R intervals).
- **P waves**: Present/absent, one P per QRS, morphology (upright in II,
  inverted, sawtooth, fibrillatory).
- **PR interval**: Normal (~0.12–0.20 s), prolonged, variable, or absent
  relationship between P and QRS.
- **QRS complex**: Width (narrow <0.12 s vs wide ≥0.12 s) and morphology
  (e.g., RSR' pattern, delta wave).
- **ST segment**: Elevation, depression, or isoelectric — and in which
  lead(s)/territory if a 12-lead is available.
- **T waves**: Normal, flattened, inverted, or peaked.
- **QT/QTc interval**: Note if it appears prolonged or shortened relative to
  the rate.

For a **12-lead ECG**, go lead by lead and group findings by territory:

- Inferior: II, III, aVF
- Lateral: I, aVL, V5, V6
- Anterior/septal: V1–V4
- Right-sided/posterior changes if mentioned

Mention an estimated electrical axis (normal, left, right, or
indeterminate) if it can reasonably be assessed from the limb leads.

## Step 4 — Read a bedside monitor / telemetry screen

Transcribe the numbers and waveform info as displayed, including:

- **HR** (heart rate, often from ECG)
- **BP** (NIBP and/or arterial line — systolic/diastolic and MAP)
- **SpO2** (and pulse rate from the pleth waveform)
- **RR** (respiratory rate)
- **Temp**
- **EtCO2** if shown
- **Displayed lead(s)** for the ECG waveform (e.g., II, V1)
- **Alarm limits** (high/low thresholds shown in the margins) and whether any
  **active alarms** are visible (color changes, flashing borders, alarm
  icons/text)
- General waveform appearance (regular vs. irregular, artifact/noise,
  flatline)

If a trend graph is shown, summarize the visible trend direction (e.g., "HR
trending down from ~110 to ~85 over the visible window") rather than reading
exact values for every point.

## Step 5 — Identify patterns worth naming (with caveats)

You can describe visual patterns commonly associated with the following, but
always frame these as "consistent with" or "may suggest", not a diagnosis:

- Sinus rhythm / sinus tachycardia / sinus bradycardia
- Atrial fibrillation (irregularly irregular, no discrete P waves)
- Atrial flutter (sawtooth flutter waves)
- Supraventricular tachycardia (narrow-complex, fast, regular)
- Ventricular tachycardia (wide-complex tachycardia)
- Ventricular fibrillation (chaotic, no discernible QRS)
- Asystole (flat line, no electrical activity)
- Premature beats (PACs/PVCs)
- AV blocks (1st degree, 2nd degree Mobitz I/II, 3rd degree/complete)
- Bundle branch blocks (wide QRS with characteristic morphology)
- ST-elevation pattern suggestive of STEMI, by territory

## Step 6 — Build a structured summary

Present findings in a clear report, for example:

```
## Image type
[Rhythm strip / 12-lead ECG / Bedside monitor / Trend view]

## Vital signs (as read from the image)
- HR: ...
- BP: ...
- SpO2: ...
- RR: ...
- Temp: ...
- Other: ...

## ECG findings
- Calibration: [paper speed, gain, or "not visible — assumed standard"]
- Rate & rhythm: ...
- P waves / PR interval: ...
- QRS: ...
- ST/T changes: ...
- QT/QTc: ...
- Lead-by-lead notes (12-lead only): ...

## Pattern impression
[e.g., "Findings are consistent with sinus rhythm with no acute ST changes
visible" or "Wide-complex tachycardia is visible — see urgent note above"]

## Image quality notes
[Anything that limited the reading]

## Disclaimer
[Standard disclaimer per the safety notice above]
```

## Red flags — escalate immediately

If any of the following are visible, lead with a clear, prominent warning
recommending immediate clinical evaluation or emergency services before the
rest of the summary:

- Asystole or a flatline rhythm
- Ventricular fibrillation or pulseless ventricular tachycardia
- Wide-complex tachycardia in a symptomatic-appearing context
- Complete (3rd-degree) AV block
- ST-elevation pattern suggestive of STEMI
- SpO2 reading critically low (e.g., <90%, especially with a low/falling trend)
- Heart rate extremes (e.g., <40 or >150 bpm) paired with an active alarm
- Any active, unsilenced alarm on the monitor that the user hasn't mentioned

## Limitations to mention when relevant

- A photo cannot fully substitute for the original tracing — fine details
  (subtle ST changes, exact interval measurements) may be distorted by
  photography, compression, or lighting.
- There's no access to the patient's history, prior ECGs for comparison, or
  symptoms, all of which are essential for real interpretation.
- Lead placement errors (e.g., limb lead reversal) can mimic pathology and
  can't always be detected from a photo alone.
