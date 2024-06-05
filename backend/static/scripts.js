


document.getElementById('compare-button').addEventListener('click', function() {
    var jdfiles = document.getElementById('jd');
    var resfiles = document.getElementById('resume');

    document.getElementById('comparison-output').innerText = 'Genarating Response..';

    if (jdfiles.value.length < 1 || resfiles.value.length < 1)  {
        alert("Please select pdf to upload..");
        return false;
     }
     else if(jdfiles.files.length > 1){
        alert("Max 1 file can be uploaded in JD.");
        return false;
     }
     else if(resfiles.files.length > 5){
        alert("Max 5 files can be uploaded in Resume.");
        return false;
     }

    const formData = new FormData();

    for (var x = 0; x < jdfiles.files.length; x++) {
        formData.append("jdfiles", jdfiles.files[x]);
    }

    for (var x = 0; x < resfiles.files.length; x++) {
        formData.append("resfiles", resfiles.files[x]);
    }

    formData.append('jdfiles', jdfiles.files[0]);
    formData.append('resfiles', resfiles.files[0]);

    fetch('http://127.0.0.1:8080/summarize_resume', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('comparison-output').innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('comparison-output').innerText = 'An error occurred during comparison.';
    });
});


document.getElementById('clear-button').addEventListener('click', function() {
    document.getElementById('upload-form').reset();
    document.getElementById('comparison-output').innerText = '';
});