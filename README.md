# enunu_timing_corrector
General timing corrector for ENUNU.

# How to Use
### As an extension
1. Paste the timing_corrector folder into the voicebank of choice.
2. Append the text written in `enuconfig.yaml` at the end of the existing `enuconfig.yaml` of the voicebank.
	- If the voicebank in question already has this part in its `enuconfig.yaml`, you may edit the `timing_editor` section to be similar to the given `enuconfig.yaml`.
3. Change the `vowels.txt` to list out the vowels of the language of the voicebank comma-separated (e.g. `a,i,u,e,o,A,I,U,E,O,N`, `aa,ae,ah,ao,aw,ax,ay,eh,er,ey,ih,iy,ow,oy,uh,uw`)

### Through terminal
Extensions in ENUNU are done by passing arguments to each possible extension. This extension takes the `mono_score` and `mono_timing` labels generated by NNSVS. The correction can therefore be invoked in this manner:

```
python script.py --mono_score "path/to/mono/score" --mono_timing "path/to/mono/timing"
```

# Remarks
This was only a quick test run of timing correction for ENUNU. There might be a potential issue where a part of the corrected label might have its end be earlier than the start, but that's all there is to its issues. The consonant lengths are based off of the timing that ENUNU generates by itself. I'm not sure if `velocity_applier` (the other script that comes with canon's timing corrector in Ritsu NNSVS) works with other languages, but if it does, it may be used to shorten consonants and decreasing the chances of the said issue.

That being said, I also think it's generally better to use canon's timing corrector for Japanese voices instead of this. This was made to hopefully support all languages.

**UPDATE 05/28:** OpenUtau partially deals with this issue mentioned by making the previous phonemes very small length. If the long length phoneme is retracted to a reasonable size, it returns the other pushed phonemes to its likely configuration. Hoping that stays the way it is. A preview of this exact case can be seen [here](https://twitter.com/C5G4D4A3/status/1530539822766780417?s=20&t=KFEn7_F0c6AQcEsUjA21Rg)

**UPDATE 07/22:** The timing correction now handles multiple vowels in a note better than the previous version. It also removes negative duration phonemes, though rather lazily. It only makes these phonemes go for one millisecond.
