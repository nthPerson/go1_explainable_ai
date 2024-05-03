scp /home/dicelabs/dog_py/src/go/speech/temp.wav pi@pi:/tmp/audio.wav
ssh pi@pi 'scp /tmp/audio.wav unitree@192.168.123.13:/tmp/audio.wav'
sshpass -p 123 ssh unitree@192.168.123.13 'aplay -D plughw:2,0 /tmp/audio.wav'
