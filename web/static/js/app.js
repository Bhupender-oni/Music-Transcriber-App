$(document).ready(function() {
    let selectedFile = null, jobId = null, pollInterval = null;
    $('#uploadArea').click(() => $('#fileInput').click());
    $('#uploadArea').on('dragover', e => { e.preventDefault(); $('#uploadArea').css('background','#e8e8ff'); });
    $('#uploadArea').on('dragleave', e => { e.preventDefault(); $('#uploadArea').css('background','#f9f9ff'); });
    $('#uploadArea').on('drop', e => {
        e.preventDefault(); $('#uploadArea').css('background','#f9f9ff');
        const file = e.originalEvent.dataTransfer.files[0];
        if (file?.type.startsWith('audio/')) handleFile(file); else alert('Please drop an audio file');
    });
    $('#fileInput').change(e => { if (e.target.files[0]) handleFile(e.target.files[0]); });

    function handleFile(file) {
        selectedFile = file; $('#uploadBtn').prop('disabled', false); $('#uploadArea h3').text(`Selected: ${file.name}`);
    }

    $('#uploadBtn').click(() => {
        if (!selectedFile) return;
        const formData = new FormData(); formData.append('file', selectedFile);
        $('#progressSection').show(); $('#resultsSection').hide(); $('#uploadBtn').prop('disabled', true);
        $('#progressFill').css('width','0%'); $('#statusText').text('Uploading...');
        $.ajax({
            url:'/upload', method:'POST', data:formData, processData:false, contentType:false,
            success: data => { jobId = data.job_id; pollStatus(); },
            error: xhr => { alert('Upload failed: ' + (xhr.responseJSON?.error || 'Unknown')); resetUI(); }
        });
    });

    function pollStatus() {
        if (!jobId) return;
        pollInterval = setInterval(() => {
            $.get(`/status/${jobId}`, data => {
                if (data.status === 'complete') { clearInterval(pollInterval); fetchResults(); }
                else if (data.status === 'error') { clearInterval(pollInterval); alert('Processing error: ' + (data.error || 'Unknown')); resetUI(); }
                else { $('#statusText').text(data.status || 'Processing...'); $('#progressFill').css('width', (data.progress||0)+'%'); }
            });
        }, 1000);
    }

    function fetchResults() {
        $.get(`/results/${jobId}`, data => {
            $('#progressSection').hide(); $('#resultsSection').show(); $('#uploadBtn').prop('disabled', false);
            $('#uploadArea h3').text('Click or Drop Audio File Here');
            let summaryHtml = `
                <div class="summary-card"><h4>Tonic (Sa)</h4><div class="value">${data.tonic?.toFixed(1)||'?'} Hz</div></div>
                <div class="summary-card"><h4>Raga</h4><div class="value">${data.raga?.primary_raga||'Unknown'}</div></div>
                <div class="summary-card"><h4>Tala</h4><div class="value">${data.tala?.primary_tala||'Unknown'}</div></div>
                <div class="summary-card"><h4>Duration</h4><div class="value">${data.duration?.toFixed(1)||'?'} s</div></div>
            `;
            $('#summaryCards').html(summaryHtml);
            $('#sargamDisplay').text(data.sargam?.map(n=>n.note).join(' ') || 'No sargam data');
            if (data.pitch_plot) $('#pitchPlotContainer').html(data.pitch_plot);
            if (data.raga_plot) $('#ragaPlotContainer').html(data.raga_plot);
            if (data.instruments?.length)
                $('#instrumentsList').html(data.instruments.map(i=>`<li>${i.name} (${(i.confidence*100).toFixed(0)}%)</li>`).join(''));
            else $('#instrumentsList').html('<li>No instruments identified</li>');
        });
    }

    function resetUI() { $('#progressSection').hide(); $('#uploadBtn').prop('disabled', false); $('#uploadArea h3').text('Click or Drop Audio File Here'); }
});