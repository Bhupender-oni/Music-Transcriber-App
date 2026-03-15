import plotly.graph_objects as go
import numpy as np
import librosa

def create_pitch_contour_plot(pitch_contour: np.ndarray, times: np.ndarray, title="Pitch Contour"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=pitch_contour, mode='lines', name='Pitch'))
    fig.update_layout(title=title, xaxis_title='Time (s)', yaxis_title='Frequency (Hz)')
    return fig.to_html()

def create_spectrogram(audio: np.ndarray, sr: int, title="Spectrogram"):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio)), ref=np.max)
    fig = go.Figure(data=go.Heatmap(z=D, colorscale='Viridis'))
    fig.update_layout(title=title, xaxis_title='Time', yaxis_title='Frequency')
    return fig.to_html()

def create_raga_plot(raga_info: dict):
    if not raga_info.get('alternatives'):
        return "<p>No alternative raga data</p>"
    labels = [raga_info['primary_raga']] + [a['raga'] for a in raga_info['alternatives']]
    values = [raga_info['confidence']] + [a.get('confidence', 0) for a in raga_info['alternatives']]
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title="Raga Confidence", xaxis_title="Raga", yaxis_title="Confidence")
    return fig.to_html()