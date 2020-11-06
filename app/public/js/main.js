window.onload = function() {
    let btn_upload = document.querySelector('#btn_upload');
    let file_upload = document.querySelector('#file_upload');
    let img_upload = document.querySelector('#img_upload');
    btn_upload.addEventListener('click', function(e) {
        var formData = new FormData();
        let file_name = file_upload.files[0].name;
        formData.append("image", file_upload.files[0]);
        axios.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'responseType': 'blob'
            }
        }).then(function(res) {
            console.log(res);
            blobToDataUrl(res.data).then(function(uri) {
                img_upload.src = uri;
            })
        });
    });
}

function blobToDataUrl(blob) {
    return new Promise(resolve => {
        const reader = new FileReader(); // https://developer.mozilla.org/en-US/docs/Using_files_from_web_applications
        reader.onload = e => resolve(e.target.result);
        reader.readAsDataURL(blob);
    })
}