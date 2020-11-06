window.onload = function () {
    let btn_upload = document.querySelector('#btn_upload');
    let file_upload = document.querySelector('#file_upload');
    let img_upload = document.querySelector('#img_upload');
    let div_prediction = document.querySelector('#div_prediction');
    btn_upload.addEventListener('click', function (e) {
        var formData = new FormData();
        let file_name = file_upload.files[0].name;
        formData.append("image", file_upload.files[0]);
        axios.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(function (res) {
            console.log(res);
            img_upload.src = res.data.url;
            div_prediction.innerHTML = res.data.prediction;
        });
    });
}