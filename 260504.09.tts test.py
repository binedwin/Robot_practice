import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

# reference audio (여기에 네 wav 파일 경로 넣기)
reference_audio = "voice.wav"   

korean_text = "안녕하세요, 오늘 날씨가 정말 좋네요. 내일은 어린이날이라서 더 행복해요. "

wav_korean = multilingual_model.generate(
    korean_text,
    language_id="ko",
    audio_prompt_path=reference_audio 

)

ta.save("test-korean.wav", wav_korean, multilingual_model.sr)


'''
(text: Any, language_id: Any, 
audio_prompt_path: Any | None = None, 
exaggeration: float = 0.5, 
cfg_weight: float = 0.5, 
temperature: float = 0.8, 
repetition_penalty: float = 2, 
min_p: float = 0.05, 
top_p: float = 1) -> Tensor
'''