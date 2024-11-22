from cover.progress import ProgressManager
import sounddevice as sd
import soundfile as sf
import queue
import math
import time

class Recorder():
    PROGRESS = ProgressManager()
    __OPEN_STREAM_MAX_TRIES = 4
    __CHANNELS = 1
    ___RATE = 44100
    __CHUNK = 512
    
    @staticmethod
    def get_available_devices():
        res = []

        for device in sd.query_devices():
            try:
                sd.check_input_settings(device['index'], Recorder.__CHANNELS, samplerate=Recorder.___RATE)
                #sd.check_output_settings(device['index'], Recorder.__CHANNELS, samplerate=Recorder.___RATE)
                res.append((device['index'], device['name']))
            except:
                pass
        
        return res

    @staticmethod
    def record(duration_sec, output_file, device_index = 0, result_obj = None):
        data_queue = queue.Queue()
        success = False
        Recorder.PROGRESS.reset(limit=100)

        def callback(indata, frames, time, status):
            data_queue.put(indata.copy())

        try:
            with sf.SoundFile(output_file, mode='w', samplerate=Recorder.___RATE, channels=Recorder.__CHANNELS) as file:
                for _try in range(Recorder.__OPEN_STREAM_MAX_TRIES):
                    try:
                        with sd.InputStream(samplerate=Recorder.___RATE, device=device_index, channels=Recorder.__CHANNELS, callback=callback):
                            start_time = time.time()

                            while time.time() - start_time < duration_sec:
                                Recorder.PROGRESS.set_steps(min((time.time() - start_time) / duration_sec * 100, 100))
                                file.write(data_queue.get())
                        
                        Recorder.PROGRESS.set_steps(100)
                        success = True
                        break
                    except Exception as e:
                        print('Try ' + str(_try) + ': ' + type(e).__name__ + ': ' + str(e))
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))
        
        result_obj.set(success)
        return success