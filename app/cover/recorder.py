from cover.progress import ProgressManager
import pyaudio
import wave
import math

class Recorder():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    PYAUDIO = None
    PROGRESS = ProgressManager()
    
    @staticmethod
    def init():
        if Recorder.PYAUDIO is not None:
            raise Exception("Already initiated")

        Recorder.PYAUDIO = pyaudio.PyAudio()
    
    @staticmethod
    def close():
        if Recorder.PYAUDIO is not None:
            Recorder.PYAUDIO.terminate()
            Recorder.PYAUDIO = None
    
    @staticmethod
    def get_available_devices():
        info = Recorder.PYAUDIO.get_host_api_info_by_index(0)
        count = Recorder.PYAUDIO.get_device_count()
        res = []

        for i in range(count):
            info = Recorder.PYAUDIO.get_device_info_by_host_api_device_index(0, i)

            if (info.get('maxInputChannels')) > 0:
                """try :
                    if(Recorder.PYAUDIO.is_format_supported(Recorder.RATE, input_device=i, input_channels=Recorder.CHANNELS, input_format=Recorder.FORMAT)):
                        print(i, info.get('name'), "VALID")
                        res.append((i, info.get('name')))
                    else:
                        print(i, info.get('name'), "INVALID")
                except:
                    print(i, info.get('name'), "INVALID")"""

                try:
                    stream = Recorder.PYAUDIO.open(format=Recorder.FORMAT, channels=Recorder.CHANNELS, rate=Recorder.RATE, input=True,
                        input_device_index=i, frames_per_buffer=Recorder.CHUNK)

                    try:
                        buffer = stream.read(Recorder.CHUNK)
                        if not stream.is_stopped():
                            stream.stop_stream()
                        
                        res.append((i, info.get('name')))
                    except:
                        pass
                    finally:
                        if steam.is_active():
                            stream.close()
                except:
                    continue
        
        return res

    @staticmethod
    def record(duration_sec, output_file, device_index = 0):
        steps_count = math.ceil(Recorder.RATE / Recorder.CHUNK * duration_sec)
        Recorder.PROGRESS.reset(limit=steps_count + 2)

        stream = Recorder.PYAUDIO.open(format=Recorder.FORMAT, channels=Recorder.CHANNELS, rate=Recorder.RATE, input=True,
            input_device_index=device_index, frames_per_buffer=Recorder.CHUNK)
        
        Recorder.PROGRESS.step()
        frames = []
        
        for i in range(steps_count):
            data = stream.read(Recorder.CHUNK)
            frames.append(data)
            Recorder.PROGRESS.step()
        
        stream.stop_stream()
        stream.close()
        
        waveFile = wave.open(output_file, 'wb')
        waveFile.setnchannels(Recorder.CHANNELS)
        waveFile.setsampwidth(Recorder.PYAUDIO.get_sample_size(Recorder.FORMAT))
        waveFile.setframerate(Recorder.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        Recorder.PROGRESS.step()