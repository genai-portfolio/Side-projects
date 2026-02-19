"use client";

import { useState, useRef, useEffect } from "react";

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(true);
  const [time, setTime] = useState(0);
  const [status, setStatus] = useState("System Ready");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamsRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const startRecording = async () => {
    try {
      setStatus("Initializing...");

      // 1. Capture Screen
      const screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: { frameRate: { ideal: 30 } },
        audio: true // Capture system audio if available
      });

      let combinedStream = screenStream;

      // 2. Capture Microphone if enabled
      if (audioEnabled) {
        try {
          const micStream = await navigator.mediaDevices.getUserMedia({
            audio: {
              echoCancellation: true,
              noiseSuppression: true,
              sampleRate: 44100
            }
          });

          // Combine tracks
          const tracks = [...screenStream.getVideoTracks(), ...micStream.getAudioTracks()];
          combinedStream = new MediaStream(tracks);
        } catch (micErr) {
          console.warn("Microphone access denied or failed:", micErr);
          setStatus("Mic failed, recording screen only...");
        }
      }

      streamsRef.current = combinedStream;
      chunksRef.current = [];

      // 3. Initialize MediaRecorder
      const options = { mimeType: 'video/webm; codecs=vp9,opus' };
      const recorder = new MediaRecorder(combinedStream, options);

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `recording_${new Date().getTime()}.webm`;
        a.click();
        URL.revokeObjectURL(url);

        // Cleanup tracks
        combinedStream.getTracks().forEach(track => track.stop());
        setStatus("Recording Saved.");
      };

      mediaRecorderRef.current = recorder;
      recorder.start(1000); // Collect data every second

      setIsRecording(true);
      setStatus("Recording...");

      // 4. Start Timer
      setTime(0);
      timerRef.current = setInterval(() => {
        setTime(prev => prev + 1);
      }, 1000);

      // Handle stream end (e.g., user clicks "Stop sharing" in browser)
      screenStream.getVideoTracks()[0].onended = () => {
        stopRecording();
      };

    } catch (err) {
      console.error("Error starting recording:", err);
      setStatus("Initialization Failed.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setIsRecording(false);
  };

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="recorder-container">
      <h1>FLASHY FLASH ⚡</h1>
      <p className="subtitle">High-performance screen recording</p>

      {!isRecording ? (
        <div className="frame-home">
          <div className="section">
            <span className="section-label">1. Capture Method</span>
            <div className="button-group">
              <button className="btn active">🚀 Web Native</button>
            </div>
          </div>

          <div className="section">
            <span className="section-label">2. Audio Settings</span>
            <button
              className={`btn btn-toggle ${audioEnabled ? 'on' : ''}`}
              onClick={() => setAudioEnabled(!audioEnabled)}
            >
              🎤 MICROPHONE: {audioEnabled ? 'ON' : 'OFF'}
            </button>
          </div>

          <div className="section">
            <span className="section-label">3. Action</span>
            <button className="btn-primary" onClick={startRecording}>
              START FLASHY RECORDING
            </button>
          </div>

          <div className="footer-status">{status}</div>
        </div>
      ) : (
        <div className="frame-recording">
          <div className="status-label">
            <div className="pulse-dot"></div>
            REC ⚡ LIVE
          </div>

          <div className="timer recording-pulse">{formatTime(time)}</div>

          <button className="btn-stop" onClick={stopRecording}>
            STOP & SAVE FILENAME
          </button>

          <div className="footer-status">Bitrate: High // Frames: 30fps</div>
        </div>
      )}
    </div>
  );
}
